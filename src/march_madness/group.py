from collections import Counter
from pathlib import Path

import pydantic

from march_madness.bracket import Bracket
from march_madness import get_bracket

url = "https://fantasy.espn.com/games/tournament-challenge-bracket-2025/group?id=79ec54c4-676f-4a01-a758-613a6f4d40d4"
user_brackets_folder = Path("data/user_brackets/parsed")


def next_user_bracket_path() -> Path:
    """Return the next available user bracket path."""
    existing_paths = list(user_brackets_folder.glob("*.json"))
    if not existing_paths:
        return user_brackets_folder / "0001.json"
    biggest_number = max(int(path.stem) for path in existing_paths)
    return user_brackets_folder / f"{biggest_number + 1:04d}.json"


class BracketEntry(pydantic.BaseModel):
    bracket: Bracket
    bracket_name: str | None = None
    user: str | None = None
    url: str | None = None
    json_path: Path | None = None
    score: int | None = None
    """Score in bracket challenge."""

    predicted_final_score: int | None = None
    """User's predicted final game total score."""

    @pydantic.model_validator(mode="after")
    def ensure_json_path(self) -> "BracketEntry":
        if not self.json_path:
            self.json_path = next_user_bracket_path()
        else:
            self.json_path = Path(self.json_path)
        return self

    # @pydantic.field_validator("json_path", mode="after")
    # @classmethod
    # def ensure_json_path(cls, value: Path | None) -> Path:
    #     if value is None:
    #         value = next_user_bracket_path()
    #     else:
    #         value = Path(value)
    #     return value

    def save(self) -> None:
        if self.json_path is None:
            raise ValueError("json_path is None")
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.json_path.write_text(self.model_dump_json(indent=4))


class Group(pydantic.BaseModel):
    entries: list[BracketEntry] = pydantic.Field(default_factory=list)

    @classmethod
    def load(cls) -> "Group":
        group_folder = user_brackets_folder
        entries = []
        for path in group_folder.glob("*.json"):
            entry = BracketEntry.model_validate_json(path.read_text())
            entries.append(entry)
        return cls(entries=entries)

    def score_all(self, actual_bracket: Bracket) -> BracketEntry:
        """Score all entries. Return the winner.

        TODO: Deal with ties."""
        for entry in self.entries:
            entry.score = actual_bracket.score(entry.bracket)
        return self.winner()

    def winner(self) -> BracketEntry:
        """TODO: Deal with ties."""
        return max(self.entries, key=lambda entry: entry.score)


class SimGroup:
    def __init__(self, group: Group, current_bracket: Bracket, sim_count: int = 100):
        self.group = group
        self.current_bracket = current_bracket
        self.sim_count = sim_count

        self._user_total_scores: dict[str, float] = {
            entry.user: 0 for entry in self.group.entries
        }
        self.user_average_scores: dict[str, float] = {}
        self._winner_counter: Counter[str, int] = Counter()
        self.winner_prob: dict[str, float] = {}

        self._do_sim()

    def _callback(self, bracket: Bracket) -> None:
        winner = None
        winning_score = 0
        for entry in self.group.entries:
            entry_score = bracket.score(entry.bracket)
            if entry_score > winning_score:
                winner = entry.user
                winning_score = entry_score
            self._user_total_scores[entry.user] += entry_score
        self._winner_counter[winner] += 1

    def _do_sim(self):
        from march_madness.simulation2 import Simulation

        sim = Simulation(
            bracket=self.current_bracket,
            sim_count=self.sim_count,
            callback=self._callback,
        )

        self.user_average_scores = {
            user: total_score / self.sim_count
            for user, total_score in self._user_total_scores.items()
        }

        self.winner_prob = {
            user: count / self.sim_count for user, count in self._winner_counter.items()
        }


if __name__ == "__main__":
    # from march_madness.simulation import best_seed_wins, sim

    # bracket = get_bracket()
    # users_picks = sim(bracket, best_seed_wins)
    # bracket_entry = BracketEntry(
    #     bracket=users_picks,
    #     bracket_name="Chalk bracket",
    #     user="Boring Person",
    #     url=None,
    #     json_path=user_brackets_folder / "0001.json",
    #     predicted_final_score=100,
    # )
    # bracket_entry.save()
    # # print(bracket_entry.json_path.read_text())
    # print("Done")
    from rich.pretty import pprint

    group = Group.load()
    pprint(group)

    sim_group = SimGroup(group=group, current_bracket=get_bracket(), sim_count=100_000)
    print(f"\nAVERAGE SCORES:")
    pprint(
        sorted(sim_group.user_average_scores.items(), key=lambda x: x[1], reverse=True),
        indent_guides=False,
    )
    print(f"\nWINNER PROBABILITIES (%):")
    pprint(
        [
            (user, prob * 100)
            for user, prob in
            sorted(sim_group.winner_prob.items(), key=lambda x: x[1], reverse=True)
        ],
        indent_guides=False,
    )

    title = "05_round_16_mid"
    import json

    with open(f"data/sim_results/{title}.json", "w") as file:
        file.write(json.dumps(
            {
                "average_scores": sim_group.user_average_scores,
                "winner_probabilities": {
                    key: value * 100
                    for key, value in
                    sim_group.winner_prob.items()
                },
            },
            indent=4,
        ))