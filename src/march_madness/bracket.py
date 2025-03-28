import math
import pydantic


class Team(pydantic.BaseModel):
    name: str
    seed: int = pydantic.Field(repr=False)
    index: int | None = pydantic.Field(default=None, repr=False)
    region: str = pydantic.Field(repr=False)
    kenpom: float | None = pydantic.Field(default=None, repr=False)
    kenpom_name: str | None = pydantic.Field(default=None, repr=False)
    espn_name: str | None = pydantic.Field(default=None, repr=False)

    @property
    def kenpom_id(self) -> str:
        return self.kenpom_name or self.name

    @property
    def espn_id(self) -> str:
        return self.espn_name or self.name


class Game(pydantic.BaseModel):
    team1_index: int | None = None
    team2_index: int | None = None
    winner_index: int | None = None
    game_id: int
    round_of: int | None = None
    """1, 2, 4, 8, etc."""


class Bracket(pydantic.BaseModel):
    teams: list[Team] = pydantic.Field(default_factory=list)
    games: list[Game] | None = None

    @pydantic.model_validator(mode="after")
    def set_games_to_empty_list(self):
        if self.games is None:
            self.games = self._generate_games_from_teams()
        return self

    def _generate_games_from_teams(self) -> list[Game]:
        games: list[Game] = []
        game_id = 0

        num_teams = len(self.teams)

        num_rounds = int(math.log2(num_teams))

        for round in range(num_rounds):
            num_games = num_teams // (2 * (2**round))
            round_of = 2 ** (num_rounds - round)
            # print(f"{num_games=} {round_of=}")

            for game_round_index in range(num_games):
                game = Game(game_id=game_id, round_of=round_of)
                games.append(game)
                game_id += 1

        for index in range(num_teams // 2):
            game = games[index]
            game.team1_index = index * 2
            game.team2_index = index * 2 + 1
            # game.team2 = self.teams[index * 2 + 1]

        return games

    def undecided_games(self) -> list[Game]:
        return [game for game in self.games if game.winner_index is None]

    def current_round_of(self) -> int:
        return max([game.round_of for game in self.undecided_games()])

    def current_round_games(self) -> list[Game]:
        round_of = self.current_round_of()
        return [game for game in self.undecided_games() if game.round_of == round_of]

    def advance_winner(self, game: Game, winner_index: int):
        # Set the winner
        self.games[game.game_id].winner_index = winner_index

        # Advance the winner

        round_start_index = -1

        if game.round_of == 64:
            round_start_index = 0
            next_round_start_index = 32
        elif game.round_of == 32:
            round_start_index = 32
            next_round_start_index = 48
        elif game.round_of == 16:
            round_start_index = 48
            next_round_start_index = 56
        elif game.round_of == 8:
            round_start_index = 56
            next_round_start_index = 60
        elif game.round_of == 4:
            round_start_index = 60
            next_round_start_index = 62
        elif game.round_of == 2:
            return
        elif game.round_of == 1:
            return

        within_round_index = game.game_id - round_start_index
        within_next_round_index = within_round_index // 2
        is_next_round_team1 = within_round_index % 2 == 0
        next_game_id = next_round_start_index + within_next_round_index
        if is_next_round_team1:
            self.games[next_game_id].team1_index = winner_index
        else:
            self.games[next_game_id].team2_index = winner_index

    def score(self, other: "Bracket") -> int:
        score = 0
        for game, other_game in zip(self.games, other.games):
            game: Game
            other_game: Game
            if game.winner_index == other_game.winner_index:
                score += 640 / game.round_of
        return score

    def clone(self) -> "Bracket":
        return Bracket.model_validate_json(self.model_dump_json())


if __name__ == "__main__":
    bracket = Bracket(
        games=None,
        teams=[
            Team(name="Gonzaga", seed=1, region="West"),
            Team(name="Texas Southern", seed=16, region="West"),
            Team(name="Oklahoma", seed=8, region="West"),
            Team(name="Missouri", seed=9, region="West"),
        ],
    )
    # bracket = Bracket()
    # print(f"{bracket.games=}")
    # print(bracket)
