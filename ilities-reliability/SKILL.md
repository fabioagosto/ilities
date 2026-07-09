---
name: ilities-reliability
description: >-
  Reliability-only review of a change: run the intent gate first, then judge one thing
  deeply, does it degrade gracefully? Use when the user wants a robustness-focused review
  ("is this robust", "will this hold up under load", "what happens if this gets retried",
  "is this idempotent", "does this fail gracefully", "could this run out of memory or spin
  forever", "will this scale"), or when a change touches a surface where things go wrong or
  grow even if they just said "review this": retry and timeout logic, loops or pagination
  over unbounded data, queues, background jobs, external or network calls, caching, memory
  and connection allocation, error-handling paths. Checks that code fails loudly on
  programmer error and safely on user or environment error, avoids unbounded
  loops/queries/memory, stays idempotent wherever a retry can reach it, and caps resource
  use as load and data grow. For a full 11-dimension review use ilities; for
  line-by-line correctness and efficiency hunting, /code-review is sharper and runs
  alongside. Intent-first: a reliability-strong change that solves the wrong problem still
  fails here.
---

# ilities: Reliability

A reliability-only review. Confirm the change does what it set out to do, then judge one
thing: does it degrade gracefully? Run the intent gate first. A change with airtight retry
logic and resource caps that quietly solves a different problem, or smuggles in an unrelated
refactor, is not mergeable no matter how gracefully the code fails. Intent is the gate;
reliability is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Robustness &
Reliability dimension definition, and the trade-off principles. Load it before scoring so
you assess against the written definition, not your gut.

## When to use this

Use it when the user wants the reliability question answered specifically, or when the
change touches a surface where things fail or grow even if they only said "review this":
retry and timeout handling, loops or pagination over data that can get large, queues and
message consumers, background workers and batch jobs, external and network calls, caching,
memory and connection allocation, or any error-handling path that has to hold when the happy
path does not.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate, and a general "is this ready to merge" question belongs there. For
mechanical, line-by-line correctness and efficiency hunting, `/code-review` is sharper and
can run alongside. This skill is intent-first: it asks whether the change should exist in
this shape at all, not only whether a line has a flaw.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the reliability score. A clean solution to the wrong problem fails even a reliability-only
   look.

3. **Assess Reliability, deeply.** Do not stop at the first issue; walk every path where this
   change can fail or grow. Are there loops, queries, or buffers whose size a caller or a
   growing dataset controls, with no ceiling (unbounded loops, queries, memory)? Does it fail
   in the right direction, loudly and early on programmer error so bugs surface, safely and
   recoverably on user or environment error so a bad input or a flaky dependency does not take
   the process down, rather than swallowing the exception and continuing on corrupt state
   (silent failure)? Is every operation a retry, a redelivery, or a re-run can reach safe to
   execute twice, or is a non-idempotent write sitting on a retry path? As load or data grows
   10x, does anything (memory, open connections, queue depth, wall-clock time) grow without a
   bound (scalability)? Score it 0 to 3 on the rubric scale, and attach a concrete finding for
   anything below 3: the location, the failure mode, and what would raise it.

4. **Verify, do not just inspect.** A reliability verdict from reading alone is dangerous:
   the failure it misses only shows up when things go wrong. Where you can, exercise the bad
   paths: make the dependency time out or throw and watch what the caller does, fire the retry
   and confirm the operation is safe the second time, feed it an input far larger than the
   happy-path one and watch memory and run time, and check that a partial failure midway leaves
   a consistent state, not a half-written one. Let what you observe set the score. Where you
   cannot (bare diff, no repo, missing deps), say so and list what you could not verify.

5. **Write the verdict**, scoped to reliability: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Reliability score of 0, or a failed gate, is
   Needs work no matter how clean the rest looks. Never say Ship on inspection alone; either
   you exercised the failure and growth paths, or the verdict names what stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you probed, give the Reliability score, and land a one-line verdict. Save the
fuller treatment for a change with real failure or growth surface. The gate and the
verification step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Reliability (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (reliability)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before reliability, always.** A change that never falls over but solves the wrong
  problem still fails. Lead with the gate, not the score.
- **Walk the failure and growth paths, not the happy path.** Reliability defects live where
  the call times out, the input arrives 100x bigger, or the job is retried after a crash, not
  in the path that reads cleanly. Go looking there on purpose.
- **Fail loud on bugs, soft on the world.** A programmer error should crash early and visibly
  so it gets fixed; a user or environment error should degrade to a safe, recoverable state.
  Swallowing the first hides bugs on corrupt state; crashing on the second turns a hiccup into
  an outage.
- **A finding names the code and its failure mode, never the author.** "This retries the
  charge call with no idempotency key, so a network blip double-bills the customer," not "you
  forgot to make it idempotent."
