# ilities — suite map

The ilities suite is **intent-first code review**: know where you're going before you move,
and whether you got there. That's land navigation — so the action-tier skills are named for
it. This map is the living picture of the suite: what each skill is, when to reach for it,
and where it sits in the mission.

> **Naming principle — two tiers.** The 11 dimension skills stay *literal* because they **are**
> the rubric (you can't rebrand "security"). The action-tier skills — the tools that move you
> through a change — carry the land-nav / Air Force names. Brand energy lives in the action
> tier; the lens tier stays plain by design.

## Action tier (the land-nav mission)

| Skill | Metaphor | What it does | Reach for it when | Status |
|-------|----------|--------------|-------------------|--------|
| **`ilities-north-star`** | the destination — the star you steer by | Pin *fuzzy* intent before code exists; grill one question at a time and produce a **North Star brief** | "what am I really building here", "grill me on this idea", "am I even solving the right problem" | **built** |
| **`ilities-lensatic`** | the compass — reads your bearing, picks your lenses | Decide which of the 11 lenses to concentrate on for this change | "what should I optimize for", "is it worth abstracting this", "how much error handling does this need" | renamed from `decide` |
| **`ilities-azimuth`** | the bearing you hold to the objective | Build to standard without drifting from the stated intent; the forward companion to `ilities` | "build X properly", "do this the right way", "self-review before I open the PR" | renamed from `guide` |
| **`ilities-resection`** | fix your unknown position from known landmarks | **Mid-flight drift check**: sight the north star + conventions + what's done, cross them, report exactly where you are — on-azimuth or drifted, and where the drift began | "am I still on track", "have I gone off-course on this refactor", "where does this stand vs what I set out to do" | **built** |
| **`ilities`** | the debrief — did the sortie achieve its objective? | Full intent-first review of a finished change: intent gate → score 11 dimensions → verdict | "review this", "is this ready to merge", "does this actually do what it should" | hero, kept |

## Lens tier (the rubric — literal, locked)

The 11 quality dimensions, each its own focused skill, named for what it is:
`readability` · `simplicity` · `flexibility` · `maintainability` · `correctness` ·
`testability` · `reliability` · `security` · `performance` · `consistency` · `observability`.

`ilities-lensatic` is the compass that tells you *which of these lenses* to point at a given
change.

## The mission, end to end

The names aren't decoration — run in order, they're a literal land-nav sequence:

1. **`north-star`** — sight the star. *What's the win?*
2. **`lensatic`** — shoot your azimuth on the compass. *Which lenses matter here?*
3. **`azimuth`** — follow the bearing. *Build without drifting.*
4. **`resection`** — periodic position fix. *Still on the star, or have I drifted?*
5. **`ilities`** — debrief. *Did we hit the objective?*

## Roadmap

All three landed in this pass:

1. ✅ **Added `ilities-north-star`** — spec: `docs/specs/2026-07-09-ilities-north-star-design.md`.
2. ✅ **Naming pass** — `decide → lensatic`, `guide → azimuth` (all cross-references updated).
3. ✅ **Added `ilities-resection`** — the mid-flight drift check.

`python build.py --check` is green: all 16 skills in sync.
