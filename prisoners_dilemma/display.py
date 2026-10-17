"""Readable console tables and observations from actual match results."""

from collections.abc import Iterable

from .models import Action, MatchResult, RoundResult, payoff
from .terminal import Color, pad, paint, panel, plain
from .tournament import TournamentResult


def show_title() -> None:
    print()
    panel("P R I S O N E R ' S   D I L E M M A  /  TP1")
    art = r"""
            ||   ||   ||   ||   ||   ||   ||
            ||  (o)   ||       ||   (o)  ||
            ||  /|\   ||  VS   ||   /|\  ||
            ||  / \   ||       ||   / \  ||
            ||   ||   ||   ||   ||   ||   ||
    """
    print(paint(art.rstrip(), Color.CYAN))
    print(paint("          TWO PRISONERS. TWO CHOICES. ONE DILEMMA.", Color.BOLD))
    print()


def show_menu() -> None:
    panel("[ SELECT YOUR GAME ]", (
        "[1] THE INTERROGATION   - Human vs human / one round",
        "[2] REPEAT OFFENDERS    - Human vs human / multiple rounds",
        "[3] HUMAN vs MACHINE   - Choose your computer opponent",
        "[4] MACHINE SHOWDOWN   - Two randomly assigned strategies",
        "[5] TOURNAMENT ARENA   - Elimination bracket + champion",
        "[0] EXIT",
    ))


def show_setup(exercise: int, rounds: int, seed: int) -> None:
    print()
    panel(f"[ EXERCISE {exercise} ]", (
        f"Rounds per match: {rounds} | Seed: {seed}",
        "Choose independently. Scores are revealed after both decisions.",
    ))


def action_label(action: Action) -> str:
    if action is Action.COOPERATE:
        return paint("[C] COOPERATE", Color.GREEN)
    return paint("[D] DEFECT", Color.RED)


def show_choices() -> None:
    print()
    print(paint("   [ C ] COOPERATE", Color.GREEN) + "       " + paint("[ D ] DEFECT", Color.RED))
    print("       Stay silent                 Betray partner")


def show_strategy_menu() -> None:
    panel("[ CHOOSE THE COMPUTER'S STRATEGY ]", (
        "[1] ALWAYS COOPERATE  - Plays C every round",
        "[2] ALWAYS DEFECT     - Plays D every round",
        "[3] RANDOM            - Chooses C or D each round",
        "[4] TIT-FOR-TAT       - Starts C, then copies your last move",
    ), Color.MAGENTA)


