"""Human and computer players share the same small decision interface."""

from dataclasses import dataclass
from getpass import GetPassWarning, getpass
from random import Random
import sys
from typing import Protocol
import warnings

from .models import Action
from .strategies import Strategy, choose_action
from .terminal import Color, notice, paint


class Player(Protocol):
    name: str

    @property
    def strategy_name(self) -> str: ...

    def choose_action(self, opponent_history: tuple[Action, ...]) -> Action: ...


@dataclass
class HumanPlayer:
    name: str

    @property
    def strategy_name(self) -> str:
        return "Human decisions"

    def choose_action(self, opponent_history: tuple[Action, ...]) -> Action:
        print(paint(f"\n[ YOUR TURN: {self.name} / Round {len(opponent_history) + 1} ]", Color.CYAN))
        print(paint("[C] Cooperate / stay silent", Color.GREEN) + "    " + paint("[D] Defect / betray", Color.RED))
        if sys.stdin.isatty():
            print("Type C or D, then press ENTER. Nothing appears while you type.")
        else:
            print("Scripted input: enter C or D, then press ENTER.")
        while True:
            prompt = f"{self.name}, choose C or D (hidden): "
            if sys.stdin.isatty():
                # Fail explicitly if the terminal cannot keep the choice private.
                with warnings.catch_warnings():
                    warnings.simplefilter("error", GetPassWarning)
                    try:
                        text = getpass(paint(prompt, Color.CYAN))
                    except GetPassWarning:
                        raise ValueError(
                            "Hidden input is unavailable. Use a terminal that "
                            "supports hidden input for human play."
                        ) from None
            else:
                # Piped input supports reproducible demonstrations and tests.
                text = input(paint(f"[>] {self.name}, choose C or D: ", Color.CYAN))
            try:
                action = Action.parse(text)
            except ValueError as error:
                notice(str(error), Color.RED)
            else:
                print(paint("[OK] Decision locked. Waiting for the round reveal.", Color.GREEN))
                return action


@dataclass
class ComputerPlayer:
    name: str
    strategy: Strategy
    rng: Random

    @property
    def strategy_name(self) -> str:
        return self.strategy.value

    def choose_action(self, opponent_history: tuple[Action, ...]) -> Action:
        return choose_action(self.strategy, opponent_history, self.rng)


def random_computer(name: str, rng: Random) -> ComputerPlayer:
    """Select a policy once; give its action draws a separate random stream."""
    strategy = rng.choice(tuple(Strategy))
    return ComputerPlayer(name, strategy, Random(rng.getrandbits(64)))
