# TP1 exercise summary and strategic interpretation

This is an assisted explanation using [TP1 pp.1-2](../Attachments/TP1.pdf).
The source gives the game and exercises; the calculations below are our results.
They are not an official answer key. Run instructions and tournament assumptions
are in the [project README](README.md).

## Intuition and mathematical model

Cooperation can help both players, but each player can gain by betraying a
cooperating opponent. The players are A and B. Each chooses C or D without seeing
the other's current action, and each maximizes their own points.
`u_A(C,C)=3`, `u_B(C,C)=3`, and the remaining payoffs are in the README matrix.
Repeated matches sum round points; Tit-for-tat can respond only from round 2.

## Exercise 1 - One round, two humans

**Verified mathematical result:** for A=C, B=D, the matrix gives `(0,5)`.
A gets 0 and B gets 5. Every action combination is tested against TP1 p.1.
The output table connects each action to the corresponding player's payoff.

## Exercise 2 - Several rounds, two humans

**Verified mathematical result:** this three-round example gives:

| Round | A | B | Round points (A,B) | Totals (A,B) |
| --- | --- | --- | --- | --- |
| 1 | C | C | (3,3) | (3,3) |
| 2 | C | D | (0,5) | (3,8) |
| 3 | D | D | (1,1) | (4,9) |

The calculation is A=`3+0+1=4`, B=`3+5+1=9`. A match total depends on the complete
sequence, rather than only the final round. This is a scripted example, not
observed human classroom behavior.

## Exercise 3 - Human against a computer strategy

**Verified mathematical result:** against human actions D,C,D, Tit-for-tat plays
C,D,C. Therefore the round payoffs are `(5,0)`, `(0,5)`, `(5,0)` and the totals
are `(10,5)` for `(human,computer)`. Tit-for-tat copies the **previous** action,
so it neither predicts nor sees the current human choice.

The other rules behave differently: Always cooperate never retaliates, Always
defect never restores cooperation, and Random has no memory. All four modes are
exercised by the console tests. A human can change decisions every round.

## Exercise 4 - Two computer players

Each player first receives one of the four strategies at random. The strategies
then generate their actions for all rounds. Randomly choosing a strategy once is
different from the Random strategy choosing a new C/D action each round.

**Verified mathematical results:** over `r` rounds, Always cooperate vs itself
earns `(3r,3r)`, Always defect vs Always cooperate earns `(5r,0)`, and Always
defect vs itself earns `(r,r)`. For Tit-for-tat vs Always defect, totals are
`(r-1,r+4)` when `r>=1`: first `(0,5)`, then `r-1` copies of `(1,1)`.
The tests check three-round instances `(9,9)`, `(15,0)`, `(2,7)` and tournament
instances of mutual defection. A random simulation is an example of these rules
in use, rather than proof of the general formulas.

## Exercise 5 - Tournament

A player advances by scoring more in its current match, or by a recorded random
tie-break. The output lists entrants, strategies, each match and each round,
cumulative points, byes, the advancing players and the champion. The automatic
summary counts cooperative actions, mutual C/C and D/D rounds, and combined
points using the actual results of that run.

**Model limitation:** a champion depends on the bracket, opponents, match length,
seed and tie/byes policy. For example, identical strategies can tie every match;
then the champion is chosen by the tie-breaks. A bye is not a scored victory.
Winning one tournament does not establish a universally best strategy.

## Why this is a dilemma

**Verified mathematical result (one-shot game):** if B chooses C, A gets 5 from D
instead of 3 from C. If B chooses D, A gets 1 from D instead of 0 from C.
By symmetry these comparisons also hold for B. Thus D strictly dominates C for
both players.

All unilateral-deviation checks for pure profiles are:

| Profile | Improving deviation? |
| --- | --- |
| (C,C) | A can change to D: 3 -> 5; B can also improve: 3 -> 5. |
| (C,D) | A can change to D: 0 -> 1. |
| (D,C) | B can change to D: 0 -> 1. |
| (D,D) | Neither improves: a unilateral C would give 0 instead of 1. |

Therefore `(D,D)` is the only pure Nash equilibrium, with payoffs `(1,1)`.
Strict dominance also rules out positive probability on C in a mixed best
response: if the opponent cooperates with probability `p` in `[0,1]`, then
`U(D)-U(C) = (5p+1-p)-3p = 1+p > 0`. So `(D,D)` is the unique equilibrium
even allowing independent mixed strategies in the one-shot game.

Yet `(C,C)` gives `(3,3)`, better for both than `(1,1)`. Individual incentives and
the best shared outcome differ. The best combined stage score is 6 at `(C,C)`;
the other combined scores are 5, 5 and 2.

Repeating the game allows strategies to react to history. Tit-for-tat can sustain
mutual cooperation against a cooperating partner and punish a defection, but it
can also alternate C/D against a changing opponent. This program executes fixed
strategies; it does not solve repeated-game equilibria, prove convergence, or
show that human players will cooperate.
