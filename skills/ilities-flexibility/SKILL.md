---
name: ilities-flexibility
description: >-
  Flexibility-only review of a change: run the intent gate first, then judge one thing
  deeply, can the likely next change be made without a rewrite? Use when the user wants an
  extensibility review ("is this extensible", "will this handle the next change", "how hard
  is it to add another case later", "should I build in an extension point here"), or is
  second-guessing an abstraction ("am I over-abstracting for the future", "is this flexible
  enough"), or when a change lands on a surface where the next variation is easy to predict
  even if they just said "review this": a switch or if/else over a type that keeps growing, a
  new provider / adapter / handler behind an interface, a config or schema other code
  branches on, a public API or plugin seam, a parser or format reader, anything shaped like
  the first of several. Checks that extension points sit where change is genuinely expected
  and only there, that nothing is abstracted for a requirement no one has, and that the
  obvious next case does not force a rewrite. Pairs with ilities-lensatic, which weighs
  whether to spend simplicity on flexibility at all; for a full 11-dimension review use
  ilities. Intent-first: a flexibility-strong change that solves the wrong problem
  still fails here.
---

# ilities: Flexibility

A flexibility-only review. Confirm the change does what it set out to do, then judge one
thing: can the likely next change be made without a rewrite? Run the intent gate first. A
change with a beautifully general extension seam that quietly solves a different problem, or
grows a plugin registry the ticket never asked for, is not mergeable no matter how
gracefully it bends to imagined future needs. Intent is the gate; flexibility is the lens
once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Flexibility &
Extensibility dimension definition, and the trade-off principles. Load it before scoring so
you assess against the written definition, not your gut.

## When to use this

Use it when the user wants the extensibility question answered specifically, or when the
change lands on a surface where the next variation is easy to predict even if they only said
"review this": a switch or if/else over a kind or type that keeps acquiring cases, a new
adapter / provider / handler behind an interface, a config or schema other code branches on,
a public API, plugin seam, or hook others build against, a parser or format reader, a
hard-coded value the next requirement will want to vary, or anything shaped like the first
of several to come.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. For the prior question, whether this code should spend any simplicity
buying flexibility at all, `ilities-lensatic` is the sharper tool; run it alongside when the
trade itself is what is in doubt. This skill is intent-first: it asks whether the change
bends where it will actually need to, not whether it bends everywhere it could.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull it
   from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say so:
   the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a "no";
   the worth-doing item is a flag. Report a gate failure before, and more prominently than,
   the flexibility score. A clean solution to the wrong problem fails even a flexibility-only
   look, and over-abstraction often is the scope failure: generality the ticket never asked
   for is exactly the "while I was here" growth the gate exists to catch.

3. **Assess Flexibility, deeply.** Do not stop at a first impression; trace where this code
   will actually be asked to change, and whether it can. Name the variation the domain
   plainly implies (another payment provider, another export format, another rule in the same
   family) and check for a clean seam: open to extension, closed to modification where it
   counts. Then check the two failures that flank a good seam. One is over-abstraction: a
   strategy interface with a single implementation, a config flag no caller sets, a generic
   pipeline built for inputs that do not exist. Flexibility no foreseeable requirement needs
   is a simplicity cost, not a virtue, and it is a finding even though it wears the face of
   foresight. The other is the opposite: the obvious next case is bolted onto a shape that
   cannot take it, so adding it means editing every call site or rewriting the core. Watch
   the tells: a switch that keeps growing with no seam, an enum other modules pattern-match
   on, branches that differ only by a constant. Score it 0 to 3 on the rubric scale, and
   attach a concrete finding for anything below 3: the location, the change it cannot absorb
   (or the one it over-built for), and what would raise it.

4. **Verify, do not just inspect.** A flexibility verdict read off the code's shape alone is
   easy to get wrong in both directions. Name the single most likely next change this code
   will face, then trace it: can it be made by adding a case, a subclass, a config entry,
   without touching what already works, or does it ripple into the core? Run the same test on
   any seam the change introduced: point at the real, expected change it is there to absorb;
   if the only change it serves is hypothetical, that is the over-abstraction finding, not a
   strength. Where you cannot trace it (a bare diff, no repo, no sight of the callers or the
   roadmap), say so and name the next change you assumed, since the whole judgment rests on
   it.

5. **Write the verdict**, scoped to flexibility: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Flexibility score of 0, or a failed gate,
   is Needs work no matter how clean the rest looks. Never say Ship on shape alone; either
   you traced the next change through, or the verdict names the change you could not trace
   and the assumption it rests on.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small or narrow diff, run
the gate, name the next change you weighed it against, give the Flexibility score, and land a
one-line verdict. Save the fuller treatment for a change that genuinely sits on a seam: an
interface, a config surface, the first of a family. The gate and the verification step
always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Flexibility (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (flexibility)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before flexibility, always.** A change with a gorgeous extension seam that solves
  the wrong problem still fails. Lead with the gate result, not the score.
- **Judge where the code must bend, not how cleverly it bends.** A general-looking
  abstraction is easy to admire and over-credit. The score comes from one question: does the
  seam line up with a change the domain is actually going to ask for? Generality with no such
  change behind it is weight, not flexibility.
- **Under- and over-abstraction fail the same test.** A switch that cannot grow and a
  strategy interface with one implementation both miss the target: flex exactly where change
  is expected, rigidity everywhere else. When in doubt favor the simpler shape and add the
  seam when the second case actually arrives; an abstraction is cheap to add on evidence and
  expensive to carry on a guess.
- **A finding names the code and its failure mode, never the author.** "Every format is a
  branch in this one function, so adding CSV means editing the shared parse-and-write path
  instead of dropping in a formatter," not "you should have made this extensible."
