---
name: ilities-readability
description: >-
  Readability-only review of a change: run the intent gate first, then judge one thing
  deeply, can a teammate understand this without the author explaining it? Use when the user
  wants a clarity-focused review ("is this readable", "is this clear", "can someone else
  follow this", "are these names good", "is this too nested", "would a teammate understand
  this without me explaining it"), or when a change lands on a surface where the next reader
  is what matters even if they just said "review this": dense or cryptic naming, deeply
  nested or branchy control flow, comments that narrate the code instead of its reasons,
  commented-out blocks, or new code written in a style the surrounding module does not use.
  Checks that names say what things are and do, that control flow stays shallow enough to
  follow, that comments explain why rather than what, and that the change reads like the code
  around it. For a full 11-dimension review use ilities; this lens answers only
  whether the change is clear to the next reader, and defers any "is this ready to merge"
  call to that fuller review. Intent-first: a clean, readability-strong change that solves
  the wrong problem still fails here.
---

# ilities: Readability

A readability-only review. Confirm the change does what it set out to do, then judge one
thing: can a teammate understand this without the author explaining it? Run the intent gate
first. A change whose every name is crisp and whose flow reads top to bottom, but which
quietly solves a different problem or folds in an unrelated rename, is not mergeable no
matter how well it reads. Intent is the gate; readability is the lens once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Readability
dimension definition (its signals and smells), and the trade-off principles. Load it before
scoring so you assess against the written definition, not your gut.

## When to use this

Use it when the user wants the clarity question answered specifically, or when the change
lands somewhere the next reader is what matters even if they only said "review this": naming
that has to be decoded, control flow that has grown deep or branchy, comments that restate
the code instead of its reasons, commented-out code left in place, or new code written in a
personal style the surrounding module does not share, anywhere a future maintainer will read
this without the author in the room.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. This lens answers only whether the change is clear to the next reader,
and defers any "is this ready to merge" verdict to that fuller review. It asks whether the
code can be understood in this shape, not whether every other quality bar is met.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the readability score. A clean solution to the wrong problem fails even a
   readability-only look.

3. **Assess Readability, deeply.** Do not stop at the first awkward name; read the whole
   change the way the person who inherits it will. Do the names say what things are and do,
   or do they need decoding (`d`, `tmp2`, a boolean called `flag`, a handler named
   `handle`)? Has the control flow grown deep or tangled, the real logic buried several
   levels in under stacked conditions? Do the comments explain why (the constraint, the edge
   case, the reason it is not the obvious way), or just restate the what the next line
   already states? Is there commented-out code left as sediment with no note on why it stays?
   Does the change read like the code around it, or is it a personal style, different naming
   and structure and idioms, dropped into a module written in another? Score it 0 to 3 on the
   rubric scale, and attach a concrete finding for anything below 3: the location, what made
   you stop, and what would make it read cleanly.

4. **Verify, do not just inspect.** A readability verdict from the author's chair is the most
   misleading thing this skill produces: you already know what the code means, which is
   exactly why you are the wrong judge of it. Read the change cold, as a teammate seeing it
   for the first time, and mark every place you had to stop and decode: the name you traced
   to its definition, the branch you re-read, the block whose purpose came clear only three
   lines later. Then read the surrounding file and check the new code reads like its
   neighbors. Where you lack the context to judge (an abbreviation that may be a domain term
   the team knows, a convention a bare diff does not show), say so rather than scoring as
   though you were sure.

5. **Write the verdict**, scoped to readability: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Readability score of 0, or a failed gate,
   is Needs work no matter how clean the rest looks. Never call it clear just because you
   followed it; you carry context the next reader will not, so either you read it cold, or
   the verdict names whose clarity you could not stand in for.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you read cold and where you stumbled, give the Readability score, and land a
one-line verdict. Save the fuller treatment for a change with real surface for a future
reader to get lost in. The gate and the cold read always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Readability (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you read cold and where you had to stop and decode, or what you lacked context to judge>

## Verdict (readability)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before readability, always.** A change that reads beautifully but solves the
  wrong problem still fails. Lead with the gate result, not the score.
- **Read it cold; you are the wrong judge of your own code.** You understand it because you
  wrote it or carry the context, which is exactly why your comfort proves nothing. The bar
  is the next reader who has neither, so read as them and note every place you stall.
- **Match the codebase, not your taste.** Readability is relative to its surroundings: code
  that is clean in a style the module does not use is still hard to read here. Judge the
  change against the conventions around it, not your own preferred idioms.
- **A finding names the code and its failure mode, never the author.** "This function nests
  four levels deep and the early-return case is buried under two conditions, so the reader
  has to hold the whole thing in mind to find it," not "you wrote this in a confusing way."
