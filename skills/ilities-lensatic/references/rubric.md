# ilities Rubric

The shared backbone for the ilities suite. It defines the **intent gate**, the
**11 quality dimensions**, the **scoring scale**, and the **trade-off principles** that
`ilities`, `ilities-azimuth`, and `ilities-lensatic` all assess against.

> **Generated file, do not edit directly.** This rubric is assembled from the shared
> source fragments in `_shared/` by `build.py`. To change a definition, edit the
> relevant file under `_shared/` and re-run `python build.py`, which regenerates this
> file for every skill in the suite. Run `python build.py --check` to verify sync.

## Table of contents

- [The core idea: intent before quality](#the-core-idea-intent-before-quality)
- [Part 1: The intent gate](#part-1-the-intent-gate)
- [The scoring scale](#the-scoring-scale)
- [Part 2: The 11 quality dimensions](#part-2-the-11-quality-dimensions)
- [Part 3: Trade-off principles](#part-3-trade-off-principles)

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

## Part 1: The intent gate

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

## Part 2: The 11 quality dimensions

Each dimension leads with the question it answers, then the signals of a strong result
and the smells of a weak one. Assess against the *change*, not the whole codebase.

### 1. Readability

*Can a teammate understand this without the author explaining it?*
- **Signals:** names say what things are and do; control flow is shallow and easy to
  follow; comments explain *why*, not *what*; new code reads like the code around it.
- **Smells:** decoding required to read a name; deep nesting; commented-out code;
  a personal style dropped into a codebase with a different one.

### 2. Simplicity (KISS / YAGNI)

*Is this the least code that fully solves the problem?*
- **Signals:** no speculative generality; abstractions earn their place; plain code
  where plain code suffices; duplication removed where it hurts.
- **Smells:** cleverness for its own sake; abstractions added "in case"; DRY pushed so
  hard the result is harder to follow than the duplication was.

### 3. Flexibility & Extensibility

*Can the likely next change be made without a rewrite?*
- **Signals:** extension points exist where change is genuinely expected, and only
  there; open to extension, closed to modification where it counts.
- **Smells:** flexibility no foreseeable requirement needs (that is a simplicity cost,
  not a virtue); or the opposite: the obvious next change forces a rewrite.

### 4. Maintainability

*Will this be cheap to change in six months?*
- **Signals:** modular, with clear boundaries; each unit does one well-defined thing
  (high cohesion); dependencies between components are minimal and explicit (loose
  coupling); no hidden state.
- **Smells:** god functions/classes; spooky action at a distance; a change here forcing
  edits in five unrelated places.
- *Absorbs modularity, cohesion, loose coupling, and portability; call them out by
  name in a finding when one is the specific problem.*

### 5. Correctness

*Does it do the right thing, including at the edges?*
- **Signals:** handles empty, null, boundary, and malformed inputs; error and failure
  paths are handled, not swallowed; concurrency, ordering, and race assumptions are
  sound where relevant.
- **Smells:** happy-path-only logic; off-by-one and boundary gaps; swallowed
  exceptions; unstated timing assumptions.
- *Correctness is assumed, so it is the easiest dimension to skip and the most common
  thing a clean-looking change gets wrong. Do not skip it.*

### 6. Testability & Tests

*Can the behavior be verified, and is it?*
- **Signals:** new behavior is covered at the right level (unit / integration); tests
  assert behavior, not implementation details; code is structured to be tested in
  isolation (dependencies injectable, side effects isolated).
- **Smells:** untested new behavior; tests coupled to internals that break on refactor;
  logic that cannot be exercised without standing up the whole system.

### 7. Robustness & Reliability

*Does it degrade gracefully?*
- **Signals:** fails loudly and early on programmer error, safely on user/environment
  error; no unbounded resource use; idempotent and retry-safe where the context calls
  for it.
- **Smells:** unbounded loops/queries/memory; silent failure; non-idempotent operations
  on a retry path.
- *Absorbs scalability; flag it by name when growth in load or data is the specific
  concern.*

### 8. Security

*Could this be misused?*
- **Signals:** inputs from outside the trust boundary are validated and/or escaped
  (injection, XSS, path traversal); authn/authz checks on anything that reads or mutates
  data; no secrets in code; least privilege; caps on anything a caller controls (page
  size, batch size, rate).
- **Smells:** trusting caller input; missing authz on a mutating path; secrets in
  source; unbounded caller-controlled limits.

### 9. Performance & Efficiency

*Is it fast enough for its actual load, and no more optimized than it needs to be?*
- **Signals:** no accidental N+1s, full-table scans, or repeated work in loops; data
  structures fit the access pattern; optimized against real expected load.
- **Smells:** N+1 queries; work repeated inside loops; premature micro-optimization that
  costs readability for no measured gain.

### 10. Consistency

*Does it fit the codebase?*
- **Signals:** follows existing patterns, conventions, and directory structure; does not
  add a second way to do something the codebase already does one way.
- **Smells:** a new pattern where an established one exists; reinvented utilities;
  structure that fights the repo's conventions.

### 11. Observability

*When it breaks in production, can we tell what happened?*
- **Signals:** meaningful logs / metrics / errors at the boundaries that matter; error
  messages are actionable (say what failed and, ideally, what to do next).
- **Smells:** silent boundaries; `catch` blocks that lose the cause; error messages that
  give the reader nothing to act on.

## Part 3: Trade-off principles

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
