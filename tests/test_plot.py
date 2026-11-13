import matplotlib.pyplot as plt
import pandas as pd

from tennis_career import plot_career_matches


def test_plot_career_matches():
    matches = pd.DataFrame({
        "player_age": [20.0, 22.0],
        "age_difference": [-2.0, 3.0],
        "result": ["W", "L"],
    })

    ax = plot_career_matches(matches)
    try:
        win, loss = ax.collections
        assert win.get_offsets().tolist() == [[20.0, -2.0]]
        assert loss.get_offsets().tolist() == [[22.0, 3.0]]
        assert win.get_label() == "Win"
        assert loss.get_label() == "Loss"
        assert tuple(win.get_facecolors()[0]) != tuple(loss.get_facecolors()[0])
        assert ax.get_xlabel() == "Player age (years)"
        assert ax.get_ylabel() == "Player age minus opponent age (years)"
    finally:
        plt.close(ax.figure)
