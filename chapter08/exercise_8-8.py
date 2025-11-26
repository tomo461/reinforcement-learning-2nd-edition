import matplotlib.pyplot as plt
import numpy as np


class Exercise8_8:
    def __init__(self):
        self.n = 0  # number of states
        self.b = 0  # number of branches per state
        self.successor = None  # shape (n, 2, b)
        self.R = None  # shape (n, b+1, 2)
        self.Q = None  # shape (n, 2)
        self.gamma = 0.9  # probability of non-terminal transition
        self.alpha = 0.1  # unused
        self.epsilon = 0.1  # exploration probability
        self.max_num_tasks = 2000
        self.randomness = [None] * self.max_num_tasks  # to store random states
        self.policy = None
        self.V = None
        self.rng = None  # Current random state

        # Initialize randomness storage
        # Mimicking Lisp's (standardize-random-state) and loop
        # We generate a sequence of seeds/states to ensure reproducibility of tasks
        init_rng = np.random.RandomState(0)
        # Advance state slightly to match "advance-random-state 0" if it means skipping
        # But here we just generate states.

        for task in range(self.max_num_tasks):
            # (loop repeat 17 do (random 2))
            for _ in range(17):
                init_rng.randint(2)
            # (setf (aref randomness task) (make-random-state))
            # We store the state of the generator
            seed = init_rng.randint(0, 2**32)
            self.randomness[task] = np.random.RandomState(seed)

    def setup(self, n_arg, b_arg):
        self.n = n_arg
        self.b = b_arg
        self.successor = np.zeros((self.n, 2, self.b), dtype=int)
        self.R = np.zeros((self.n, self.b + 1, 2))
        self.Q = np.zeros((self.n, 2))
        self.policy = np.zeros(self.n, dtype=int)
        self.V = np.zeros(self.n)

    def init(self, task_num):
        # (setq *random-state* (make-random-state (aref randomness task-num)))
        # We use a copy of the stored state to avoid mutating the stored one if we want to reuse it exactly
        # But RandomState is mutable. We should create a new one with the same state?
        # Or just use the stored one if we don't mind it advancing (since we only run each task once per experiment usually, or we re-generate).
        # To be safe and allow re-runs, we should clone it.
        # Getting state and creating new RandomState:
        state = self.randomness[task_num].get_state()
        self.rng = np.random.RandomState()
        self.rng.set_state(state)

        for s in range(self.n):
            for a in range(2):
                self.Q[s, a] = 0.0
                # (setf (aref R s b a) (random-normal))
                self.R[s, self.b, a] = self.rng.randn()  # Terminal reward

                # (loop for sp in (random-b-of-n b n) ...)
                # random-b-of-n: unique b integers from 0..n-1
                candidates = self.rng.choice(self.n, self.b, replace=False)
                for i, sp in enumerate(candidates):
                    self.successor[s, a, i] = sp
                    self.R[s, i, a] = self.rng.randn()

    def next_state(self, s, a):
        # (with-prob gamma (aref successor s a (random b)) n)
        if self.rng.rand() < self.gamma:
            idx = self.rng.randint(self.b)
            return self.successor[s, a, idx]
        else:
            return self.n  # Terminal state

    def full_backup(self, s, a):
        # (+ (* (- 1 gamma) (aref R s b a))
        #    (* gamma (/ b)
        #       (loop for i below b
        #             for sp = (aref successor s a i)
        #             sum (aref R s i a)
        #             sum (* gamma (loop for ap below 2 maximize (aref Q sp ap))))))

        term1 = (1 - self.gamma) * self.R[s, self.b, a]

        sum_val = 0.0
        for i in range(self.b):
            sp = self.successor[s, a, i]
            r_sia = self.R[s, i, a]

            # maximize (aref Q sp ap)
            # sp is in 0..n-1
            max_q = np.max(self.Q[sp])

            sum_val += r_sia + self.gamma * max_q

        term2 = self.gamma * (1.0 / self.b) * sum_val

        return term1 + term2

    def measure_performance(self):
        # (loop for s below n do (setf (aref V s) 0.0) ...)
        self.V.fill(0.0)
        for s in range(self.n):
            if self.Q[s, 0] >= self.Q[s, 1]:
                self.policy[s] = 0
            else:
                self.policy[s] = 1

        # (loop for delta = ... until (< delta .001))
        while True:
            delta = 0.0
            for s in range(self.n):
                old_v = self.V[s]
                # (setf (aref V s) (full-backup s (aref policy s)))
                # Note: full_backup uses self.Q, not self.V.
                new_v = self.full_backup(s, self.policy[s])
                self.V[s] = new_v
                delta += abs(old_v - new_v)

            if delta < 0.001:
                break

        return self.V[0]

    def runs_sweeps(self, n_arg, b_arg, num_runs, num_sweeps, sweeps_per_measurement):
        if self.n != n_arg or self.b != b_arg:
            self.setup(n_arg, b_arg)

        backups_per_measurement = int(sweeps_per_measurement * 2 * self.n)
        backups_per_sweep = self.n * 2
        num_backups = num_sweeps * backups_per_sweep
        num_measurements = int(num_backups / backups_per_measurement)
        perf = np.zeros(num_measurements)

        for run in range(num_runs):
            print(f"Running sweep run {run}...", end="\r")
            self.init(run)
            # (format t "~A " run)
            # print(f"{run}", end=' ', flush=True)

            backups = 0
            for _ in range(num_sweeps):
                for s in range(self.n):
                    for a in range(2):
                        if backups % backups_per_measurement == 0:
                            m_idx = backups // backups_per_measurement
                            if m_idx < num_measurements:
                                perf[m_idx] += self.measure_performance()

                        self.Q[s, a] = self.full_backup(s, a)
                        backups += 1

        print()
        return perf / num_runs

    def runs_trajectories(
        self, n_arg, b_arg, num_runs, num_sweeps, sweeps_per_measurement
    ):
        if self.n != n_arg or self.b != b_arg:
            self.setup(n_arg, b_arg)
        backups_per_measurement = int(sweeps_per_measurement * 2 * self.n)
        backups_per_sweep = self.n * 2
        num_backups = num_sweeps * backups_per_sweep
        num_measurements = int(num_backups / backups_per_measurement)
        perf = np.zeros(num_measurements)

        for run in range(num_runs):
            print(f"Running trajectory run {run}...", end="\r")
            self.init(run)
            # print(f"{run}", end=' ', flush=True)

            backups = 0
            while backups < num_backups:
                state = 0  # Start state
                while state != self.n:
                    # Action selection
                    if self.rng.rand() < self.epsilon:
                        action = self.rng.randint(2)
                    else:
                        if self.Q[state, 0] >= self.Q[state, 1]:
                            action = 0
                        else:
                            action = 1

                    next_s = self.next_state(state, action)

                    if backups % backups_per_measurement == 0:
                        m_idx = backups // backups_per_measurement
                        if m_idx < num_measurements:
                            perf[m_idx] += self.measure_performance()

                    self.Q[state, action] = self.full_backup(state, action)
                    backups += 1

                    if backups == num_backups:
                        break

                    state = next_s

        print()
        return perf / num_runs

    def both(self, n_arg, b_arg, runs_arg, sweeps_arg, measure_arg):
        print(
            f"n={n_arg}, b={b_arg}, runs={runs_arg}, sweeps={sweeps_arg}, measure={measure_arg}"
        )
        perf_sweeps = self.runs_sweeps(n_arg, b_arg, runs_arg, sweeps_arg, measure_arg)
        print("Sweeps:", perf_sweeps)
        perf_traj = self.runs_trajectories(
            n_arg, b_arg, runs_arg, sweeps_arg, measure_arg
        )
        print("Trajectories:", perf_traj)
        return perf_sweeps, perf_traj

    def reproduce_figure_8_8_above(self):
        n = 1000
        runs = 200
        sweeps = 10
        measure = 0.2

        b_values = [1, 3, 10]
        colors = {1: "green", 3: "red", 10: "blue"}

        plt.figure(figsize=(10, 8))

        for b in b_values:
            print(f"Running experiment for n={n}, b={b}...")
            perf_sweeps, perf_traj = self.both(n, b, runs, sweeps, measure)

            backups_per_measurement = int(measure * 2 * n)
            x = np.arange(1, len(perf_sweeps) + 1) * backups_per_measurement

            plt.plot(x, perf_sweeps, label=f"b={b} uniform", color=colors[b], alpha=0.4)
            plt.plot(x, perf_traj, label=f"b={b} on-policy", color=colors[b])

        plt.title(f"{n:,} STATES")
        plt.xlabel("Computation time, in expected updates")
        plt.ylabel("Value of start state under greedy policy")
        plt.legend()
        plt.savefig("exercise_8-8_above.png")
        print("Graph saved to exercise_8-8_above.png")
        # plt.show()

    def reproduce_figure_8_8_below(self):
        n = 10000
        runs = 200
        sweeps = 10
        measure = 0.2

        b_values = [1, 3]
        colors = {1: "green", 3: "red"}

        plt.figure(figsize=(10, 8))

        for b in b_values:
            print(f"Running experiment for n={n}, b={b}...")
            perf_sweeps, perf_traj = self.both(n, b, runs, sweeps, measure)

            backups_per_measurement = int(measure * 2 * n)
            x = np.arange(1, len(perf_sweeps) + 1) * backups_per_measurement

            plt.plot(x, perf_sweeps, label=f"b={b} uniform", color=colors[b], alpha=0.4)
            plt.plot(x, perf_traj, label=f"b={b} on-policy", color=colors[b])

        plt.title(f"{n:,} STATES")
        plt.xlabel("Computation time, in expected updates")
        plt.ylabel("Value of start state under greedy policy")
        plt.legend()
        plt.savefig("exercise_8-8_below.png")
        print("Graph saved to exercise_8-8_below.png")
        # plt.show()


if __name__ == "__main__":
    ex = Exercise8_8()
    ex.reproduce_figure_8_8_below()
