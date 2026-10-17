"""Behavior checks against hand-calculated TP1 outcomes."""

from contextlib import redirect_stdout
from io import StringIO
from random import Random
import unittest
from unittest.mock import patch

from prisoners_dilemma.display import show_observations
from prisoners_dilemma.engine import play_match
from prisoners_dilemma.models import Action, payoff
from prisoners_dilemma.players import ComputerPlayer, HumanPlayer, random_computer
from prisoners_dilemma.strategies import Strategy, choose_action
from prisoners_dilemma.tournament import play_tournament


C = Action.COOPERATE
D = Action.DEFECT


class ScriptedPlayer:
    strategy_name = "Test sequence"

    def __init__(self, name, actions):
        self.name = name
        self.actions = actions
        self.seen_histories = []

    def choose_action(self, opponent_history):
        self.seen_histories.append(opponent_history)
        return self.actions[len(self.seen_histories) - 1]


def computer(name, strategy):
    return ComputerPlayer(name, strategy, Random(7))


class PayoffTests(unittest.TestCase):
    def test_all_four_source_cells_and_coordinate_order(self):
        for a, b, expected in [(C, C, (3, 3)), (C, D, (0, 5)), (D, C, (5, 0)), (D, D, (1, 1))]:
            with self.subTest(a=a, b=b):
                self.assertEqual(payoff(a, b), expected)

    def test_invalid_actions_cannot_be_scored(self):
        with self.assertRaises(ValueError):
            payoff("C", D)

    def test_parse_accepts_case_and_whitespace(self):
        self.assertIs(Action.parse(" c "), C)
        self.assertIs(Action.parse("d"), D)

    def test_parse_rejects_other_decisions(self):
        for value in ["", "cooperate", "X", "CD"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                Action.parse(value)


class StrategyTests(unittest.TestCase):
    def test_constant_strategies_ignore_history(self):
        for history in [(), (C,), (D,), (C, D, C)]:
            self.assertIs(choose_action(Strategy.ALWAYS_COOPERATE, history, Random(1)), C)
            self.assertIs(choose_action(Strategy.ALWAYS_DEFECT, history, Random(1)), D)

    def test_tit_for_tat_starts_cooperating_and_copies_last_action(self):
        for history, expected in [((), C), ((C,), C), ((D,), D), ((D, C), C), ((C, D), D)]:
            with self.subTest(history=history):
                self.assertIs(choose_action(Strategy.TIT_FOR_TAT, history, Random(1)), expected)

    def test_random_actions_are_valid_and_reproducible(self):
        first, second = Random(123), Random(123)
        actions = [choose_action(Strategy.RANDOM, (), first) for _ in range(40)]
        self.assertEqual(actions, [choose_action(Strategy.RANDOM, (), second) for _ in range(40)])
        self.assertEqual(set(actions), {C, D})

    def test_random_strategy_selection_is_reproducible_and_fixed(self):
        first, second = Random(42), Random(42)
        for number in range(10):
            a = random_computer(str(number), first)
            b = random_computer(str(number), second)
            original = a.strategy
            self.assertEqual(a.strategy, b.strategy)
            self.assertEqual([a.choose_action(()) for _ in range(8)], [b.choose_action(()) for _ in range(8)])
            self.assertIs(a.strategy, original)

    def test_unsupported_strategy_fails(self):
        with self.assertRaises(ValueError):
            choose_action("Unknown", (), Random(1))


class MatchTests(unittest.TestCase):
    def test_mutual_cooperation_totals(self):
        result = play_match(computer("A", Strategy.ALWAYS_COOPERATE), computer("B", Strategy.ALWAYS_COOPERATE), 3)
        self.assertEqual(result.totals, (9, 9))
        self.assertEqual(len(result.rounds), 3)

    def test_defection_exploits_cooperation(self):
        result = play_match(computer("A", Strategy.ALWAYS_DEFECT), computer("B", Strategy.ALWAYS_COOPERATE), 3)
        self.assertEqual(result.totals, (15, 0))

    def test_tit_for_tat_responds_from_second_round(self):
        result = play_match(computer("A", Strategy.TIT_FOR_TAT), computer("B", Strategy.ALWAYS_DEFECT), 3)
        self.assertEqual([r.action_a for r in result.rounds], [C, D, D])
        self.assertEqual(result.totals, (2, 7))

    def test_no_player_receives_current_opponent_action(self):
        a = ScriptedPlayer("A", [D, C, D])
        b = ScriptedPlayer("B", [C, D, C])
        revealed = []
        result = play_match(a, b, 3, revealed.append)
        self.assertEqual(a.seen_histories, [(), (C,), (C, D)])
        self.assertEqual(b.seen_histories, [(), (D,), (D, C)])
        self.assertEqual(tuple(revealed), result.rounds)
        self.assertEqual(result.totals, (10, 5))

    def test_reused_tit_for_tat_starts_new_match_with_empty_history(self):
        player = computer("A", Strategy.TIT_FOR_TAT)
        play_match(player, computer("B", Strategy.ALWAYS_DEFECT), 2)
        result = play_match(player, computer("C", Strategy.ALWAYS_COOPERATE), 1)
        self.assertIs(result.rounds[0].action_a, C)
        self.assertEqual(result.totals, (3, 3))

    def test_invalid_round_counts_fail(self):
        for count in [0, -1, 1.5, True]:
            with self.subTest(count=count), self.assertRaises(ValueError):
                play_match(computer("A", Strategy.ALWAYS_COOPERATE), computer("B", Strategy.ALWAYS_DEFECT), count)


class HumanInputTests(unittest.TestCase):
    @patch("prisoners_dilemma.players.sys.stdin.isatty", return_value=False)
    @patch("builtins.input", side_effect=["wrong", " d "])
    def test_bad_action_is_retried(self, read, isatty):
        with redirect_stdout(StringIO()) as output:
            self.assertIs(HumanPlayer("A").choose_action(()), D)
        self.assertEqual(read.call_count, 2)
        self.assertIn("Enter C", output.getvalue())

    @patch("prisoners_dilemma.players.sys.stdin.isatty", return_value=True)
    @patch("prisoners_dilemma.players.getpass", return_value="C")
    @patch("builtins.input")
    def test_interactive_human_choice_uses_hidden_input(self, read, hidden, isatty):
        self.assertIs(HumanPlayer("A").choose_action(()), C)
        hidden.assert_called_once()
        read.assert_not_called()

    @patch("prisoners_dilemma.players.sys.stdin.isatty", return_value=True)
    @patch("prisoners_dilemma.players.getpass")
    def test_unsupported_hidden_input_fails_without_visible_retry(self, hidden, isatty):
        from getpass import GetPassWarning
        hidden.side_effect = GetPassWarning("Cannot hide input")
        with self.assertRaisesRegex(ValueError, "Hidden input"):
            HumanPlayer("A").choose_action(())


class TournamentTests(unittest.TestCase):
    def test_even_fields_finish_and_only_winners_advance(self):
        for count in [2, 4, 6, 8, 10, 14]:
            with self.subTest(count=count):
                players = [computer(f"P{i}", Strategy.ALWAYS_DEFECT) for i in range(count)]
                result = play_tournament(players, 2, Random(5))
                self.assertEqual(len(result.matches), count - 1)
                self.assertIn(result.champion, [p.name for p in players])
                remaining = {p.name for p in players}
                for stage in sorted({m.stage for m in result.matches}):
                    participants = []
                    next_stage = set()
                    for match in result.matches:
                        if match.stage == stage:
                            a, b = match.result.player_a, match.result.player_b
                            self.assertIn(a, remaining)
                            self.assertIn(b, remaining)
                            participants.extend((a, b))
                            next_stage.add(match.winner)
                            self.assertTrue(match.tied)
                            self.assertEqual(match.result.totals, (2, 2))
                    for bye in result.byes:
                        if bye.stage == stage:
                            participants.append(bye.player)
                            next_stage.add(bye.player)
                    self.assertCountEqual(participants, remaining)
                    remaining = next_stage
                self.assertEqual(remaining, {result.champion})

    def test_six_entrants_receive_one_later_bye(self):
        players = [computer(f"P{i}", Strategy.ALWAYS_COOPERATE) for i in range(6)]
        result = play_tournament(players, 1, Random(1))
        self.assertEqual(len(result.byes), 1)
        self.assertEqual(result.byes[0].stage, 2)

    def test_higher_score_advances_without_tiebreak(self):
        players = [computer("C", Strategy.ALWAYS_COOPERATE), computer("D", Strategy.ALWAYS_DEFECT)]
        result = play_tournament(players, 4, Random(0))
        self.assertEqual(result.champion, "D")
        self.assertFalse(result.matches[0].tied)
        self.assertEqual(result.matches[0].result.totals, (0, 20))

    def test_seed_reproduces_whole_tournament(self):
        def run():
            rng = Random(43)
            players = [random_computer(str(i), rng) for i in range(6)]
            return play_tournament(players, 7, rng)
        self.assertEqual(run(), run())

    def test_invalid_fields_fail(self):
        for count in [0, 1, 3, 5]:
            with self.subTest(count=count), self.assertRaises(ValueError):
                play_tournament([computer(str(i), Strategy.RANDOM) for i in range(count)], 1, Random(0))

    def test_duplicate_or_blank_names_fail(self):
        for names in [("A", "A"), ("", "B"), (" ", "B")]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                play_tournament([computer(name, Strategy.RANDOM) for name in names], 1, Random(0))

    def test_invalid_match_rounds_fail(self):
        with self.assertRaises(ValueError):
            play_tournament([computer("A", Strategy.RANDOM), computer("B", Strategy.RANDOM)], 0, Random(0))


class ObservationTests(unittest.TestCase):
    def test_summary_uses_observed_actions_and_points(self):
        result = play_match(ScriptedPlayer("A", [C, D, D]), ScriptedPlayer("B", [C, C, D]), 3)
        with redirect_stdout(StringIO()) as output:
            show_observations([result])
        self.assertIn("Cooperative decisions: 3/6 (50.0%)", output.getvalue())
        self.assertIn("Mutual cooperation: 1; mutual defection: 1", output.getvalue())
        self.assertIn("Combined points: 13", output.getvalue())


if __name__ == "__main__":
    unittest.main()
