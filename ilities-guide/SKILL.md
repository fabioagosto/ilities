---
name: ilities-guide
description: >-
  Steer new code so it passes an intent review by construction: state the change's
  intent in one sentence, keep scope contained to that intent, build in the 11
  code-quality dimensions as you go, and self-run the intent gate before you call
  the work done or open a PR. Use this whenever you are about to write or are
  writing a non-trivial feature, bugfix, refactor, or change and want it to be
  right the first time rather than fixed in review; whenever the user says "build
  X properly," "do this the right way," "make it production-quality," or asks for a
  self-review before opening a PR. This is the forward-facing companion to
  ilities: same rubric, applied while writing instead of after.
---

# ilities Guide

Write the change so it would pass an intent review, instead of writing it and hoping
review catches the gaps. Same rubric as `ilities`, run forward. The core
discipline is to **know the one sentence of intent before you touch code, and refuse to
drift from it.**

Read `references/rubric.md` for the intent gate, the 11 dimensions with signals and
smells, and the trade-off principles. Load it before you start so you are building
toward the written definitions.

## When to use this

Use it whenever you are about to write or are writing something with enough substance to
get wrong: a feature, a bugfix, a refactor, a migration. Triggers: "build X properly,"
"do this the right way," "make it production-quality," "self-review before I open the
PR," or any moment you feel scope starting to sprawl.

For quick throwaway scripts and one-liners this is overkill; the value shows up when the
code will be read, changed, or relied on later.

## Before you write

1. **Write the one-sentence intent.** What is this change supposed to accomplish? If you
   cannot say it in a sentence, you are not ready to write; clarify with the user or in
   the ticket first. This sentence is your scope contract for the rest of the work.

2. **Decide where to concentrate.** Every dimension that applies still deserves to be
   met; the point is where the *extra* care goes, since attention is finite. A hot path
   leans on Performance and Robustness; a public API on Flexibility and Consistency; a
   security-boundary change on Security and Correctness. This is about focus, not about
   deliberately letting a dimension slide. If the trade-offs are genuinely unclear (some
   dimensions truly pull against each other), that is what `ilities-decide` is for;
   use it, then come back.

3. **Note what is explicitly out of scope.** The refactor you are tempted to do "while
   here," the adjacent bug you spotted. Write them down as follow-ups; do not smuggle them
   into this change. Scope creep is an intent-gate failure even when the extra code is good.

## While you write

Build the dimensions in rather than bolting them on. The high-leverage habits:

- **Read the surrounding code first and match it** (Consistency, Readability). Use the
  idioms, naming, and structure already there; do not introduce a second way to do
  something the codebase already does one way.
- **Handle the edges as you write the happy path** (Correctness, Robustness). Empty,
  null, boundary, malformed input; the failure path; the retry. Correctness is assumed,
  so it is the easiest to skip and the most common thing a clean change gets wrong.
- **Keep units small and boundaries clean** (Maintainability). One well-defined job per
  unit, minimal and explicit dependencies, no hidden state.
- **Resist speculative abstraction** (Simplicity). Add an extension point only where a
  change is genuinely expected. Flexibility no foreseeable requirement needs is a cost,
  not a virtue.
- **Validate what crosses the trust boundary and cap what a caller controls** (Security,
  Robustness). Page size, batch size, rate; injection and path-traversal surfaces.
- **Write the test as you write the behavior** (Testability). Structure the code so it can
  be exercised in isolation; assert behavior, not internals.
- **Leave a trail at the boundaries that matter** (Observability). Actionable error
  messages; a log or metric where a production failure would otherwise be invisible.

## Before you call it done

Self-run the intent gate from the rubric on your own change, honestly:

- Does the diff match the one-sentence intent, no more and no less?
- Did any out-of-scope work sneak in? If so, split it out.
- Is the problem actually solved, or patched in a way that resurfaces elsewhere?
- Walk the dimensions you chose to optimize for: are they actually strong, or just
  intended?

Then **verify, do not assume.** Run whatever checks the change actually has (tests,
build, linter) and exercise the path you changed; "it should work" is not evidence that
it does. A doc-only or config change may have nothing to run, and that is fine; the rule
is to not *imply* verification you did not do. If something is genuinely unverifiable in
this environment, say so plainly. This is the same discipline as the audit's verification step: never report a
change as done on the strength of having written it.

If you would not pass your own gate, or the checks are not green, fix it before handing
over. Then, when the work is substantial, running `ilities` (or asking the user
to) is a good final check; the forward pass and the review pass catch different things.

## Principles

- **Intent is a contract, not a starting point.** Drifting from the one sentence is the
  most common way good code becomes an unmergeable change.
- **Choose your trade-offs on purpose.** Simplicity and flexibility pull against each
  other; pick the one this code needs and spend the other consciously. See the rubric's
  trade-off principles.
- **Cheap now beats expensive in six months.** Small units, clean boundaries, and tests
  are what make the *next* change cheap; that is the real payoff of building to the rubric.
