---
name: ilities-observability
description: >-
  Observability-only review of a change: run the intent gate first, then judge one thing
  deeply, when it breaks in production can we tell what happened? Use when the user wants
  an observability review ("can we debug this in prod", "are the logs good enough here",
  "is this error message actionable", "will we know if this breaks", "is this observable",
  "does this swallow the error"), or when a change touches a surface where a silent failure
  would sting even if they just said "review this": error handling and catch blocks,
  retries and fallbacks, background jobs, queues and cron, outbound network and I/O calls,
  third-party integrations, or data pipelines where a dropped record leaves no trace.
  Checks for meaningful logs, metrics, and errors at the boundaries that matter, catch
  blocks that keep the cause instead of losing it, and error messages an on-call engineer
  could actually act on. For a full 11-dimension review use ilities, which also
  owns a general "is this ready to merge?" question. Intent-first: an observability-strong
  change that solves the wrong problem still fails here.
---

# ilities: Observability

An observability-only review. Confirm the change does what it set out to do, then judge one
thing: when it breaks in production, can we tell what happened? Run the intent gate first. A
change that logs beautifully and emits a metric for everything but quietly solves a
different problem, or smuggles in an unrelated refactor, is not mergeable no matter how
well-instrumented the code is. Intent is the gate; observability is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Observability
dimension definition, and the trade-off principles. Load it before scoring so you assess
against the written definition, not your gut.

## When to use this

Use it when the user wants the observability question answered specifically, or when the
change touches a surface where a silent failure would sting even if they only said "review
this": error handling and catch blocks, retries and fallbacks, background jobs, queues and
schedulers, outbound network and I/O calls, third-party integrations, data pipelines and
migrations, or anything that can fail on a path no one is watching.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate, and a general "is this ready to merge?" question belongs there too. This
lens answers only one thing: whether a production failure in this change would be
diagnosable. It is intent-first: it asks whether the change can be understood when it fails,
not only whether a line reads cleanly.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the observability score. A clean solution to the wrong problem fails even an
   observability-only look.

3. **Assess Observability, deeply.** Do not stop at the first missing log; walk every
   boundary in the change where something can fail out of sight. Is there a silent boundary
   where a production failure would leave no trace, no log, no metric, no error, for the
   engineer paging through at 3am? Does any `catch` swallow the exception, or re-raise a bare
   message that drops the original cause and stack? When something is logged or thrown, does
   the message say what failed and give the reader something to act on, or just "an error
   occurred"? Are the boundaries that matter, the outbound call that timed out, the retry
   that gave up, the job that skipped a record, the fallback that silently kicked in,
   emitting anything you could find later? Score it 0 to 3 on the rubric scale, and attach a
   concrete finding for anything below 3: the location, the failure mode, and what would
   raise it.

4. **Verify, do not just inspect.** An observability verdict from reading alone is the easy
   one to get wrong: instrumentation that looks present can still say nothing useful when it
   fires. Where you can, trigger the failure path and watch what surfaces: force the
   exception, make the dependency time out, feed the bad record, and read what actually lands
   in the logs, metrics, or error channel. Then read each error message the way the on-call
   engineer will, with no context but that one line, and ask whether it names what failed and
   what to do next. Where you cannot (bare diff, no repo, missing deps), say so and list what
   you could not verify.

5. **Write the verdict**, scoped to observability: Ship, Ship with follow-ups, or Needs
   work, plus the single most important thing to fix. An Observability score of 0, or a
   failed gate, is Needs work no matter how clean the rest looks. Never say Ship on
   inspection alone; either you triggered the failure path and saw what it emits, or the
   verdict names what stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you probed, give the Observability score, and land a one-line verdict. Save the
fuller treatment for a change with real failure surface. The gate and the verification step
always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Observability (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (observability)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before observability, always.** A perfectly instrumented change that solves the
  wrong problem still fails. Lead with the gate, not the score.
- **Read the failure paths; the happy path tells you nothing.** Observability only pays out
  when something breaks, so the code that reads cleanly on success is the code you learn the
  least from. Go to the `catch`, the timeout branch, the retry-exhausted case, the
  empty-result path; that is where you find out whether a real incident leaves a trail or a
  blank.
- **A swallowed error is a lie of omission.** A `catch` that logs nothing, or collapses the
  cause into a generic string, tells production everything is fine while it is not. Silence
  at a boundary is a finding on its own, even when nothing is failing today, because the day
  it does, no one will know where to look.
- **A finding names the code and its failure mode, never the author.** "This `catch`
  re-raises `RuntimeError('request failed')` and discards the original exception, so a 3am
  page shows no status code, host, or stack to act on," not "you didn't log enough here."
