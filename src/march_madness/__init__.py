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
    # CURRENT_BRACKET_PATH.write_text(bracket.model_dump_json(indent=4))
    # pprint(get_bracket())

    # pprint(sorted(bracket.teams, key=lambda team: team.kenpom, reverse=True))

    bracket = Bracket.model_validate_json(INITIAL_BRACKET_PATH.read_text())

    # THURSDAY GAMES, FIRST ROUND
    bracket.advance_winner(game=bracket.games[0], winner_index=bracket.games[0].team1_index)
    bracket.advance_winner(game=bracket.games[1], winner_index=bracket.games[1].team2_index)
    bracket.advance_winner(game=bracket.games[2], winner_index=bracket.games[2].team1_index)
    bracket.advance_winner(game=bracket.games[3], winner_index=bracket.games[3].team1_index)

    bracket.advance_winner(game=bracket.games[12], winner_index=bracket.games[12].team2_index)
    bracket.advance_winner(game=bracket.games[13], winner_index=bracket.games[13].team1_index) # TT
    bracket.advance_winner(game=bracket.games[14], winner_index=bracket.games[14].team2_index)
    bracket.advance_winner(game=bracket.games[15], winner_index=bracket.games[15].team1_index)

    bracket.advance_winner(game=bracket.games[20], winner_index=bracket.games[20].team1_index)
    bracket.advance_winner(game=bracket.games[21], winner_index=bracket.games[21].team1_index)

    bracket.advance_winner(game=bracket.games[24], winner_index=bracket.games[24].team1_index)
    bracket.advance_winner(game=bracket.games[25], winner_index=bracket.games[25].team1_index)
    bracket.advance_winner(game=bracket.games[26], winner_index=bracket.games[26].team2_index)
    bracket.advance_winner(game=bracket.games[27], winner_index=bracket.games[27].team1_index)
    
    bracket.advance_winner(game=bracket.games[30], winner_index=bracket.games[30].team1_index)
    bracket.advance_winner(game=bracket.games[31], winner_index=bracket.games[31].team1_index)


    CURRENT_BRACKET_PATH.write_text(bracket.model_dump_json(indent=4))

    from march_madness.visualize import plot_bracket

    plot_bracket(bracket)