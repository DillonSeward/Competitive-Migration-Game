from cmg.lib import Agent, Territory, GlobalState
from typing import List, Dict


class TestCase:
    def __init__(
        self,
        agents: List[Agent],
        territories: List[Territory],
        expected: Dict[int, List[int]],
    ):
        self.agents = agents
        self.territories = territories
        self.expected = expected

    def validate(state: GlobalState):
        for tId, agents in state.territory_agents.items():
            for agent in agents:
                evals = agent.evals(state.territories)
                print(f"agent {agent.id} evals: ", evals)
                max_eval = max(evals.values(), default=float("-inf"))
                max_keys = [k for k, v in evals.items() if v == max_eval]
                print(f"agent {agent.id} should be in any of: {max_keys}")

                # expected_territory = agent.check_migration(None, state.territories)
                # if expected_territory != tId:
                # print(
                #     f"Agent {agent.id} is not in expected territory\nexpected: {expected_territory}\ngot: {tId}"
                # )

    def run_test(self):
        print("Running Test Case")
        state = GlobalState()
        state.add_agents(self.agents)
        state.add_territories(self.territories)
        state.run()

        TestCase.validate(state)

        print(f"Main Loop Ended:\n{state}")

        got_territories: Dict[int, List[int]] = {}

        # Iterate over each territory's agents and gather their IDs
        for id, agent_list in state.territory_agents.items():
            got_territories[id] = [agent.id for agent in agent_list]

        print("Expected Territories:", self.expected)
        # print("Got Territories:", got_territories)

        # Compare sets of agent IDs instead of lists
        for territory_id, expected_agents in self.expected.items():
            got_agents = got_territories.get(territory_id, [])

            # Convert both lists to sets and compare
            if set(expected_agents) != set(got_agents):
                print(f"Territory {territory_id} does not match.")
                print(f"Expected: {expected_agents}, Got: {got_agents}")
            else:
                print("passed!")


def main():
    case1 = TestCase(
        {
            Agent(1, [4, 3, 5, 2, 1]),
            Agent(2, [5, 2, 3, 4, 1]),
            Agent(3, [1, 5, 4, 3, 1]),
            Agent(4, [5, 2, 3, 4, 1]),
            Agent(5, [1, 2, 3, 4, 5]),
        },
        {
            Territory(1, [0, 0, 1, 0, 0]),
            Territory(2, [1, 0, 0, 0, 0]),
            Territory(3, [0, 1, 0, 0, 0]),
        },
        {1: [1, 5], 2: [2, 4], 3: [3]},
    )
    case2 = TestCase(
        {
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
        },
        {
            Territory(1, [0, 0, 1, 0, 0]),
            Territory(2, [1, 0, 0, 0, 0]),
            Territory(3, [0, 1, 0, 0, 0]),
        },
        {1: [1, 5], 5: [2, 4], 3: [3]},
    )
    case1.run_test()
    case2.run_test()


if __name__ == "__main__":
    main()
