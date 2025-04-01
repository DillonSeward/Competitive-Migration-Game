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

    def validate(state: GlobalState):
        print("VALIDATING")
        for tId, agents in state.territory_agents.items():
            for agent in agents:
                evals = agent.evals(tId, state.territories)
                max_eval = max(evals.values(), default=float("-inf"))
                max_keys = [k for k, v in evals.items() if v == max_eval]
                if tId in max_keys:
                    print(f"✅ Agent {agent.id} is in NE (no better territory found)\n")
                else:
                    print(f"❌ Agent {agent.id} IS NOT in NE (better territory(s): {max_keys}\n")
    
    def run(self):
        print("-------Running--------")
        state = GlobalState()
        state.add_agents(self.agents)
        state.add_territories(self.territories)
        state.start()
        TestCase.validate(state)

        print(f"Main Loop Ended:\n{state}")


def main():
    list_agents = []
    list_territories = []

    num_agents = int(input("Please Enter Number of Agents (Vehicles): "))
    print("NUMBER OF AGENT PREFERNCES AND TERRITORY FEATURES MUST BE THE SAME")
    for agent_i in range(1, num_agents + 1):
            preference_vector_str = input(f"Enter Agent {agent_i}'s "
            "Preference Vector(Comma-Sperated w/ Space (', ')): ")
            preference_vector = [int(x.strip()) for x in preference_vector_str.split(',')]
            list_agents.append(Agent(agent_i, preference_vector))
    
    num_territories = int(input("Please Enter Number of Territories (Platoons): "))
    print("NUMBER OF AGENT PREFERNCES AND TERRITORY FEATURES MUST BE THE SAME")
    for territory_i in range(1, num_territories + 1):
            feature_vector_str = input(f"Enter Agent {territory_i}'s "
            "Feature Vector(Comma-Sperated w/ Space (', ')): ")
            feature_vector = [int(x.strip()) for x in feature_vector_str.split(',')]
            list_territories.append(Territory(territory_i, feature_vector))
    user_case =  TestCase(list_agents, list_territories)

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
    user_case.run()
    case1.run()
    case2.run()


if __name__ == "__main__":
    main()
