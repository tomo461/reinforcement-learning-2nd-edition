"""Monte Carlo Exploring Starts solution of the simple blackjack task.

This module is a direct Python transcription of the original Lisp code that
appears in the comments of the book source.  It implements Example 5.3 from
Sutton & Barto (second edition) using incremental Monte Carlo estimation with
exploring starts to learn both the optimal action-value function `Q` and the
corresponding greedy policy.
"""

from __future__ import annotations

import random
from types import ModuleType
from typing import Dict, List, Optional, Tuple

import numpy as np

# Actions
HIT = 1
STICK = 0

# (dealer showing: dc, player count: pc, usable ace: ace, action)
EpisodeStep = Tuple[int, int, bool, int]

Q: Optional[np.ndarray] = None  # Action-value function (dc, pc, ace, action)
N: Optional[np.ndarray] = None  # State-action visit counts (dc, pc, ace, action)
policy: Optional[np.ndarray] = None  # Current greedy policy (dc, pc, ace)

dc: int = 0
pc: int = 0
ace: bool = False
current_episode: List[EpisodeStep] = []


def _require_tables() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if Q is None or N is None or policy is None:
        raise RuntimeError("Call setup() before generating episodes.")
    return Q, N, policy


def card(rng: Optional[random.Random | ModuleType] = None) -> int:
    """Draw a card where face cards count as 10."""
    rng = rng or random
    return min(10, rng.randint(1, 13))


def setup(seed: Optional[int] = None) -> None:
    """Initialise Q, N, and the target policy."""
    global Q, N, policy, dc, pc, ace, current_episode

    if seed is not None:
        random.seed(seed)

    Q = np.zeros((11, 22, 2, 2), dtype=float)
    N = np.zeros((11, 22, 2, 2), dtype=int)
    policy = np.ones((11, 22, 2), dtype=int)

    policy[:, 20:, :] = STICK  # stick on 20 or 21

    dc = 0
    pc = 0
    ace = False
    current_episode = []


def exploring_episode(
    rng: Optional[random.Random | ModuleType] = None,
) -> Tuple[int, List[EpisodeStep]]:
    """Generate one exploring-start episode and update Q."""
    global current_episode, dc, pc, ace

    rng = rng or random
    _, _, pol = _require_tables()

    current_episode = []

    dc_hidden = card(rng)
    dc = rng.randint(1, 10)
    ace = bool(rng.randint(0, 1))
    pc = 12 + rng.randint(0, 9)
    action = rng.randint(0, 1)

    while True:
        current_episode.append((dc, pc, ace, action))
        if action == STICK:
            break
        draw_card(rng)
        if bust():
            break
        action = int(pol[dc, pc, 1 if ace else 0])

    outcome_value = outcome(dc, dc_hidden, rng)
    trace = list(current_episode)
    learn(trace, outcome_value)
    return outcome_value, trace


def episode(
    rng: Optional[random.Random | ModuleType] = None,
) -> Tuple[int, List[EpisodeStep]]:
    """Generate one episode following the current greedy policy."""
    global current_episode, dc, pc, ace

    rng = rng or random
    _, _, pol = _require_tables()

    current_episode = []

    dc_hidden = card(rng)
    dc = card(rng)

    pcard1 = card(rng)
    pcard2 = card(rng)

    ace = pcard1 == 1 or pcard2 == 1
    pc = pcard1 + pcard2 + (10 if ace else 0)

    if pc != 21:
        while True:
            action = int(pol[dc, pc, 1 if ace else 0])
            current_episode.append((dc, pc, ace, action))
            if action == STICK:
                break
            draw_card(rng)
            if bust():
                break

    outcome_value = outcome(dc, dc_hidden, rng)
    trace = list(current_episode)
    learn(trace, outcome_value)
    return outcome_value, trace


def learn(episode_trace: List[EpisodeStep], outcome_value: int) -> None:
    """Incrementally update Q and the greedy policy using one episode."""
    q, n, pol = _require_tables()

    for dc_val, pc_val, ace_bool, action in episode_trace:
        if pc_val <= 11:
            continue

        ace_idx = 1 if ace_bool else 0

        n[dc_val, pc_val, ace_idx, action] += 1
        alpha = 1.0 / n[dc_val, pc_val, ace_idx, action]
        q[dc_val, pc_val, ace_idx, action] += alpha * (
            outcome_value - q[dc_val, pc_val, ace_idx, action]
        )

        policy_action = int(pol[dc_val, pc_val, ace_idx])
        other_action = 1 - policy_action

        if (
            q[dc_val, pc_val, ace_idx, other_action]
            > q[dc_val, pc_val, ace_idx, policy_action]
        ):
            pol[dc_val, pc_val, ace_idx] = other_action


