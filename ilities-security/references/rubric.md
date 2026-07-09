# ilities Rubric: Security lens

The slice of the ilities rubric this skill needs: the **intent gate** (run
first, every time), the **scoring scale**, the **Security** dimension, and
the **trade-off principles**. For the full 11-dimension rubric, see `ilities`.

> **Generated file, do not edit directly.** This rubric is assembled from the shared
> source fragments in `_shared/` by `build.py`. To change a definition, edit the
> relevant file under `_shared/` and re-run `python build.py`, which regenerates this
> file for every skill in the suite. Run `python build.py --check` to verify sync.

## The core idea: intent before quality

A normal code review asks *"is this code good?"* An **intent review** asks first
*"does this change do what it set out to do, no more and no less?"* That ordering is
the whole point. Scope creep, half-solved problems, and clean solutions to the wrong
problem are all failures even when the code itself is spotless. You cannot judge
quality until you know what the change was trying to be, so intent is a gate you pass
before the quality dimensions even open.

So intent is the **first lens**, not one score among many: a change can fail here no
matter how clean its code. But treat the gate as a scope-and-goal check, not a back-door
into the quality dimensions. "Does it solve the stated problem *at all*" is a gate
question; "is it correct at the edges" is the Correctness dimension. Keep them separate
so the gate stays about *what the change is*, not *how well it is built*.

This is why the rubric is **not an average**. A change can be a 3 on ten dimensions
and still be unmergeable because it quietly solved a different problem, or smuggled in
an unrelated refactor. One failing gate stops the merge. The scores are a diagnostic
that tells you *where* the work is weak, not a number to optimize.

## The intent gate (run this first)

Answer these first. A "no" on the four **blockers** below stops the merge, and the
finding is the "no" itself. The fifth is a **flag**, not a blocker.

Blockers:

- **Intent is stated.** The change has a clear, one-sentence goal. If you cannot write
  that sentence, the change is not ready to review: that is itself the finding.
- **The change matches the intent.** It solves the stated problem, not an adjacent or
  larger one.
- **Scope is contained.** No unrelated refactors, drive-by edits, or "while I was here"
  additions. Those are not free; they belong in a separate change where they can be
  reviewed on their own terms.
- **The problem is actually solved at the goal level.** Not partially patched, not worked
  around in a way that reintroduces the problem elsewhere. (This is the *goal*-level
  question: "did it address the stated problem." Edge-case correctness is scored
  separately under the Correctness dimension.)

Flag (raise, do not block):

- **Is the intent worth doing?** Ideally it maps to a real bug, backlog item, or user
  need. But judging product value usually needs context an agent does not have, so raise
  this as a question ("this does not obviously map to a stated need, intended?") rather
  than blocking the merge on it. Only treat it as a blocker when the waste is unambiguous
  (dead code, a feature the change itself shows is unreachable).

## The scoring scale

| Score | Meaning |
|-------|---------|
| **3: Strong** | Clearly meets the bar; nothing to add. |
| **2: Adequate** | Meets the bar with minor, non-blocking nits. |
| **1: Weak** | Falls short; address before or soon after merge. |
| **0: Failing** | Blocks the merge. |
| **N/A** | Dimension genuinely does not apply to this change. |

A dimension scoring **0 blocks the merge** regardless of the total. Mark **N/A**
honestly: a dimension that does not apply is good judgment; N/A used to dodge thinking
is how bugs ship.

## The Security dimension

*Could this be misused?*
- **Signals:** inputs from outside the trust boundary are validated and/or escaped
  (injection, XSS, path traversal); authn/authz checks on anything that reads or mutates
  data; no secrets in code; least privilege; caps on anything a caller controls (page
  size, batch size, rate).
- **Smells:** trusting caller input; missing authz on a mutating path; secrets in
  source; unbounded caller-controlled limits.

## Trade-off principles

- **One failing gate stops the merge.** The score is a diagnostic, not an average to
  game.
- **Simplicity and flexibility trade off.** Every abstraction added for flexibility
  costs simplicity. Decide which one *this specific code* should optimize for; do not
  try to max both.
- **Performance trades against readability and portability.** Spend that trade only
  against measured load, not imagined load.
- **Security and robustness caps trade against convenience.** Usually worth it on
  anything crossing a trust boundary; note the cost rather than pretending there is
  none.
- **Correctness is assumed, so it is easy to skip. Don't.**
- **Review the change, not the author.** Findings describe the code and its failure
  mode, never the person.
