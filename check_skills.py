#!/usr/bin/env python3
"""Check every skill's frontmatter for the two things Claude Code silently punishes.

  - `description` longer than 1024 characters is truncated at load time, and the tail is
    where each skill's routing text lives (the deferral to `ilities`, the closing
    intent-first clause). A truncated description still installs; it just stops routing.
  - `name` that does not match the skill's directory installs under a name nobody expects.

No third-party dependency: the frontmatter here is plain `key: value` pairs plus `>-` / `|`
block scalars, and that is all this parses. Exits non-zero and lists the offenders so CI
fails loudly instead of the skill failing quietly.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / "skills"
MAX_DESCRIPTION = 1024


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    return m.group(1).splitlines() if m else None


def field(lines, key):
    """Value of a top-level frontmatter key, folding `>` and joining `|` block scalars."""
    for i, line in enumerate(lines):
        if not line.startswith(f"{key}:"):
            continue
        value = line[len(key) + 1:].strip()
        if value in (">", ">-", ">+", "|", "|-", "|+"):
            block = []
            for cont in lines[i + 1:]:
                if cont.strip() == "" or cont.startswith((" ", "\t")):
                    block.append(cont.strip())
                else:
                    break
            joiner = " " if value.startswith(">") else "\n"
            return joiner.join(part for part in block if part).strip()
        return value.strip("'\"")
    return None


def main():
    problems = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        skill = skill_md.parent.name
        lines = frontmatter(skill_md.read_text(encoding="utf-8"))
        if lines is None:
            problems.append(f"{skill}: no YAML frontmatter")
            continue
        name = field(lines, "name")
        if name != skill:
            problems.append(f"{skill}: name is {name!r}, directory is {skill!r}")
        desc = field(lines, "description")
        if not desc:
            problems.append(f"{skill}: missing description")
        elif len(desc) > MAX_DESCRIPTION:
            problems.append(
                f"{skill}: description is {len(desc)} chars, over the {MAX_DESCRIPTION} "
                f"limit by {len(desc) - MAX_DESCRIPTION}; the tail gets truncated"
            )
    if problems:
        print("Skill frontmatter problems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"Skill frontmatter OK: {len(list(SKILLS.glob('*/SKILL.md')))} skills.")


if __name__ == "__main__":
    main()