def outcome(
    dc_showing: int, dc_hidden: int, rng: Optional[random.Random | ModuleType] = None
) -> int:
    """Play out the dealer hand and return the game result."""
    global pc, current_episode

    rng = rng or random

    dace = dc_showing == 1 or dc_hidden == 1
    dcount = dc_showing + dc_hidden + (10 if dace else 0)
    dnatural = dcount == 21
    pnatural = len(current_episode) == 0

    if pnatural and dnatural:
        return 0
    if pnatural:
        return 1
    if dnatural:
        return -1
    if bust():
        return -1

    while dcount < 17:
        card_value = card(rng)
        dcount += card_value
        if not dace and card_value == 1:
            dcount += 10
            dace = True
        if dace and dcount > 21:
            dcount -= 10
            dace = False

    if dcount > 21:
        return 1
    if dcount > pc:
        return -1
    if dcount == pc:
        return 0
    return 1


def draw_card(rng: Optional[random.Random | ModuleType] = None) -> None:
    """Update the player count/state after drawing one card."""
    global pc, ace

    rng = rng or random
    card_value = card(rng)
    pc += card_value

    if not ace and card_value == 1:
        pc += 10
        ace = True

    if ace and pc > 21:
        pc -= 10
        ace = False


def bust() -> bool:
    """Return True if the current player count exceeds 21."""
    return pc > 21


def gr(
    source: np.ndarray, ace_flag: bool, action: int, out: Optional[np.ndarray] = None
) -> np.ndarray:
    """Populate a 10x10 grid with either Q values or counts for plotting."""
    if out is None:
        out = np.zeros((10, 10), dtype=float)

    ace_idx = 1 if ace_flag else 0

    for i in range(10):
        for j in range(10):
            out[i, j] = source[i + 1, j + 12, ace_idx, action]

    return out


def grp(ace_flag: bool, out: Optional[np.ndarray] = None) -> np.ndarray:
    """Populate a 10x10 grid with the greedy policy values."""
    _, _, pol = _require_tables()

    if out is None:
        out = np.zeros((10, 10), dtype=int)

    ace_idx = 1 if ace_flag else 0

    for i in range(10):
        for j in range(10):
            out[i, j] = pol[i + 1, j + 12, ace_idx]

    return out


def experiment(
    num_snapshots: int = 500,
    episodes_per_snapshot: int = 1000,
    use_exploring_starts: bool = True,
    rng: Optional[random.Random | ModuleType] = None,
) -> List[Dict[str, np.ndarray | int]]:
    """Replicate the original experiment loop, returning grids for inspection."""
    if Q is None:
        setup()

    q, _, _ = _require_tables()
    generator = exploring_episode if use_exploring_starts else episode
    snapshots: List[Dict[str, np.ndarray | int]] = []

    for count in range(num_snapshots + 1):
        print(count)

        snapshot: Dict[str, np.ndarray | int] = {
            "iteration": count,
            "no_usable_ace_stick": gr(q, False, STICK).copy(),
            "no_usable_ace_hit": gr(q, False, HIT).copy(),
            "usable_ace_stick": gr(q, True, STICK).copy(),
            "usable_ace_hit": gr(q, True, HIT).copy(),
            "policy_no_ace": grp(False).copy(),
            "policy_with_ace": grp(True).copy(),
        }

        snapshots.append(snapshot)

        if count == num_snapshots:
            break

        for _ in range(episodes_per_snapshot):
            generator(rng=rng)

    return snapshots


if __name__ == "__main__":
    setup(seed=2025)
    snapshots = experiment(use_exploring_starts=True)

    final_snapshot = snapshots[-1]
    print("Final policy with usable ace:")
    print(final_snapshot["policy_with_ace"])
    print("Final policy without usable ace:")
    print(final_snapshot["policy_no_ace"])
