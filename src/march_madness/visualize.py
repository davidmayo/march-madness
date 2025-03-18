# UV quirk workaround: https://github.com/astral-sh/uv/issues/7036#issuecomment-2416063312
from os import environ
from pathlib import Path
from sys import base_prefix

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")
import tkinter as tk


import matplotlib.pyplot as plt

from march_madness import get_bracket, Bracket, Game, Team

bracket = get_bracket()


def visualize_bracket(bracket: Bracket) -> None:
    """Visualize the bracket."""

    round_of = -1

    for game in bracket.games:
        if game.round_of != round_of:
            print(f"=== ROUND OF {game.round_of} ===")
            round_of = game.round_of
        indexes = [game.team1_index, game.team2_index]
        teams = []
        for index in indexes:
            if index is None:
                team = None
            else:
                team = bracket.teams[index]
            if team:
                text = f"({team.seed}) {team.name}"
            else:
                text = ""
            teams.append(text)
        print(f"{teams[0]} v {teams[1]}")


if __name__ == "__main__":
    visualize_bracket(bracket)
