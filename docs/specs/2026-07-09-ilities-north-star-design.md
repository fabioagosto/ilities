# ilities-north-star — design

**Date:** 2026-07-09
**Status:** Approved (brainstorming), pending implementation plan
**Author:** fabioagosto (with Claude Code)

## Summary

`ilities-north-star` is a new skill in the ilities suite: a **forward, interactive
intent interrogation**. Before any code exists, it grills the user — one pointed question
at a time — until it can write a **North Star brief**: the win the work is steering
toward, the one-sentence intent that serves it, the scope boundaries, and the decisions
the interrogation resolved. It scores nothing. Its job is to make the intent so clear that
the intent gate passes by construction downstream.

It is the new front of the suite's pipeline:

> **`ilities-north-star`** (pin the star) → **`ilities-guide`** (build to it) → **`ilities`** (review against it)

## Naming (locked)

The action-tier skills carry evocative, Air-Force-flavored names; the 11 dimension lenses
stay literal because they *are* the rubric. Decisions made during brainstorming:

- **`ilities-north-star`** — the new skill's name. Chosen over `spears` and `criticality`;
  names the outcome (the destination you steer by), not the mechanism.
- **`ilities-lensatic`** — rename of `ilities-decide`, tracked as a **separate, contained
  change** (not part of adding north-star). A lensatic compass is the military field
  compass; the skill's job is choosing *which lenses* to apply, so the name is both an
  AF/navigation term and a pun on the suite's own "lenses."
- **`ilities-azimuth`** — rename of `ilities-guide`. An azimuth is the precise bearing you
  *follow* to reach the objective; guide's whole discipline is holding the intent without
  drifting. Rides with `decide → lensatic` as the same separate naming-pass change.
- **`ilities`** — kept; the hero name. (`north-star → lensatic → azimuth` is a literal
  land-nav sequence: sight the star, shoot the azimuth on the compass, follow it.)
- **AF vocabulary** — dropped. Considered threading terms like "mission brief" / "Go-No-Go"
  through the prose; cut to keep the skills' language plain.

## The gap it fills

Every existing ilities skill is **backward-facing** — it reviews a change that already
exists (or, in `ilities-guide`'s case, steers code as it's being written against a *known*
intent). None of them help when the intent itself is still fuzzy. That is the most
expensive failure the suite is built to catch — "a clean solution to the wrong problem" —
and today it can only catch it *after* the code is written. `ilities-north-star` catches it
before, by refusing to let the work start until the North Star is explicit.

This is the same insight the intent gate encodes, run *forward and interactively* instead
of as an after-the-fact checklist. The Pragmatic Programmer line — "no one knows exactly
what they want" — is precisely the intent problem, and interrogation is how you resolve it.

## Position and routing

The one skill it sits closest to is `ilities-guide`, so the routing line must be sharp:

- **`ilities-guide`** assumes you *know what you're building* and want to build it to the
  rubric. Its input is a stated intent; its output is well-built code.
- **`ilities-north-star`** is for when the intent is *still fuzzy*. Its input is a vague
  idea; its output is a crisp North Star brief. It runs *before* guide.

**Trigger phrasing** for the description: "grill me on this idea," "pressure-test what I'm
about to build," "help me pin down what this actually needs to do," "what's the north star
here," "I have a rough idea, interrogate it before I start," "am I even solving the right
problem?"

The description must emphasize **interrogation + fuzzy/unstated intent + producing a North
Star** so it does not steal routing from `ilities-guide` (known intent) or, for users who
also run Superpowers, from `superpowers:brainstorming` (broad collaborative design).
`ilities-north-star` is narrower and adversarial: it interrogates toward a checkable intent
artifact tied to the ilities gate.

## Behavior — the grilling method

The behavioral core, to live in the bespoke body of `SKILL.md`:

- **One question at a time.** Adaptive — each question follows from the last answer, not a
  fixed questionnaire.
