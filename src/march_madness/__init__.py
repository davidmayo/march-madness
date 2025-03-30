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

    # FIRST ROUND
    bracket.advance_winner(
        game=bracket.games[0], winner_index=bracket.games[0].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[1], winner_index=bracket.games[1].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[2], winner_index=bracket.games[2].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[3], winner_index=bracket.games[3].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[4], winner_index=bracket.games[4].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[5], winner_index=bracket.games[5].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[6], winner_index=bracket.games[6].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[7], winner_index=bracket.games[7].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[8], winner_index=bracket.games[8].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[9], winner_index=bracket.games[9].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[10], winner_index=bracket.games[10].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[11], winner_index=bracket.games[11].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[12], winner_index=bracket.games[12].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[13], winner_index=bracket.games[13].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[14], winner_index=bracket.games[14].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[15], winner_index=bracket.games[15].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[16], winner_index=bracket.games[16].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[17], winner_index=bracket.games[17].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[18], winner_index=bracket.games[18].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[19], winner_index=bracket.games[19].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[20], winner_index=bracket.games[20].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[21], winner_index=bracket.games[21].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[22], winner_index=bracket.games[22].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[23], winner_index=bracket.games[23].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[24], winner_index=bracket.games[24].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[25], winner_index=bracket.games[25].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[26], winner_index=bracket.games[26].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[27], winner_index=bracket.games[27].team1_index
    )

    bracket.advance_winner(
        game=bracket.games[28], winner_index=bracket.games[28].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[29], winner_index=bracket.games[29].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[30], winner_index=bracket.games[30].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[31], winner_index=bracket.games[31].team1_index
    )

    # ROUND OF 32
    bracket.advance_winner(
        game=bracket.games[32], winner_index=bracket.games[32].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[33], winner_index=bracket.games[33].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[34], winner_index=bracket.games[34].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[35], winner_index=bracket.games[35].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[36], winner_index=bracket.games[36].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[37], winner_index=bracket.games[37].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[38], winner_index=bracket.games[38].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[39], winner_index=bracket.games[39].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[40], winner_index=bracket.games[40].team1_index
    )
    # bracket.advance_winner(game=bracket.games[41], winner_index=bracket.games[41].team1_index)  # OREGON
    bracket.advance_winner(
        game=bracket.games[41], winner_index=bracket.games[41].team2_index
    )  # ARIZONA
    bracket.advance_winner(
        game=bracket.games[42], winner_index=bracket.games[42].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[43], winner_index=bracket.games[43].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[44], winner_index=bracket.games[44].team1_index
    )
    bracket.advance_winner(
        game=bracket.games[45], winner_index=bracket.games[45].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[46], winner_index=bracket.games[46].team2_index
    )
    bracket.advance_winner(
        game=bracket.games[47], winner_index=bracket.games[47].team2_index
    )

    # ROUND OF 16
    bracket.advance_winner(game=bracket.games[48 + 0], winner_index=bracket.games[48 + 0].team1_index) # AUB/MICH
    bracket.advance_winner(game=bracket.games[48 + 1], winner_index=bracket.games[48 + 1].team2_index) # OLE MISS/MICH ST
    bracket.advance_winner(
        game=bracket.games[48 + 2], winner_index=bracket.games[48 + 2].team1_index
    )  # FLA
    bracket.advance_winner(
        game=bracket.games[48 + 3], winner_index=bracket.games[48 + 3].team1_index
    )  # TTECH
    bracket.advance_winner(
        game=bracket.games[48 + 4], winner_index=bracket.games[48 + 4].team1_index
    )  # Duke
    bracket.advance_winner(
        game=bracket.games[48 + 5], winner_index=bracket.games[48 + 5].team2_index
    )  # Bama
    bracket.advance_winner(game=bracket.games[48 + 6], winner_index=bracket.games[48 + 6].team1_index) # HOU/PUR
    bracket.advance_winner(game=bracket.games[48 + 7], winner_index=bracket.games[48 + 7].team2_index) # UK/UT

    # ROUND OF 8
    bracket.advance_winner(game=bracket.games[56 + 1], winner_index=bracket.games[56 + 1].team1_index) # Game 1 - FLA/TTECH
    # bracket.advance_winner(game=bracket.games[56 + 2], winner_index=bracket.games[56 + 2].team1_index) # Game 2 - DUKE/BAMA
    # bracket.advance_winner(game=bracket.games[56 + 0], winner_index=bracket.games[56 + 0].team1_index) # Game 3 - AUB/MSU
    # bracket.advance_winner(game=bracket.games[56 + 3], winner_index=bracket.games[56 + 3].team1_index) # Game 4 - HOU/TENN

    CURRENT_BRACKET_PATH.write_text(bracket.model_dump_json(indent=4))

    from march_madness.visualize import plot_bracket

    plot_bracket(bracket)
