import dash
from dash import dcc, html
import plotly.graph_objects as go

from march_madness import get_bracket, Bracket, Team, Game
from march_madness.simulation2 import Simulation

# Initialize the Dash app
app = dash.Dash(__name__)


def create_bracket(bracket: Bracket | None = None) -> go.Figure:
    """Creates a Plotly figure for the bracket."""
    bracket = bracket or get_bracket()

    # # DEBUG: Force a winner
    # bracket.advance_winner(bracket.games[1], bracket.games[1].team2_index)

    sim = Simulation(bracket=bracket, sim_count=100)

    figure = go.Figure()

    # Add the games
    for game in bracket.games:
        # Final game handled specially
        if game.round_of <= 2:
            continue
        if game.team1_index is not None:
            team1 = bracket.teams[game.team1_index]
        else:
            team1 = None
        if game.team2_index is not None:
            team2 = bracket.teams[game.team2_index]
        else:
            team2 = None

        round_index = {
            64: 0,
            32: 1,
            16: 2,
            8: 3,
            4: 4,
            2: 5,
            1: 6,
        }[game.round_of]

        games_this_round = int(2 ** (5 - round_index))

        within_round_indx = (
            game.game_id
            - {
                0: 0,
                1: 32,
                2: 48,
                3: 56,
                4: 60,
                5: 62,
                6: 63,
            }[round_index]
        )

        is_right = within_round_indx >= games_this_round / 2
        is_left = not is_right

        x_offset = 5.75 - round_index
        """Distance this thing should be from 0"""

        y_spacing = 32 / games_this_round
        # y_spacing = 1 # TODO: Fix this

        if is_left:
            y_index = within_round_indx
        else:
            y_index = within_round_indx - games_this_round / 2

        y_base_position = (
            -(y_index - games_this_round / 4 + 0.5) * y_spacing
        )  # This works, somehow

        wall_height = y_spacing / 2

        x_inner = x_offset
        x_outer = x_offset - 1

        y_bottom = y_base_position - wall_height / 2
        y_top = y_base_position + wall_height / 2

        y_winner_bottom = y_base_position
        x_winner = x_outer - 0.5

        print(f"DEBUG: {games_this_round=} {y_base_position=}")
        if is_left:
            x_offset = -x_offset
            x_inner = -x_inner
            x_outer = -x_outer
            x_winner = -x_winner

        x_center = (x_inner + x_outer) / 2

        figure.add_trace(
            go.Scatter(
                x=[x_inner, x_outer, x_outer, x_inner],
                y=[y_bottom, y_bottom, y_top, y_top],
                mode="lines+markers",
                line=dict(color="black"),
                marker=dict(color="black"),
                showlegend=False,
                hoverinfo="skip",
                text=f"Game ID: {game.game_id}",
            )
        )

        def get_text(
            team: Team | None, top_bottom: str, game_id: int | None = None
        ) -> str:
            if game.game_id >= 32:
                return ""
            if team is None:
                return f"games[{game.game_id}] {top_bottom}"
            return f"({team.seed}) {team.name}"

        top_text = get_text(team1, "TOP", game.game_id)
        bottom_text = get_text(team2, "BOT", game.game_id)

        figure.add_annotation(
            x=x_center,
            y=y_bottom,
            text=bottom_text,
            showarrow=False,
            yanchor="bottom",
        )
        figure.add_annotation(
            x=x_center,
            y=y_top,
            text=top_text,
            showarrow=False,
            yanchor="bottom",
        )

        def get_winner_text(game: Game) -> str:
            if game.winner_index is None:
                return sim.most_likely_pretty_result(game.game_id)
            else:
                winner = bracket.teams[game.winner_index]
                return f"{winner.name}"

        def get_winner_hover_text(game: Game) -> str:
            if game.winner_index is None:
                return sim.pretty_results(game.game_id).replace("\n", "<br>")
            else:
                return None

        if game.round_of > 4:
            figure.add_annotation(
                x=x_winner,
                y=y_winner_bottom,
                text=get_winner_text(game),
                showarrow=False,
                yanchor="bottom",
                hovertext=get_winner_hover_text(game),
                hoverlabel=dict(bgcolor="white"),
            )

    # FINAL FOUR
    championship_game = bracket.games[-1]
    semifinalist1_index = championship_game.team1_index
    semifinalist2_index = championship_game.team2_index
    if semifinalist1_index is not None:
        semifinalist1 = bracket.teams[championship_game.team1_index]
    else:
        semifinalist1 = None
    if semifinalist2_index is not None:
        semifinalist2 = bracket.teams[championship_game.team2_index]
    else:
        semifinalist2 = None

    # LEFT SEMIFINALIST
    game = bracket.games[-3]
    winner_text = get_winner_text(game)
    winner_hover_text = get_winner_hover_text(game)

    x_inner = -0.75
    x_outer = x_inner + 1
    x_center = (x_inner + x_outer) / 2
    y_top = 2
    top_text = get_text(semifinalist1, "TOP")

    figure.add_trace(
        go.Scatter(
            x=[x_inner, x_outer],
            y=[y_top, y_top],
            mode="lines+markers",
            line=dict(color="black"),
            marker=dict(color="black"),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    figure.add_annotation(
        x=x_center,
        y=y_top,
        text=winner_text,
        showarrow=False,
        yanchor="bottom",
        hovertext=winner_hover_text,
        hoverlabel=dict(bgcolor="white"),
    )

    # RIGHT SEMIFINALIST
    x_inner = -0.25
    x_outer = x_inner + 1
    x_center = (x_inner + x_outer) / 2
    y_top = -2
    top_text = get_text(semifinalist2, "BOT")
    game = bracket.games[-2]
    winner_text = get_winner_text(game)
    winner_hover_text = get_winner_hover_text(game)

    figure.add_trace(
        go.Scatter(
            x=[x_inner, x_outer],
            y=[y_top, y_top],
            mode="lines+markers",
            line=dict(color="black"),
            marker=dict(color="black"),
            showlegend=False,
            hoverinfo="skip",
            text=f"Game ID: {championship_game.game_id}",
        )
    )
    figure.add_annotation(
        x=x_center,
        y=y_top,
        text=winner_text,
        showarrow=False,
        yanchor="bottom",
        hovertext=winner_hover_text,
        hoverlabel=dict(bgcolor="white"),
    )

    # CHAMPION
    x_inner = -0.5
    x_outer = x_inner + 1
    x_center = (x_inner + x_outer) / 2
    y_top = 0.25
    y_bottom = -y_top
    y_center = (y_top + y_bottom) / 2
    winner_text = get_text(semifinalist1, "WIN")
    game = championship_game
    winner_text = get_winner_text(game)
    winner_hover_text = get_winner_hover_text(game)

    figure.add_trace(
        go.Scatter(
            x=[x_inner, x_outer, x_outer, x_inner, x_inner],
            y=[y_bottom, y_bottom, y_top, y_top, y_bottom],
            mode="lines+markers",
            line=dict(color="black"),
            marker=dict(color="black"),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    figure.add_annotation(
        x=x_center,
        y=y_center,
        text=winner_text,
        showarrow=False,
        yanchor="middle",
        hovertext=winner_hover_text,
        hoverlabel=dict(bgcolor="white"),
    )

    return figure

    return go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 1, 2], mode="lines+markers"))


bracket_figure = create_bracket()

# Define the layout
app.layout = html.Div(
    style={"display": "flex", "height": "100vh"},  # Set full view height
    children=[
        html.Div(
            dcc.Graph(
                id="bracket", figure=bracket_figure, style={"height": "100%"}
            ),  # Ensure the graph itself fills the height
            style={
                "flex": "1",
                "padding": "10px",
                "height": "100%",
            },  # Ensure the container fills the height
        ),
        html.Div(
            id="right",
            children="This is the right component",
            style={"flex": "1", "padding": "10px"},
        ),
    ],
)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=9001)
