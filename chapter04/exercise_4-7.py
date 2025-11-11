# 以下の変更を加えた上で、ジャックのレンタカー問題を解き直す方策反復のプログラムを書け。
# ジャックの一つ目の支所に勤める従業員の一人は、毎夜バスに乗って二つ目の支所の近くの自宅に帰るとする。
# 彼女は喜んでタダで車を1台、二つ目の支所に送り届けてくれる。
# 2台目以降は変わらず2ドルかかり、逆方向への車の移動にも変わらず2ドルかかる．
# 加えて、ジャックの各支所の駐車場の大きさには限界があるとする。
# （車を移動したあとに）支所に10台よりも多くの車があれば、（台数にかかわらず）二つ目の駐車場を使うため4ドルの追加料金がかかる。
# これらの非線形で恣意的なダイナミクスは実問題ではしばしば起こることであり、動的計画法以外の最適化手法では簡単に扱えない。
# プログラムが正しいかを確かめるために、まずは元の問題の結果を再現せよ。


from typing import Optional

import numpy as np
from scipy.stats import poisson  # type: ignore

# Global variables
RENT1_MEAN = 3
RENT2_MEAN = 4
RETURN1_MEAN = 3
RETURN2_MEAN = 2


MAX_CARS = 20
MAX_MOVE = 5
FREE_MOVE_CAR = 1  # 無料で移動できる車の台数
PARKING_LIMIT = 10  # 駐車場の台数制限

MOVE_CAR_COST = 2
ADDITIONAL_PARKING_COST = 4  # 駐車場超過料金
REWARDS_PER_MOVE = 10

GAMMA = 0.9
THETA = 1e-7

V: np.ndarray
policy: np.ndarray
P1: np.ndarray
P2: np.ndarray
R1: np.ndarray
R2: np.ndarray


# ポアソン分布の確率を事前計算してキャッシュ
poisson_cache = {}


def show_value():
    print("[")
    for i in range(V.shape[0]):
        print(" ", end="")
        print("[", end="")
        for j in range(V.shape[1]):
            print(f"{V[i, j]:6.2f}", end="")
            if j < V.shape[1] - 1:
                print(", ", end="")
        print(" ]", end="")
        if i < V.shape[0] - 1:
            print(",", end="")
        print()
    print("]")


def show_policy():
    print("[")
    for i in range(policy.shape[0]):
        print(" ", end="")
        print("[", end="")
        for j in range(policy.shape[1]):
            print(f"{policy[i, j]:2d}", end="")
            if j < policy.shape[1] - 1:
                print(", ", end="")
        print(" ]", end="")
        if i < policy.shape[0] - 1:
            print(",", end="")
        print()
    print("]")


def poisson_prob(n: int, lam: float) -> float:
    key = (n, lam)
    if key not in poisson_cache:
        poisson_cache[key] = poisson.pmf(n, lam)
    return poisson_cache[key]


def init_P_and_R(P, R, lambda_requests, lambda_dropoffs):
    """Load transition probabilities and expected rewards"""
    requests = 0
    while True:
        request_prob = poisson_prob(requests, lambda_requests)
        if request_prob < 0.000001:
            break

        for n in range(MAX_CARS + 1 + MAX_MOVE):
            R[n] += REWARDS_PER_MOVE * request_prob * min(requests, n)

        dropoffs = 0
        while True:
            drop_prob = poisson_prob(dropoffs, lambda_dropoffs)
            if drop_prob < 0.000001:
                break

            for n in range(MAX_CARS + 1 + MAX_MOVE):
                satisfied_requests = min(requests, n)
                new_n = max(0, min(MAX_CARS, n + dropoffs - satisfied_requests))
                P[n, new_n] += request_prob * drop_prob

            dropoffs += 1

        requests += 1


def init():
    global V, policy, P1, P2, R1, R2

    V = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
    policy = np.zeros((MAX_CARS + 1, MAX_CARS + 1), dtype=int)

    # transition probabilities for location 1 P(s1, new_s1)
    P1 = np.zeros((MAX_CARS + 1 + MAX_MOVE, MAX_CARS + 1))
    # transition probabilities for location 2 P(s2, new_s2)
    P2 = np.zeros((MAX_CARS + 1 + MAX_MOVE, MAX_CARS + 1))
    # expected rewards for location 1
    R1 = np.zeros(MAX_CARS + 1 + MAX_MOVE)
    # expected rewards for location 2
    R2 = np.zeros(MAX_CARS + 1 + MAX_MOVE)

    init_P_and_R(P1, R1, RENT1_MEAN, RETURN1_MEAN)
    init_P_and_R(P2, R2, RENT2_MEAN, RETURN2_MEAN)


