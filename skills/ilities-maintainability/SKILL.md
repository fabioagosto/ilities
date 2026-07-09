---
name: ilities-maintainability
description: >-
  Maintainability-only review of a change: run the intent gate first, then judge one thing
  deeply, will this be cheap to change in six months? Use when the user wants a
  maintainability-focused read ("will this be a pain to maintain", "is this too coupled",
  "is this doing too much", "is this cohesive", "how hard will this be to change later",
  "is there hidden state here"), or when a change touches a surface where future edits get
  expensive even if they just said "review this": a new module or class, a function quietly
  growing several jobs, a refactor, a fresh abstraction, shared mutable state, or code many
  callers already lean on. Checks whether each unit does one well-defined thing, whether
  coupling stays minimal and explicit, whether state is visible rather than hidden, and
  whether a likely later edit stays contained instead of rippling across unrelated files.
  For a full 11-dimension review use ilities, and any general "is this ready to
  merge" review belongs there too. Intent-first: a clean, maintainable-looking change that
  solves the wrong problem still fails here.
---

# ilities: Maintainability

A maintainability-only review. Confirm the change does what it set out to do, then judge one
thing: will this be cheap to change in six months? Run the intent gate first. A change that
is beautifully factored but quietly solves a different problem, or smuggles in an unrelated
refactor, is not mergeable no matter how clean the seams are. Intent is the gate;
maintainability is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Maintainability
dimension definition (its signals and smells), and the trade-off principles. Load it before
scoring so you assess against the written definition, not your gut.

## When to use this

Use it when the user wants the maintainability question answered specifically, or when the
change touches a surface where the cost of future edits lives even if they only said "review
this": a new module, class, or service; a function accreting several jobs; a refactor; a
freshly introduced abstraction; shared or mutable state; a dependency newly wired between two
components; or code that a lot of callers already depend on.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. This lens answers only whether the change will be cheap to live with and
modify later, so a general "is this ready to merge" question belongs there. This skill is
intent-first: it asks whether the change should exist in this shape at all, not only whether
the seams read cleanly.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the maintainability score. A clean solution to the wrong problem fails even a
   maintainability-only look.

3. **Assess Maintainability, deeply.** Do not stop at the first smell; trace the unit's shape
   and its ties to everything around it. Is any function or class a god unit that has quietly
   absorbed several responsibilities? Does each unit hold together around one job, or is
   cohesion low, unrelated concerns bundled because they happened to land in the same file?
   Is coupling minimal and explicit, or tight and hidden: a caller reaching into another's
   internals, an import that should not exist, a shared object mutated from two directions?
   Is there hidden state, where setting a field here changes behavior somewhere far away? And
   the load-bearing test: if you had to change this next quarter, would the edit stay
   contained, or would one change force edits in five unrelated places? Score it 0 to 3 on
   the rubric scale, and attach a concrete finding for anything below 3: the location, the
   failure mode, and what would raise it. When modularity, cohesion, loose coupling, or
   portability is the specific problem, name it.

4. **Verify, do not just inspect.** A maintainability verdict from reading alone flatters
   code that merely looks tidy. Where you can, pressure-test the shape: pick a plausible
   future change (a new case, a swapped-out backend, a renamed field) and trace what it would
   force you to touch, following imports and call sites outward to the edge of the blast
   radius. For each new unit, try to name its one job in a single sentence; if you need an
   "and", cohesion is the finding. Check that its dependencies are declared and passed in, not
   reached for globally. Where you cannot trace the callers (a bare diff, no repo access,
   missing context), say so and list what you could not verify.

5. **Write the verdict**, scoped to maintainability: Ship, Ship with follow-ups, or Needs
   work, plus the single most important thing to fix. A Maintainability score of 0, or a
   failed gate, is Needs work no matter how clean the rest looks. Never say Ship on inspection
   alone; either you traced a real future change through the code, or the verdict names what
   stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small or narrow diff, run
the gate, note the future change you traced, give the Maintainability score, and land a
one-line verdict. Save the fuller treatment for a change that adds real structure: a new
module, a broad refactor, a shared abstraction others will build on. The gate and the
verification step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Maintainability (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what future change you traced and what it touched, or what you could not verify and why>

## Verdict (maintainability)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before maintainability, always.** A beautifully factored change that solves the
  wrong problem still fails. Lead with the gate, not the score.
- **Judge the shape, not the surface.** Neatly formatted code can still be a chore to change.
  The cost lives in how the pieces are wired: the responsibilities crammed into one unit, the
  coupling between modules, the state you cannot see from the call site, not in whether the
  lines read cleanly.
- **A finding names the code and its failure mode, never the author.** "`OrderService`
  reaches into `Inventory`'s private cache, so any change to how inventory is stored breaks
  order processing too," not "you coupled these too tightly."
- **Weigh the cost against the change, not against perfection.** Some coupling is fine; a
  one-off script does not need the seams of a shared library. The question is never "is this
  maximally modular" but "is it modular enough that the edits this code will actually see stay
  cheap." Flag the structure that will bite, not every structure that could theoretically be
  looser.
