# UV quirk workaround: https://github.com/astral-sh/uv/issues/7036#issuecomment-2416063312
from os import environ
from pathlib import Path
from sys import base_prefix

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")


import matplotlib.pyplot as plt

from march_madness import get_bracket, Bracket

bracket = get_bracket()


def plot_bracket(bracket: Bracket) -> None:
    """Plot the bracket."""

    fig, ax = plt.subplots(layout="tight")

    # ax.axis('off')

    round_ofs = [
        64,
        32,
        16,
        8,
        4,
    ]
    offset = len(round_ofs)

    x_left = 0
    x_base = 0 - offset - 1
    for round_index, round_of in enumerate(round_ofs):
        x_step = round_index
        x_left = x_base + x_step
        x_right = x_left + 1

        x_center = (x_left + x_right) / 2
        ax.text(x_center, 0, f"Round of {round_of}", va="bottom", ha="center")
        ax.text(-x_center, 0, f"Round of {round_of}", va="bottom", ha="center")

        y_base = 2**round_index / 4
        y_step = 2**round_index

        game_index = -1
        for game in bracket.games:
            if game.round_of != round_of:
                continue
            game_index += 1

            is_right = game_index >= round_of / 4

            y_top = y_base + game_index * y_step
            y_bottom = y_top + y_step / 2
            y_top = -y_top
            y_bottom = -y_bottom

            if is_right:
                pass
                x_left_plot = -x_left
                x_right_plot = -x_right
                x_center_plot = -x_center
                y_top_plot = y_top + max(round_ofs) / 4
                y_bottom_plot = y_bottom + max(round_ofs) / 4
            else:
                x_left_plot = x_left
                x_right_plot = x_right
                x_center_plot = x_center
                y_top_plot = y_top
                y_bottom_plot = y_bottom

            ax.plot(
                [x_left_plot, x_right_plot, x_right_plot, x_left_plot],
                [y_top_plot, y_top_plot, y_bottom_plot, y_bottom_plot],
                color="black",
            )

            top_text = f"game[{game.game_id}] TOP <{game_index}> {'L' if not is_right else 'R'}"
            bottom_text = f"game[{game.game_id}] BOT <{game_index}> {'L' if not is_right else 'R'}"
            if game.team1_index is not None:
                team1 = bracket.teams[game.team1_index]
                top_text = f"{team1.seed} {team1.name}"
            if game.team2_index is not None:
                team2 = bracket.teams[game.team2_index]
                bottom_text = f"{team2.seed} {team2.name}"

            ax.text(x_center_plot, y_top_plot, top_text, va="bottom", ha="center")
            ax.text(x_center_plot, y_bottom_plot, bottom_text, va="bottom", ha="center")

            # ax.plot([x, x + 1], [y, y], color="black")
            # if game.team1_index is not None:
            #     team1 = bracket.teams[game.team1_index]
            #     ax.text(x, y, f"{team1.seed} {team1.name}", va="center", ha="right")
            # if game.team2_index is not None:
            #     team2 = bracket.teams[game.team2_index]
            #     ax.text(x + 1, y, f"{team2.seed} {team2.name}", va="center", ha="left")
            # if game.winner_index is not None:
            #     winner = bracket.teams[game.winner_index]
            #     ax.text(x + 0.5, y, f"{winner.seed} {winner.name}", va="center", ha="center")
        pass

        # Final Four handled specially
        winner_position_x = 0
        winner_position_y = -8

        semifinalist_1_x_left = -1
        semifinalist_1_x_right = 0
        semifinalist_1_x_center = (semifinalist_1_x_left + semifinalist_1_x_right) / 2
        semifinalist_1_y = winner_position_y + 2

        semifinalist_2_x_left = 0
        semifinalist_2_x_right = 1
        semifinalist_2_x_center = (semifinalist_2_x_left + semifinalist_2_x_right) / 2
        semifinalist_2_y = winner_position_y - 2

        ax.plot(
            [semifinalist_1_x_left, semifinalist_1_x_right],
            [semifinalist_1_y, semifinalist_1_y],
            color="black",
        )
        ax.plot(
            [semifinalist_2_x_left, semifinalist_2_x_right],
            [semifinalist_2_y, semifinalist_2_y],
            color="black",
        )
        winner_rectangle = [
            (-0.75, +0.5),
            (+0.75, +0.5),
            (+0.75, -0.5),
            (-0.75, -0.5),
            (-0.75, +0.5),
        ]
        ax.plot(
            [x + winner_position_x for x, y in winner_rectangle],
            [y + winner_position_y for x, y in winner_rectangle],
            color="black",
        )

    final_game = bracket.games[-1]

    top_text = f"game[{final_game.game_id}] TOP"
    bottom_text = f"game[{final_game.game_id}] BOT"
    if final_game.team1_index is not None:
        team1 = bracket.teams[final_game.team1_index]
        top_text = f"{team1.seed} {team1.name}"
    if final_game.team2_index is not None:
        team2 = bracket.teams[final_game.team2_index]
        bottom_text = f"{team2.seed} {team2.name}"

    winner_text = f"game[{final_game.game_id}] WINNER"
    if final_game.winner_index is not None:
        winner = bracket.teams[final_game.winner_index]
        winner_text = f"{winner.seed} {winner.name}"
    ax.text(
        semifinalist_1_x_center,
        semifinalist_1_y,
        top_text,
        va="bottom",
        ha="center",
    )
    ax.text(
        semifinalist_2_x_center,
        semifinalist_2_y,
        bottom_text,
        va="bottom",
        ha="center",
    )

    ax.text(
        winner_position_x,
        winner_position_y,
        winner_text,
        va="center",
        ha="center",
    )

    plt.show()


def visualize_bracket(bracket: Bracket) -> None:
    """Visualize the bracket."""

    round_of = -1

    for game_index, game in enumerate(bracket.games):
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
                text = "TBD"

            if game.winner_index is not None and game.winner_index == index:
                text = f"**{text}**"
            teams.append(text)
        print(f"game {game_index:<2}: {teams[0]} v {teams[1]}")


if __name__ == "__main__":
    visualize_bracket(bracket)
    plot_bracket(bracket)
