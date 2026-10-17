"""Interactive menu and reproducible command-line options."""

import argparse
from random import Random, SystemRandom

from .display import show_payoff_matrix
from .exercises import exercise_1, exercise_2, exercise_3, exercise_4, exercise_5
from .strategies import Strategy


def read_integer(prompt: str, minimum: int = 1, even: bool = False, maximum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Enter a whole number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            print(f"Enter a number from {minimum} to {maximum}." if maximum is not None else f"Enter a number of at least {minimum}.")
        elif even and value % 2:
            print("Enter an even number of players.")
        else:
            return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TP1: Prisoner's Dilemma, exercises 1-5.")
    parser.add_argument("--exercise", type=int, choices=range(1, 6), help="Omit to open the menu.")
    parser.add_argument("--rounds", type=int, help="Rounds per match (exercise 1 always uses 1).")
    parser.add_argument("--players", type=int, help="Even tournament entrant count, at least 2 (exercise 5).")
    parser.add_argument("--strategy", type=int, choices=range(1, 5), help="Exercise 3: 1 cooperate, 2 defect, 3 random, 4 tit-for-tat.")
    parser.add_argument("--seed", type=int, help="Reproduce computer choices and tournament tie-breaks.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.rounds is not None and args.rounds < 1:
        parser.error("--rounds must be positive.")
    if args.players is not None and (args.players < 2 or args.players % 2):
        parser.error("--players must be even and at least 2.")
    try:
        exercise = args.exercise
        if exercise is None:
            print("\nPrisoner's Dilemma - TP1")
            print("1. One round: human vs human")
            print("2. Multiple rounds: human vs human")
            print("3. Human vs computer")
            print("4. Computer vs computer (randomly selected strategies)")
            print("5. Computer elimination tournament and strategy summary")
            print("0. Exit")
            exercise = read_integer("Choose exercise: ", minimum=0, maximum=5)
            if exercise == 0:
                return 0
        if exercise == 1 and args.rounds not in (None, 1):
            parser.error("Exercise 1 has exactly one round; use exercise 2 for more.")
        if args.players is not None and exercise != 5:
            parser.error("--players applies only to exercise 5.")
        if args.strategy is not None and exercise != 3:
            parser.error("--strategy applies only to exercise 3.")

        rounds = 1 if exercise == 1 else args.rounds
        if rounds is None:
            rounds = read_integer("Rounds per match: ")
        seed = args.seed if args.seed is not None else SystemRandom().getrandbits(64)
        rng = Random(seed)
        print(f"\nExercise {exercise} | Rounds per match: {rounds} | Seed: {seed}")
        show_payoff_matrix()
        if exercise == 1:
            exercise_1()
        elif exercise == 2:
            exercise_2(rounds)
        elif exercise == 3:
            strategy_number = args.strategy
            if strategy_number is None:
                for number, strategy in enumerate(Strategy, 1):
                    print(f"{number}. {strategy.value}")
                strategy_number = read_integer("Computer strategy: ", maximum=4)
            exercise_3(rounds, tuple(Strategy)[strategy_number - 1], rng)
        elif exercise == 4:
            exercise_4(rounds, rng)
        else:
            player_count = args.players
            if player_count is None:
                player_count = read_integer("Number of computer players (even): ", minimum=2, even=True)
            exercise_5(rounds, player_count, rng)
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nGame cancelled before completion.")
        return 130
    except ValueError as error:
        print(f"Cannot run game: {error}")
        return 1
