from collections import Counter
from typing import Callable

from march_madness import Bracket, Game, get_bracket
from march_madness.simulation import elo_style, sim


class Simulation:
    def __init__(
        self,
        *,
        bracket: Bracket,
        sim_game_function: Callable[[Game, Bracket], int] = elo_style,
        sim_count: int = 100,
    ):
        self.bracket = bracket
        self.sim_game_function = sim_game_function
        self.sim_count = sim_count
        self._results: dict[int, Counter[int, int]] = {}
        self._do_sim()

    def results(self, game_id: int) -> list[tuple[str, float]]:
        def name(index: int) -> str:
            team = self.bracket.teams[index]
            return f"{team.name}"

        return [
            (name(index), count / self.sim_count)
            for index, count in self._results[game_id].most_common()
        ]

    def pretty_results(self, game_id: int, cutoff: int | None = None) -> str:
        results = self.results(game_id)
        # if len(results) == 1:
        #     return results[0][0]
        if cutoff is None:
            cutoff = len(results)
        rv = ""
        for result in results[:cutoff]:
            rv += f"{result[0]}: {result[1] * 100:.1f}%\n"
        if len(results) > cutoff:
            rv += (
                f"<others>: {sum(result[1] for result in results[cutoff:]) * 100:.1f}%"
            )
        return rv.strip()

    def most_likely_pretty_result(self, game_id: int) -> str:
        return self.pretty_results(game_id).splitlines()[0]

    def _do_sim(self) -> None:
        self._results = {game.game_id: Counter() for game in self.bracket.games}

        for index in range(self.sim_count):
            print(f"Simulating {index + 1}/{self.sim_count}")
            simmed_bracket = sim(
                bracket=self.bracket, sim_game_function=self.sim_game_function
            )
            for game in simmed_bracket.games:
                if game.winner_index is not None:
                    self._results[game.game_id][game.winner_index] += 1


if __name__ == "__main__":
    simulation = Simulation(bracket=get_bracket(), sim_count=100)
    from rich.pretty import pprint

    for game_id in range(63):
        print(f"Game {game_id}:")
        pprint(simulation.results(game_id))
        print(simulation.pretty_results(game_id))
        print()
    pass
