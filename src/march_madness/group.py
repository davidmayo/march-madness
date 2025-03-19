from pathlib import Path

import pydantic

from march_madness.bracket import Bracket
from march_madness import get_bracket

url = "https://fantasy.espn.com/games/tournament-challenge-bracket-2025/group?id=79ec54c4-676f-4a01-a758-613a6f4d40d4"
user_brackets_folder = Path("data/user_brackets")


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


if __name__ == "__main__":
    from march_madness.simulation import best_seed_wins, sim

    bracket = get_bracket()
    users_picks = sim(bracket, best_seed_wins)
    bracket_entry = BracketEntry(
        bracket=users_picks,
        bracket_name="Chalk bracket",
        user="Boring Person",
        url=None,
        json_path=user_brackets_folder / "0001.json",
        predicted_final_score=100,
    )
    bracket_entry.save()
    # print(bracket_entry.json_path.read_text())
    print("Done")

    group = Group.load()
    print(group)
