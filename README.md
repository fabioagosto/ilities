# ilities

A suite of skills for **intent-first code review**. Most review asks *"is this code good?"* ilities asks a
sharper question first: *"does this do what it set out to do?"*

**intent is a the gate you pass before quality is scored**, that is the
whole point of the suite, and every skill in it runs the gate first.

## The Suite of Skills

Three flagship skills work across the whole rubric; eleven focused skills each drill into
one lens when you want to point your review at a single thing.

### Flagships

| Skill | What it does |
|-------|--------------|
| [`ilities-audit`](ilities-audit) | Review an existing change against the full rubric: intent gate → score all 11 dimensions → verdict. |
| [`ilities-guide`](ilities-guide) | The rubric run *forward*, write a change that passes the intent review by construction. |
| [`ilities-decide`](ilities-decide) | Decide which dimensions to concentrate on for a given change, since attention is finite. |

### Focused audit lenses

Each runs the intent gate, then scores **one** dimension deeply and returns a verdict
scoped to it. Reach for these when the user asks for a specific angle ("is this safe to
ship?", "is this maintainable?", "are the edge cases covered?") rather than a full review.

| Skill | Lens |
|-------|------|
| [`ilities-audit-correctness`](ilities-audit-correctness) | Does it do the right thing, including at the edges? |
| [`ilities-audit-security`](ilities-audit-security) | Could this be misused? |
| [`ilities-audit-simplicity`](ilities-audit-simplicity) | Is this the least code that fully solves the problem? |
| [`ilities-audit-readability`](ilities-audit-readability) | Can a teammate understand it without the author explaining it? |
| [`ilities-audit-maintainability`](ilities-audit-maintainability) | Will it be cheap to change in six months? |
| [`ilities-audit-flexibility`](ilities-audit-flexibility) | Can the likely next change be made without a rewrite? |
| [`ilities-audit-testability`](ilities-audit-testability) | Can the behavior be verified, and is it? |
| [`ilities-audit-reliability`](ilities-audit-reliability) | Does it degrade gracefully? |
| [`ilities-audit-performance`](ilities-audit-performance) | Is it fast enough for its actual load, and no more optimized than it needs to be? |
| [`ilities-audit-consistency`](ilities-audit-consistency) | Does it fit the codebase? |
| [`ilities-audit-observability`](ilities-audit-observability) | When it breaks in production, can we tell what happened? |

## Install

Claude Code loads skills from `~/.claude/skills/` (personal) or `.claude/skills/`
(per-project). Copy in whichever skills you want:

```sh
# all of them
cp -r ilities-* ~/.claude/skills/

# or just the flagships
cp -r ilities-audit ilities-guide ilities-decide ~/.claude/skills/
```

Each skill is self-contained: its `references/rubric.md` ships alongside it, so a skill
works on its own once copied.

## Contributing

- To change a rubric definition, edit the fragment under `_shared/` and run `python
  build.py`. Commit both the fragment and the regenerated `references/rubric.md` files.
- To change a skill's process or output format, edit its `SKILL.md` directly (only the
  rubric is generated).
- `python build.py --check` must pass before a change merges.

## License

[MIT](LICENSE).
