# TP1 - Prisoner's Dilemma

A small Python console program implementing **all five exercises** from
[TP1, pp.1-2](../Attachments/TP1.pdf), with context from
[Week 1, pp.18-21](../Attachments/Week%201_Introduction%20to%20Game%20Theory.pdf).
No third-party packages or installation step are needed. Requires Python 3.10+;
verification uses Python 3.12.14.

## Run the program

Open PowerShell and run:

```powershell
cd 'D:\I4-SE\Game Theories\tp1_prisoners_dilemma'
python main.py
```

Choose an exercise from the menu, then answer its prompts. Enter `C` to cooperate
or `D` to defect. Lowercase and surrounding spaces are accepted. Invalid actions,
round counts, and player counts are requested again. Ctrl+C or end of input
cancels play without announcing a completed match.

On an interactive terminal, human actions are hidden while typed: **press Enter
after C or D even though nothing appears**. Both players commit before a result
is revealed. All previous completed rounds are public. Use a normal terminal
supporting hidden input for human play; unsupported hidden input ends play with
an explanation. Redirected input is available for scripted demonstrations/tests,
where the caller is responsible for supplying the choices independently.

## Console appearance

The game uses ASCII prison artwork, framed menus and scoreboards, round reveal
messages, point bars and a tournament trophy. Green labels identify cooperation,
red labels identify defection, cyan identifies prompts/tables, and yellow marks
draws, tie-breaks and the champion. All meanings also appear as text, so color
is optional. Score bars show points out of the per-player ceiling `5 * rounds`;
they are not win probabilities.

Human turns explain that typing is hidden and confirm **Decision locked** without
revealing which choice was entered. Press Enter after C or D. Exercise 4 reveals
each round as it runs; the tournament prints each complete match and advancement.

Colors are detected automatically for interactive terminals. Windows consoles
are asked to enable ANSI processing; unsupported consoles and redirected output
use plain text. No external terminal package is required.

```powershell
python main.py --color always   # Force ANSI colors if auto detection misses support
python main.py --no-color       # Plain ASCII presentation
```

`--color never` also disables colors. In auto mode, the `NO_COLOR` environment
variable (even empty) and `TERM=dumb` disable ANSI output. There are no artificial
delays, screen clearing or extra keypresses between rounds, so scripted input
and saved results keep working. An explicit `--color always` overrides auto
detection and may show raw ANSI codes on unsupported displays.

| Exercise | What it does | Example command |
| --- | --- | --- |
| 1 | Two humans, exactly one round; decisions and final scores. | `python main.py --exercise 1` |
| 2 | Two humans for a chosen number of rounds; round and cumulative scores. | `python main.py --exercise 2 --rounds 3` |
| 3 | Human A against computer B using a selected strategy. | `python main.py --exercise 3 --rounds 5 --strategy 4 --seed 42` |
| 4 | Two computers, each randomly assigned one of the four strategies. | `python main.py --exercise 4 --rounds 5 --seed 42` |
| 5 | Computer elimination tournament; entrants, strategies, all decisions/scores, bracket advancement, champion, observations and summary. | `python main.py --exercise 5 --players 6 --rounds 3 --seed 42` |

Exercise 3's strategy numbers are `1` Always cooperate, `2` Always defect,
`3` Random, `4` Tit-for-tat. Omit arguments to enter values interactively.
`python main.py --help` lists the options. A seed is generated and printed if
omitted. Reuse the seed, options, human choices, code and Python version to
reproduce a run. The menu runs one selected exercise; launch again to choose another.

## Game model and source distinction

**Official requirement:** TP1 p.1 supplies this points matrix. A is the row player;
B is the column player; each pair is `(A points, B points)`. Both maximize points.

| A / B | Cooperate (C) | Defect (D) |
| --- | --- | --- |
| Cooperate (C) | (3, 3) | (0, 5) |
| Defect (D) | (5, 0) | (1, 1) |

There are two players per match with action sets `{C,D}`. Each round has
simultaneous decisions: neither decision method receives the other player's
current action. Decisions are collected sequentially on the computer but are
revealed only after both are committed. The rules, payoff table and completed
rounds are public; there is no communication or binding agreement implemented.
This is a symmetric, non-zero-sum game. Points accumulate without discounting.
The strategies are fixed rules, not learning agents or optimizing solvers.
The one-shot interpretation assumes rational utility maximizers who know the
game; computer simulations simply execute their chosen rules.

