#!/usr/bin/env python3
"""Generate each skill's references/rubric.md from the shared source in _shared/.

The ilities rubric is the shared backbone of every skill in this suite. Rather than
keep a copy of it inside each skill (which drifts the moment someone edits one copy and
forgets the rest), the rubric lives once as small body-only fragments under _shared/,
and this script assembles the right subset for each skill:

  - Flagship skills (ilities, ilities-guide, ilities-decide) get the FULL rubric: the
    intent gate, the scoring scale, all 11 dimensions, and the trade-offs.
  - Focused lens skills (ilities-<dimension>) get a FOCUSED rubric: the intent gate
    (which every skill runs first), the scoring scale, that skill's one dimension, and
    the trade-offs. About 80 lines instead of 194, so the reviewer loads only what the
    lens needs.

Usage:
  python build.py           Regenerate references/rubric.md for every skill.
  python build.py --check   Verify every copy matches what would be generated. Prints
                            the skills that are stale and exits non-zero. Use this in CI
                            so a hand-edited rubric.md (or a forgotten rebuild) fails the
                            build instead of shipping silently out of sync.

To change a rubric definition, edit the relevant file under _shared/ and re-run this
script. Never hand-edit a generated references/rubric.md: your change will be
overwritten on the next build, and --check will flag it in the meantime.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED = ROOT / "_shared"
SKILLS = ROOT / "skills"

# The 11 quality dimensions, in rubric order. `key` is the fragment filename stem and the
# suffix of the focused skill (ilities-<key>); `title` is the heading in the full rubric;
# `focus_title` is the (cleaner) heading when the dimension stands alone.
DIMENSIONS = [
    {"num": 1,  "key": "readability",     "title": "Readability",                 "focus_title": "Readability"},
    {"num": 2,  "key": "simplicity",      "title": "Simplicity (KISS / YAGNI)",   "focus_title": "Simplicity"},
    {"num": 3,  "key": "flexibility",     "title": "Flexibility & Extensibility", "focus_title": "Flexibility & Extensibility"},
    {"num": 4,  "key": "maintainability", "title": "Maintainability",             "focus_title": "Maintainability"},
    {"num": 5,  "key": "correctness",     "title": "Correctness",                 "focus_title": "Correctness"},
    {"num": 6,  "key": "testability",     "title": "Testability & Tests",         "focus_title": "Testability & Tests"},
    {"num": 7,  "key": "reliability",     "title": "Robustness & Reliability",    "focus_title": "Robustness & Reliability"},
    {"num": 8,  "key": "security",        "title": "Security",                    "focus_title": "Security"},
    {"num": 9,  "key": "performance",     "title": "Performance & Efficiency",    "focus_title": "Performance & Efficiency"},
    {"num": 10, "key": "consistency",     "title": "Consistency",                 "focus_title": "Consistency"},
    {"num": 11, "key": "observability",   "title": "Observability",               "focus_title": "Observability"},
]
DIM_BY_KEY = {d["key"]: d for d in DIMENSIONS}

# Skills that carry the full rubric. The bare `ilities` is the flagship review; guide and
# decide run the same full rubric forward and for prioritization. These share the
# `ilities-` prefix with the focused lenses, so target_skills() skips them explicitly when
# it globs for lenses.
FLAGSHIPS = ["ilities", "ilities-guide", "ilities-decide"]

GENERATED_NOTE = (
    "> **Generated file, do not edit directly.** This rubric is assembled from the shared\n"
    "> source fragments in `_shared/` by `build.py`. To change a definition, edit the\n"
    "> relevant file under `_shared/` and re-run `python build.py`, which regenerates this\n"
    "> file for every skill in the suite. Run `python build.py --check` to verify sync."
)

FULL_PREAMBLE = (
    "The shared backbone for the ilities suite. It defines the **intent gate**, the\n"
    "**11 quality dimensions**, the **scoring scale**, and the **trade-off principles** that\n"
    "`ilities`, `ilities-guide`, and `ilities-decide` all assess against."
)

FULL_TOC = (
    "## Table of contents\n\n"
    "- [The core idea: intent before quality](#the-core-idea-intent-before-quality)\n"
    "- [Part 1: The intent gate](#part-1-the-intent-gate)\n"
    "- [The scoring scale](#the-scoring-scale)\n"
    "- [Part 2: The 11 quality dimensions](#part-2-the-11-quality-dimensions)\n"
    "- [Part 3: Trade-off principles](#part-3-trade-off-principles)"
)


def frag(rel_path):
    """Read a shared fragment, trimming trailing whitespace so joins are predictable."""
    return (SHARED / rel_path).read_text(encoding="utf-8").rstrip("\n")


def section(heading, body):
    return f"{heading}\n\n{body}"


def build_full():
    parts = [
        "# ilities Rubric",
        FULL_PREAMBLE,
        GENERATED_NOTE,
        FULL_TOC,
        section("## The core idea: intent before quality", frag("core-idea.md")),
        section("## Part 1: The intent gate", frag("intent-gate.md")),
        section("## The scoring scale", frag("scoring-scale.md")),
        section("## Part 2: The 11 quality dimensions", frag("dimensions-intro.md")),
    ]
    for d in DIMENSIONS:
        parts.append(section(f"### {d['num']}. {d['title']}", frag(f"dimensions/{d['key']}.md")))
    parts.append(section("## Part 3: Trade-off principles", frag("trade-offs.md")))
    return "\n\n".join(parts) + "\n"


def build_focused(key):
    d = DIM_BY_KEY[key]
    preamble = (
        f"The slice of the ilities rubric this skill needs: the **intent gate** (run\n"
        f"first, every time), the **scoring scale**, the **{d['focus_title']}** dimension, and\n"
        f"the **trade-off principles**. For the full 11-dimension rubric, see `ilities`."
    )
    parts = [
        f"# ilities Rubric: {d['focus_title']} lens",
        preamble,
        GENERATED_NOTE,
        section("## The core idea: intent before quality", frag("core-idea.md")),
        section("## The intent gate (run this first)", frag("intent-gate.md")),
        section("## The scoring scale", frag("scoring-scale.md")),
        section(f"## The {d['focus_title']} dimension", frag(f"dimensions/{d['key']}.md")),
        section("## Trade-off principles", frag("trade-offs.md")),
    ]
    return "\n\n".join(parts) + "\n"


def target_skills():
    """(skill_dir, expected_rubric_text) for every skill present in the repo."""
    out = []
    for name in FLAGSHIPS:
        if (SKILLS / name).is_dir():
            out.append((name, build_full()))
    for path in sorted(SKILLS.glob("ilities-*")):
        if not path.is_dir():
            continue
        if path.name in FLAGSHIPS:
            # ilities-guide / ilities-decide share the prefix but carry the full rubric.
            continue
        key = path.name[len("ilities-"):]
        if key not in DIM_BY_KEY:
            print(f"  ! {path.name}: unknown dimension '{key}', not in DIMENSIONS registry", file=sys.stderr)
            sys.exit(2)
        out.append((path.name, build_focused(key)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Assemble each skill's references/rubric.md from _shared/.")
    ap.add_argument("--check", action="store_true",
                    help="Verify copies are in sync; exit non-zero if any are stale. Does not write.")
    args = ap.parse_args()

    stale, wrote = [], []
    for name, expected in target_skills():
        rubric = SKILLS / name / "references" / "rubric.md"
        current = rubric.read_text(encoding="utf-8") if rubric.exists() else None
        if args.check:
            if current != expected:
                stale.append(name)
        else:
            if current != expected:
                rubric.parent.mkdir(parents=True, exist_ok=True)
                rubric.write_text(expected, encoding="utf-8")
                wrote.append(name)

    if args.check:
        if stale:
            print("Out of sync (run `python build.py`):")
            for n in stale:
                print(f"  - skills/{n}/references/rubric.md")
            sys.exit(1)
        print(f"In sync: all {len(target_skills())} skills.")
        return

    if wrote:
        print(f"Regenerated {len(wrote)} rubric(s):")
        for n in wrote:
            print(f"  - skills/{n}/references/rubric.md")
    else:
        print("Nothing to do: all rubrics already up to date.")


if __name__ == "__main__":
    main()
