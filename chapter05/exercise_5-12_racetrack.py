# 図5.5に示すような曲がり角でレーシングカーを運転することを考える。
# できる限り速く、しかしトラックから飛び出すほどではない速さで走りたい。
# この単純化したレーストラックでは、車はグリッドの位置の離散的な集合、つまり図中のセルの一つにある、
# 速度も離散的で、時間ステップごとに水平と垂直方向に動いたグリッドセルの数で表す。
# 行動は、速度成分の増分となる。合計で9通り（3✕3）の行動について、それぞれ各ステップで＋1，-1,0に変わる可能性がある。
# 速度の両方の成分は非負で5以下に制限されていて、スタートライン以外では両方が0になることはない。
# 各エピソードはランダムに選ばれた開始状態から速度成分が両方0で始まり、車がゴールラインを超えたときに終わる。
# 報酬は車がゴールラインを横切るまでの各ステップで-1とする。
# もし車がトラックの境界線にぶつかった場合、スタートラインのランダムな場所に戻され、速度の各成分は0に減らされ、エピソードは継続する、
# 各時間ステップで車の場所を更新する前に、車の見積もった経路がトラックの境界線を横切らないかを確認する。
# もしゴールラインを横切ったら、エピソードは終了する。もしそれ以外の境界線を横切ったら、トラックの境界にぶつかったと考えられ、スタートラインに送り返される、
# タスクをより難しくするために、各時間ステップにおいて確率0.1で、意図していた地分に関係なく、速度の増分が両方とも0になるとする。
# 各開始状態からの最適方策を計算するために、モンテカルロ制御法を適用せよ。
# 最適方策に従ったいくつかの軌跡を示せ。ただし、これらの軌跡ではノイズはオフにせよ。

import random
from types import ModuleType
from typing import List, Optional, Tuple

import numpy as np

track_img0 = """
#GGGGGGGGG#
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#         #
#SSSSSSSSS#
"""

track_img1 = """
    ###############
   #              G
   #              G
  #               G
 #                G
#                 G
#                 G
#           #######
#          #
#         #
#         #
#         #
#         #
#         #
 #        #
 #        #
 #        #
 #        #
 #        #
 #        #
 #        #
 #        #
  #       #
  #       #
  #       #
  #       #
  #       #
  #       #
  #       #
   #      #
   #      #
   #SSSSSS#
"""


track_img2 = """
                 #################
              ###                G
             #                   G
            #                    G
           #                     G
           #                     G
           #                     G
           #                     G
            #                    G
             #                  ##
              #              ###
              #             #
              #           ##
              #          #
              #         #
             #          #
            #           #
           #            #
          #             #
         #              #
        #               #
       #                #
      #                 #
     #                  #
    #                   #
   #                    #
  #                     #
 #                      #
#                       #
#                       #
#SSSSSSSSSSSSSSSSSSSSSSS#
"""


Position = Tuple[int, int]  # (x, y)
Velocity = Tuple[int, int]  # (vx, vy)
State = Tuple[Position, Velocity]  # ((x, y), (vx, vy))
Action = Tuple[int, int]  # (delta_vx, delta_vy)

EpisodeStep = Tuple[State, int, float]  # (state, action, reward)
Episode = Tuple[int, List[EpisodeStep]]  # (reward, trajectory)

Q: Optional[np.ndarray] = None  # Action-value function (State, Action)
C: Optional[np.ndarray] = None  # Cumulative weights (State, Action)
policy: Optional[np.ndarray] = None  # Target policy (State)

