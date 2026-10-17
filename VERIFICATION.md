# TP1 verification record

Verification date: **2026-10-17** (Asia/Bangkok).

## Current console refresh verification

At the user's request, the console now has ASCII artwork/panels, optional ANSI
colors, round reveals, point bars, a tournament trophy and clearer hidden-input
instructions/confirmation. The mathematical model, strategies, bracket rules
and input sequence are unchanged. Existing examples below are retained as the
initial implementation record; refreshed captures are stored separately.

**Verified computational result:** **38 tests passed** on Python 3.12.14 using
the same `python -B -m unittest discover -s tests -v` command. The
[current test output](examples/console-refresh/test-results.txt) includes the
original checks plus color/plain layout equivalence and action-independent
feedback before revealing a round. Redirected output contains no ANSI escapes.

All five configurations in the table below were rerun twice. Each exited 0,
reproduced identical output, and retained its original scores/champion:
[exercise 1](examples/console-refresh/exercise1_seed42.txt),
[exercise 2](examples/console-refresh/exercise2_seed42.txt),
[exercise 3](examples/console-refresh/exercise3_seed42.txt),
[exercise 4](examples/console-refresh/exercise4_seed42.txt), and
[exercise 5](examples/console-refresh/exercise5_seed42.txt).
The [current code manifest](examples/console-refresh/code-sha256.json) identifies
all 13 Python files. The [forced-color capture](examples/console-refresh/exercise4_color.ansi.txt)
has identical text and table alignment after stripping ANSI color codes.

Physical terminal colors and input echo remain environment-dependent; they have
not been manually verified on the user's terminal. Console output was also
rendered to an image for visual review; that is a rendering of captured text,
not a screenshot proving physical terminal behavior.

Final scope checks passed: all 3 original PDFs, root instructions, Git metadata,
the scoring model, engine, strategy rules and tournament logic retain their
pre-refresh hashes. No existing file was deleted. Changes are limited to the
project and its assignment/troubleshooting records. All 186 relative Markdown
links resolve, and all 13 Python files parse and match the current manifest.

## Initial implementation - reproducible run configuration

All commands below run from this project directory, with Python 3.12.14 on
Windows and the standard library only. The interpreter used for verification is:

```text
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

The shorter `python` command in the README means any compatible Python 3.10+
interpreter; that exact system command has not been assumed available.

Before the recorded demonstrations, the configured model is: TP1 point matrix,
both current decisions private until committed, previous-round feedback, fixed
round horizon, no discounting, total points per match, no strategy learning.
Tournament pairing, tie, bye and history rules are the documented README
assumptions. Computer strategies are sampled uniformly once at creation; Random
actions sample C/D uniformly. Seed **42** is used for all captured examples.
Metrics are round actions/points, cumulative scores, tournament advancement,
cooperation frequency, mutual cooperation/defection counts and combined points.

| Capture | CLI arguments | Standard input, one line per choice |
| --- | --- | --- |
| Exercise 1 | `--exercise 1 --seed 42` | C, D |
| Exercise 2 | `--exercise 2 --rounds 3 --seed 42` | C, C, C, D, D, D |
| Exercise 3 | `--exercise 3 --rounds 3 --strategy 4 --seed 42` | D, C, D |
| Exercise 4 | `--exercise 4 --rounds 5 --seed 42` | None |
| Exercise 5 | `--exercise 5 --players 6 --rounds 3 --seed 42` | None |

## Initial implementation - executed results

**Verified computational result:** all **36 tests passed**, using:

```powershell
python -B -m unittest discover -s tests -v
```

The [test output](examples/test-results.txt) records the checks actually run.
Tests cover every source payoff cell, input retries/rejections, all four
strategies, Tit-for-tat's initial and previous-round actions, history reset,
both players' information boundaries, observed summary arithmetic, reproducible
random behavior, tournament fields of 2, 4, 6, 8, 10 and 14 players, winner-only
advancement, ties, byes, invalid options, cancellation, and all five CLI exercises.

The five configured demonstration processes each exited successfully. Each was
also rerun with identical inputs and seed, producing identical standard output:

| Captured output | Actual result |
| --- | --- |
| [Exercise 1](examples/exercise1_seed42.txt) | Human A 0, Human B 5. |
| [Exercise 2](examples/exercise2_seed42.txt) | Human A 4, Human B 9. |
| [Exercise 3](examples/exercise3_seed42.txt) | Human A 10, Tit-for-tat computer B 5. |
| [Exercise 4](examples/exercise4_seed42.txt) | A Always cooperate: 6; B Random: 21. Cooperative actions 7/10; mutual C/C 2; mutual D/D 0; combined points 27. |
| [Exercise 5](examples/exercise5_seed42.txt) | 6 entrants; 5 matches and 15 played rounds; Computer 3 (Always defect) champion after a 3-3 final and recorded random tie-break. Computer 6 received a stage-2 bye. Cooperative actions 12/30; mutual C/C 2; mutual D/D 5; combined points 62. |

The first three scores also match the independent arithmetic in
[SUMMARY](SUMMARY.md). The seeded computer runs are reproducible examples, not a
statistical comparison across seeds. [SHA-256 manifest](examples/code-sha256.json)
identifies the Python source and test files used for the captures. No code or
test changes should be described as covered by these captures unless rerun.

Final source/scope checks also passed: all 3 original PDFs and root AGENTS.md
retained their SHA-256 hashes; no existing files were deleted; all new files are
inside this project; existing modifications are limited to 10 affected course
Markdown records. All 175 relative links across 27 Markdown files resolve within
the workspace, and all 12 Python files parse and match the captured code manifest.

## Evidence boundary

Scripted human choices are supplied by a test/demonstration harness. They are not
real human observations. Computer examples are simulations for specified rules
and seeds, with no empirical or general optimality claim. Unit tests verify the
hidden-input path with mocks; physical terminal echo behavior has not been
manually verified. No classroom play, student mastery, submission, instructor
approval, benchmark, or repeated-game equilibrium solution is claimed.
