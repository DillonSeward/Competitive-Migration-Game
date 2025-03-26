from typing import Optional, List, Dict
import numpy as np


class Territory:
    def __init__(self, id: int, features: List[float] = None):
        self.id = id
        self.features = np.array(features)
        self.count = 0

    def __str__(self):
        return (
            f"ID: {self.id}, Count: {self.count}, Agents: {[a.id for a in self.agents]}"
        )


class Agent:
    def __init__(self, id: int, preferences: List[float]):
        self.id = id
        self.preferences = np.array(preferences)

    def evaluate(self, territory_map: Dict[int, Territory]) -> Optional[int]:
        alpha = 1
        beta = 1
        vals = {}
        for id, territory in territory_map.items():
            eval = (alpha * np.dot(self.preferences, territory.features)) - (
                beta * territory.count
            )
            vals[id] = eval

        best_id = max(vals, key=vals.get)

        return best_id


class GlobalState:
    def __init__(self):
        # Agents in territories
        self.territory_agents: Dict[int, List[Agent]] = {}
        self.territories: Dict[int, Territory] = {}
        self.incoming: List[Agent] = []

    def add_agents(self, agents: List[Agent]):
        for agent in agents:
            self.incoming.append(agent)

    def add_territories(self, territories: List[Territory]):
        for territory in territories:
            self.territories[territory.id] = territory
            self.territory_agents[territory.id] = []

    def add_agent_to_territory(self, agent: Agent, tId: int):
        self.territories.get(tId).count += 1
        t_agents = self.territory_agents.get(tId)
        t_agents.append(agent)

    def __str__(self):
        territory_info = "\n".join(
            f"Territory {tid}: {[agent.id for agent in agents]}"
            for tid, agents in self.territory_agents.items()
        )

        return (
            f"Territories and Agents:\n{territory_info}\n\n"
            f"All Territories: {list(self.territories.keys())}\n"
            f"Incoming Agents: {[agent.id for agent in self.incoming]}"
        )

    def main_loop(self):
        print("MAIN")

        while len(self.incoming) > 0:
            territory_change: Optional[int] = None
            agent = self.incoming.pop(0)
            print("adding agent: ", agent.id)
            territory_change = agent.evaluate(self.territories)
            if territory_change is not None:
                self.add_agent_to_territory(agent, territory_change)

            if territory_change is not None:
                id = territory_change
                territory_change = None
                t_agents = self.territory_agents.get(id)
                for i, agent in enumerate(t_agents):
                    territory_change = agent.evaluate(self.territories)
                    if territory_change is not None:
                        t_agents.pop(i)
                        self.add_agent_to_territory(agent, territory_change)
                        break

        print(self)
