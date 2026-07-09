# ilities

A suite of skills for **intent-first code review**. Most review asks *"is this code good?"* ilities asks the question: *"does this do what it set out to do?"* Intent is the gate you pass before quality is scored, that is the purpose of this suite, and every skill in it runs that gate first.

## Quick Start

### Install as a plugin

```sh
/plugin marketplace add fabioagosto/ilities
/plugin install ilities@ilities
```

Then ask for a review and Claude picks the right skill, or invoke one directly — `ilities`
for a full-rubric review, `ilities-security` (or any lens) for a single angle.

### Install manually

Prefer to vendor the skills yourself:

```sh
git clone https://github.com/fabioagosto/ilities.git

# All skills
cp -r ilities/skills/ilities* ~/.claude/skills/

# Or just the flagships
cp -r ilities/skills/ilities ilities/skills/ilities-guide ilities/skills/ilities-decide ~/.claude/skills/
```

Restart Claude Code if it is already running.

## The Suite of Skills

Three flagship skills work across the whole rubric; eleven focused skills each drill into
one lens when you want to point your review at a single thing.

### Flagships

| Skill | What it does |
|-------|--------------|
| [`ilities`](skills/ilities) | Review an existing change against the full rubric: intent gate → score all 11 dimensions → verdict. |
| [`ilities-guide`](skills/ilities-guide) | The rubric run *forward*, write a change that passes the intent review by construction. |
| [`ilities-decide`](skills/ilities-decide) | Decide which dimensions to concentrate on for a given change, since attention is finite. |

### Focused lenses

Each runs the intent gate, then scores **one** dimension deeply and returns a verdict
scoped to it. Reach for these when the user asks for a specific angle ("is this safe to
ship?", "is this maintainable?", "are the edge cases covered?") rather than a full review.

| Skill | Lens |
|-------|------|
| [`ilities-correctness`](skills/ilities-correctness) | Does it do the right thing, including at the edges? |
| [`ilities-security`](skills/ilities-security) | Could this be misused? |
| [`ilities-simplicity`](skills/ilities-simplicity) | Is this the least code that fully solves the problem? |
| [`ilities-readability`](skills/ilities-readability) | Can a teammate understand it without the author explaining it? |
| [`ilities-maintainability`](skills/ilities-maintainability) | Will it be cheap to change in six months? |
| [`ilities-flexibility`](skills/ilities-flexibility) | Can the likely next change be made without a rewrite? |
| [`ilities-testability`](skills/ilities-testability) | Can the behavior be verified, and is it? |
| [`ilities-reliability`](skills/ilities-reliability) | Does it degrade gracefully? |
| [`ilities-performance`](skills/ilities-performance) | Is it fast enough for its actual load, and no more optimized than it needs to be? |
| [`ilities-consistency`](skills/ilities-consistency) | Does it fit the codebase? |
| [`ilities-observability`](skills/ilities-observability) | When it breaks in production, can we tell what happened? |

## Contributing

- To change a rubric definition, edit the fragment under `_shared/` and run `python
  build.py`. Commit both the fragment and the regenerated `references/rubric.md` files.
- To change a skill's process or output format, edit its `SKILL.md` directly (only the
  rubric is generated).
- `python build.py --check` must pass before a change merges.

## License

[MIT](LICENSE).
