"""The four computer strategies required by TP1, page 2."""

from enum import Enum
from random import Random

from .models import Action


class Strategy(str, Enum):
    ALWAYS_COOPERATE = "Always cooperate"
    ALWAYS_DEFECT = "Always defect"
    RANDOM = "Random"
    TIT_FOR_TAT = "Tit-for-tat"


def choose_action(
    strategy: Strategy, opponent_history: tuple[Action, ...], rng: Random
) -> Action:
    """History contains completed rounds only, in chronological order."""
    if strategy is Strategy.ALWAYS_COOPERATE:
        return Action.COOPERATE
    if strategy is Strategy.ALWAYS_DEFECT:
        return Action.DEFECT
    if strategy is Strategy.RANDOM:
        return rng.choice(tuple(Action))
    if strategy is Strategy.TIT_FOR_TAT:
        return opponent_history[-1] if opponent_history else Action.COOPERATE
    raise ValueError("Unknown computer strategy.")
