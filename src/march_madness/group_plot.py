import json

from pathlib import Path

folder = Path("data/sim_results")

files = sorted(folder.glob("*.json"))

file_names = [path.stem for path in files]

user_names = [path.stem for path in Path("data/user_brackets/parsed").glob("*.json")]
print(user_names)
print(file_names)

win_percent_data = {}
score_data = {}

for user in user_names:
    win_percent_data[user] = []
    score_data[user] = []

for file_index, file in enumerate(files):
    with open(file, "r") as file:
        data = json.load(file)

    for user in user_names:
        win_percent_data[user].append(data["winner_probabilities"][user])
        score_data[user].append(data["average_scores"][user])
# UV quirk workaround: https://github.com/astral-sh/uv/issues/7036#issuecomment-2416063312
from os import environ
from pathlib import Path
from sys import base_prefix
from matplotlib.patches import Rectangle

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")
import matplotlib.pyplot as plt
fig, [ax_score, ax_win] = plt.subplots(1, 2, figsize=(16, 9), layout="constrained")

ax_score: plt.Axes
ax_win: plt.Axes

for user in user_names:
    first_name = user.split("_")[0].capitalize()
    ax_score.plot(score_data[user], label=user, marker="o")
    ax_win.plot(win_percent_data[user], label=user, marker="o")

    color = ax_score.get_lines()[-1].get_color()
    ax_score.text(0, score_data[user][0], first_name + " ", ha='right', va='center', fontsize=10, color=color)
    ax_score.text(len(score_data[user]) - 1, score_data[user][-1], " " + first_name, ha='left', va='center', fontsize=10, color=color)

    ax_win.text(0, win_percent_data[user][0], first_name + " ", ha='right', va='center', fontsize=10, color=color)
    ax_win.text(len(win_percent_data[user]) - 1, win_percent_data[user][-1], " " + first_name, ha='left', va='center', fontsize=10, color=color)
    # ax_score.text(0, score_data[user][0], first_name, ha='center', va='bottom', fontsize=10)
    # ax_score.text(len(score_data[user]) - 1, score_data[user][-1], first_name, ha='center', va='bottom', fontsize=10)
    # ax_win.text(0, win_percent_data[user][0], first_name, ha='center', va='bottom', fontsize=10)
    # ax_win.text(len(win_percent_data[user]) - 1, win_percent_data[user][-1], first_name, ha='center', va='bottom', fontsize=10)

ax_score.set_title("Average Scores")
ax_score.set_xlabel("Simulation Number")

ax_win.set_title("Winner Probabilities")
ax_win.set_xlabel("Simulation Number")

ax_score.legend()
ax_win.legend()

ax_score.set_xticks(range(len(file_names)))
label_names = [" ".join(name.split("_")[1:]).upper() for name in file_names]
ax_score.set_xticklabels(label_names, rotation=45, ha="right")

ax_win.set_xticks(range(len(file_names)))
ax_win.set_xticklabels(label_names, rotation=45, ha="right")

# ax_win.grid()
# ax_score.grid()
ax_win.set_title("Predicted probability of being in first\nplace at tournament end (percentage)")
ax_score.set_title("Predicted total score at\ntournament end (average)")

plt.show()