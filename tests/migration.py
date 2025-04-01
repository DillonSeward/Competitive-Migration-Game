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
    print("INPUT SOURCE\n"
          "RANDOMLY GENERATED AGENTS AND TERRITORIES [1]: \n"
          "INPUT FILE DATA(.csv): [2] \n"
          "USER IN-LINE INPUT: [3] ")
    user_input_type = int(input(""))
    
    match user_input_type:
        case 1:
            list_agents = []
            list_territories = []

            num_agents = int(input("Please Enter Number of Agents (Vehicles): ")) 
            num_territories = int(input("Please Enter Number of Territories (Platoons): "))
            num_feat_pref = int(input("Please Enter Number of Features/Prefences(Must be the same): "))
            
            for agent_i in range(1, num_agents + 1):
                rand_pref_vector = np.random.uniform(0, 1, num_feat_pref).tolist()
                # THIS IS [0, 1) (can be 0 but not 1) #
                print(f"Vector for Agent {agent_i} = {rand_pref_vector}\n")
                list_agents.append(Agent(agent_i, rand_pref_vector))
            for territory_i in range(1, num_territories + 1):
                rand_feat_vector = np.random.uniform(0, 1, num_feat_pref).tolist()
                # THIS IS [0, 1) (can be 0 but not 1) #
                print(f"Vector for Territory {territory_i} = {rand_feat_vector}\n")
                list_territories.append(Territory(territory_i, rand_feat_vector))
                
            rand_case =  TestCase(list_agents, list_territories)
            rand_case.run()

        case 2:
            print("Case 2 not deifned yet")

        case 3:
            list_agents = []
            list_territories= []

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
            user_case.run()

if __name__ == "__main__":
    main()
