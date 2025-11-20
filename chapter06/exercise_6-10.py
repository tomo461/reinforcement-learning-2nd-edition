# Exercise 6.10: Stochastic Wind (programming) Re-solve the windy gridworld task with
# King’s moves, assuming that the e↵ect of the wind, if there is any, is stochastic, sometimes
# varying by 1 from the mean values given for each column. That is, a third of the time
# you move exactly according to these values, as in the previous exercise, but also a third
# of the time you move one cell above that, and another third of the time you move one
# cell below that. For example, if you are one cell to the right of the goal and you move
# left, then one-third of the time you move one cell above the goal, one-third of the time
# you move two cells above the goal, and one-third of the time you move to the goal.


import pprint
import random
from typing import List, Optional, Tuple

import numpy as np

Position = Tuple[int, int]  # (x, y)
State = Position  # (x, y)
Action = Tuple[int, int]  # (delta_x, delta_y)
Reward = int

EpisodeStep = Tuple[State, int, Reward]  # (state, action index, reward)
Episode = Tuple[Reward, List[EpisodeStep]]  # (reward, trajectory)

Q: Optional[np.ndarray] = None  # Action-value function (State, Action)

ACTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (0, 0),
    #
]
ACTION_CHARS = ["↑", "→", "↓", "←", "↗", "↘", "↙", "↖", "·"]
REWARD_PER_STEP = -1  # Reward per time step
alpha = 0.5  # Step-size parameter
epsilon = 0.1  # epsilon for epsilon-greedy
gamma = 1.0  # Discount factor

GRID_WIDTH = 10
GRID_HEIGHT = 7
START_POSITION = (0, 3)
GOAL_POSITION = (7, 3)
WIND_STRENGTH = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]  # Wind strength per column
WIND_STRENGTH_VARIATION = [-1, 0, 1]  # Wind variation


def get_grid() -> np.ndarray:
    grid = [[" " for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    grid[START_POSITION[1]][START_POSITION[0]] = "S"
    grid[GOAL_POSITION[1]][GOAL_POSITION[0]] = "G"

    return np.array(grid)


def _require_tables() -> np.ndarray:
    if Q is None:
        raise RuntimeError("Tables have not been initialised. Call setup() first.")
    return Q


def setup(seed: Optional[int] = None) -> None:
    """Initialise the global tables and reset the episode state."""
    global Q, policy

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    Q = np.zeros(
        (
            GRID_WIDTH,  # map (row, column) to (x, y)
            GRID_HEIGHT,
            len(ACTIONS),
        ),
        dtype=float,
    )


def move(position: Position, action: Action) -> Tuple[State, Reward, bool]:
    """Compute the new position after taking the action."""
    finished = False
    x, y = position
    dx, dy = action
    dy += WIND_STRENGTH[x] + random.choice(WIND_STRENGTH_VARIATION)

    new_x = x + dx
    new_y = y - dy  # y axis is inverted in the grid

    new_x = max(0, min(GRID_WIDTH - 1, new_x))
    new_y = max(0, min(GRID_HEIGHT - 1, new_y))

    # check for goal: 途中で横切った場合もgoal
    def _bresenham(x0, y0, x1, y1):
        pts = []
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            pts.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return pts

    if GOAL_POSITION in _bresenham(x, y, new_x, new_y):
        new_x, new_y = GOAL_POSITION

    reward = REWARD_PER_STEP

    finished = (new_x, new_y) == GOAL_POSITION
    if finished:
        reward = 0

    return (new_x, new_y), reward, finished


def pi(state: State, epsilon: float, rng: random.Random) -> int:
    Q = _require_tables()

    x, y = state
    if rng.random() < epsilon:
        return rng.randint(0, len(ACTIONS) - 1)
    else:
        return int(np.argmax(Q[x, y]))


def sarsa(
    num_episodes: int,
    rng: random.Random,
):
    """Compute running off-policy estimates using the supplied episodes."""
    Q = _require_tables()

    episodes: List[Episode] = []

    step = 0
    for idx in range(num_episodes):
        state = START_POSITION
        action_idx = pi(state, epsilon, rng)
        trajectory: List[EpisodeStep] = []
        while True:
            new_state, reward, finished = move(state, ACTIONS[action_idx])

            trajectory.append((state, action_idx, reward))

            new_action_idx = pi(new_state, epsilon, rng)
            Q[state[0], state[1], action_idx] += alpha * (
                reward
                + gamma * Q[new_state[0], new_state[1], new_action_idx]
                - Q[state[0], state[1], action_idx]
            )
            state = new_state
            action_idx = new_action_idx

            if finished:
                print(
                    f"Episode {idx + 1} Steps: {len(trajectory) + 1} Total steps: {step + 1}",
                    end="\r",
                )
                break

            step += 1

        episodes.append((reward, trajectory))
        # draw_trajectory(trajectory)
    print()

    return episodes


def draw_trajectory(trajectory: List[EpisodeStep]) -> None:
    grid = get_grid()
    for step in trajectory:
        state, action_idx, _ = step
        x, y = state
        grid[y, x] = ACTION_CHARS[action_idx]
    # grid[START_POSITION[1], START_POSITION[0]] = "S"
    grid[GOAL_POSITION[1], GOAL_POSITION[0]] = "G"
    pprint.pprint(grid.tolist())


def main() -> None:
    rng = random.Random(2025)

    setup(seed=2025)
    episodes = sarsa(1000, rng=rng)
    draw_trajectory(episodes[-1][1])


if __name__ == "__main__":
    main()
