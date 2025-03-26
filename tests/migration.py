from cmg.lib import Agent, Territory, GlobalState
from typing import List, Dict


def mock_agents() -> List[Agent]:
    all = []
    all.append(Agent(1, [4, 3, 5, 2, 1]))
    all.append(Agent(2, [5, 2, 3, 4, 1]))
    all.append(Agent(3, [1, 5, 4, 3, 1]))
    all.append(Agent(4, [5, 2, 3, 4, 1]))
    all.append(Agent(5, [1, 2, 3, 4, 5]))
    return all


def mock_territories() -> List[Territory]:
    all = []
    all.append(Territory(1, [0, 0, 1, 0, 0]))
    all.append(Territory(2, [1, 0, 0, 0, 0]))
    all.append(Territory(3, [0, 1, 0, 0, 0]))
    return all


def main():
    expected_territories: Dict[int, List[int]] = {}
    expected_territories[1] = [1, 5]
    expected_territories[2] = [2, 4]
    expected_territories[3] = [3]

    state = GlobalState()
    agents = mock_agents()
    territories = mock_territories()
    state.add_agents(agents)
    state.add_territories(territories)
    state.main_loop()

    got_territories: Dict[int, List[int]] = {}

    # Iterate over each territory's agents and gather their IDs
    for id, agent_list in state.territory_agents.items():
        got_territories[id] = [agent.id for agent in agent_list]

    print("Expected Territories:", expected_territories)
    print("Got Territories:", got_territories)

    # Compare sets of agent IDs instead of lists
    for territory_id, expected_agents in expected_territories.items():
        got_agents = got_territories.get(territory_id, [])

        # Convert both lists to sets and compare
        if set(expected_agents) != set(got_agents):
            print(f"Territory {territory_id} does not match.")
            print(f"Expected: {expected_agents}, Got: {got_agents}")
        else:
            print("passed!")


if __name__ == "__main__":
    main()
