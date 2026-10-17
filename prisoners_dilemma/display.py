"""Readable console tables and observations from actual match results."""

from collections.abc import Iterable

from .models import Action, MatchResult, RoundResult, payoff
from .tournament import TournamentResult


def print_table(headers: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> None:
    data = [headers, *rows]
    widths = [max(len(row[i]) for row in data) for i in range(len(headers))]
    for index, row in enumerate(data):
        print(" | ".join(cell.ljust(width) for cell, width in zip(row, widths)))
        if index == 0:
            print("-+-".join("-" * width for width in widths))


def show_payoff_matrix() -> None:
    print("\nTP1 payoff matrix: (A points, B points); higher is better.")
    print("C = cooperate / stay silent; D = defect / betray.")
    print_table(
        ("A / B", "B: C", "B: D"),
        [
            (f"A: {action.value}", *(str(payoff(action, b)) for b in Action))
            for action in Action
        ],
    )


def show_round(result: RoundResult) -> None:
    print(
        f"Round {result.number}: A={result.action_a.value}, B={result.action_b.value}"
        f" -> points ({result.score_a}, {result.score_b})"
    )


def show_match(result: MatchResult) -> None:
    print(f"\nPlayer A: {result.player_a} | Strategy: {result.strategy_a}")
    print(f"Player B: {result.player_b} | Strategy: {result.strategy_b}")
    rows = []
    total_a = total_b = 0
    for round_ in result.rounds:
        total_a += round_.score_a
        total_b += round_.score_b
        rows.append(
            tuple(
                str(value)
                for value in (
                    round_.number, round_.action_a.value, round_.action_b.value,
                    round_.score_a, round_.score_b, total_a, total_b,
                )
            )
        )
    print_table(("Round", "A", "B", "A points", "B points", "A total", "B total"), rows)
    print(f"Final score: {result.player_a} = {total_a}; {result.player_b} = {total_b}")
    if total_a == total_b:
        print("Match result: draw.")
    else:
        print(f"Match winner by total points: {result.player_a if total_a > total_b else result.player_b}")


def show_observations(results: Iterable[MatchResult]) -> None:
    matches = tuple(results)
    rounds = [round_ for match in matches for round_ in match.rounds]
    count = len(rounds)
    if not count:
        return
    cooperation_count = sum(
        (round_.action_a is Action.COOPERATE) + (round_.action_b is Action.COOPERATE)
        for round_ in rounds
    )
    mutual_c = sum(r.action_a is r.action_b is Action.COOPERATE for r in rounds)
    mutual_d = sum(r.action_a is r.action_b is Action.DEFECT for r in rounds)
    print("\nObserved summary (this run only):")
    print(f"Matches: {len(matches)}; total played rounds: {count}")
    print(f"Cooperative decisions: {cooperation_count}/{2 * count} ({cooperation_count / (2 * count):.1%})")
    print(f"Mutual cooperation: {mutual_c}; mutual defection: {mutual_d}")
    print(f"Combined points: {sum(r.score_a + r.score_b for r in rounds)}")
    print("These simulated results depend on opponents, rounds, random seed and bracket.")
    print("They do not prove that the winner's strategy is universally best.")


def show_tournament(result: TournamentResult) -> None:
    print("\nTournament entrants (strategies stay fixed):")
    print_table(("Player", "Strategy"), result.entrants)
    for stage in sorted({match.stage for match in result.matches}):
        print(f"\n=== Tournament stage {stage} ===")
        for match in result.matches:
            if match.stage == stage:
                print(f"\nMatch {match.number}")
                show_match(match.result)
                if match.tied:
                    print(f"Tie-break: seeded random draw; {match.winner} advances.")
                else:
                    print(f"Advancing: {match.winner}")
        for bye in result.byes:
            if bye.stage == stage:
                print(f"Bye: {bye.player} advances without playing or earning points.")
    print(f"\nTournament champion: {result.champion}")
    show_observations(match.result for match in result.matches)


def show_strategy_summary() -> None:
    print("\nStrategy interpretation:")
    print("One round: D earns 5 rather than 3 against C, and 1 rather than 0 against D.")
    print("So D strictly dominates C; (D,D) is the unique one-shot Nash equilibrium.")
    print("Both cooperating earns (3,3), better for both than mutual defection (1,1).")
    print("Always cooperate can be exploited; always defect gives up mutual cooperation.")
    print("Random ignores history; Tit-for-tat starts C and copies the last opposing move.")
    print("Tit-for-tat responds to both defection and a later return to cooperation.")
    print("Repeated play permits responses, but cooperation and convergence are not guaranteed.")
