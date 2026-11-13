## Installation

Install the package from GitHub using an account with access to the repository.

```bash
python -m pip install "git+https://github.com/UCB-stat159-f26/hw03-3-liaorita2k03-hub.git"
```

## Example

```python
import matplotlib.pyplot as plt

from tennis_career import get_career_matches, plot_career_matches

serena = get_career_matches("Serena Williams")
plot_career_matches(serena)
plt.show()
```

The x-axis shows the player's age at the match. The y-axis shows the
player's age minus the opponent's age. A positive value means the player
was older, a negative value means the player was younger, and zero means
they had the same age. Point colors indicate wins and losses.

## Running the tests

From the repository folder, run:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

The tests use local JavaScript fixtures and run without contacting
Tennis Abstract.

## Personal reflection

In HW2, I only worked with Serena Williams’s data. When I adapted my code for HW3, I learned that Tennis Abstract gives the opponent’s birth date in Serena’s file and the opponent’s age in Nadal’s file. That explained why the same calculation wouldn’t work for both players. Using small JS fixtures helped me check how my code handled each format without having to download the data every time I ran the tests.