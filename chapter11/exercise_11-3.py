"""
Exercise 11.3

Apply 1‑step semi‑gradient Q‑learning to Baird's counterexample and
save the weight trajectories. The setup mirrors chapter11/example.py so
that the saved plot can be compared easily.
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm import tqdm

# Environment is identical to example.py (Baird's counterexample)
STATES = np.arange(0, 7)  # 0-5: upper states, 6: lower state
LOWER_STATE = 6
DISCOUNT = 0.99

# Feature construction for states (length 8) from example.py
STATE_FEATURE_SIZE = 8
STATE_FEATURES = np.zeros((len(STATES), STATE_FEATURE_SIZE))
for i in range(LOWER_STATE):
    STATE_FEATURES[i, i] = 2
    STATE_FEATURES[i, 7] = 1
STATE_FEATURES[LOWER_STATE, 6] = 1
STATE_FEATURES[LOWER_STATE, 7] = 2

# Actions
DASHED = 0
SOLID = 1
ACTIONS = [DASHED, SOLID]

REWARD = 0


def step(state: int, action: int) -> int:
    """Transition function for Baird's counterexample."""

    if action == SOLID:
        return LOWER_STATE
    return np.random.choice(STATES[:LOWER_STATE])


# Behavior policy: solid with small probability (off-policy setting)
BEHAVIOR_SOLID_PROBABILITY = 1.0 / 7


def behavior_policy(state: int) -> int:
    if np.random.binomial(1, BEHAVIOR_SOLID_PROBABILITY) == 1:
        return SOLID
    return DASHED


# Target for Q-learning is greedy w.r.t current parameters, so no explicit
# target policy function is needed.


def build_action_features() -> np.ndarray:
    """Create action-specific feature vectors by block-diagonal stacking.

    q(s, a) = theta^T phi(s, a), where phi has length 2 * STATE_FEATURE_SIZE.
    The first block corresponds to DASHED, the second to SOLID.
    """

    feature_size = STATE_FEATURE_SIZE * len(ACTIONS)
    features = np.zeros((len(STATES), len(ACTIONS), feature_size))
    for s in STATES:
        dashed_slice = slice(0, STATE_FEATURE_SIZE)
        solid_slice = slice(STATE_FEATURE_SIZE, feature_size)
        features[s, DASHED, dashed_slice] = STATE_FEATURES[s]
        features[s, SOLID, solid_slice] = STATE_FEATURES[s]
    return features


ACTION_FEATURES = build_action_features()
FEATURE_SIZE = ACTION_FEATURES.shape[-1]


def semi_gradient_q_learning(state: int, theta: np.ndarray, alpha: float) -> int:
    """Perform one 1-step semi-gradient Q-learning update.

    Returns the next state reached under the behavior policy.
    """

    action = behavior_policy(state)
    next_state = step(state, action)

    phi_sa = ACTION_FEATURES[state, action]
    q_sa = np.dot(theta, phi_sa)

    q_next = np.dot(ACTION_FEATURES[next_state], theta)
    target = REWARD + DISCOUNT * np.max(q_next)

    delta = target - q_sa
    theta += alpha * delta * phi_sa

    return next_state


def run_experiment(steps: int = 2000, alpha: float = 0.01) -> np.ndarray:
    """Run Q-learning and record theta over time."""

    theta = np.ones(FEATURE_SIZE)
    # As in example.py, make one component large to accentuate divergence.
    theta[STATE_FEATURE_SIZE + 6] = 10  # solid-action feature for lower state

    thetas = np.zeros((FEATURE_SIZE, steps))
    state = np.random.choice(STATES)
    for t in tqdm(range(steps), desc="Q-learning steps"):
        state = semi_gradient_q_learning(state, theta, alpha)
        thetas[:, t] = theta

    return thetas


def plot_thetas(
    thetas: np.ndarray, save_path: str = "./figure_exercise_11-3.png"
) -> None:
    plt.figure(figsize=(10, 8))
    for i in range(thetas.shape[0]):
        plt.plot(thetas[i], label=f"theta{i + 1}")
    plt.xlabel("Steps")
    plt.ylabel("Theta value")
    plt.title("1-step semi-gradient Q-learning (Baird's counterexample)")
    plt.legend(ncol=2, fontsize=8)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    np.random.seed(1234)
    thetas = run_experiment()
    plot_thetas(thetas)


if __name__ == "__main__":
    main()
