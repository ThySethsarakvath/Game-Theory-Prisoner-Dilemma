"""Actions, TP1's payoff rule, and immutable match results."""

from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    COOPERATE = "C"
    DEFECT = "D"

    @classmethod
    def parse(cls, text: str) -> "Action":
        try:
            return cls(text.strip().upper())
        except ValueError:
            raise ValueError("Enter C to cooperate or D to defect.") from None


def payoff(action_a: Action, action_b: Action) -> tuple[int, int]:
    """Return (A's points, B's points), using TP1 p.1, not prison years."""
    if not isinstance(action_a, Action) or not isinstance(action_b, Action):
        raise ValueError("Both decisions must be Action values.")
    matrix = {
        (Action.COOPERATE, Action.COOPERATE): (3, 3),
        (Action.COOPERATE, Action.DEFECT): (0, 5),
        (Action.DEFECT, Action.COOPERATE): (5, 0),
        (Action.DEFECT, Action.DEFECT): (1, 1),
    }
    return matrix[action_a, action_b]


def require_positive_integer(value: int, label: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{label} must be a positive integer.")


@dataclass(frozen=True)
class RoundResult:
    number: int
    action_a: Action
    action_b: Action
    score_a: int
    score_b: int


@dataclass(frozen=True)
class MatchResult:
    player_a: str
    player_b: str
    strategy_a: str
    strategy_b: str
    rounds: tuple[RoundResult, ...]

    @property
    def totals(self) -> tuple[int, int]:
        return (
            sum(round_.score_a for round_ in self.rounds),
            sum(round_.score_b for round_ in self.rounds),
        )
