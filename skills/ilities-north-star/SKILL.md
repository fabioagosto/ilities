---
name: ilities-north-star
description: >-
  Interrogate a fuzzy idea into a clear, checkable intent BEFORE any code is written: grill
  the user one pointed question at a time until the change's North Star — the win it steers
  toward, the one-sentence intent that serves it, and the scope boundaries — is explicit, then
  hand back a short North Star brief. Use this whenever the intent is still vague and worth
  pinning down: "help me figure out what I'm actually building", "grill me on this idea",
  "pressure-test this before I start", "what's the north star here", "am I even solving the
  right problem". This is the forward front of the suite: it runs before ilities-azimuth (which
  assumes a known intent and builds to it) and before ilities (which reviews a change that
  already exists). The distinguishing move is the interrogation: it refuses to let work start
  until the intent would pass the intent gate, catching a clean solution to the wrong problem
  before a line of code exists rather than in review. Prefer this over jumping straight to
  building whenever you cannot yet state the change's intent in one sentence.
---

# ilities North Star

Pin the intent before you build, by interrogation. Most work goes wrong not in the code but in
the intent behind it — a change that is locally sensible yet serves the wrong goal. This skill
refuses to let the building start until the intent is explicit enough to pass the intent gate.
It scores nothing; it grills, one question at a time, until it can write a **North Star brief**
the rest of the suite can steer by.

Read `references/rubric.md` for the core idea (intent before quality) and the intent gate. The
gate is your finish line: keep grilling until its four blockers would pass.

## When to use this

Reach for it when the intent is still fuzzy and the work is worth getting right: a feature or
change you are about to start but cannot yet state in one sentence, an idea that "sounds right"
but has not been pressured, a ticket whose real goal is unclear. Triggers: "help me figure out
what I'm building," "grill me on this," "pressure-test this idea," "what's the north star
here," "am I solving the right problem."

This is the forward *front* of the suite. It runs before `ilities-azimuth`, which assumes the
intent is already known and builds to it, and long before `ilities`, which reviews a change
that already exists. If you can already state the intent in one clean sentence, skip this and
go straight to building.

## The method — the grill

Interrogate, do not brainstorm. The job is to extract and sharpen the intent that is already
latent in the user's head, not to invent scope.

1. **Ask one question at a time.** Adaptive — each question follows from the last answer, never
   a fixed questionnaire. Wait for the answer before the next.
2. **Make every question load-bearing.** A question earns its place only if its answer could
   change the North Star, a scope boundary, or a decision. A question whose answer moves nothing
   is noise; do not ask it.
3. **Probe the places intent hides:**
   - **The win** — how will you know this worked? (surfaces the North Star)
   - **The why-not** — why this and not the simpler or adjacent thing? (catches the wrong problem)
   - **The boundary** — what is explicitly *not* part of this? (kills scope creep before it starts)
   - **The assumptions** — "you said X; what has to be true for that to hold?"
   - **The real need** — who actually hits this, and what do they need?
4. **Stop at the finish line.** Terminate when you can write the brief *and* the four intent-gate
   blockers would pass: intent stated, matches a real need, scope contained, solvable at the goal
   level. Do not grill past that point — the brief being writable is the point.

**Guardrails.** If the user genuinely does not know something, park it as an open question in the
brief rather than interrogating in circles. Stop when the user says enough. You are pinning the
intent, not designing the solution — resist drifting into implementation.

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

The two altitudes — the North Star and this change's intent — are the point. Forcing the link
between the larger win and the immediate work is exactly where "locally sensible but serves the
wrong goal" gets caught, before any code exists. The brief maps straight onto the intent gate's
blockers, so `ilities-azimuth` and `ilities` inherit a clean intent for free.

## Principles

- **The intent is the risk, not the code.** The most expensive mistakes are decided before the
  first line is written. Spend your attention here.
- **Extract, do not invent.** Grill the intent out of the user; do not add scope they did not ask
  for. A brief bigger than the need is its own failure.
- **A question that moves nothing is noise.** If the answer cannot change the brief, do not ask it.
- **Stop when the gate would pass.** The finish line is a writable brief that clears the four
  blockers — not a perfect one, and not an endless interview.