**Lecture context:** Week 1 p.19 supplies simultaneous C/D decisions; p.20 uses
negative prison-sentence utilities `(-1,-1)`, `(-10,0)`, `(0,-10)`, `(-5,-5)`.
TP1 deliberately supplies different numerical payoffs, so its positive points
are used throughout this program. Neither PDF is modified.

## Strategies and implementation assumptions

The four strategy definitions are **official requirements**, TP1 p.2:

| Strategy | Decision rule |
| --- | --- |
| Always cooperate | C every round. |
| Always defect | D every round. |
| Random | Randomly choose C or D each round. |
| Tit-for-tat | C on round 1, then copy the opponent's previous action. |

The brief leaves the following details open. These are **implementation
assumptions**, not claimed instructor rules:

- Exercises 3-5 allow a user-selected positive number of rounds per match.
- Random actions have probability 1/2 each. Exercises 4-5 independently assign
  each computer one of the four strategies with probability 1/4 each at creation.
  Multiple computers may have the same strategy. The strategy stays fixed.
- Exercise 5 uses computer entrants and single elimination, with any even number
  of entrants at least 2. Initial pairs follow entrant order (1 vs 2, 3 vs 4, ...);
  winners pair in that order at the next stage.
- Highest **match total** advances. A tied match uses a random draw, explicitly
  printed as a tie-break rather than a points victory. Repeating rounds alone
  cannot resolve ties between identical deterministic strategies.
- If a later stage has an odd survivor count (e.g. 6 -> 3), its last entrant gets
  a bye. A bye earns no points. Powers of two (2, 4, 8, ...) avoid byes.
- Histories and totals reset between matches; Tit-for-tat starts C with each new
  opponent. A Random player's pseudorandom stream continues across its matches.
- A separate pseudorandom stream for each computer prevents one player's action
  draws from directly consuming another's action stream. Selection, tie-breaks
  and action streams are reproducible from the printed seed; these are ordinary
  simulation draws, not cryptographic randomness.

The tournament always has `n-1` played matches. With `r` rounds per match, the
engine performs `O(n*r)` decision/scoring steps and stores `O(n*r)` round results.
A single match uses `O(r)` result storage; immutable history snapshots also cost
`O(r^2)` total copying work across a match (`O(n*r^2)` over the tournament).
This is adequate for small classroom
games, rather than an optimized large simulation. Full tournament output stores
and prints every round; use small round/player counts for readability.

## Project layout

| File | Responsibility |
| --- | --- |
| [main.py](main.py) | Starts the console program. |
| [cli.py](prisoners_dilemma/cli.py) | Menu, command-line arguments, validated prompts and seed. |
| [exercises.py](prisoners_dilemma/exercises.py) | Five exercise entry points using shared components. |
| [models.py](prisoners_dilemma/models.py) | Actions, point matrix, round/match data and score totals. |
| [strategies.py](prisoners_dilemma/strategies.py) | The four decision rules. |
| [players.py](prisoners_dilemma/players.py) | Hidden human input and computer players. |
| [engine.py](prisoners_dilemma/engine.py) | Match loop; history isolation and round feedback. |
| [tournament.py](prisoners_dilemma/tournament.py) | Pairing, advancement, ties, byes and champion. |
| [display.py](prisoners_dilemma/display.py) | Matrix, decision/score tables and summaries. |
| [terminal.py](prisoners_dilemma/terminal.py) | ANSI color detection, Windows console support, ASCII panels and color-aware padding. |
| [tests/test_game.py](tests/test_game.py) | Scoring, strategies, match behavior, privacy boundary, tournaments and observations. |
| [tests/test_cli.py](tests/test_cli.py) | All five exercises through the actual console entry point. |

## Verify and study

From this directory:

```powershell
python -B -m unittest discover -s tests -v
```

The [verification record](VERIFICATION.md) contains the actual execution evidence
and its limits. The [exercise summary](SUMMARY.md) explains the calculations and
strategy observations. These are assisted worked examples, not evidence of
student practice, submission, or instructor approval of the unspecified rules.