- **Every question must be load-bearing.** A question earns its place only if its answer
  could change the North Star, a scope boundary, or a locked decision. A question whose
  answer moves nothing is noise. (Same ethos as `ilities-decide` / `ilities-lensatic`: "a
  priority list that includes everything is worthless.")
- **What it probes:**
  - **The win** — how will you know this worked? (surfaces the North Star)
  - **The why-not** — why this and not the simpler or adjacent thing? (catches
    wrong-problem)
  - **The boundary** — what is explicitly *not* part of this? (kills scope creep
    pre-emptively)
  - **Hidden assumptions** — "you said X; what has to be true for that?"
  - **The real need** — who hits this, and what do they actually need?
- **Termination:** stop when the North Star brief is writable **and** the four intent-gate
  blockers would pass (intent stated / matches a real need / scope contained / solvable at
  the goal level). The gate is the finish line.
- **Guardrails against over-grilling:**
  - If the user genuinely does not know something, **park it** as an explicit open question
    in the brief rather than interrogating in circles.
  - Stop when the user says enough.
  - Do not grill past the point of value — the brief being writable *is* the point.

## Output — the North Star brief

```
## North Star
<1–2 sentences: the win, where this is headed — the thing you steer by>

## This change's intent
<one sentence: what we'll do now to serve the star — the line the intent gate checks>

## Scope
In:  <what this change covers>
Out: <what it deliberately does not — the follow-ups, the "while I'm here" temptations>

## Decisions locked
- <branch the grilling resolved> → <the call>

## Open questions
- <anything the user couldn't answer yet, parked rather than guessed>
```

The two altitudes (North Star + this change's intent) are the distinctive move: forcing the
link between the larger win and the immediate work is exactly where "locally sensible but
serves the wrong goal" gets caught. The brief maps straight onto the intent gate's blockers,
so `ilities-guide` and `ilities` inherit a clean intent for free.

## Architecture — file layout

A **third skill category** alongside the existing two (full-rubric flagships;
one-dimension lenses):

```
skills/ilities-north-star/
  SKILL.md                 # bespoke: frontmatter + grilling method + brief format + principles
  references/rubric.md     # GENERATED by build.py — intent-only slice
```

`ilities-north-star`'s reference material is a **narrow slice** of the rubric: the core idea
(`_shared/core-idea.md`) + the intent gate (`_shared/intent-gate.md`). **No dimensions, no
scoring scale, no trade-offs** — it does not score, it interrogates.

## build.py change

`build.py` today knows two shapes: `build_full()` (flagships) and `build_focused(key)`
(lenses, keyed by dimension). `ilities-north-star` is neither, and its suffix `north-star`
is not a dimension key — so the existing lens glob would hit
`unknown dimension 'north-star'` and `sys.exit(2)`. The change:

1. Add an intent-skill registry and builder:
   ```python
   INTENT_SKILLS = ["ilities-north-star"]

   def build_intent():
       parts = [
           "# ilities Rubric: the intent gate",
           <preamble: "the slice north-star needs — the core idea and the intent gate">,
           GENERATED_NOTE,
           section("## The core idea: intent before quality", frag("core-idea.md")),
           section("## The intent gate", frag("intent-gate.md")),
       ]
       return "\n\n".join(parts) + "\n"
   ```
2. In `target_skills()`, emit `(name, build_intent())` for each present `INTENT_SKILLS`
   entry (mirroring the `FLAGSHIPS` handling).
3. In the lens glob, **skip `INTENT_SKILLS`** the same way `FLAGSHIPS` is skipped, so
   `north-star` is never treated as a missing dimension.

`python build.py --check` must stay green in CI after the change.

## Other files

- **README.md** — add `ilities-north-star` to the suite. It is a new category (not a
  flagship, not a lens); give it a short "Forward intent" entry and place it at the front of
  the pipeline narrative (north-star → guide → review).
- **Plugin / marketplace manifest** — verify whether skills are auto-discovered from
  `skills/` or listed explicitly (`.claude-plugin/`, `plugin.json`, marketplace file). If
  listed explicitly, add `ilities-north-star`. (To confirm during implementation.)

## Non-goals (YAGNI)

- **No scoring, no dimensions.** It pins intent; quality scoring is `ilities`' job.
- **Not a spec generator.** The brief is deliberately tighter than a spec (that is Matt
  Pocock's `to-spec` territory). No risk register, no rejected-alternatives log.
- **No shared grilling engine.** Matt factors a reusable `grilling` loop because two skills
  use it; here there is exactly one consumer, so the method lives inline in `SKILL.md`. If a
  second griller (e.g. a backward red-team) ever appears, factor a `_shared/` fragment then.
- **Forward only.** No backward "red-team an existing diff" mode — that would duplicate
  `ilities`.

## Open questions / risks

- **Routing overlap with `ilities-guide`.** Mitigated by the description emphasis above
  (fuzzy/unstated intent vs known intent). Worth a real trigger-accuracy check once written.
- **Routing overlap with `superpowers:brainstorming`** for users who run both. Acceptable:
  within the standalone ilities plugin, north-star is *the* forward intent tool, and its
  adversarial + North-Star-artifact framing differentiates it.