def print_table(headers: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> None:
    data = [headers, *rows]
    widths = [max(len(plain(row[i])) for row in data) for i in range(len(headers))]
    border = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(paint(border, Color.DIM))
    for index, row in enumerate(data):
        cells = [pad(cell, width) for cell, width in zip(row, widths)]
        line = "| " + " | ".join(cells) + " |"
        print(paint(line, Color.CYAN) if index == 0 else line)
        if index == 0:
            print(paint(border, Color.DIM))
    print(paint(border, Color.DIM))


def show_payoff_matrix() -> None:
    print(paint("\n[ THE DEAL ]", Color.CYAN))
    print("TP1 payoff matrix: (A points, B points); higher is better.")
    print("C = cooperate / stay silent; D = defect / betray.")
    print_table(
        ("A / B", "B: C", "B: D"),
        [
            (f"A: {action.value}", *(str(payoff(action, b)) for b in Action))
            for action in Action
        ],
    )
    show_choices()


def show_round(result: RoundResult) -> None:
    print(paint(f"\n--- [ Round {result.number} / DECISIONS REVEALED ] ---", Color.CYAN))
    print(f"  PLAYER A  {action_label(result.action_a)}")
    print(f"  PLAYER B  {action_label(result.action_b)}")
    print(paint(
        f"Round {result.number}: A={result.action_a.value}, B={result.action_b.value}"
        f" -> points ({result.score_a}, {result.score_b})", Color.BOLD
    ))
    if result.action_a is result.action_b is Action.COOPERATE:
        print(paint("[++] MUTUAL COOPERATION - Both kept the pact. +3 each.", Color.GREEN))
    elif result.action_a is result.action_b is Action.DEFECT:
        print(paint("[!!] MUTUAL DEFECTION - Both betrayed. +1 each.", Color.YELLOW))
    else:
        defector = "A" if result.action_a is Action.DEFECT else "B"
        print(paint(f"[X] BETRAYAL - Player {defector} takes +5; the other gets 0.", Color.RED))


def show_match(result: MatchResult) -> None:
    print()
    panel("[ MATCH SCOREBOARD ]")
    print(f"Player A: {result.player_a} | Strategy: {result.strategy_a}")
    print(f"Player B: {result.player_b} | Strategy: {result.strategy_b}")
    rows = []
    total_a = total_b = 0
    for round_ in result.rounds:
        total_a += round_.score_a
        total_b += round_.score_b
        rows.append((
            str(round_.number),
            paint(round_.action_a.value, Color.GREEN if round_.action_a is Action.COOPERATE else Color.RED),
            paint(round_.action_b.value, Color.GREEN if round_.action_b is Action.COOPERATE else Color.RED),
            str(round_.score_a), str(round_.score_b), str(total_a), str(total_b),
        ))
    print_table(("Round", "A", "B", "A points", "B points", "A total", "B total"), rows)
    print(f"Final score: {result.player_a} = {total_a}; {result.player_b} = {total_b}")
    maximum = 5 * len(result.rounds)
    for name, total in ((result.player_a, total_a), (result.player_b, total_b)):
        filled = round(20 * total / maximum) if maximum else 0
        bar = "#" * filled + "." * (20 - filled)
        print(f"  {name:<12} " + paint(f"[{bar}] {total}/{maximum} points", Color.CYAN))
    if total_a == total_b:
        print(paint("[=] Match result: draw.", Color.YELLOW))
    else:
        print(paint(f"[W] Match winner by total points: {result.player_a if total_a > total_b else result.player_b}", Color.GREEN))


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
    print()
    panel("[ RUN OBSERVATIONS ]")
    print("Observed summary (this run only):")
    print(f"Matches: {len(matches)}; total played rounds: {count}")
    print(f"Cooperative decisions: {cooperation_count}/{2 * count} ({cooperation_count / (2 * count):.1%})")
    print(f"Mutual cooperation: {mutual_c}; mutual defection: {mutual_d}")
    print(f"Combined points: {sum(r.score_a + r.score_b for r in rounds)}")
    print("These simulated results depend on opponents, rounds, random seed and bracket.")
    print("They do not prove that the winner's strategy is universally best.")


def show_tournament(result: TournamentResult) -> None:
    print()
    panel("[ TOURNAMENT ARENA ]", ("Win your match. Advance through the bracket. Claim the trophy.",), Color.MAGENTA)
    print("Tournament entrants (strategies stay fixed):")
    print_table(("Player", "Strategy"), result.entrants)
    for stage in sorted({match.stage for match in result.matches}):
        print()
        panel(f"=== Tournament stage {stage} ===", color=Color.MAGENTA)
        for match in result.matches:
            if match.stage == stage:
                print(paint(f"\n[ MATCH {match.number} ] {match.result.player_a} vs {match.result.player_b}", Color.BOLD))
                show_match(match.result)
                if match.tied:
                    print(paint(f"[?] Tie-break: seeded random draw; {match.winner} advances.", Color.YELLOW))
                else:
                    print(paint(f"[>] Advancing: {match.winner}", Color.GREEN))
        for bye in result.byes:
            if bye.stage == stage:
                print(paint(f"[>] Bye: {bye.player} advances without playing or earning points.", Color.YELLOW))
    print(paint(r"""
                       ___________
                      '._==_==_=_.'
                      .-\:      /-.
                     | (|:.     |) |
                      '-|:.     |-'
                        \::.    /
                         '::. .'
                           ) (
                         _.' '._
                        [_______]
    """.rstrip(), Color.YELLOW))
    panel(f"Tournament champion: {result.champion}", color=Color.YELLOW)
    show_observations(match.result for match in result.matches)


def show_strategy_summary() -> None:
    print()
    panel("[ STRATEGY DEBRIEF ]")
    print("Strategy interpretation:")
    print("One round: D earns 5 rather than 3 against C, and 1 rather than 0 against D.")
    print("So D strictly dominates C; (D,D) is the unique one-shot Nash equilibrium.")
    print("Both cooperating earns (3,3), better for both than mutual defection (1,1).")
    print("Always cooperate can be exploited; always defect gives up mutual cooperation.")
    print("Random ignores history; Tit-for-tat starts C and copies the last opposing move.")
    print("Tit-for-tat responds to both defection and a later return to cooperation.")
    print("Repeated play permits responses, but cooperation and convergence are not guaranteed.")
