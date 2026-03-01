import random
import matplotlib.pyplot as plt
import csv
import math

# DYNAMIC ENVIRONMENT

def calculate_entropy(choices):
    counts = {c: choices.count(c) for c in set(choices)}
    total = len(choices)

    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def calculate_trust_volatility(trust_history):
    changes = [abs(trust_history[i] - trust_history[i-1]) 
               for i in range(1, len(trust_history))]
    return sum(changes) / len(changes) if changes else 0

def get_environment(round_num):
    if round_num < 300:
        prob_A, prob_B = 0.7, 0.3
    elif round_num < 600:
        prob_A, prob_B = 0.4, 0.6
    else:
        prob_A, prob_B = 0.5, 0.5

    option_A = {"prob": prob_A, "reward": 10}
    option_B = {"prob": prob_B, "reward": 50}

    return option_A, option_B


def play_round(choice, round_num):
    option_A, option_B = get_environment(round_num)
    option = option_A if choice == "A" else option_B

    if random.random() < option["prob"]:
        return option["reward"]
    return 0

# HUMAN AGENT

class HumanAgent:
    def __init__(self, name, risk_tolerance):
        self.name = name
        self.risk_tolerance = risk_tolerance
        self.trust = 0.5

    def choose(self):
        if random.random() < self.risk_tolerance:
            return "B"
        return "A"

    def reconsider(self, ai_choice, peer_choices):
        # AI influence
        ai_influence = ai_choice if random.random() < self.trust else None

        # Peer majority influence
        majority = max(set(peer_choices), key=peer_choices.count)
        peer_influence = majority if random.random() < 0.5 else None

        influences = [i for i in [ai_influence, peer_influence] if i]

        if influences:
            return random.choice(influences)

        return self.choose()

    def update_trust(self, ai_reward):
        if ai_reward > 0:
            self.trust = min(1.0, self.trust + 0.01)
        else:
            self.trust = max(0.0, self.trust - 0.01)

# AI AGENT (MULTIPLE STRATEGIES)

class AIAgent:
    def __init__(self, name, strategy="rational", error_rate=0.1):
        self.name = name
        self.strategy = strategy
        self.error_rate = error_rate

    def choose(self):
        ev_A = 0.7 * 10
        ev_B = 0.3 * 50
        rational_choice = "B" if ev_B > ev_A else "A"

        if self.strategy == "rational":
            choice = rational_choice
        elif self.strategy == "conservative":
            choice = "A"
        elif self.strategy == "risky":
            choice = "B"
        elif self.strategy == "random":
            choice = random.choice(["A", "B"])
        elif self.strategy == "adversarial":
            choice = "A" if rational_choice == "B" else "B"
        else:
            choice = rational_choice

        if random.random() < self.error_rate:
            choice = "A" if choice == "B" else "B"

        return choice

# GROUP DECISION MECHANISM

def group_decision(choices, ai_choice, method="majority"):
    if method == "majority":
        return max(set(choices), key=choices.count)

    elif method == "confidence":
        weighted_choices = choices + [ai_choice] * 2
        return max(set(weighted_choices), key=weighted_choices.count)

    elif method == "ai_leader":
        return ai_choice

    return max(set(choices), key=choices.count)

# SAVE RESULTS

def save_results_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Round", "Average_Trust"])
        writer.writerows(data)

# MAIN SIMULATION

def run_simulation(rounds=1000):
    entropy_history = []
    minority_correct = 0
    humans = [
        HumanAgent("Safe", 0.2),
        HumanAgent("Balanced", 0.5),
        HumanAgent("Risky", 0.8)
    ]

    ai = AIAgent("AI", strategy="rational", error_rate=0.15)
    #ai = AIAgent("AI", strategy="random")
    #ai = AIAgent("AI", strategy="conservative")
    #ai = AIAgent("AI", strategy="risky")
    #ai = AIAgent("AI", strategy="adversarial")
    human_only_total = 0
    ai_only_total = 0
    human_ai_total = 0

    trust_history = []
    csv_log = []

    for round_num in range(rounds):

        # Humans only scenario
        for human in humans:
            human_only_total += play_round(human.choose(), round_num)

        # AI only scenario
        ai_choice = ai.choose()
        ai_reward = play_round(ai_choice, round_num)
        ai_only_total += ai_reward

        # Human + AI + Peer influence
        peer_choices = [h.choose() for h in humans]
        final_choices = []

        # Humans reconsider first
        for human in humans:
            final_choice = human.reconsider(ai_choice, peer_choices)
            final_choices.append(final_choice)
            human.update_trust(ai_reward)

        # NOW calculate entropy
        entropy = calculate_entropy(final_choices)
        entropy_history.append(entropy)

        # Minority correctness calculation
        majority_choice = max(set(final_choices), key=final_choices.count)
        minority_choice = "A" if majority_choice == "B" else "B"

        option_A, option_B = get_environment(round_num)

        majority_expected = option_A["prob"] * option_A["reward"] if majority_choice == "A" else option_B["prob"] * option_B["reward"]
        minority_expected = option_A["prob"] * option_A["reward"] if minority_choice == "A" else option_B["prob"] * option_B["reward"]

        if minority_expected > majority_expected:
            minority_correct += 1

        for human in humans:
            final_choice = human.reconsider(ai_choice, peer_choices)
            final_choices.append(final_choice)
            human.update_trust(ai_reward)

        # Collective group decision
        group_choice = group_decision(final_choices, ai_choice, method="majority")
        reward = play_round(group_choice, round_num)

        human_ai_total += reward * len(humans)

        avg_trust = sum(h.trust for h in humans) / len(humans)
        trust_history.append(avg_trust)
        csv_log.append([round_num, avg_trust])

    save_results_to_csv("simulation_results.csv", csv_log)

    human_only_avg = human_only_total / rounds
    ai_only_avg = ai_only_total / rounds
    human_ai_avg = human_ai_total / rounds

    print("\n===== PERFORMANCE COMPARISON =====")
    print(f"{'Scenario':<20} {'Avg Reward':<15}")
    print("-" * 35)
    print(f"{'Humans Only':<20} {human_only_avg:.2f}")
    print(f"{'AI Only':<20} {ai_only_avg:.2f}")
    print(f"{'Humans + AI':<20} {human_ai_avg:.2f}")

    # Performance graph
    plt.figure()
    labels = ["Humans Only", "AI Only", "Humans + AI"]
    values = [human_only_avg, ai_only_avg, human_ai_avg]
    plt.bar(labels, values)
    plt.title("Collective Intelligence Comparison")
    plt.ylabel("Average Reward")
    plt.show()

    avg_entropy = sum(entropy_history) / len(entropy_history)
    trust_volatility = calculate_trust_volatility(trust_history)

    print("\n===== ADVANCED RESEARCH METRICS =====")
    print("Average Decision Entropy:", round(avg_entropy, 3))
    print("Trust Volatility:", round(trust_volatility, 3))
    print("Minority Correctness Rate:", minority_correct / rounds)

    # Trust evolution graph
    plt.figure()
    plt.plot(trust_history)
    plt.title("Trust Evolution Over Time")
    plt.xlabel("Rounds")
    plt.ylabel("Average Trust")
    plt.show()

# RUN

run_simulation(1000)
