import matplotlib.pyplot as plt


_OUTCOMES = (
    ("W", "Win", "#2166ac"),
    ("L", "Loss", "#b2182b"),
)


def plot_career_matches(matches):
    """Plot career matches by player age and return the Matplotlib Axes."""
    _, ax = plt.subplots()

    for result, label, color in _OUTCOMES:
        outcome = matches.loc[matches["result"] == result]
        ax.scatter(
            outcome["player_age"],
            outcome["age_difference"],
            color=color,
            label=label,
            alpha=0.75,
        )

    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Player age minus opponent age (years)")
    ax.axhline(0, color="0.65", linewidth=1, zorder=0)
    ax.legend()
    return ax
