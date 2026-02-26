import random
import matplotlib.pyplot as plt
import csv

# GAME ENVIRONMENT

def play_round(choice):
    option_A = {"prob": 0.7, "reward": 10}
    option_B = {"prob": 0.3, "reward": 50}

    option = option_A if choice == "A" else option_B

    if random.random() < option["prob"]:
        return option["reward"]
    return 0

# HUMAN AGENT

class HumanAgent:
    def __init__(self, name, risk_tolerance):
        self.name = name
        self.risk_tolerance = risk_tolerance
        self.trust = 0.5  # Initial trust in AI

    def choose(self):
        if random.random() < self.risk_tolerance:
            return "B"
        return "A"

    def reconsider(self, ai_choice):
        if random.random() < self.trust:
            return ai_choice
        return self.choose()

    def update_trust(self, ai_reward):
        if ai_reward > 0:
            self.trust = min(1.0, self.trust + 0.01)
        else:
            self.trust = max(0.0, self.trust - 0.01)

# AI AGENT

class AIAgent:
    def __init__(self, name, error_rate=0.1):
        self.name = name
        self.error_rate = error_rate

    def choose(self):
        ev_A = 0.7 * 10
        ev_B = 0.3 * 50

        correct_choice = "B" if ev_B > ev_A else "A"

        # AI makes mistake sometimes
        if random.random() < self.error_rate:
            return "A" if correct_choice == "B" else "B"

        return correct_choice

# SAVE RESULTS

def save_results_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Round", "Average_Trust"])
        writer.writerows(data)

# FULL SIMULATION

def run_simulation(rounds=1000):
    humans = [
        HumanAgent("Safe", 0.2),
        HumanAgent("Balanced", 0.5),
        HumanAgent("Risky", 0.8)
    ]

    ai = AIAgent("AI", error_rate=0.15)

    human_only_total = 0
    ai_only_total = 0
    human_ai_total = 0

    trust_history = []
    csv_log = []

    for round_num in range(rounds):

        #  Humans Only 
        for human in humans:
            human_only_total += play_round(human.choose())

        #  AI Only 
        ai_choice = ai.choose()
        ai_reward = play_round(ai_choice)
        ai_only_total += ai_reward

        # Humans + AI Influence 
        for human in humans:
            final_choice = human.reconsider(ai_choice)
            reward = play_round(final_choice)
            human_ai_total += reward
            human.update_trust(ai_reward)

        # Track average trust
        avg_trust = sum(h.trust for h in humans) / len(humans)
        trust_history.append(avg_trust)
        csv_log.append([round_num, avg_trust])

    # Save CSV
    save_results_to_csv("simulation_results.csv", csv_log)

    # Averages
    human_only_avg = human_only_total / rounds
    ai_only_avg = ai_only_total / rounds
    human_ai_avg = human_ai_total / rounds

    print("\n===== PERFORMANCE COMPARISON =====")
    print(f"{'Scenario':<20} {'Avg Reward':<15}")
    print("-" * 35)
    print(f"{'Humans Only':<20} {human_only_avg:.2f}")
    print(f"{'AI Only':<20} {ai_only_avg:.2f}")
    print(f"{'Humans + AI':<20} {human_ai_avg:.2f}")

    # Bar Chart
    labels = ["Humans Only", "AI Only", "Humans + AI"]
    values = [human_only_avg, ai_only_avg, human_ai_avg]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Collective Intelligence Comparison")
    plt.ylabel("Average Reward")
    plt.show()

    # Trust Evolution Graph
    plt.figure()
    plt.plot(trust_history)
    plt.title("Trust Evolution Over Time")
    plt.xlabel("Rounds")
    plt.ylabel("Average Trust")
    plt.show()

run_simulation(1000)