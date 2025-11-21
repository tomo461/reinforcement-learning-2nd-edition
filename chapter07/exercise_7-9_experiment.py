from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

# Small off-policy MDP for Exercise 7.9
# States: 'A','B','C' (C is terminal)
# Actions: 0 (a1), 1 (a2)
# Transitions:
# A,a1 -> B (+1), A,a2 -> C (0)
# B,a1 -> C (+1), B,a2 -> C (0)

gamma = 1.0
alpha = 0.1

states_all = ["A", "B", "C"]
terminal = "C"


def step(s, a):
    if s == "A":
        if a == 0:
            return "B", 1
        else:
            return "C", 0
    elif s == "B":
        if a == 0:
            return "C", 1
        else:
            return "C", 0
    else:
        return "C", 0


# Target policy pi: always a1 (0)
def pi(a, s):
    return 1.0 if a == 0 else 0.0


# Behavior policy b: a1 with 0.1, a2 with 0.9
def b_prob(a, s):
    return 0.1 if a == 0 else 0.9


trueV = {"A": 2.0, "B": 1.0, "C": 0.0}


def run_experiment(n_steps=2, episodes=500, runs=50):
    def naive_nstep_offpolicy():
        # Uses product importance sampling weight rho_{t:t+n-1}
        errors_runs = []
        for run in range(runs):
            V = defaultdict(float)
            errors = []
            for ep in range(episodes):
                s = "A"
                states = [s]
                actions = []
                rewards = [0]

                t = 0
                T = 1e9

                while True:
                    if t < T:
                        # choose action from behavior policy
                        a = 0 if np.random.rand() < 0.1 else 1
                        actions.append(a)
                        s_next, r = step(s, a)
                        states.append(s_next)
                        rewards.append(r)
                        if s_next == terminal:
                            T = t + 1
                        s = s_next

                    tau = t - n_steps + 1
                    if tau >= 0:
                        h = int(min(tau + n_steps, T))
                        # standard n-step return
                        G = 0.0
                        for i in range(tau + 1, h + 1):
                            G += (gamma ** (i - tau - 1)) * rewards[i]
                        if tau + n_steps < T:
                            G += (gamma**n_steps) * V[states[tau + n_steps]]

                        # importance weight product
                        rho = 1.0
                        for k in range(tau, min(tau + n_steps, int(T))):
                            a_k = actions[k]
                            s_k = states[k]
                            rho *= pi(a_k, s_k) / b_prob(a_k, s_k)

                        V[states[tau]] += alpha * rho * (G - V[states[tau]])

                    if tau == T - 1:
                        break
                    t += 1

                # RMSE
                rmse = np.sqrt(np.mean([(V[s] - trueV[s]) ** 2 for s in trueV]))
                errors.append(rmse)
            errors_runs.append(errors)
        return np.mean(np.array(errors_runs), axis=0)

    def per_decision_offpolicy():
        # Uses per-decision off-policy return (Eq 7.13)
        errors_runs = []
        for run in range(runs):
            V = defaultdict(float)
            errors = []
            for ep in range(episodes):
                s = "A"
                states = [s]
                actions = []
                rewards = [0]

                t = 0
                T = 1e9

                while True:
                    if t < T:
                        a = 0 if np.random.rand() < 0.1 else 1
                        actions.append(a)
                        s_next, r = step(s, a)
                        states.append(s_next)
                        rewards.append(r)
                        if s_next == terminal:
                            T = t + 1
                        s = s_next

                    tau = t - n_steps + 1
                    if tau >= 0:
                        h = int(min(tau + n_steps, T))
                        # boundary for G_h:h per Eq(7.13)
                        if h == int(T):
                            # episode ended at T, use R_T
                            G = rewards[int(T)]
                        else:
                            # horizon not terminal: use V(S_h)
                            G = V[states[h]]

                        # backward recursion for k = h-1 down to tau+1 (importance-sampled steps)
                        for k in range(h - 1, tau, -1):
                            a_k = actions[k]
                            s_k = states[k]
                            rho = pi(a_k, s_k) / b_prob(a_k, s_k)
                            G = rho * (rewards[k + 1] + gamma * G) + (1 - rho) * V[s_k]

                        # for the first step k == tau: do NOT importance-sample (per note under Eq(7.13))
                        # G = R_{tau+1} + gamma * G
                        G = rewards[tau + 1] + gamma * G

                        V[states[tau]] += alpha * (G - V[states[tau]])

                    if tau == T - 1:
                        break
                    t += 1

                rmse = np.sqrt(np.mean([(V[s] - trueV[s]) ** 2 for s in trueV]))
                errors.append(rmse)
            errors_runs.append(errors)
        return np.mean(np.array(errors_runs), axis=0)

    return naive_nstep_offpolicy(), per_decision_offpolicy()


if __name__ == "__main__":
    A, B = run_experiment(n_steps=2, episodes=500, runs=50)

    plt.plot(A, label="Naive rho-product n-step")
    plt.plot(B, label="Per-decision off-policy (Eq7.13)")
    plt.legend()
    plt.xlabel("Episode")
    plt.ylabel("RMSE")
    plt.show()
