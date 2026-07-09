---
name: ilities-simplicity
description: >-
  Simplicity-only review of a change: run the intent gate first, then judge one thing
  deeply, is this the least code that fully solves the problem? Use when the user asks
  whether something is over-engineered or too complex, whether it could be simpler, whether
  they really need this abstraction, whether this is YAGNI, whether they are over-abstracting
  this, or whether there is a simpler way, or when a change adds structure even if they just
  said "review this": a new base class or interface, a wrapper or factory, layers of
  indirection, generic or configurable machinery, config knobs nobody asked for, premature
  parameterization, or a heavy DRY refactor that unifies code which only looked alike. Weighs
  speculative generality, indirection that only forwards, cleverness that costs more clarity
  than it buys, and DRY pushed past where it helps. For a full 11-dimension review use
  ilities; for mechanically applying reuse and simplification cleanups /simplify is
  the sharper tool and runs alongside; pairs with ilities-decide when simplicity trades
  against flexibility. Intent-first: a clean, simplicity-strong change that solves the wrong
  problem still fails here.
---

# ilities: Simplicity

A simplicity-only review. Confirm the change does what it set out to do, then judge one
thing: is this the least code that fully solves the problem? Run the intent gate first. A
change that could not be leaner but quietly solves a different problem, or earns its tidiness
by dropping a case the ticket required, is not mergeable no matter how little code it is.
Intent is the gate; simplicity is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Simplicity dimension
definition (its signals and smells), and the trade-off principles. Load it before scoring so
you assess against the written definition, not your gut.

## When to use this

Use it when the user wants the simplicity question answered specifically ("is this
over-engineered," "could this be simpler," "do we really need this abstraction," "is this
YAGNI"), or when a change adds structure even if they only said "review this": a new base
class, interface, or generic type; a wrapper, adapter, or factory; extra layers of
indirection; configurable or plugin-style machinery; config knobs and parameters nobody asked
for; or a DRY refactor that folds several blocks into one shared helper.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. For mechanically applying reuse and simplification cleanups, `/simplify`
is the sharper tool, and it pairs with `ilities-decide` when simplicity genuinely trades
against flexibility. This skill is intent-first: it asks whether the change should exist in
this shape at all, not only whether a line could be tidier.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the simplicity score. The leanest possible solution to the wrong problem fails even a
   simplicity-only look.

3. **Assess Simplicity, deeply.** Do not stop at the first tidy helper; read the whole shape
   the change adds. Is there speculative generality: a base class, generic type, interface, or
   config knob added for a second caller that does not exist yet? Indirection that buys
   nothing: a wrapper that only forwards, a layer you pass straight through, a factory with one
   implementation? Cleverness that trades clarity for no real gain, a dense one-liner or
   metaprogramming where a plain loop would read? DRY pushed so hard that one tangled helper is
   harder to follow than the duplication it removed? Score it 0 to 3 on the rubric scale, and
   attach a concrete finding for anything below 3: the location, the failure mode (what the
   extra structure costs the reader), and what would raise it, usually inline it, delete it, or
   wait for the real second caller.

4. **Verify, do not just inspect.** A simplicity verdict from reading alone rewards code that
   looks elegant over code that is actually minimal. Test the structure against deletion:
   mentally inline each helper, collapse each layer, remove each parameter, and check whether
   anything real is lost, a case stops being handled, a caller breaks, the stated problem goes
   unsolved. If nothing is lost, the abstraction was decoration, and that is your finding.
   Confirm the plainer version still fully solves the stated problem, not a smaller one. Where
   you cannot run the code or see all the call sites (bare diff, no repo), say so and name the
   abstractions whose real usage you could not confirm.

5. **Write the verdict**, scoped to simplicity: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to simplify. A Simplicity score of 0, or a failed
   gate, is Needs work no matter how clean the rest looks. Never call an abstraction justified
   on looks alone; either you checked that removing it loses something, or the verdict names
   the structure whose worth you could not confirm.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you probed, give the Simplicity score, and land a one-line verdict. Save the fuller
treatment for a change that actually introduces new abstraction or structure. The gate and the
verification step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Simplicity (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (simplicity)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before simplicity, always.** The leanest change that solves the wrong problem
  still fails. Lead with the gate, not the score.
- **Judge by deletion, not by looks.** The question is never "is this clean?" but "would a
  plainer version solve the same stated problem?" If inlining a helper, dropping a layer, or
  removing a knob loses nothing real, the structure was decoration, however elegant it reads.
  Elegant and minimal are not the same bar.
- **Duplication is cheaper than the wrong abstraction.** Two straightforward blocks that
  repeat are easy to read and change apart; one premature generalization couples code that
  only looked alike, and now every change fights the shared shape. An abstraction earns its
  place by paying for itself now: one real caller is a function, the pattern starts at the
  third. When simplicity and flexibility genuinely pull apart, that is a `ilities-decide`
  call, not a reflex to abstract.
- **A finding names the code and its failure mode, never the author.** "This factory has one
  implementation and one caller, so the interface adds a hop the reader must trace without
  buying anything a plain function would not," not "you over-engineered this."
