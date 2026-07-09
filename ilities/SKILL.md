---
name: ilities
description: >-
  Review a change (PR, commit, diff, or design) against its stated intent first,
  then against 11 code-quality dimensions, and return a scored verdict with the
  single most important thing to fix. Use this whenever the user asks you to
  review, audit, critique, or sanity-check a change or PR; asks "is this ready to
  merge / ship?"; asks "does this do what it should?"; or hands you a diff and asks
  what you think. (For steering code you are about to write, or a self-review before
  you open your own PR, use ilities-guide instead: this skill reviews a change
  that already exists.) The distinguishing
  move is the intent gate: it catches scope creep, half-solved problems, and clean
  solutions to the wrong problem, which ordinary "is this code good?" review misses.
  Prefer this over an ad-hoc review whenever a change has a purpose worth checking
  it against.
---

# ilities

An **intent review** of a change: first confirm it does what it set out to do (no
more, no less), then score its quality, then give a verdict. This is not the same as
"is this code good?" A clean change that solves the wrong problem, creeps in scope, or
only half-fixes the bug still fails the review. Intent is a gate you pass before the
quality dimensions open.

Read `references/rubric.md` for the full intent gate, the 11 dimension definitions with
signals and smells, the scoring scale, and the trade-off principles. It is the shared
backbone of the ilities suite. Load it before scoring so you assess against the
written definitions rather than your gut.

## When to use this

Reach for an audit whenever there is a change with a purpose worth checking it against:
a PR, a commit, a working-tree diff, a proposed design. Typical triggers: "review this,"
"is this ready to merge," "does this actually solve X," "what do you think of this diff."
(If the code does not exist yet, or you are checking your *own* work before opening a PR,
that is `ilities-guide`: audit reviews a change that already exists.)

For finding *bugs* in a diff mechanically, the `/code-review` command is the sharper
tool and you can run it alongside. ilities is broader and intent-first: it asks
whether the change should exist in this shape at all, not only whether the code has
defects.

## Scale the review to the change

The full ritual fits a substantial PR. Do not inflate a two-line fix into an eleven-line
score sheet, and do not force scores onto a design doc where "file:line" makes no sense.
Match the depth to the change: for a tiny or narrow diff, run the intent gate, report
only the dimensions that are actually at risk, note what you verified, and give a
one-line verdict. Reserve the full scored grid for changes big enough that a reader
benefits from the map. The intent gate and verification always run; only the scoring
depth flexes.

## The process

Work in this order. The ordering is the method: do not skip to scoring.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull
   it from the PR description, commit message, ticket, or the user. If you cannot write
   that sentence, stop and say so: the change is not reviewable yet, and that is your
   first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers (stated, matches intent,
   scope contained, problem solved at the goal level) each stop the merge on a "no." The
   fifth, "is the intent worth doing," is a flag: raise it as a question rather than
   blocking, unless the waste is unambiguous. When a blocker trips, the finding *is* the
   failed check, for example "solves an adjacent problem: the ticket asks for X, the diff
   does Y" or "unrelated refactor in `foo.py` should be a separate change." Report gate
   failures before, and more prominently than, any dimension score.

3. **Score the dimensions 0 to 3** (or N/A), at the depth the change warrants (see "Scale
   the review"). For a substantial change, score all 11 against the change, not the whole
   codebase; for a small or narrow one, score only the dimensions genuinely at risk and
   skip the rest. For every score below 3, attach a concrete finding: the location (file/
   line where the code exists; otherwise the specific element), the failure mode, and what
   would raise it. A score without a reason is noise. Mark N/A honestly; do not pad the
   sheet.

4. **Verify, do not just inspect.** A verdict from reading alone is the most dangerous
   thing this skill can produce. Where the environment allows it, run the tests, the
   build, the linter, or the actual code path the change touches, and let what you
   observe move the scores. Where you cannot (no repo access, a bare diff, missing
   deps), say so explicitly: list what you were unable to verify. Correctness and
   Testability scores in particular should reflect evidence, not a hunch.

5. **Write the verdict.** Ship / Ship with follow-ups / Needs work, plus the single most
   important thing to fix. Remember this is not an average: one 0, or a failed gate,
   means Needs work no matter how strong the rest is. Never say Ship on inspection
   alone: either you verified, or the verdict names what remains unverified.

## Output format

Use this structure for a full review. The scores grid is a quick scannable map, so it is
fine to show a dimension as `N/A` there; the findings list, by contrast, carries only
dimensions that scored below 3, each tied to a location. For a small change (see "Scale
the review"), drop the grid and report just the gate, the at-risk dimensions, what you
verified, and the verdict. The verdict never omits verification regardless of size: even
a one-line review states what was checked or what could not be.

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Scores
Readability      [n]   Correctness        [n]   Security      [n]
Simplicity       [n]   Testability/Tests  [n]   Performance   [n]
Flexibility      [n]   Robustness         [n]   Consistency   [n]
Maintainability  [n]   Observability      [n]

## Findings
- <dimension> (<score>): <file:line>: <failure mode> → <what would fix it>
- ...

## Verification
<what you ran and observed, or what you could not verify and why>

## Verdict
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
Follow-ups (non-blocking): <...>
```

## Principles that change how you review

- **Intent before quality, always.** A high total cannot rescue a failed gate. Lead with
  the gate result.
- **Correctness is assumed, so it is the easiest to skip and the most common thing a
  clean-looking change gets wrong.** Actively probe empty/null/boundary/malformed inputs
  and failure paths before you score it.
- **A finding names the code and its failure mode, never the author.** "This swallows the
  connection error so a retry loop spins silently," not "you forgot to handle the error."
- **Simplicity and flexibility trade off.** If a change is over-abstracted, that is a
  simplicity finding even though the code is "flexible." Say which one this code should
  have optimized for. See the trade-off principles in the rubric.
- **N/A is a judgment, not an escape.** Use it when a dimension truly does not apply; do
  not use it to avoid thinking about correctness or security.
