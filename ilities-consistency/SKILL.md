---
name: ilities-consistency
description: >-
  Consistency-only review of a change: run the intent gate first, then judge one thing
  deeply, does it fit the codebase? Use when the user wants a fit review ("does this fit our
  conventions", "is this consistent with the rest of the codebase", "am I reinventing
  something we already have", "does this match how we do X elsewhere", "is this the
  established pattern here"), or when a change lands where fit is what's at stake even if
  they just said "review this": a new helper that may already exist, a second way to do data
  access / error handling / logging / config the repo already does one way, a module whose
  naming or structure or directory placement departs from its siblings, or a dependency that
  duplicates one already in the tree. Checks that the change follows the patterns,
  conventions, and layout already established, and does not open a parallel path to something
  the codebase already has. For a full 11-dimension review use ilities; for
  mechanically flagging a reinvented or duplicated helper, /code-review and /simplify are
  sharper and run alongside. Intent-first: a consistency-strong change that solves the wrong
  problem still fails here.
---

# ilities: Consistency

A consistency-only review. Confirm the change does what it set out to do, then judge one
thing: does it fit the codebase? Run the intent gate first. A change that slots perfectly
into the repo's conventions but quietly solves a different problem, or smuggles in an
unrelated refactor while it tidies, is not mergeable no matter how well it matches the
surrounding code. Intent is the gate; consistency is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Consistency
dimension definition, and the trade-off principles. Load it before scoring so you assess
against the written definition, not your gut.

## When to use this

Use it when the user wants the fit question answered specifically, or when the change lands
somewhere fit is what's at stake even if they only said "review this": a new utility or
helper the repo may already provide, a second way to do something it already does one way
(data access, error handling, config loading, logging, validation), a module whose naming,
structure, or directory placement diverges from its siblings, or an import that overlaps a
dependency already in the tree.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. For mechanically flagging a reinvented or duplicated helper,
`/code-review` and `/simplify` are sharper and can run alongside. This skill is intent-first:
it asks whether the change reads like the code around it, not only whether one helper
happens to duplicate another.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the consistency score. A clean solution to the wrong problem fails even a
   consistency-only look.

3. **Assess Consistency, deeply.** Do not stop at the first mismatch; read the change
   against its neighbors and against how the repo already does this kind of work. Does it
   introduce a new pattern where an established one sits a few files over? Does it reinvent a
   utility (a date formatter, an HTTP client wrapper, a result type) the repo already ships
   and everyone imports? Does it add a second way to do something the codebase already does
   one way, so the next reader has to know both? Does its structure, naming, or directory
   placement fight the conventions around it, a flat file where the repo groups by feature,
   camelCase where the rest is snake_case, a reach into another module's internals where
   everything else goes through the seam? Score it 0 to 3 on the rubric scale, and attach a
   concrete finding for anything below 3: the location, the divergence, and the existing
   pattern it should match.

4. **Verify, do not just inspect.** A consistency verdict from the diff alone misses the
   thing that decides it: what the rest of the repo already does. Where you can, go look:
   grep for the utility you suspect is reinvented, open two or three sibling files for the
   established pattern, check how config, errors, and logging are handled elsewhere before
   you call the approach novel, and follow the directory layout to see where the file should
   live. Let what the surrounding code does set the score. Where you cannot (bare diff, no
   repo access), say so and list what you could not check against the existing patterns.

5. **Write the verdict**, scoped to consistency: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Consistency score of 0, or a failed gate,
   is Needs work no matter how clean the rest looks. Never say Ship on inspection alone;
   either you compared the change against the repo's existing patterns, or the verdict names
   what stays unchecked.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you compared it against, give the Consistency score, and land a one-line verdict.
Save the fuller treatment for a change that adds real surface: a new module, a new utility,
a new way of doing something the repo already had a way to do. The gate and the verification
step always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Consistency (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (consistency)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before consistency, always.** A change that matches every convention in the repo
  and still solves the wrong problem fails. Lead with the gate, not the score.
- **Compare against the code, not your taste.** The convention that matters is the one
  already in the tree, not the one you would have chosen. Read the neighbors and confirm the
  pattern exists before you call something a divergence; confirm it matches before you bless
  it.
- **A second way to do it is a cost, even when it is better.** Every parallel way of doing
  the same thing is one more thing the next reader has to learn and keep in sync. If the new
  way really is better, the change is a migration of the old one, not a fresh island beside
  it: separate, larger work than the diff in front of you.
- **A finding names the code and its failure mode, never the author.** "This adds a second
  HTTP client wrapper next to the `apiClient` every other service imports, so callers now
  have to know which one to reach for," not "you should have known we already had one."
