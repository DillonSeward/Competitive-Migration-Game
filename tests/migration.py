from cmg.lib import Agent, Territory, GlobalState
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
                    print(
                        f"✅ Agent {agent.id} is in NE (no better territory found)\n")
                else:
                    print(
                        f"❌ Agent {agent.id} IS NOT in NE (better territory(s): {max_keys}\n")

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
          "USER IN-LINE INPUT: [3] \n"
          "RUN ALPHA/BETA TESTS [4]")
    user_input_type = int(input(""))

    match user_input_type:
        case 1:
            list_agents = []
            list_territories = []

            num_agents = int(
                input("Please Enter Number of Agents (Vehicles): "))
            num_territories = int(
                input("Please Enter Number of Territories (Platoons): "))
            num_feat_pref = int(
                input("Please Enter Number of Features/Prefences(Must be the same): "))

            for agent_i in range(1, num_agents + 1):
                rand_pref_vector = np.random.uniform(
                    0, 1, num_feat_pref).tolist()
                # THIS IS [0, 1) (can be 0 but not 1) #
                print(f"Vector for Agent {agent_i} = {rand_pref_vector}\n")
                list_agents.append(Agent(agent_i, rand_pref_vector))
            for territory_i in range(1, num_territories + 1):
                rand_feat_vector = np.random.uniform(
                    0, 1, num_feat_pref).tolist()
                # THIS IS [0, 1) (can be 0 but not 1) #
                print(f"Vector for Territory {
                      territory_i} = {rand_feat_vector}\n")
                list_territories.append(
                    Territory(territory_i, rand_feat_vector))

            rand_case = TestCase(list_agents, list_territories)
            rand_case.run()

        case 2:
            print("Case 2 not deifned yet")

        case 3:
            list_agents = []
            list_territories = []

            num_agents = int(
                input("Please Enter Number of Agents (Vehicles): "))
            print("NUMBER OF AGENT PREFERNCES AND TERRITORY FEATURES MUST BE THE SAME")
            for agent_i in range(1, num_agents + 1):
                preference_vector_str = input(f"Enter Agent {agent_i}'s "
                                              "Preference Vector(Comma-Sperated w/ Space (', ')): ")
                preference_vector = [int(x.strip())
                                     for x in preference_vector_str.split(',')]
                list_agents.append(Agent(agent_i, preference_vector))

            num_territories = int(
                input("Please Enter Number of Territories (Platoons): "))
            print("NUMBER OF AGENT PREFERNCES AND TERRITORY FEATURES MUST BE THE SAME")
            for territory_i in range(1, num_territories + 1):
                feature_vector_str = input(f"Enter Agent {territory_i}'s "
                                           "Feature Vector(Comma-Sperated w/ Space (', ')): ")
                feature_vector = [int(x.strip())
                                  for x in feature_vector_str.split(',')]
                list_territories.append(Territory(territory_i, feature_vector))

            user_case = TestCase(list_agents, list_territories)
            user_case.run()

        case 4:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D projection

            num_agents = int(input("Enter number of agents (vehicles): "))
            num_territories = int(input("Enter number of territories (platoons): "))
            num_feat_pref = int(input("Enter number of features/preferences: "))

            # Generate fixed base vectors for reproducibility across experiments
            base_pref_vectors = [np.random.rand(num_feat_pref).tolist() for _ in range(num_agents)]
            base_feat_vectors = [np.random.rand(num_feat_pref).tolist() for _ in range(num_territories)]

            def run_sim(alpha_val, beta_val):
                agents = [
                    Agent(id=i, preferences=base_pref_vectors[i - 1], alpha=alpha_val, beta=beta_val)
                    for i in range(1, num_agents + 1)
                ]
                territories = [
                    Territory(id=i, features=base_feat_vectors[i - 1])
                    for i in range(1, num_territories + 1)
                ]

                state = GlobalState()
                state.add_agents(agents)
                state.add_territories(territories)
                state.start()

                max_agents = np.max([len(a) for a in state.territory_agents.values()])
                return state.switches, max_agents

            # Define hybrid alpha/beta values for labeling
            alpha_labels = [round(x, 2) for x in np.concatenate([np.arange(0.1, 1.0, 0.1), np.arange(1.0, 11.0, 1.0)])]
            beta_labels  = [round(x, 2) for x in np.concatenate([np.arange(0.1, 1.0, 0.1), np.arange(1.0, 11.0, 1.0)])]

            num_alpha = len(alpha_labels)
            num_beta = len(beta_labels)

            # Index-based meshgrid (visually uniform spacing)
            alpha_idx = np.arange(num_alpha)
            beta_idx = np.arange(num_beta)
            A, B = np.meshgrid(beta_idx, alpha_idx)

            # Fill data matrices
            switch_matrix = np.zeros((num_alpha, num_beta))
            max_agents_matrix = np.zeros((num_alpha, num_beta))

            print("\nRunning visually-even alpha-beta sweep...")

            for i, alpha in enumerate(alpha_labels):
                for j, beta in enumerate(beta_labels):
                    switches, max_agents = run_sim(alpha, beta)
                    switch_matrix[i, j] = switches
                    max_agents_matrix[i, j] = max_agents

            # ----- Plot: Switches Surface -----
            fig = plt.figure(figsize=(14, 6))
            ax1 = fig.add_subplot(121, projection='3d')
            surf1 = ax1.plot_surface(A, B, switch_matrix, cmap='viridis')

            ax1.set_title("Number of Switches")
            ax1.set_xlabel("Beta")
            ax1.set_ylabel("Alpha")
            ax1.set_zlabel("Switches")
            ax1.view_init(elev=30, azim=135)
            fig.colorbar(surf1, ax=ax1, shrink=0.5, pad = 0.15)

            # ----- Plot: Max Agents Surface -----
            ax2 = fig.add_subplot(122, projection='3d')
            surf2 = ax2.plot_surface(A, B, max_agents_matrix, cmap='plasma')

            ax2.set_title("Max Agents in Any Territory")
            ax2.set_xlabel("Beta")
            ax2.set_ylabel("Alpha")
            ax2.set_zlabel("Max Agents")
            ax2.view_init(elev=30, azim=135)
            fig.colorbar(surf2, ax=ax2, shrink=0.5, pad = 0.15)

            # ✅ Clean tick labels and avoid crowding
            label_stride = 2

            # Axes 1
            ax1.set_xticks(beta_idx[::label_stride])
            ax1.set_xticklabels(beta_labels[::label_stride], rotation=30, fontsize=8)
            ax1.set_yticks(alpha_idx[::label_stride])
            ax1.set_yticklabels(alpha_labels[::label_stride], fontsize=8)

            # Axes 2
            ax2.set_xticks(beta_idx[::label_stride])
            ax2.set_xticklabels(beta_labels[::label_stride], rotation=30, fontsize=8)
            ax2.set_yticks(alpha_idx[::label_stride])
            ax2.set_yticklabels(alpha_labels[::label_stride], fontsize=8)

            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()
