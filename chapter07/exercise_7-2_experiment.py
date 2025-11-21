from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

# Simple deterministic Gridworld 5x5
N = 5
terminal_states = [(0, 0), (4, 4)]
actions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
gamma = 1.0
alpha = 0.1


def step(s, a):
    if s in terminal_states:
        return s, 0
    x, y = s
    dx, dy = a
    nx, ny = np.clip(x + dx, 0, N - 1), np.clip(y + dy, 0, N - 1)
    r = -1
    return (nx, ny), r


def run_experiment(n_steps=3, episodes=1000):
    def nstep_td(use_delta_sum=False):
        V = defaultdict(float)
        errors = []

        for ep in range(episodes):
            s = (2, 2)
            states = [s]
            rewards = [0]

            t = 0
            T = 1e9

            while True:
                if t < T:
                    a = actions[np.random.randint(len(actions))]
                    s_next, r = step(s, a)
                    states.append(s_next)
                    rewards.append(r)
                    if s_next in terminal_states:
                        T = t + 1
                    s = s_next

                tau = t - n_steps + 1
                if tau >= 0:
                    # Compute update target G
                    if use_delta_sum:
                        # ---- use sum of TD errors ----
                        G = 0
                        for k in range(tau, min(tau + n_steps, T) - 1):
                            delta = (
                                rewards[k + 1] + gamma * V[states[k + 1]] - V[states[k]]
                            )
                            G += (gamma ** (k - tau)) * delta
                        target = V[states[tau]] + G
                    else:
                        # ---- standard n-step return ----
                        G = 0
                        for i in range(tau + 1, min(tau + n_steps, T) + 1):
                            G += (gamma ** (i - tau - 1)) * rewards[i]
                        if tau + n_steps < T:
                            G += gamma**n_steps * V[states[tau + n_steps]]
                        target = G

                    V[states[tau]] += alpha * (target - V[states[tau]])

                if tau == T - 1:
                    break
                t += 1

            # RMS error vs true V of gridworld
            trueV = {
                (i, j): -(abs(i - 0) + abs(j - 0)) for i in range(5) for j in range(5)
            }
            rmse = np.sqrt(np.mean([(V[s] - trueV[s]) ** 2 for s in trueV]))
            errors.append(rmse)

        return np.array(errors)

    return nstep_td(False), nstep_td(True)


A, B = run_experiment()


plt.plot(A, label="Standard n-step TD")
plt.plot(B, label="Sum-of-TD-errors version")
plt.legend()
plt.xlabel("Episode")
plt.ylabel("RMSE")
plt.show()
