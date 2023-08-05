import logging
import os
import tempfile
import zipfile
from functools import wraps
from typing import List, Text, Optional, Union, Callable, Any

from inspect import isawaitable
from sanic import Sanic, response
from sanic.request import Request
from sanic_cors import CORS
from sanic_jwt import Initialize
from sanic_jwt import exceptions

import kidx_nlu
from kidx_core import utils, constants
from kidx_core.channels import CollectingOutputChannel, UserMessage
from kidx_core.evaluate import run_story_evaluation
from kidx_core.events import Event
from kidx_core.domain import Domain
from kidx_core.policies import PolicyEnsemble
from kidx_core.trackers import DialogueStateTracker, EventVerbosity
from kidx_core.version import __version__

import kidx_nlu.utils

logger = logging.getLogger(__name__)


class ErrorResponse(Exception):
    def __init__(self, status, reason, message, details=None, help_url=None):
        self.error_info = {
            "version": __version__,
            "status": "failure",
            "message": message,
            "reason": reason,
            "details": details or {},
            "help": help_url,
            "code": status
        }
        self.status = status


def _docs(sub_url: Text) -> Text:
    """Create a url to a subpart of the docs."""
    return constants.DOCS_BASE_URL + sub_url


def ensure_loaded_agent(agent):
    """Wraps a request handler ensuring there is a loaded and usable model."""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not agent.is_ready():
                raise ErrorResponse(
                    503,
                    "NoAgent",
                    "No agent loaded. To continue processing, a "
                    "model of a trained agent needs to be loaded.",
                    help_url=_docs("/server.html#running-the-http-server"))

            return f(*args, **kwargs)

        return decorated

    return decorator


def request_parameters(request):
    if request.method == 'GET':
        return request.raw_args
    else:
        try:
            return request.json
        except ValueError as e:
            logger.error("Failed to decode json during respond request. "
                         "Error: {}.".format(e))
            raise


def requires_auth(app: Sanic,
                  token: Optional[Text] = None
                  ) -> Callable[[Any], Any]:
    """Wraps a request handler with token authentication."""

    def decorator(f: Callable[[Any, Any, Any], Any]
                  ) -> Callable[[Any, Any], Any]:
        def sender_id_from_args(args: Any,
                                kwargs: Any) -> Optional[Text]:
            argnames = utils.arguments_of(f)
            try:
                sender_id_arg_idx = argnames.index("sender_id")
                if "sender_id" in kwargs:  # try to fetch from kwargs first
                    return kwargs["sender_id"]
                if sender_id_arg_idx < len(args):
                    return args[sender_id_arg_idx]
                return None
            except ValueError:
                return None

        def sufficient_scope(request,
                             *args: Any,
                             **kwargs: Any) -> Optional[bool]:
            jwt_data = request.app.auth.extract_payload(request)
            user = jwt_data.get("user", {})

            username = user.get("username", None)
            role = user.get("role", None)

            if role == "admin":
                return True
            elif role == "user":
                sender_id = sender_id_from_args(args, kwargs)
                return sender_id is not None and username == sender_id
            else:
                return False

        @wraps(f)
        async def decorated(request: Request,
                            *args: Any,
                            **kwargs: Any) -> Any:

            provided = utils.default_arg(request, 'token', None)
            # noinspection PyProtectedMember
            if token is not None and provided == token:
                result = f(request, *args, **kwargs)
                if isawaitable(result):
                    result = await result
                return result
            elif (app.config.get('USE_JWT') and
                  request.app.auth.is_authenticated(request)):
                if sufficient_scope(request, *args, **kwargs):
                    result = f(request, *args, **kwargs)
                    if isawaitable(result):
                        result = await result
                    return result
                raise ErrorResponse(
                    403, "NotAuthorized",
                    "User has insufficient permissions.",
                    help_url=_docs(
                        "/server.html#security-considerations"))
            elif token is None and app.config.get('USE_JWT') is None:
                # authentication is disabled
                result = f(request, *args, **kwargs)
                if isawaitable(result):
                    result = await result
                return result
            raise ErrorResponse(
                401, "NotAuthenticated", "User is not authenticated.",
                help_url=_docs("/server.html#security-considerations"))

        return decorated

    return decorator


def event_verbosity_parameter(request, default_verbosity):
    event_verbosity_str = request.args.get(
        'include_events', default=default_verbosity.name).upper()
    try:
        return EventVerbosity[event_verbosity_str]
    except KeyError:
        enum_values = ", ".join([e.name for e in EventVerbosity])
        raise ErrorResponse(404, "InvalidParameter",
                            "Invalid parameter value for 'include_events'. "
                            "Should be one of {}".format(enum_values),
                            {"parameter": "include_events", "in": "query"})


async def authenticate(request):
    return dict(user_id='some_id')


