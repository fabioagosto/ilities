---
name: ilities-correctness
description: >-
  Correctness-only review of a change: run the intent gate first, then judge one thing
  deeply, does it do the right thing, including at the edges? Use when the user wants a
  correctness review ("is this correct", "does this handle the edge cases", "what happens on
  empty / null input", "any off-by-one here", "will this break on malformed input", "check
  the error handling on this", "did I miss a failure path"), or when a change touches logic
  whose edges are easy to get wrong even if they just said "review this": parsing and input
  handling, loops and indexing, boundary and range checks, retries and fallbacks, state
  transitions, date/time and arithmetic, pagination, concurrency or ordering assumptions.
  Checks that empty, null, boundary, and malformed inputs are handled, that error and failure
  paths are caught rather than swallowed, that off-by-one and boundary conditions hold, and
  that timing and race assumptions are sound. For a full 11-dimension review use
  ilities; for line-by-line bug hunting, /code-review is sharper and runs alongside.
  Intent-first: a correctness-strong change that solves the wrong problem still fails here.
---

# ilities: Correctness

A correctness-only review. Confirm the change does what it set out to do, then judge one
thing: does it do the right thing, including at the edges? Run the intent gate first. A
change whose every branch and boundary is handled flawlessly but which computes the wrong
quantity, or fixes a different bug than the ticket names, is not mergeable no matter how
carefully the edges are covered. Intent is the gate; correctness is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Correctness dimension
definition, and the trade-off principles. Load it before scoring so you assess against the
written definition, not your gut.

## When to use this

Use it when the user wants the correctness question answered specifically, or when the change
touches logic whose edges are easy to get wrong even if they only said "review this": parsing
and input handling, loops and indexing, boundary and range checks, error and exception
handling, retries and fallbacks, state transitions, arithmetic and rounding, date/time and
timezone math, pagination, or anything carrying concurrency or ordering assumptions.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. For line-by-line bug hunting, `/code-review` is sharper and can run
alongside. This skill is intent-first: it asks whether the change solves the right problem
correctly, not only whether a line has a defect.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the correctness score. A clean solution to the wrong problem fails even a correctness-only
   look.

3. **Assess Correctness, deeply.** Do not stop at the first issue; walk every edge the change
   touches, not just the happy path that reads cleanly. What happens on empty, single-element,
   null, or missing input; on the maximum and just-past-maximum value; on malformed input that
   violates the contract the code assumes? Are error and failure paths handled, or swallowed by
   a bare catch, an ignored return code, or a default that papers over the failure? Do the
   boundary conditions hold: loop bounds, off-by-one at the first and last element,
   inclusive-versus-exclusive ranges, division and overflow? Where order or timing matters, are
   the concurrency and race assumptions sound, or does the code quietly assume a single caller,
   a fixed ordering, or an atomicity it never enforces? Score it 0 to 3 on the rubric scale, and
   attach a concrete finding for anything below 3: the location, the failure mode, and what
   would raise it.

4. **Verify, do not just inspect.** A correctness verdict from reading alone is what this skill
   gets wrong most: correctness is assumed, so it is the least examined and the one inspection
   is worst at. Where you can, run the edges: feed the empty list, the null, the malformed
   record, the boundary value; drive the error path and watch whether it is handled or
   swallowed; run the test suite and read what it does and does not cover. Let what you observe
   set the score. Where you cannot (bare diff, no repo, missing deps), say so and list what you
   could not verify.

5. **Write the verdict**, scoped to correctness: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Correctness score of 0, or a failed gate, is
   Needs work no matter how clean the rest looks. Never say Ship on inspection alone; either you
   ran the edges, or the verdict names what stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note which edges you probed, give the Correctness score, and land a one-line verdict. Save the
fuller treatment for a change with real logic to get wrong at its edges. The gate and the
verification step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Correctness (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (correctness)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before correctness, always.** A change whose every edge is handled but that solves
  the wrong problem still fails. Lead with the gate, not the score.
- **The bug is on the path you did not run.** The happy path is what the author already
  exercised and what reads cleanly on the page; the defects hide in the empty input, the last
  loop iteration, the swallowed exception, the second concurrent caller. Go looking there.
- **Run the edge; do not reason about it.** Correctness is the dimension you are most tempted
  to sign off from inspection, and the one inspection is worst at. Feed the boundary value and
  watch what happens; if you could not, the verdict says so rather than implying a correctness
  you never confirmed.
- **A finding names the code and its failure mode, never the author.** "This loop runs to
  `<= len(items)`, so the last pass indexes one past the end and throws on every non-empty
  list," not "you made an off-by-one error."
