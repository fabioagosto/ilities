---
name: ilities-testability
description: >-
  Testability-only review of a change: run the intent gate first, then judge one thing
  deeply, can the behavior be verified, and is it? Use when the user wants a test-focused
  review ("is this tested", "are these tests any good", "do the tests cover the new
  behavior", "can this even be tested", "is this testable", "are these tests too coupled to
  the implementation"), or when a change adds or alters behavior worth checking even if they
  just said "review this": new logic or branches with no test, a bug fix with no regression
  test, a refactor whose tests reach into private internals, or code wired so tightly to a
  database, clock, or network client that it cannot be exercised without standing up the
  whole system. Checks that new behavior is covered at the right level, that tests assert
  observable behavior rather than implementation detail, and that dependencies are
  injectable and side effects isolated. For a full 11-dimension review use ilities;
  a general "is this ready to merge" review defers to it. Intent-first: a well-tested change
  that solves the wrong problem still fails here.
---

# ilities: Testability

A testability-only review. Confirm the change does what it set out to do, then judge one
thing: can the behavior be verified, and is it? Run the intent gate first. A change with a
thorough, green suite that quietly solves a different problem, or that pins down behavior
nobody asked for, is not mergeable no matter how well it is tested. Intent is the gate;
testability is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Testability & Tests
dimension definition, and the trade-off principles. Load it before scoring so you assess
against the written definition, not your gut.

## When to use this

Use it when the user wants the testing question answered specifically, or when the change
adds or alters behavior whose verification is worth checking even if they only said "review
this": new logic, branches, or edge handling with no test; a bug fix that lands without a
regression test that would have caught it; a refactor whose tests reach into private
internals and will break on the next honest cleanup; a feature wired so tightly to its
dependencies (a real database, the wall clock, a network client, a global singleton) that
it cannot be exercised without standing up the whole system; or a test file whose
assertions you want a second read on.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. Always defer a general "is this ready to merge?" review to it rather
than answering from the testability slice alone. This skill is intent-first: it asks
whether the behavior in this change can be pinned down at all, not only whether a given test
is well written.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull
   it from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say
   so: the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a
   "no"; the worth-doing item is a flag. Report a gate failure before, and more prominently
   than, the testability score. A well-tested solution to the wrong problem fails even a
   testability-only look.

3. **Assess Testability, deeply.** Do not stop at the first missing test; walk every piece
   of behavior the change adds or alters and ask, for each, how it would be caught if it
   broke. Is the new behavior covered, and at the right level: a unit test for the branch
   logic, an integration test for the wiring, not a slow end-to-end test standing in for
   either or a mock-heavy unit test standing in for the wiring? Do the tests assert what the
   code is supposed to do, its observable outputs and effects, or do they pin how it does
   it, so any honest refactor turns them red without a real regression? Can the code even be
   reached in a test: are its dependencies injectable, or does it construct a database
   client, read the clock, or call the network itself? Are side effects isolated, or tangled
   through the logic so you cannot exercise a decision without triggering the write? Does a
   bug fix land with a regression test that fails on the old code and passes on the new?
   Score it 0 to 3 on the rubric scale, and attach a concrete finding for anything below 3:
   the location, the failure mode, and what would raise it.

4. **Verify, do not just inspect.** A testability verdict from reading test names alone is
   the most misleading thing this skill can produce: a green-looking suite can assert
   nothing that matters. Where the environment allows, run the tests: confirm they exist,
   pass, and exercise the new behavior rather than skipping it. Break the change's own logic
   on purpose, revert a line or flip a condition, and check that a test goes red; one that
   stays green is not testing it. Read a few assertions to confirm they check behavior, not
   internal shape. Where you cannot run anything (a bare diff, no repo, missing deps), say
   so and list what you could not verify.

5. **Write the verdict**, scoped to testability: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Testability score of 0, or a failed gate,
   is Needs work no matter how clean the rest looks. Never say Ship on inspection alone;
   either you ran the tests and watched them cover the behavior, or the verdict names what
   stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you probed, give the Testability score, and land a one-line verdict. Save the
fuller treatment for a change with real behavior to cover. The gate and the verification
step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Testability (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (testability)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before testability, always.** An exhaustively tested change that solves the
  wrong problem still fails. Lead with the gate, not the score.
- **Green is not the same as covered.** A passing suite tells you the tests that exist pass,
  not that the new behavior is exercised. The gap lives where no assertion reaches: the new
  branch, the error path, the fix that shipped with no regression test. Go looking there,
  and make a line fail to prove a test would have caught it.
- **Coverage that pins implementation is a tax, not an asset.** A test that asserts on
  private structure or restates the code breaks on the next honest refactor without any real
  regression, and trains the team to delete tests to get the build green. Count that kind
  against the score, not for it.
- **A finding names the code and its failure mode, never the author.** "The retry loop has
  no test, so a change to its backoff could silently stop it retrying and nothing would
  catch the regression," not "you didn't write a test for this."
