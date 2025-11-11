# Gambler's problem.  The gambler has a stake s between 0 and 100.  At each
# play he wagers an integer <= s.  He wins that much with prob p, else he
# loses that much.  If he builds his stake to 100 he wins (thus he never
# wagers more than (- 100 s)); if his stake falls to 0 he loses.

# Thus, the stake s is the state the actions are the size of the bid.

# Here we implement value iteration.

import numpy as np

# Initialize value function array
V = np.zeros(101)
V[100] = 1
p = 0.45


def backup_action(s, a):
    """Calculate the expected value of taking action a in state s"""
    return p * V[s + a] + (1 - p) * V[s - a]


def value_iteration(epsilon=1e-8):
    """Value iteration to the criterion epsilon"""
    iterations = []

    while True:
        # Store current iteration's values
        iterations.append([(i, V[i]) for i in range(1, 100)])

        # Calculate max change in this iteration
        delta = 0
        for s in range(1, 100):
            old_V = V[s]
            # Find best action value
            V[s] = max(backup_action(s, a) for a in range(1, min(s, 100 - s) + 1))
            delta = max(delta, abs(old_V - V[s]))

        # Check convergence
        if delta < epsilon:
            break

    return iterations


def policy(s, epsilon=1e-10):
    """Return the best action for state s"""
    best_value = -1
    best_action = None

    for a in range(1, min(s, 100 - s) + 1):
        this_value = backup_action(s, a)
        if this_value > best_value + epsilon:
            best_value = this_value
            best_action = a

    return best_action


if __name__ == "__main__":
    iterations = value_iteration()

    # Print the results
    print("Optimal Value Function:")
    for s in range(101):
        print(f"V({s}) = {V[s]:.6f}")

    print("\nOptimal Policy:")
    for s in range(1, 100):
        a = policy(s)
        print(f"Policy({s}) = Bet {a}")