ACTIONS = [(1, 1), (1, 0), (1, -1), (0, 1), (0, 0), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
REWARD_PER_STEP = -1  # Reward per time step
MAX_VELOCITY = 5  # Maximum velocity
NOISE_PROB = 0.1  # Probability of action noise


def get_track(track_img):
    x_max = max(map(len, track_img.split("\n")))
    track = []
    for line in track_img.split("\n"):
        if line == "":
            continue
        line += " " * x_max
        track.append(list(line)[:x_max])

    return np.array(track)


def _require_tables() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if Q is None or C is None or policy is None:
        raise RuntimeError("Tables have not been initialised. Call setup() first.")
    return Q, C, policy


def setup(track_img: str, seed: Optional[int] = None) -> None:
    """Initialise the global tables and reset the episode state."""
    global Q, C, policy

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    track = get_track(track_img)
    Q = np.zeros(
        (
            track.shape[1],  # map (row, column) to (x, y)
            track.shape[0],
            MAX_VELOCITY + 1,
            MAX_VELOCITY + 1,
            len(ACTIONS),
        ),
        dtype=float,
    )
    Q.fill(REWARD_PER_STEP * Q.shape[0] * Q.shape[1])  # pessimistic initialisation
    C = np.zeros(
        (
            track.shape[1],
            track.shape[0],
            MAX_VELOCITY + 1,
            MAX_VELOCITY + 1,
            len(ACTIONS),
        ),
        dtype=float,
    )
    policy = np.zeros(
        (track.shape[1], track.shape[0], MAX_VELOCITY + 1, MAX_VELOCITY + 1), dtype=int
    )
    policy.fill(4)  # initially select action (0,0)


def check_line_collision(
    start: Position, end: Position, track: np.ndarray
) -> Tuple[bool, bool]:
    """Check if the line from start to end collides with track boundaries."""
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if not (0 <= x0 < track.shape[1] and 0 <= y0 < track.shape[0]):
            return True, False
        tile = track[y0, x0]
        if tile == "#":
            return True, False
        if tile == "G":
            return False, True
        if x0 == x1 and y0 == y1:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x0 += sx
        if err2 < dx:
            err += dx
            y0 += sy

    return False, False


def move(position: Position, velocity: Velocity, action: Action) -> State:
    """Compute the new position and velocity after taking the action."""
    x, y = position
    vx, vy = velocity
    dvx, dvy = action

    # Velocity must be within [0, MAX_VELOCITY]
    new_vx = min(MAX_VELOCITY, max(0, vx + dvx))
    new_vy = min(MAX_VELOCITY, max(0, vy + dvy))
    # Velocity should be > 0 except at start line
    if new_vx == 0 and new_vy == 0:
        new_vx, new_vy = vx, vy

    new_x = x + new_vx
    new_y = y - new_vy  # y axis is inverted in the grid

    return (new_x, new_y), (new_vx, new_vy)


def outcome(trajectory: List[EpisodeStep]) -> int:
    """Compute the outcome reward for the current episode state."""
    return REWARD_PER_STEP * len(trajectory)  # -1 per step


def generate_episode(
    bpolicy: np.ndarray,
    track_img: str,
    epsilon: float,
    noise: float,
    rng: Optional[random.Random | ModuleType] = None,
) -> Episode:
    """Generate one behaviour-policy episode from the fixed start state."""
    rng = rng or random
    _require_tables()

    trajectory: List[EpisodeStep] = []

    track = get_track(track_img)
    start_positions = np.argwhere(track == "S")
    pos_idx = rng.randint(0, len(start_positions) - 1)
    position: Position = (
        start_positions[pos_idx][1],
        start_positions[pos_idx][0],
    )  # (x, y)
    velocity: Velocity = (0, 0)  # (vx, vy)

    max_iter = 10000
    for _ in range(max_iter):
        state: State = (position, velocity)
        x, y = position
        vx, vy = velocity

        if rng.random() < epsilon:
            action_idx = rng.randint(0, len(ACTIONS) - 1)
        else:
            action_idx = bpolicy[x, y, vx, vy]

        action = ACTIONS[action_idx]
        trajectory.append((state, action_idx, REWARD_PER_STEP))

        # Apply noise
        if rng.random() < noise:
            action = (0, 0)

        # Move the car
        (new_x, new_y), (new_vx, new_vy) = move(position, velocity, action)

        # Check for boundary conditions
        collision, reached_goal = check_line_collision(position, (new_x, new_y), track)
        if collision:
            # Reset to start position and zero velocity
            pos_idx = rng.randint(0, len(start_positions) - 1)
            position = (start_positions[pos_idx][1], start_positions[pos_idx][0])
            velocity = (0, 0)
        else:
            position = (new_x, new_y)
            velocity = (new_vx, new_vy)

        # Check for goal condition
        if reached_goal:
            break

    total_return = outcome(trajectory)
    return total_return, trajectory


def off_policy_estimate(
    track_img: str,
    num_episodes: int,
    rng: Optional[random.Random | ModuleType] = None,
):
    """Compute running off-policy estimates using the supplied episodes."""
    Q, C, policy = _require_tables()

    rng = rng or random

    for idx in range(num_episodes):
        # uniform random
        behaviour_policy = policy.copy()
        behaviour_policy_eps = 0.1
        outcome, trajectory = generate_episode(
            behaviour_policy,
            track_img,
            epsilon=behaviour_policy_eps,
            noise=NOISE_PROB,
            rng=rng,
        )

        g = 0.0  # Return
        w = 1.0  # Importance sampling weight
        for state, action, reward in reversed(trajectory):
            (pos, vel) = state
            (x, y) = pos
            (vx, vy) = vel
            a = action

            g = g + reward
            C[x, y, vx, vy, a] += w
            Q[x, y, vx, vy, a] += (w) * (g - Q[x, y, vx, vy, a]) / C[x, y, vx, vy, a]

            # Update the target policy to be greedy w.r.t. Q
            best_action = np.argmax(Q[x, y, vx, vy, :])
            policy[x, y, vx, vy] = best_action

            if action != best_action:
                break

            # Importance sampling weight update
            # Behavior policy is epsilon-soft
            w *= 1.0 / (
                (1.0 - behaviour_policy_eps) + behaviour_policy_eps / len(ACTIONS)
            )

        if idx % 1000 == 0 and idx > 0:
            print(
                f"Episode {idx + 1}/{num_episodes}, outcome: {outcome}",
            )
            draw_policy(track_img, episode=(outcome, trajectory))


def draw_policy(track_img: str, episode: Optional[Episode] = None) -> None:
    if episode is None:
        Q, _, policy = _require_tables()
        total_return, trajectory = generate_episode(
            policy, track_img, epsilon=0.0, noise=0.0
        )  # Generate episode with greedy policy
    else:
        total_return, trajectory = episode

    track = get_track(track_img).copy()
    policy_grid = track.copy()
    for (pos, vel), action_idx, reward in trajectory:
        x, y = pos
        policy_grid[y, x] = "+"
    for row in policy_grid:
        print("".join(row))
    print(f"Total steps to reach goal: {len(trajectory)}, Total reward: {total_return}")


def main() -> None:
    rng = random.Random(2025)
    track_img = track_img1

    setup(track_img, seed=2025)
    off_policy_estimate(track_img, 200000, rng=rng)
    draw_policy(track_img)


if __name__ == "__main__":
    main()
