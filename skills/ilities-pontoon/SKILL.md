---
name: ilities-pontoon
description: >-
  Wire any temporary, dev-only integration into a codebase so that removing it later is one
  module delete plus reverting a handful of greppable tagged hooks — never a hunt through core
  files. Use this whenever code is being added that is explicitly temporary or dev-only: a
  local-dev auth or billing bridge, a mock or fake provider, a debug endpoint, a feature spike
  behind a flag, an instrumentation shim, a workaround pending an upstream fix. Trigger on
  "this is just for dev", "temporary until X ships", "we'll rip this out later", "add a mock
  provider for local testing", "I need a debug hook but it must not ship", or any request to
  scaffold something with a known removal date. Also use it in reverse: to audit existing
  temp code for how cleanly it would unwire, or to perform the unwire itself ("remove the
  scaffolding", "rip out the temp provider"). The distinguishing move is designing the REMOVAL
  first — every touch point tagged, the unwire documented at wire time — because untagged temp
  code becomes permanent the day its author forgets where the tendrils are.
---

# ilities-pontoon — scaffolding built to be dismantled (companion)

> A **pontoon bridge** is a temporary military crossing: assembled fast from standard
> sections, load-bearing for exactly as long as the mission needs it, and dismantled without
> a trace when the force moves on. Temporary dev code should be built the same way — and
> almost never is. The default failure mode of "we'll rip it out later" is that *later* nobody
> remembers where all the tendrils went, so the temp code quietly becomes permanent.

This is a **wiring pattern**, not a review skill. It generalizes the scaffolding discipline
proven in `ilities-q-route` (a dev-only auth bridge wired under `# TEMP:` tags): the same
moves work for any integration with a known removal date.

## When to use this

Reach for it whenever code is temporary *by declared intent*: dev-only providers and auth
bridges, mocks and fakes for local testing, debug endpoints and instrumentation shims,
spikes behind a flag, workarounds pending an upstream fix. Triggers: "this is just for dev,"
"temporary until X ships," "we'll rip this out later," "it must not ship to prod."

Also use it in reverse — to **audit** existing temp code ("how cleanly would this unwire?")
or to **perform the unwire** ("remove the scaffolding"). The audit is simple: grep the tag;
if you can't find every touch point from the grep alone, the scaffolding has already failed.

Do *not* use it for code that is merely *small* or *experimental but might stay* — a feature
you may keep deserves normal architecture, not a demolition plan. The pattern applies when
removal is part of the requirement.

## The method — build the bridge for the demolition

Design the removal first; the wiring follows from it.

1. **One module owns the scaffolding.** All the temporary logic — the adapter, the mock, the
   debug handler — lives in its own file(s), named so its purpose is obvious
   (`llm_provider_agentsdk.py`, `dev_auth_bridge.ts`). The module is the unit of deletion:
   removal step one is always "delete this file."

2. **Tag every touch point in permanent code.** Wherever the scaffolding hooks into core
   files — a factory branch, a registry entry, a validation-list addition, a config key, a
   dependency line — mark it with a single greppable tag: `# TEMP:<name>` /
   `// TEMP:<name>` (e.g. `# TEMP:agentsdk`). One consistent tag per scaffold, so
   `grep -rn "TEMP:agentsdk"` returns the *complete* removal map. An untagged touch point is
   the tendril that survives the demolition.

3. **Keep the hooks tiny and degenerate.** Each touch point in permanent code should be one
   or two lines: a branch that delegates to the module, an entry in a list. All behavior
   stays in the scaffold module. If a hook is growing logic, the scaffolding is invading the
   structure it was meant to stand beside — move the logic into the module.

4. **Leave the permanent path intact.** The scaffold *adds an alternative*, it never rewires
   the real one. The production code path must keep working with the scaffold present, and
   selecting it back must be one setting/flag — not a code change. If installing the scaffold
   required editing the permanent path's behavior, it isn't scaffolding anymore.

5. **Lazy-load and gate at the seam.** Import the scaffold module only when it is selected
   (a heavy dev dependency should cost nothing when inactive), and make any availability
   check honest: the scaffold reports available only when its preconditions (env var, dep
   installed) actually hold.

6. **Write the unwire down at wire time.** In the scaffold module's header or the PR, state
   the removal procedure — typically: flip the setting back, delete the module, revert the
   tagged hooks (`grep TEMP:<name>` finds them), drop the dependency — and the condition or
   date that triggers it ("remove when X ships"). This is the step that keeps *later* from
   becoming *never*.

7. **Verify the demolition, not just the bridge.** Before calling it done, confirm the
   removal map is complete: grep the tag, check every touch point is on the list, and
   confirm the app runs on the permanent path with the scaffold unselected. The scaffold
   working is half the acceptance test; the scaffold being *removable* is the other half.

## Output — when wiring, deliver the removal map

Alongside the code, state the demolition plan:

```
## Scaffold
<name> — <what it does and why it is temporary>

## Tag
TEMP:<name> — grep this for the complete touch-point map

## Touch points
<file:line — what each tagged hook does, one line each>

## Unwire
1. <flip the setting/flag back to the permanent path>
2. delete <module file(s)>
3. revert the TEMP:<name> tagged hooks (grep finds them)
4. <drop the dependency / config key, if any>

## Remove when
<the condition or date that triggers removal>
```

## Principles

- **Design the removal before the installation.** If you can't write the unwire in four
  steps, the wiring is wrong — restructure until you can.
- **The grep is the contract.** One tag, every touch point, nothing findable only by memory.
  A removal map that lives in someone's head has a bus factor of one and a half-life of weeks.
- **Scaffolding stands beside the structure, never inside it.** Tiny delegating hooks in
  permanent code; all behavior in the deletable module.
- **The permanent path is sacred.** It keeps working with the scaffold present and is one
  flip away at all times. Dev-only code that production can see is a defect (and if it
  carries credentials or auth, a security finding — see `ilities-q-route` for the canonical
  case).
- **Temp code without a removal trigger is permanent code with worse quality standards.**
  Name the condition that removes it, or admit it's staying and build it properly.
