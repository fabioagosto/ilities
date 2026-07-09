---
name: ilities-resection
description: >-
  Fix your position mid-build: when you have been working a while and lost the thread, take a
  quick bearing on where the change actually stands versus the intent it set out to serve, and
  report whether you are still on course or have drifted — and if drifted, where it started. Use
  this whenever you are partway through and unsure you are still on track: "am I still on target",
  "have I gone off-course on this refactor", "does this still match what I set out to do", "I've
  been at this a while, check I haven't drifted". It sights known references — the stated intent
  (or North Star), the codebase's conventions, and what is actually done so far — crosses them,
  and returns a short position fix. This is a light, mid-flight check, not the full ilities review
  (the thorough, scored, merge-readiness audit) and not ilities-azimuth (which holds the line
  continuously as you write); reach for it as a discrete "where am I?" checkpoint during the work.
  Intent-first: it measures drift against the intent, so if the intent was never clear it says so
  and points you to pin it first.
---

# ilities Resection

A quick position fix for work in flight. You have been building for a while and are no longer
sure you are still on course. Resection answers one question — *where am I right now, relative to
where I set out to go?* — by sighting known references and crossing them, the way you fix an
unknown position on a map from two or three known landmarks. It is deliberately light: not a
scored review, just a bearing.

Read `references/rubric.md` for the core idea (intent before quality) and the intent gate. Drift
is measured against the intent; the gate is what "on course" means.

## When to use this

Reach for it mid-change, when you have lost the thread and want a fast read on whether you have
drifted: a refactor that has been sprawling, a feature that keeps growing, a session long enough
that the original goal has gone fuzzy. Triggers: "am I still on track," "have I gone off-course,"
"does this still match what I set out to do," "I've been at this a while — check I haven't
drifted."

It is a *checkpoint*, not a verdict. For the thorough, scored, is-this-mergeable question, use
`ilities` (the full review). For holding the line continuously as you write, that is
`ilities-azimuth`. Resection is the discrete "where am I right now?" you run *during* the work.

## The method — take the fix

1. **Sight your references.** The stated intent or North Star; the conventions of the surrounding
   code; what is actually done so far.
2. **Cross them.** Does the work so far still serve the intent? Has scope crept in? Have you
   drifted from the codebase's conventions? Is the *intent itself* still right, or has building it
   revealed it was the wrong target?
3. **Report the position.** On course, or drifted — and if drifted, name where the divergence
   began (the file or decision it started at) and the smallest correction back on course.

If the intent was never made explicit, resection has nothing to take a bearing against. Say so,
and send the user to `ilities-north-star` to pin it before continuing.

## Output — the position fix

```
## Position
<on course | drifted>

## Bearing to intent
<how the work so far measures against the stated intent / North Star>

## Drift
<where the divergence began, if any — the file or decision where it started>

## Correction
<the smallest move back on course, or "hold current heading" if on course>
```

## Principles

- **A fix is a bearing, not an audit.** Keep it quick. If the change needs a full scored review,
  that is `ilities`, not this.
- **Measure drift against intent, not taste.** The reference is the stated goal and the codebase's
  conventions, not your preferences.
- **Name where the drift began.** "Off course" is not actionable; "it diverged when the helper
  grew a second responsibility in `x.py`" is.
- **No intent, no fix.** You cannot resect a position without landmarks. If the intent was never
  clear, pin it first with `ilities-north-star`.