def create_app(agent,
               cors_origins: Union[Text, List[Text]] = "*",
               auth_token: Optional[Text] = None,
               jwt_secret: Optional[Text] = None,
               jwt_method: Optional[Text] = "HS256",
               ):
    """Class representing a Kidx Core HTTP server."""

    app = Sanic(__name__)
    CORS(app,
         resources={r"/*": {"origins": cors_origins or ""}},
         automatic_options=True)

    # Setup the Sanic-JWT extension
    if jwt_secret and jwt_method:
        # since we only want to check signatures, we don't actually care
        # about the JWT method and set the passed secret as either symmetric
        # or asymmetric key. jwt lib will choose the right one based on method
        app.config['USE_JWT'] = True
        Initialize(app,
                   secret=jwt_secret,
                   authenticate=authenticate,
                   algorithm=jwt_method,
                   user_id="username")

    if not agent.is_ready():
        logger.info("The loaded agent is not ready to be used yet "
                    "(e.g. only the NLU interpreter is configured, "
                    "but no Core model is loaded). This is NOT AN ISSUE "
                    "some endpoints are not available until the agent "
                    "is ready though.")

    @app.exception(ErrorResponse)
    async def ignore_404s(request: Request, exception: ErrorResponse):
        return response.json(exception.error_info,
                             status=exception.status)

    @app.get("/")
    async def hello(request):
        """Check if the server is running and responds with the version."""
        return response.text("hello from Rasa Core: " + __version__)

    @app.get("/version")
    async def version(request):
        """respond with the version number of the installed kidx core."""

        return response.json({
            "version": __version__,
            "minimum_compatible_version": constants.MINIMUM_COMPATIBLE_VERSION
        })

    # <sender_id> can be be 'default' if there's only 1 client
    @app.post("/conversations/<sender_id>/execute")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def execute_action(request, sender_id):
        request_params = request.json

        # we'll accept both parameters to specify the actions name
        action_to_execute = (request_params.get("name") or
                             request_params.get("action"))

        policy = request_params.get("policy", None)
        confidence = request_params.get("confidence", None)
        verbosity = event_verbosity_parameter(request,
                                              EventVerbosity.AFTER_RESTART)

        try:
            out = CollectingOutputChannel()
            await agent.execute_action(sender_id,
                                       action_to_execute,
                                       out,
                                       policy,
                                       confidence)

            # retrieve tracker and set to requested state
            tracker = agent.tracker_store.get_or_create_tracker(sender_id)
            state = tracker.current_state(verbosity)
            return response.json({"tracker": state,
                                  "messages": out.messages})

        except ValueError as e:
            raise ErrorResponse(400, "ValueError", e)
        except Exception as e:
            logger.error("Encountered an exception while running action '{}'. "
                         "Bot will continue, but the actions events are lost. "
                         "Make sure to fix the exception in your custom "
                         "code.".format(action_to_execute))
            logger.debug(e, exc_info=True)
            raise ErrorResponse(500, "ValueError",
                                "Server failure. Error: {}".format(e))

    @app.post("/conversations/<sender_id>/tracker/events")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def append_event(request, sender_id):
        """Append a list of events to the state of a conversation"""

        # request_params = request.get_json(force=True)
        request_params = request.json
        evt = Event.from_parameters(request_params)
        tracker = agent.tracker_store.get_or_create_tracker(sender_id)
        verbosity = event_verbosity_parameter(request,
                                              EventVerbosity.AFTER_RESTART)

        if evt:
            tracker.update(evt)
            agent.tracker_store.save(tracker)
            return response.json(tracker.current_state(verbosity))
        else:
            logger.warning(
                "Append event called, but could not extract a "
                "valid event. Request JSON: {}".format(request_params))
            raise ErrorResponse(400, "InvalidParameter",
                                "Couldn't extract a proper event from the "
                                "request body.",
                                {"parameter": "", "in": "body"})

    @app.put("/conversations/<sender_id>/tracker/events")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def replace_events(request, sender_id):
        """Use a list of events to set a conversations tracker to a state."""

        request_params = request.json
        verbosity = event_verbosity_parameter(request,
                                              EventVerbosity.AFTER_RESTART)

        tracker = DialogueStateTracker.from_dict(sender_id,
                                                 request_params,
                                                 agent.domain.slots)
        # will override an existing tracker with the same id!
        agent.tracker_store.save(tracker)
        return response.json(tracker.current_state(verbosity))

    @app.get("/conversations")
    @requires_auth(app, auth_token)
    async def list_trackers(request):
        if agent.tracker_store:
            keys = list(agent.tracker_store.keys())
        else:
            keys = []
        return response.json(keys)

    @app.get("/conversations/<sender_id>/tracker")
    @requires_auth(app, auth_token)
    async def retrieve_tracker(request, sender_id):
        """Get a dump of a conversations tracker including its events."""

        if not agent.tracker_store:
            raise ErrorResponse(503, "NoTrackerStore",
                                "No tracker store available. Make sure to "
                                "configure a tracker store when starting "
                                "the server.")

        # parameters
        default_verbosity = EventVerbosity.AFTER_RESTART

        # this is for backwards compatibility
        if "ignore_restarts" in request.raw_args:
            ignore_restarts = utils.bool_arg(request, 'ignore_restarts',
                                             default=False)
            if ignore_restarts:
                default_verbosity = EventVerbosity.ALL

        if "events" in request.raw_args:
            include_events = utils.bool_arg(request, 'events',
                                            default=True)
            if not include_events:
                default_verbosity = EventVerbosity.NONE

        verbosity = event_verbosity_parameter(request,
                                              default_verbosity)

        # retrieve tracker and set to requested state
        tracker = agent.tracker_store.get_or_create_tracker(sender_id)
        if not tracker:
            raise ErrorResponse(503,
                                "NoDomain",
                                "Could not retrieve tracker. Most likely "
                                "because there is no domain set on the agent.")

        until_time = utils.float_arg(request, 'until')
        if until_time is not None:
            tracker = tracker.travel_back_in_time(until_time)

        # dump and return tracker

        state = tracker.current_state(verbosity)
        return response.json(state)

    @app.get("/conversations/<sender_id>/story")
    @requires_auth(app, auth_token)
    async def test_story_export(request, sender_id):
        """Get an end-to-end story corresponding to this conversation."""

        if not agent.tracker_store:
            raise ErrorResponse(503, "NoTrackerStore",
                                "No tracker store available. Make sure to "
                                "configure "
                                "a tracker store when starting the server.")

        # retrieve tracker and set to requested state
        tracker = agent.tracker_store.get_or_create_tracker(sender_id)
        if not tracker:
            raise ErrorResponse(503,
                                "NoDomain",
                                "Could not retrieve tracker. Most likely "
                                "because there is no domain set on the agent.")

        until_time = utils.float_arg(request, 'until')
        if until_time is not None:
            tracker = tracker.travel_back_in_time(until_time)

        # dump and return tracker
        state = tracker.export_stories(e2e=True)
        return response.text(state)

    @app.route("/conversations/<sender_id>/respond", methods=['GET', 'POST'])
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def respond(request, sender_id):
        request_params = request_parameters(request)

        if 'query' in request_params:
            message = request_params['query']
        elif 'q' in request_params:
            message = request_params['q']
        else:
            raise ErrorResponse(400,
                                "InvalidParameter",
                                "Missing the message parameter.",
                                {"parameter": "query", "in": "query"})

        try:
            # Set the output channel
            out = CollectingOutputChannel()
            # Fetches the appropriate bot response in a json format
            responses = await agent.handle_text(message,
                                                output_channel=out,
                                                sender_id=sender_id)
            return response.json(responses)

        except Exception as e:
            logger.exception("Caught an exception during respond.")
            raise ErrorResponse(500, "ActionException",
                                "Server failure. Error: {}".format(e))

    @app.post("/conversations/<sender_id>/predict")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def predict(request, sender_id):
        try:
            # Fetches the appropriate bot response in a json format
            responses = agent.predict_next(sender_id)
            return response.json(responses)

        except Exception as e:
            logger.exception("Caught an exception during prediction.")
            raise ErrorResponse(500, "PredictionException",
                                "Server failure. Error: {}".format(e))

    @app.post("/conversations/<sender_id>/messages")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def log_message(request, sender_id):
        request_params = request.json
        try:
            message = request_params["message"]
        except KeyError:
            message = request_params.get("text")

        sender = request_params.get("sender")
        parse_data = request_params.get("parse_data")
        verbosity = event_verbosity_parameter(request,
                                              EventVerbosity.AFTER_RESTART)

        # TODO: implement properly for agent / bot
        if sender != "user":
            raise ErrorResponse(500,
                                "NotSupported",
                                "Currently, only user messages can be passed "
                                "to this endpoint. Messages of sender '{}' "
                                "can not be handled. ".format(sender),
                                {"parameter": "sender", "in": "body"})

        try:
            usermsg = UserMessage(message, None, sender_id, parse_data)
            tracker = agent.log_message(usermsg)
            return response.json(tracker.current_state(verbosity))

        except Exception as e:
            logger.exception("Caught an exception while logging message.")
            raise ErrorResponse(500, "MessageException",
                                "Server failure. Error: {}".format(e))

    @app.post("/model")
    @requires_auth(app, auth_token)
    async def load_model(request):
        """Loads a zipped model, replacing the existing one."""

        if 'model' not in request.files:
            # model file is missing
            raise ErrorResponse(400, "InvalidParameter",
                                "You did not supply a model as part of your "
                                "request.",
                                {"parameter": "model", "in": "body"})

        model_file = request.files['model']

        logger.info("Received new model through REST interface.")
        zipped_path = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        zipped_path.close()
        model_directory = tempfile.mkdtemp()

        model_file.save(zipped_path.name)

        logger.debug("Downloaded model to {}".format(zipped_path.name))

        zip_ref = zipfile.ZipFile(zipped_path.name, 'r')
        zip_ref.extractall(model_directory)
        zip_ref.close()
        logger.debug("Unzipped model to {}".format(
            os.path.abspath(model_directory)))

        domain_path = os.path.join(os.path.abspath(model_directory),
                                   "domain.yml")
        domain = Domain.load(domain_path)
        ensemble = PolicyEnsemble.load(model_directory)
        agent.update_model(domain, ensemble, None)
        logger.debug("Finished loading new agent.")
        return '', 204

    @app.post("/evaluate")
    @requires_auth(app, auth_token)
    async def evaluate_stories(request):
        """Evaluate stories against the currently loaded model."""
        tmp_file = kidx_nlu.utils.create_temporary_file(request.body,
                                                        mode='w+b')
        use_e2e = utils.bool_arg(request, 'e2e', default=False)
        try:
            evaluation = run_story_evaluation(tmp_file, agent, use_e2e=use_e2e)
            return response.json(evaluation)
        except ValueError as e:
            raise ErrorResponse(400, "FailedEvaluation",
                                "Evaluation could not be created. Error: {}"
                                "".format(e))

    @app.get("/domain")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def get_domain(request):
        """Get current domain in yaml or json format."""

        accepts = request.headers.get("Accept", default="application/json")
        if accepts.endswith("json"):
            domain = agent.domain.as_dict()
            return response.json(domain)
        elif accepts.endswith("yml"):
            domain_yaml = agent.domain.as_yaml()
            return response.text(domain_yaml,
                                 status=200,
                                 content_type="application/x-yml")
        else:
            raise ErrorResponse(406,
                                "InvalidHeader",
                                """Invalid accept header. Domain can be 
                                   provided as json 
                                   ("Accept: application/json")
                                   or yml ("Accept: application/x-yml").
                                   Make sure you've set the appropriate Accept
                                   header.""")

    @app.post("/finetune")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def continue_training(request):
        epochs = request.raw_args.get("epochs", 30)
        batch_size = request.raw_args.get("batch_size", 5)
        request_params = request.json
        sender_id = UserMessage.DEFAULT_SENDER_ID

        try:
            tracker = DialogueStateTracker.from_dict(sender_id,
                                                     request_params,
                                                     agent.domain.slots)
        except Exception as e:
            raise ErrorResponse(400, "InvalidParameter",
                                "Supplied events are not valid. {}".format(e),
                                {"parameter": "", "in": "body"})

        try:
            # Fetches the appropriate bot response in a json format
            agent.continue_training([tracker],
                                    epochs=epochs,
                                    batch_size=batch_size)
            return '', 204

        except Exception as e:
            logger.exception("Caught an exception during prediction.")
            raise ErrorResponse(500, "TrainingException",
                                "Server failure. Error: {}".format(e))

    @app.get("/status")
    @requires_auth(app, auth_token)
    async def status(request):
        return response.json({
            "model_fingerprint": agent.fingerprint,
            "is_ready": agent.is_ready()
        })

    @app.post("/predict")
    @requires_auth(app, auth_token)
    @ensure_loaded_agent(agent)
    async def tracker_predict(request):
        """ Given a list of events, predicts the next action"""

        sender_id = UserMessage.DEFAULT_SENDER_ID
        request_params = request.json
        verbosity = event_verbosity_parameter(request,
                                              EventVerbosity.AFTER_RESTART)

        try:
            tracker = DialogueStateTracker.from_dict(sender_id,
                                                     request_params,
                                                     agent.domain.slots)
        except Exception as e:
            raise ErrorResponse(400, "InvalidParameter",
                                "Supplied events are not valid. {}".format(e),
                                {"parameter": "", "in": "body"})

        policy_ensemble = agent.policy_ensemble
        probabilities, policy = \
            policy_ensemble.probabilities_using_best_policy(tracker,
                                                            agent.domain)

        scores = [{"action": a, "score": p}
                  for a, p in zip(agent.domain.action_names, probabilities)]

        return response.json({
            "scores": scores,
            "policy": policy,
            "tracker": tracker.current_state(verbosity)
        })

    return app


if __name__ == '__main__':
    raise RuntimeError("Calling `kidx_core.server` directly is "
                       "no longer supported. "
                       "Please use `kidx_core.run --enable_api` instead.")
