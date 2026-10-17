"""Single-elimination tournament for an even number of computer entrants."""

from collections.abc import Sequence
from dataclasses import dataclass
from random import Random

from .engine import play_match
from .models import MatchResult, require_positive_integer
from .players import ComputerPlayer


@dataclass(frozen=True)
class TournamentMatch:
    stage: int
    number: int
    result: MatchResult
    winner: str
    tied: bool


@dataclass(frozen=True)
class Bye:
    stage: int
    player: str


@dataclass(frozen=True)
class TournamentResult:
    entrants: tuple[tuple[str, str], ...]
    matches: tuple[TournamentMatch, ...]
    byes: tuple[Bye, ...]
    champion: str


def play_tournament(
    players: Sequence[ComputerPlayer], rounds: int, rng: Random
) -> TournamentResult:
    """Pair in list order; later odd stages give the last survivor a bye."""
    require_positive_integer(rounds, "Rounds per match")
    if len(players) < 2 or len(players) % 2:
        raise ValueError("Tournament needs an even number of players, at least 2.")
    names = [player.name for player in players]
    if any(not name.strip() for name in names) or len(set(names)) != len(names):
        raise ValueError("Tournament player names must be nonempty and unique.")

    entrants = tuple((player.name, player.strategy_name) for player in players)
    remaining = list(players)
    matches: list[TournamentMatch] = []
    byes: list[Bye] = []
    stage = 1
    while len(remaining) > 1:
        winners: list[ComputerPlayer] = []
        for index in range(0, len(remaining) - 1, 2):
            player_a, player_b = remaining[index : index + 2]
            # Every match creates fresh histories, including for Tit-for-Tat.
            result = play_match(player_a, player_b, rounds)
            total_a, total_b = result.totals
            tied = total_a == total_b
            if tied:
                winner = rng.choice((player_a, player_b))
            else:
                winner = player_a if total_a > total_b else player_b
            winners.append(winner)
            matches.append(
                TournamentMatch(stage, index // 2 + 1, result, winner.name, tied)
            )
        if len(remaining) % 2:
            bye_player = remaining[-1]
            winners.append(bye_player)
            byes.append(Bye(stage, bye_player.name))
        remaining = winners
        stage += 1
    return TournamentResult(entrants, tuple(matches), tuple(byes), remaining[0].name)
