"""Run a fixed number of simultaneous-decision rounds."""

from collections.abc import Callable

from .models import Action, MatchResult, RoundResult, payoff, require_positive_integer
from .players import Player


def play_match(
    player_a: Player,
    player_b: Player,
    rounds: int,
    on_round: Callable[[RoundResult], None] | None = None,
) -> MatchResult:
    """Collect both actions before revealing results or updating either history."""
    require_positive_integer(rounds, "Rounds")
    history_a: list[Action] = []
    history_b: list[Action] = []
    results: list[RoundResult] = []
    for number in range(1, rounds + 1):
        action_a = player_a.choose_action(tuple(history_b))
        action_b = player_b.choose_action(tuple(history_a))
        score_a, score_b = payoff(action_a, action_b)
        result = RoundResult(number, action_a, action_b, score_a, score_b)
        results.append(result)
        history_a.append(action_a)
        history_b.append(action_b)
        if on_round is not None:
            on_round(result)
    return MatchResult(
        player_a.name,
        player_b.name,
        player_a.strategy_name,
        player_b.strategy_name,
        tuple(results),
    )
