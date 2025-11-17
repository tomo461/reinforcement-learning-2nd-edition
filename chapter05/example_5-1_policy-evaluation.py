"""Monte Carlo policy evaluation for the simple blackjack task (Example 5.1).

This module is a direct Python rewrite of ``example_5-1_policy-evaluation.lisp``
from Sutton & Barto (2nd edition).  It keeps the same global-state structure as
the original listing: arrays of values, visit counts, and a fixed policy that
hits below 20 and sticks otherwise.  The code can be imported for experiments
or run directly to reproduce the basic experiment loop from the book comments.
"""

from __future__ import annotations

import random
from types import ModuleType
from typing import Dict, List, Optional, Tuple

import numpy as np

HIT = 1  # Draw another card
STICK = 0  # Stop drawing cards

State = Tuple[int, int, bool]  # (dealer showing: dc, player count: pc, usable ace: ace)

V: Optional[np.ndarray] = None  # State-value function
N: Optional[np.ndarray] = None  # State visit counts
policy: Optional[np.ndarray] = None  # Fixed policy to be evaluated

dc: int = 0  # Dealer's showing card [1-10]
pc: int = 0  # Player's current count [12-21]
ace: bool = False  # Whether the player holds a usable ace [True/False]
current_episode: List[State] = []  # States visited in the current episode


def _require_tables() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if V is None or N is None or policy is None:
        raise RuntimeError("Call setup() before using the blackjack module.")
    return V, N, policy


def card(rng: Optional[random.Random | ModuleType] = None) -> int:
    """Draw a card where face cards count as 10 (1-13 compressed to 1-10)."""
    rng = rng or random
    return min(10, rng.randint(1, 13))


def setup(seed: Optional[int] = None) -> None:
    """Initialise the global tables and reset the episode state."""
    global V, N, policy, dc, pc, ace, current_episode

    if seed is not None:
        random.seed(seed)

    # (dealer showing: 1-10, player count: 12-21, usable ace: 0/1)
    V = np.zeros((11, 22, 2), dtype=float)
    N = np.zeros((11, 22, 2), dtype=int)
    policy = np.ones((11, 22, 2), dtype=int)

    policy[:, 20:, :] = STICK  # stick on player counts of 20 or 21

    dc = 0
    pc = 0
    ace = False
    current_episode = []


def episode(
    rng: Optional[random.Random | ModuleType] = None,
) -> Tuple[int, List[State]]:
    """Generate one episode following the fixed policy and update V."""
    global current_episode, dc, pc, ace

    rng = rng or random
    _, _, pol = _require_tables()

    current_episode = []

    dc_hidden = card(rng)  # Dealer's hidden card
    dc = card(rng)  # Dealer's showing card

    pcard1 = card(rng)  # Player's first card
    pcard2 = card(rng)  # Player's second card

    ace = pcard1 == 1 or pcard2 == 1  # Usable ace if either card is an ace
    pc = pcard1 + pcard2 + (10 if ace else 0)  # usable ace adds 10

    if pc != 21:  # natural blackjack: no decisions required
        while True:
            current_episode.append((dc, pc, ace))

            action = int(pol[dc, pc, 1 if ace else 0])
            if action == STICK:
                break

            draw_card(rng)
            if bust():
                break

    outcome_value = outcome(dc, dc_hidden, rng)
    trace = list(current_episode)
    learn(trace, outcome_value)

    return outcome_value, trace


def learn(episode_trace: List[State], outcome_value: int) -> None:
    """Incrementally update state-value estimates using one episode return."""
    values, counts, _ = _require_tables()

    for dc_val, pc_val, ace_bool in episode_trace:
        if pc_val <= 11:  # skip because never bust with <=11
            continue

        ace_idx = 1 if ace_bool else 0
        counts[dc_val, pc_val, ace_idx] += 1

        alpha = 1.0 / counts[dc_val, pc_val, ace_idx]
        values[dc_val, pc_val, ace_idx] += alpha * (
            outcome_value - values[dc_val, pc_val, ace_idx]
        )


def outcome(
    dc_showing: int, dc_hidden: int, rng: Optional[random.Random | ModuleType] = None
) -> int:
    """Play out the dealer hand and return the episode reward."""
    global pc, current_episode

    rng = rng or random

    dace = dc_showing == 1 or dc_hidden == 1
    dcount = dc_showing + dc_hidden + (10 if dace else 0)

    dnatural = dcount == 21
    pnatural = len(current_episode) == 0  # natural if no player actions taken

    if pnatural and dnatural:  # Both player and dealer have natural blackjack
        return 0
    if pnatural:  # Player has a natural blackjack
        return 1
    if dnatural:  # Dealer has a natural blackjack
        return -1
    if bust():  # Player busts
        return -1

    while dcount < 17:  # Dealer hits until reaching 17 or higher
        card_value = card(rng)
        dcount += card_value

        if not dace and card_value == 1:
            dcount += 10
            dace = True

        if dace and dcount > 21:
            dcount -= 10
            dace = False

    if dcount > 21:  # Dealer busts
        return 1
    if dcount > pc:  # Dealer has higher count than player
        return -1
    if dcount == pc:  # Dealer and player have the same count
        return 0
    return 1  # Player has higher count than dealer


def draw_card(rng: Optional[random.Random | ModuleType] = None) -> None:
    """Update the player hand variables after drawing one card."""
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
    """Return ``True`` if the player count exceeds 21."""
    return pc > 21


def gr(
    source: np.ndarray, ace_flag: bool, out: Optional[np.ndarray] = None
) -> np.ndarray:
    """Populate a 10x10 grid with slices from ``source`` for plotting."""
    if out is None:
        out = np.zeros((10, 10), dtype=float)

    ace_idx = 1 if ace_flag else 0

    for i in range(10):
        for j in range(10):
            out[i, j] = source[i + 1, j + 12, ace_idx]

    return out


def experiment(
    num_snapshots: int = 500,
    episodes_per_snapshot: int = 1000,
    seed: Optional[int] = None,
    rng: Optional[random.Random | ModuleType] = None,
) -> List[Dict[str, np.ndarray | int]]:
    """Replicate the original experiment loop, yielding value-surface grids."""
    if V is None:
        setup(seed=seed)
    elif seed is not None:
        random.seed(seed)

    values, _, _ = _require_tables()
    snapshots: List[Dict[str, np.ndarray | int]] = []

    for count in range(num_snapshots + 1):
        print(count)

        snapshot: Dict[str, np.ndarray | int] = {
            "iteration": count,
            "no_usable_ace": gr(values, False).copy(),
            "usable_ace": gr(values, True).copy(),
        }
        snapshots.append(snapshot)

        if count == num_snapshots:
            break

        for _ in range(episodes_per_snapshot):
            episode(rng=rng)

    return snapshots


if __name__ == "__main__":
    seed = 2025
    num_snapshots = 500
    episodes_per_snapshot = 1000

    rng = random.Random(seed)
    setup(seed=seed)
    snapshots = experiment(
        num_snapshots=num_snapshots,
        episodes_per_snapshot=episodes_per_snapshot,
        rng=rng,
    )

    final_snapshot = snapshots[-1]
    total_episodes = num_snapshots * episodes_per_snapshot

    print(f"Completed {total_episodes} episodes under the fixed policy.")
    print("Final value surface without a usable ace:")
    print(final_snapshot["no_usable_ace"])
    print("\nFinal value surface with a usable ace:")
    print(final_snapshot["usable_ace"])
