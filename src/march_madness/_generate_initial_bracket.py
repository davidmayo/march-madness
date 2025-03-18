from rich.pretty import pprint

from pathlib import Path
from march_madness import Team, Bracket
from march_madness.kenpom import update_bracket_kenpoms

regions = ["South", "West", "East", "Midwest"]
seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

name_to_kenpom_name = {
    # FIRST FOUR
    "ALST/SFU": "Alabama St.",
    # "ALST/SFU": "Saint Francis",
    "SDSU/UNC": "San Diego St.",
    # "SDSU/UNC": "North Carolina",
    "AMER/MTSM": "American",
    # "AMER/MTSM": "Mount St. Mary's",
    "TEX/XAV": "Texas",
    # "TEX/XAV": "Xavier",
    # OTHERS
    "Ole Miss": "Mississippi",
    "Mich. St.": "Michigan St.",
    "UConn": "Connecticut",
    "Colo. St.": "Colorado St.",
    "UNCW": "UNC Wilmington",
    "Omaha": "Nebraska Omaha",
    "Miss. St.": "Mississippi St.",
}

path = Path("teams.txt")

lines = path.read_text().strip().splitlines()

teams: list[Team] = []

for index, line in enumerate(lines):
    seed = seeds[index % 16]
    region = regions[index // 16]
    team = Team(name=line, seed=seed, region=region, index=index)
    team.kenpom_name = name_to_kenpom_name.get(line)
    teams.append(team)


pprint(teams[-1])

bracket = Bracket(teams=teams)
update_bracket_kenpoms(bracket)
# update_bracket_kenpoms(bracket)
# pprint(bracket)

pprint(bracket.current_round_of())
pprint(bracket.current_round_games())

out_path = Path("data/initial_bracket.json")

if out_path.exists():
    raise FileExistsError(f"File exists: {out_path}. Manually delete to rebuild.")


with open(out_path, "w") as file:
    file.write(bracket.model_dump_json(indent=4))
