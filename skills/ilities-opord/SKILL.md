---
name: ilities-opord
description: >-
  Write a PR description, commit message body, or change summary as a statement of intent —
  mission, purpose, scope boundaries, execution, verification — so an intent-first review has
  something to gate against. Use this whenever the user is about to open a PR and asks for a
  description ("write the PR description", "draft the commit message for this branch",
  "summarize this change for review", "what should the PR body say"), or wants their change
  communicated so reviewers can judge it against what it set out to do ("make this reviewable",
  "explain what this PR is for"). Also use it to retrofit intent onto an existing PR whose
  description is a bare title or a file list — the classic case where the ilities intent gate
  has nothing to gate against. This is a writing companion, not a review: it produces the
  document the ilities suite reviews against. It pairs with ilities-north-star (which pins
  intent before code exists — an OPORD is that intent restated at delivery time) and feeds
  ilities (whose intent gate reads this description first).
---

# ilities-opord — the change, stated as orders (companion)

> An **OPORD** (operations order) is the military document issued before execution: the
> mission in one sentence, the commander's intent behind it, the boundaries of the operation,
> how it will be executed, and how success will be confirmed. A PR description should be
> exactly that — because the first thing an intent-first review does is read the stated
> intent, and a PR body that says "misc fixes" or lists changed files gives the intent gate
> nothing to gate against.

This is a **writing companion**, not a review skill. It produces the document the rest of the
ilities suite consumes: `ilities-north-star` pins the intent before code exists; the OPORD
restates it at delivery time; `ilities`' intent gate reads it first and judges the change
against it.

## When to use this

Reach for it when a change is done (or nearly done) and needs to be communicated for review:
"write the PR description," "draft the commit body," "summarize this branch," "make this
reviewable." Also when an existing PR's description is a title, a file list, or a changelog —
retrofit the intent so review can gate on it.

Do **not** use it to *discover* the intent. If you cannot state what the change set out to do,
the problem is upstream — that is `ilities-north-star` (before code) or `ilities-resection`
(mid-flight), not a writing problem.

## The method — write the order

Work from evidence, not memory: read the diff, the branch's commits, and any linked issue or
North Star brief. Then write the five paragraphs. Keep the whole thing short — an OPORD is
read under time pressure; so is a PR description.

1. **Mission** — the intent in **one sentence**: what this change does and for whom/why. This
   is the sentence the intent gate will test the diff against. If you cannot write it in one
   sentence, the PR probably contains more than one mission — say so, and suggest the split.
2. **Intent** — the *why* behind the mission: the problem or win that made this worth doing.
   One short paragraph. A reviewer who reads only Mission + Intent should be able to judge
   whether the approach even aims at the right target.
3. **Scope** — the boundaries, both directions. *In:* what the change deliberately covers.
   *Out:* what it deliberately does not (deferred, out of scope, someone else's problem).
   The Out list is what lets a reviewer tell scope *discipline* from scope *creep* — an
   unlisted extra in the diff is creep; a listed deferral is a decision.
4. **Execution** — how, in brief: the approach taken and any decision a reviewer would
   otherwise have to reverse-engineer from the diff (why this design, what was tried and
   rejected, known trade-offs). Not a file-by-file narration — the diff already shows *what*
   changed; this explains *why it changed that way*.
5. **Verification** — how the change was proven: the tests run, the feature exercised
   end-to-end, what was observed. "Exercised the real flow and saw X" beats "tests pass."
   If something was *not* verified, say that too — an honest gap beats a silent one.

Cross-check before delivering: does every substantive change in the diff trace to the Mission
or appear in Scope-Out? Anything that traces to neither is the first thing an intent review
will flag — surface it to the author now, not in review.

## Output — the OPORD

```
## Mission
<one sentence: what this change does and why>

## Intent
<the problem or win behind it — why this was worth doing>

## Scope
**In:** <what this deliberately covers>
**Out:** <what this deliberately defers or excludes>

## Execution
<the approach, and any decision a reviewer would otherwise reverse-engineer>

## Verification
<what was run/exercised and what was observed; name any gaps honestly>
```

Adapt the headings to the house style if the repo has a PR template — the five pieces of
information matter, the exact headings do not.

## Principles

- **One mission per order.** A PR that needs two Mission sentences is two PRs. Recommend the
  split rather than papering over it with an "and."
- **Write for the gate.** The first reader is the intent gate — of `ilities`, or of a human
  reviewer asking "does this do what it says?" Every sentence should help answer that.
- **Scope-Out is load-bearing.** It is the difference between "the author forgot" and "the
  author decided." Never omit it just because it feels like admitting incompleteness.
- **Evidence over recollection.** Derive the OPORD from the actual diff and commits, then
  reconcile with what the author *says* it does — mismatches between the two are findings,
  not editing problems.
- **Verification is observed behavior.** "CI is green" is a fact about a pipeline; "I ran the
  import flow against a real file and the dedupe fired" is a fact about the change.
