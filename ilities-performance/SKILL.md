---
name: ilities-performance
description: >-
  Performance-only review of a change: run the intent gate first, then judge one question
  deeply, is it fast enough for its actual load and no more optimized than it needs to be?
  Use when the user wants a performance-focused read ("is this fast enough", "is there an
  N+1 here", "will this be slow at scale", "is this a hot path", "why is this slow", "am I
  over-optimizing this", "does this do redundant work in the loop"), or when a change
  touches a performance-sensitive surface even if they just said "review this": a query
  issued inside a loop, a hot path or request handler under load, nested iteration over a
  collection that can grow, a batch or scheduled job, a data structure picked against its
  access pattern, a cache added by hand. Checks for accidental N+1s, full-table scans, work
  repeated per iteration, structures that fit how the code reads and writes, and the
  opposite failure, micro-optimization that costs readability for no measured gain. For a
  full 11-dimension review use ilities; for line-by-line efficiency cleanups,
  /code-review and /simplify are sharper and run alongside. Intent-first: a
  performance-strong change that solves the wrong problem still fails here.
---

# ilities: Performance

A performance-only review. Confirm the change does what it set out to do, then judge one
question: is it fast enough for its actual load, and no more optimized than it needs to be?
Run the intent gate first. A change asked to bound an export endpoint that instead makes the
same unbounded query run twice as fast has lovely numbers and the wrong outcome: it still
streams the whole table, and the problem it was filed against is untouched. Intent is the
gate; performance is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Performance &
Efficiency dimension definition, and the trade-off principles. Load it before scoring so you
assess against the written definition, not your gut.

## When to use this

Use it when the user wants the performance question answered specifically, or when the change
touches a performance-sensitive surface even if they only said "review this": a query issued
inside a loop or once per result row, a hot path or request handler under real load, nested
iteration over a collection that can grow, a batch or scheduled job that processes many items,
a data structure chosen against how the code reads or writes it, or a hand-rolled cache or
optimization added on a hunch.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate, and a general "is this ready to merge?" question belongs there too. For
line-by-line efficiency cleanups, `/code-review` and `/simplify` are sharper and can run
alongside. This skill is intent-first: it asks whether the change should exist in this shape
at all, not only whether a given line could be quicker.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the performance score. A clean solution to the wrong problem fails even a performance-only
   look.

3. **Assess Performance, deeply.** Do not stop at the first hotspot; follow the work through
   the whole path the change touches and ask at each step where it repeats. Look for the
   accidental N+1: a query fired once per result row that should have been one join or a
   batched fetch. Look for the full-table scan behind a missing index or an unfiltered read.
   Look for work hoisted into a loop that belonged outside it: a recompiled regex, a re-fetched
   config, an allocation or round-trip per iteration. Ask whether the data structure fits the
   access pattern, or whether the code is doing a linear scan of a list where a set or map
   lookup was the point. Then check the opposite failure, because it is a real one: premature
   micro-optimization, a hand-unrolled loop or a bespoke cache that costs readability for a
   speedup nobody measured and the load does not need. Score it 0 to 3 on the rubric scale, and
   attach a concrete finding for anything below 3: the location, the failure mode, and what
   would raise it.

4. **Verify, do not just inspect.** A performance verdict from reading alone is a guess, and
   guesses about speed are usually wrong. Where the environment allows it, measure: count the
   queries the path actually issues, profile the hot path, run it against a realistic input
   size rather than a three-row fixture, and watch how cost grows as the input grows. Judge it
   against the load the code will really carry: an O(n²) loop over a list never longer than
   five is fine, the same loop over an unbounded upload is not. Measure against real expected
   load, not an imagined worst case and not an imagined best one. Where you cannot run it (bare
   diff, no repo, missing data), say so and list what you could not verify.

5. **Write the verdict**, scoped to performance: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Performance score of 0, or a failed gate, is
   Needs work no matter how clean the rest looks. Never say Ship on inspection alone; either
   you measured the path, or the verdict names what stays unmeasured.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you measured, give the Performance score, and land a one-line verdict. Save the
fuller treatment for a change with real performance surface: a query path, a loop over live
data, a hot endpoint. The gate and the verification step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Performance (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you measured and observed, or what you could not verify and why>

## Verdict (performance)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before performance, always.** A blazing-fast change that solves the wrong problem
  still fails. Lead with the gate, not the score.
- **Follow the work that multiplies; do not admire the happy path.** Performance problems hide
  where an operation repeats, once per row, per request, per loop pass, so a query or scan that
  reads cleanly at n=1 quietly becomes the bottleneck at n=10,000. Go looking where the work is
  multiplied, not where the code reads well.
- **Fast enough is the target, not fastest.** Over-optimization is a real finding, not a free
  bonus: a hand-tuned loop or a bespoke cache that costs readability for a speedup no one
  measured scores below the plain version. Spend the trade against measured load, then stop.
- **A finding names the code and its failure mode, never the author.** "This issues one query
  per row of the result set, so a 500-row page fans out into 500 round-trips," not "you wrote
  an inefficient loop."