def calc_v(
    s1: int, s2: int, action: int, value_table: Optional[np.ndarray] = None
) -> float:
    # V(s) = sigma_s',r P(s',r|s,a)[r + gammaV(s')]

    action = max(-s2, min(action, s1))  # 移動できる台数の物理的制約
    action = max(-MAX_MOVE, min(MAX_MOVE, action))  # ポリシーの制約（±5台まで）

    morning_s1 = s1 - action
    morning_s2 = s2 + action
    morning_s1 = max(0, min(MAX_CARS, morning_s1))
    morning_s2 = max(0, min(MAX_CARS, morning_s2))

    total = -MOVE_CAR_COST * abs(action)  # Cost of moving cars
    if action > 0:
        total += MOVE_CAR_COST * min(FREE_MOVE_CAR, action)  # Free move cars

    # Cost of additional parking
    if morning_s1 > PARKING_LIMIT:
        total -= ADDITIONAL_PARKING_COST
    if morning_s2 > PARKING_LIMIT:
        total -= ADDITIONAL_PARKING_COST

    table = V if value_table is None else value_table

    for new_s1 in range(MAX_CARS + 1):
        for new_s2 in range(MAX_CARS + 1):
            prob = P1[morning_s1, new_s1] * P2[morning_s2, new_s2]
            reward = R1[morning_s1] + R2[morning_s2]
            total += prob * (reward + GAMMA * table[new_s1, new_s2])

    return total


def policy_evaluation():
    delta = THETA + 1
    eval_iter = 0
    while delta >= THETA:
        delta = 0
        eval_iter += 1
        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                v = V[i, j]
                a = policy[i, j]
                # V(s) = sigma_s',r P(s',r|s,pi(s))[r + gammaV(s')]
                V[i, j] = calc_v(i, j, a)
                delta = max(delta, abs(v - V[i, j]))
        print(f"  Eval iter {eval_iter}: delta={delta:.8f}", end="\r")
    print(f"\n  Policy evaluation converged after {eval_iter} iterations")


def policy_improvement() -> bool:
    policy_stable = True
    changes = 0
    for i in range(policy.shape[0]):
        for j in range(policy.shape[1]):
            old_action = policy[i, j]
            action_values = [
                calc_v(i, j, action)
                for action in range(-min(j, MAX_MOVE), min(i, MAX_MOVE) + 1)
            ]
            best_action = np.argmax(action_values) - min(j, MAX_MOVE)
            policy[i, j] = best_action
            if old_action != best_action:
                policy_stable = False
                changes += 1

    print(f"  Policy changes: {changes}")

    return policy_stable


def policy_iteration(n_iterations: int = 1000):
    init()

    print("Initial value:")
    show_value()
    print("Initial policy:")
    show_policy()

    it = 0
    while True:
        print(f"\nIteration {it + 1}")

        policy_evaluation()

        if policy_improvement():
            print(f"\nPolicy converged after {it + 1} iterations!")
            break

    print("Final value:")
    show_value()
    print("Final policy:")
    show_policy()


def value_iteration(max_iterations: int = 1000):
    init()

    iteration = 0
    while iteration < max_iterations:
        delta = 0.0
        new_V = np.zeros_like(V)

        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                # V(s) = max_a sigma_s',r P(s',r|s,a)[r + gammaV(s')]
                possible_actions = [
                    action for action in range(-min(j, MAX_MOVE), min(i, MAX_MOVE) + 1)
                ]

                action_values = [calc_v(i, j, action, V) for action in possible_actions]

                best_value = max(action_values)
                new_V[i, j] = best_value
                delta = max(delta, abs(best_value - V[i, j]))

        V[:, :] = new_V
        iteration += 1
        print(f"Iteration {iteration}: delta={delta:.8f}", end="\r")

        if delta < THETA:
            break

    print(
        f"\nValue iteration terminated after {iteration} iterations with delta={delta:.8f}"
    )

    for i in range(policy.shape[0]):
        for j in range(policy.shape[1]):
            # pi(s) = argmax_a sigma_s',r P(s',r|s,a)[r + gammaV(s')]
            possible_actions = [
                action for action in range(-min(j, MAX_MOVE), min(i, MAX_MOVE) + 1)
            ]
            action_values = [calc_v(i, j, action, V) for action in possible_actions]
            best_action = possible_actions[int(np.argmax(action_values))]
            policy[i, j] = best_action

    print("Final value:")
    show_value()
    print("Final greedy policy:")
    show_policy()


if __name__ == "__main__":
    policy_iteration()
    # value_iteration()
