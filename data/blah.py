import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.metrics import r2_score

# Data from https://www.boydsbets.com/college-basketball-spread-to-moneyline-conversion/
# Is this accurate? Is it old? Who knows?
df = pd.read_csv("data/spread_to_win.tsv", sep="\t")

df["fave_win_prob"] = df["fave_win_percent"].str.rstrip("%").astype("float") / 100.0

lines = df["line"].to_numpy()
fave_win_probs = df["fave_win_prob"].to_numpy()

favorite_point_differentials = []
favorite_win_probabilities = []
data = []
for line, fave_win_prob in zip(lines, fave_win_probs):
    data.append((line, fave_win_prob))
    favorite_point_differentials.append(line)
    favorite_win_probabilities.append(fave_win_prob)

    data.append((-line, 1 - fave_win_prob))
    favorite_point_differentials.append(-line)
    favorite_win_probabilities.append(1 - fave_win_prob)

data.sort(key=lambda x: x[0])

favorite_point_differentials = [x[0] for x in data]
favorite_win_probabilities = [x[1] for x in data]

print(lines)


fig, ax = plt.subplots()

ax.plot(
    favorite_point_differentials,
    favorite_win_probabilities,
    linestyle="-",
    marker="o",
    color="b",
    label="Actual",
)


def win_prob(margin: float, scale_factor: float) -> float:
    team1_win_prob = 1 / (1 + 10 ** (margin / scale_factor))
    return team1_win_prob


xs = np.linspace(-30, 30, 100)


def objective(scale_factor):
    predicted_probs = [
        win_prob(x, scale_factor=scale_factor) for x in favorite_point_differentials
    ]
    return -r2_score(favorite_win_probabilities, predicted_probs)


result = minimize(objective, x0=[15], bounds=[(1, 50)])
best_scale_factor = result.x[0]

ys = [win_prob(x, scale_factor=best_scale_factor) for x in xs]
r2 = r2_score(
    favorite_win_probabilities,
    [win_prob(x, scale_factor=best_scale_factor) for x in favorite_point_differentials],
)
ax.plot(
    xs,
    ys,
    linestyle="--",
    color="r",
    label=f"Best fit (scale_factor={best_scale_factor:.4f}, r^2={r2:.4f})",
)

ax.legend()


plt.show()


print(df)
