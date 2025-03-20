from pathlib import Path
from march_madness.bracket import Bracket, Game, Team  # noqa: F401
from march_madness.kenpom import update_bracket_kenpoms


INITIAL_BRACKET_PATH = Path("data/initial_bracket.json")
CURRENT_BRACKET_PATH = Path("data/current_bracket.json")


def get_bracket() -> Bracket:
    if CURRENT_BRACKET_PATH.exists():
        bracket = Bracket.model_validate_json(CURRENT_BRACKET_PATH.read_text())
    elif INITIAL_BRACKET_PATH.exists():
        bracket = Bracket.model_validate_json(INITIAL_BRACKET_PATH.read_text())
    else:
        bracket = None
    if bracket:
        update_bracket_kenpoms(bracket)
    return bracket

def get_team(espn_id: str) -> Team | None:
    bracket = get_bracket()
    for team in bracket.teams:
        if team.espn_id == espn_id:
            return team
    return None

if __name__ == "__main__":
    from rich.pretty import pprint

    bracket = get_bracket()
    pprint(get_bracket())

    pprint(sorted(bracket.teams, key=lambda team: team.kenpom, reverse=True))
