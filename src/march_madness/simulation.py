import scipy.stats as stats
import random
from typing import Callable
from march_madness import get_bracket, Bracket, Game, Team

rand = random.Random(40351)
AVERAGE_TEMPO = 70
"""Average tempo (possessions per 40 minutes) for college basketball."""


def random_winner(game: Game, bracket: Bracket) -> int:
    return rand.choice([game.team1_index, game.team2_index])


def best_kenpom_wins(game: Game, bracket: Bracket) -> int:
    team1: Team = bracket.teams[game.team1_index]
    team2: Team = bracket.teams[game.team2_index]
    if team1.kenpom > team2.kenpom:
        return game.team1_index
    else:
        return game.team2_index


def best_seed_wins(game: Game, bracket: Bracket) -> int:
    team1: Team = bracket.teams[game.team1_index]
    team2: Team = bracket.teams[game.team2_index]
    if team1.seed < team2.seed:
        return game.team1_index
    else:
        return game.team2_index


# At one point, Ken Pomeroy used 11: https://www.reddit.com/r/CollegeBasketball/comments/5tl6gj/comment/ddnk56m/
# This is very slow.
def normal_distribution(
    game: Game,
    bracket: Bracket,
    standard_deviation: float = 11,
) -> int:
    def win_probability_normal(adjEM_A, adjEM_B, std_dev=11):
        """Calculate the probability of Team A beating Team B using a normal CDF approach."""
        predicted_margin = adjEM_A - adjEM_B
        return 1 - stats.norm.cdf(0, loc=predicted_margin, scale=std_dev)

    team1: Team = bracket.teams[game.team1_index]
    team2: Team = bracket.teams[game.team2_index]

    team1_win_prob = win_probability_normal(
        team1.kenpom, team2.kenpom, standard_deviation
    )
    if rand.random() < team1_win_prob:
        return game.team1_index
    else:
        return game.team2_index


# No clue what this scale factor should be.
# ChatGPT suggested 20, 15, and 12.5 at various points, and I couldn't find any actual source.
# (I blame sports betting for this. All this used to be a lot more open.)
def elo_style(
    game: Game,
    bracket: Bracket,
    scale_factor: float = 13.7420,  # Empirically determined in `data/blah.py`
) -> int:
    team1: Team = bracket.teams[game.team1_index]
    team2: Team = bracket.teams[game.team2_index]

    team2_scoring_margin = (team2.kenpom - team1.kenpom) * (AVERAGE_TEMPO / 100)

    team1_win_prob = 1 / (1 + 10 ** (team2_scoring_margin / scale_factor))

    # print(f"DEBUG: {team1_win_prob*100:.2f}% that ({team1.seed}) {team1.name} [kenpom={team1.kenpom}] beats ({team2.seed}) {team2.name} [kenpom={team2.kenpom}]")
    if rand.random() < team1_win_prob:
        return game.team1_index
    else:
        return game.team2_index


def sim(
    bracket: Bracket,
    sim_game_function: Callable[[Game, Bracket], int] = random_winner,
) -> Bracket:
    bracket = bracket.clone()
    for game in bracket.games:
        if game.winner_index is not None:
            continue
        if game.team1_index is not None and game.team2_index is not None:
            game.winner_index = sim_game_function(game=game, bracket=bracket)
            bracket.advance_winner(game, game.winner_index)
    return bracket


if __name__ == "__main__":
    from march_madness.visualize import plot_bracket

    bracket = get_bracket()

    from rich.pretty import pprint

    # pprint(bracket)
    from collections import Counter

    winner_counter = Counter()
    # bracket = bracket.clone()
    import time

    start = time.monotonic()
    for _ in range(10000):
        simmed_bracket = sim(
            bracket,
            sim_game_function=normal_distribution,
        )
        winner_index = simmed_bracket.games[-1].winner_index
        winner = simmed_bracket.teams[winner_index]
        winner_text = f"({winner.seed}) {winner.name}"
        winner_counter[winner_text] += 1
    end = time.monotonic()
    print(f"Time: {end - start:.2f}s for {len(winner_counter):,} sims")
    # pprint(simmed_bracket)
    pprint(list(enumerate(winner_counter.most_common(), start=1)))
    plot_bracket(simmed_bracket)
