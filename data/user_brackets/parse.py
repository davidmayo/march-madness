from pathlib import Path

from march_madness import get_bracket, Bracket, Team, Game, get_team
from march_madness.group import Group, BracketEntry

bracket = get_bracket()
teams = bracket.teams

raw_path = Path("./data/user_brackets/raw")
parsed_path = Path("./data/user_brackets/parsed")


espn_to_existing = {
    "AUB": "Auburn",
    "CREI": "Creighton",
    "UCSD": "UC San Diego",
}


for file in raw_path.glob("*.txt"):
    print(file)
    lines = file.read_text().splitlines()

    index = 0
    picks = []
    while index < len(lines):
        line = lines[index]
        if "Pick:" in line:
            # long_line = lines[index + 1]
            short_line = lines[index + 2]
            # print(short_line)
            picks.append(short_line)
            index += 3
        elif "Championship Pick" in line:
            # long_line = lines[index + 1]
            short_line = lines[index + 1]
            # print(short_line)
            picks.append(short_line)
            index += 3
        else:
            index += 1

    user_picks_bracket = bracket.clone()

    for index, pick in enumerate(picks):
        # if index >= 62:
        #     continue
        if index == 62:
            pick = None
            if file.stem in ("austin_jude", "danika_sparks", "ian_warford"):
                pick = "DUKE"
            elif file.stem in ("carrie_bruce"):
                pick = "ALA"
            elif file.stem in ("mila_shearer"):
                pick = "HOU"
            elif file.stem in ("chloe_hart"):
                pick = "UK"
            elif file.stem in ("noah_patrick"):
                pick = "AUB"
            elif file.stem in ("diddy_didier"):
                pick = "LOU"
            elif file.stem in ("david_mayo"):
                pick = "WIS"
            assert pick is not None
        team = get_team(pick)
        if not team:
            print(index, pick, get_team(pick))
            continue
        else:
            user_picks_bracket.advance_winner(user_picks_bracket.games[index], team.index)


    entry = BracketEntry(
        bracket=user_picks_bracket,
        bracket_name=file.stem,
        user=file.stem,
        url=None,
        # json_path=parsed_path / (file.stem + ".json"),
        predicted_final_score=None,
    )
    output_path = parsed_path / (file.stem + ".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(entry.model_dump_json(indent=4))
