from cmg.lib import Agent, Territory, GlobalState
from typing import List, Dict
import numpy as np


class TestCase:
    def __init__(
        self,
        agents: List[Agent],
        territories: List[Territory],
    ):
        self.agents = agents
        self.territories = territories

    # Outputting evals that are 1 too high
    def validate_evals(
        agent: Agent, current: int, territory_map: Dict[int, Territory]
    ) -> Dict[int, float]:
        alpha = 1
        beta = 1
        vals = {}
        for id, territory in territory_map.items():
            projected_count = territory.count + 1
            if id == current:
                projected_count -= 1
            dot_prod = np.dot(agent.preferences, territory.features)
            eval = (alpha * dot_prod) - (beta * projected_count)
            vals[id] = eval
        print(f"EVALS for agent {agent.id}:\n{vals}")
        return vals

    def validate(state: GlobalState):
        print("VALIDATING")
        for tId, agents in state.territory_agents.items():
            for agent in agents:
                evals = TestCase.validate_evals(agent, tId, state.territories)
                max_eval = max(evals.values(), default=float("-inf"))
                max_keys = [k for k, v in evals.items() if v == max_eval]
                if tId in max_keys:
                    print(f"✅ Agent {agent.id} is in NE (no better territory found)\n")
                else:
                    print(f"❌ Agent {agent.id} IS NOT in NE (better territory(s): {max_keys}\n")
    
    def run_test(self):
        print("Running Test Case")
        state = GlobalState()
        state.add_agents(self.agents)
        state.add_territories(self.territories)
        state.run()

        TestCase.validate(state)

        print(f"Main Loop Ended:\n{state}")


def main():
    case1 = TestCase(
        [
            Agent(1, [4, 3, 5, 2, 1]),
            Agent(2, [5, 2, 3, 4, 1]),
            Agent(3, [1, 5, 4, 3, 1]),
            Agent(4, [5, 2, 3, 4, 1]),
            Agent(5, [1, 2, 3, 4, 5]),
        ],
        [
            Territory(1, [0, 0, 1, 0, 0]),
            Territory(2, [1, 0, 0, 0, 0]),
            Territory(3, [0, 1, 0, 0, 0]),
        ],
    )
    case2 = TestCase(
        [
            Agent(1, [4, 3, 5, 2, 1]),
            Agent(2, [5, 2, 3, 4, 1]),
            Agent(3, [1, 5, 4, 3, 1]),
            Agent(4, [5, 2, 3, 4, 1]),
            Agent(5, [1, 2, 3, 4, 5]),
            # Same as 2
            Agent(6, [5, 2, 3, 4, 1]),
            Agent(7, [5, 2, 3, 4, 1]),
            Agent(8, [5, 2, 3, 4, 1]),
            Agent(9, [5, 2, 3, 4, 1]),
            Agent(10, [5, 2, 3, 4, 1]),
        ],
        [
            Territory(1, [0, 0, 1, 0, 0]),
            Territory(2, [1, 0, 0, 0, 0]),
            Territory(3, [0, 1, 0, 0, 0]),
        ],
    )
    case1.run_test()
    case2.run_test()


if __name__ == "__main__":
    main()
