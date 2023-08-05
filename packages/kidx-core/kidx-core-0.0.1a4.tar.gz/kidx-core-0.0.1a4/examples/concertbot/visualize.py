from kidx_core.agent import Agent
from kidx_core.policies.keras_policy import KerasPolicy
from kidx_core.policies.memoization import MemoizationPolicy

if __name__ == '__main__':
    agent = Agent("domain.yml",
                  policies=[MemoizationPolicy(), KerasPolicy()])

    agent.visualize("data/stories.md",
                    output_file="graph.html", max_history=2)
