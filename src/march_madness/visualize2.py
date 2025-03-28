import functools
from typing import Literal

import pydantic


class Line(pydantic.BaseModel):
    points: list[tuple[float, float]] = pydantic.Field(default_factory=list)

    @property
    @functools.lru_cache()
    def xs(self) -> list[float]:
        return [point[0] for point in self.points]

    @property
    @functools.lru_cache()
    def ys(self) -> list[float]:
        return [point[1] for point in self.points]

    def __hash__(self):
        return hash(id(self))


class GameLocation(pydantic.BaseModel):
    game_id: int
    team_1_point: tuple[float, float]
    team_2_point: tuple[float, float]
    winner_point: tuple[float, float]


class BracketViz(pydantic.BaseModel):
    lines: list[Line] = pydantic.Field(default_factory=list)
    game_locations: dict[int, GameLocation] = pydantic.Field(default_factory=dict)
    # model_config = pydantic.ConfigDict(extra="allow")

    def __hash__(self):
        return hash(id(self))

    @functools.lru_cache()
    def find_game(self, point: tuple[float, float]) -> tuple[int, Literal[1, 2]] | None:
        """Given a point, determine if this is in the bounding box of a game's source teams."""
        x_left = -0.45
        x_right = 0.45
        y_bottom = 0.00
        y_top = 0.40
        for game_id, game_location in self.game_locations.items():
            team_1_bounding_box_x_left = game_location.team_1_point[0] + x_left
            team_1_bounding_box_x_right = game_location.team_1_point[0] + x_right
            team_1_bounding_box_y_bottom = game_location.team_1_point[1] + y_bottom
            team_1_bounding_box_y_top = game_location.team_1_point[1] + y_top
            if (
                team_1_bounding_box_x_left <= point[0] <= team_1_bounding_box_x_right
                and team_1_bounding_box_y_bottom
                <= point[1]
                <= team_1_bounding_box_y_top
            ):
                return game_id, 1

            team_2_bounding_box_x_left = game_location.team_2_point[0] + x_left
            team_2_bounding_box_x_right = game_location.team_2_point[0] + x_right
            team_2_bounding_box_y_bottom = game_location.team_2_point[1] + y_bottom
            team_2_bounding_box_y_top = game_location.team_2_point[1] + y_top
            if (
                team_2_bounding_box_x_left <= point[0] <= team_2_bounding_box_x_right
                and team_2_bounding_box_y_bottom
                <= point[1]
                <= team_2_bounding_box_y_top
            ):
                return game_id, 2

        return None


if __name__ == "__main__":
    from pathlib import Path
    from matplotlib import pyplot as plt

    # UV quirk workaround: https://github.com/astral-sh/uv/issues/7036#issuecomment-2416063312
    from os import environ
    from pathlib import Path
    from sys import base_prefix
    from matplotlib.patches import Rectangle

    environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
    environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")
    bracket_viz = BracketViz.model_validate_json(
        Path("data/bracket_viz.json").read_text()
    )

    fig, ax = plt.subplots(layout="tight")
    for line in bracket_viz.lines:
        ax.plot(line.xs, line.ys, linestyle="--", color="black", alpha=0.3)

    for game_id, game_location in bracket_viz.game_locations.items():
        # winner_rect = Rectangle(
        #     (game_location.winner_point[0] - 0.5, game_location.winner_point[1]),
        #     1,
        #     0.5,
        #     # color="green",
        #     alpha=0.3,
        # )
        # ax.add_patch(winner_rect)
        ax.text(
            *game_location.team_1_point,
            f"g[{game_id}]-team1",
            verticalalignment="bottom",
            horizontalalignment="center",
            alpha=0.3,
        )
        ax.text(
            *game_location.team_2_point,
            f"g[{game_id}]-team2",
            verticalalignment="bottom",
            horizontalalignment="center",
            alpha=0.3,
        )
        # ax.text(*game_location.winner_point, f"g[{game_id}]-win", verticalalignment="bottom", horizontalalignment="center", alpha=0.3)

    import numpy as np

    team_1_points = []
    team_2_points = []
    for x in np.arange(-6, 6, 0.05 / 2):
        for y in np.arange(-9, 9, 0.1 / 2):
            result = bracket_viz.find_game((x, y))
            if result is None:
                continue
            game_id, team = result
            if team == 1:
                team_1_points.append((x, y))
            else:
                team_2_points.append((x, y))

    team_1_points = np.array(team_1_points)
    team_2_points = np.array(team_2_points)

    ax.scatter(*team_1_points.T, marker=".", color="blue", alpha=0.03)
    ax.scatter(*team_2_points.T, marker=".", color="red", alpha=0.03)
    plt.show()
