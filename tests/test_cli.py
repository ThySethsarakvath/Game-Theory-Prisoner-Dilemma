"""Exercise-level checks through the actual entry point, with scripted input."""

from pathlib import Path
import re
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]


def run_cli(*args, input_text=""):
    return subprocess.run(
        [sys.executable, "-B", str(PROJECT / "main.py"), *args],
        cwd=PROJECT, input=input_text, capture_output=True, text=True, timeout=15,
    )


class CliTests(unittest.TestCase):
    def test_exercise_1_scores_and_table(self):
        result = run_cli("--exercise", "1", "--seed", "42", input_text="C\nD\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Human A = 0; Human B = 5", result.stdout)
        self.assertIn("A points", result.stdout)

    def test_exercise_2_cumulative_totals(self):
        result = run_cli("--exercise", "2", "--rounds", "3", input_text="C\nC\nC\nD\nD\nD\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Human A = 4; Human B = 9", result.stdout)
        self.assertIn("Round 3", result.stdout)

    def test_exercise_3_all_four_strategies(self):
        for number in range(1, 5):
            with self.subTest(number=number):
                result = run_cli("--exercise", "3", "--rounds", "3", "--strategy", str(number), "--seed", "42", input_text="D\nC\nD\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Final score:", result.stdout)
                if number == 4:
                    self.assertIn("Human A = 10; Computer B = 5", result.stdout)

    def test_exercise_4_is_reproducible(self):
        args = ("--exercise", "4", "--rounds", "5", "--seed", "42")
        first, second = run_cli(*args), run_cli(*args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertIn("Observed summary", first.stdout)
        self.assertNotIn("\x1b", first.stdout)

    def test_color_changes_neither_visible_layout_nor_scores(self):
        args = ("--exercise", "4", "--rounds", "3", "--seed", "42")
        colored = run_cli(*args, "--color", "always")
        plain = run_cli(*args, "--no-color")
        self.assertEqual(colored.returncode, 0, colored.stderr)
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertIn("\x1b[", colored.stdout)
        self.assertNotIn("\x1b", plain.stdout)
        self.assertEqual(re.sub(r"\x1b\[[0-9;]*m", "", colored.stdout), plain.stdout)

    def test_exercise_5_finishes_six_player_tournament(self):
        result = run_cli("--exercise", "5", "--players", "6", "--rounds", "3", "--seed", "42")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Tournament champion:", result.stdout)
        self.assertIn("Bye:", result.stdout)
        self.assertIn("Matches: 5; total played rounds: 15", result.stdout)
        self.assertIn("Strategy interpretation:", result.stdout)

    def test_menu_and_round_validation_recover_from_bad_input(self):
        result = run_cli("--seed", "42", input_text="x\n9\n2\n0\n2\nC\nD\nD\nC\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Enter a whole number", result.stdout)
        self.assertIn("Human A = 5; Human B = 5", result.stdout)

    def test_tournament_prompt_recovers_from_odd_count(self):
        result = run_cli("--exercise", "5", "--rounds", "1", "--seed", "42", input_text="3\n2\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Enter an even number", result.stdout)
        self.assertIn("Tournament champion:", result.stdout)

    def test_exit_without_starting_game(self):
        result = run_cli(input_text="0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Final score", result.stdout)

    def test_eof_cancels_without_fabricating_result(self):
        result = run_cli("--exercise", "1", input_text="C\n")
        self.assertEqual(result.returncode, 130)
        self.assertIn("cancelled before completion", result.stdout)
        self.assertNotIn("Final score:", result.stdout)

    def test_invalid_options_fail_cleanly(self):
        cases = [
            ("--exercise", "2", "--rounds", "0"),
            ("--exercise", "5", "--players", "3"),
            ("--exercise", "1", "--rounds", "2"),
            ("--exercise", "4", "--strategy", "1"),
            ("--exercise", "4", "--players", "4"),
        ]
        for args in cases:
            with self.subTest(args=args):
                result = run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
