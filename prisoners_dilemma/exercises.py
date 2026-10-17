"""Five small exercise entry points sharing the same tested game engine."""

from random import Random

from .display import (
    show_match, show_observations, show_round, show_strategy_summary, show_tournament,
)
from .engine import play_match
from .models import MatchResult
from .players import ComputerPlayer, HumanPlayer, random_computer
from .strategies import Strategy
from .tournament import TournamentResult, play_tournament
from .terminal import Color, paint


def exercise_1() -> MatchResult:
    result = play_match(HumanPlayer("Human A"), HumanPlayer("Human B"), 1, show_round)
    show_match(result)
    return result


def exercise_2(rounds: int) -> MatchResult:
    result = play_match(HumanPlayer("Human A"), HumanPlayer("Human B"), rounds, show_round)
    show_match(result)
    return result


def exercise_3(rounds: int, strategy: Strategy, rng: Random) -> MatchResult:
    computer = ComputerPlayer("Computer B", strategy, Random(rng.getrandbits(64)))
    print(paint(f"\n[CPU] Computer strategy: {strategy.value}", Color.MAGENTA))
    result = play_match(HumanPlayer("Human A"), computer, rounds, show_round)
    show_match(result)
    return result


def exercise_4(rounds: int, rng: Random) -> MatchResult:
    player_a = random_computer("Computer A", rng)
    player_b = random_computer("Computer B", rng)
    print(paint(f"\n[CPU] Computer A: {player_a.strategy_name}", Color.MAGENTA))
    print(paint(f"[CPU] Computer B: {player_b.strategy_name}", Color.MAGENTA))
    result = play_match(player_a, player_b, rounds, show_round)
    show_match(result)
    show_observations([result])
    return result


def exercise_5(rounds: int, player_count: int, rng: Random) -> TournamentResult:
    players = [random_computer(f"Computer {i}", rng) for i in range(1, player_count + 1)]
    print("\nTournament rules: total points decide each match; tied scores use a random draw.")
    print("Pair in entrant order. Later odd stages give the last survivor a bye.")
    print("Each match starts fresh history; points reset for each match.")
    result = play_tournament(players, rounds, rng)
    show_tournament(result)
    show_strategy_summary()
    return result
