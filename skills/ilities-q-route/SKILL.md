---
name: ilities-q-route
description: >-
  Use when a developer wants to run their Python app's LLM calls on their own
  Claude Pro/Max subscription during LOCAL development/testing — instead of
  paying a per-token ANTHROPIC_API_KEY — by wiring the Claude Agent SDK's
  single-shot query() into the app as a plain generate() provider, authenticated
  with a personal CLAUDE_CODE_OAUTH_TOKEN. Trigger on "use my Claude subscription
  for the app," "avoid a second API bill just for dev," "add the Agent SDK /
  claude-agent-sdk as an LLM provider," or a mention of CLAUDE_CODE_OAUTH_TOKEN
  in the context of wiring it into an app / provider (NOT plain Claude Code usage
  or its CI action). Strictly a DEV-ONLY pattern: do NOT use it for production,
  staging, or any shared / user-facing backend, where subscription (claude.ai)
  auth is not permitted.
---

# ilities-q-route — SDK-backed inference (dev-only)

> **A Q-route is a swept, safe channel through mined waters.** This skill is the
> ilities suite's companion tool: a *sanctioned safe lane* for running an app's
> LLM calls on your own Claude subscription during local dev — with the "don't
> stray into production" boundary built into the metaphor. It is **not** a code-
> review lens; it ships alongside the review skills as a bundled dev-tooling how-to.

Run an app's LLM calls on **your own** Claude subscription while you develop and
test locally — a good Claude model without a second, per-token API bill. It works
by treating the **Claude Agent SDK** as a plain text-generation backend: one
prompt in, one string out, no agent loop, no tools.

## The one boundary that keeps this defensible

The Claude **subscription** (what powers Claude Code) and the Claude **API**
(pay-per-token) are separate billing systems. Routing a **product's** or a
**shared / user-facing backend's** inference through subscription auth is **not
permitted**. Even for personal use, subscription (claude.ai) auth for
*programmatic* inference is a **gray area** — you are responsible for compliance
with Anthropic's Consumer Terms and usage policies; when in doubt, use an API key.

So treat this skill as strictly:

- ✅ **Local development and testing**, run by the developer, on their own machine,
  with their own `CLAUDE_CODE_OAUTH_TOKEN`. A solo/personal CI pipeline that runs
  *as you* is a maybe — but a shared-repo CI where others can trigger runs or read
  the token secret crosses back into "shared infrastructure": use an API key there.
- ❌ **Not** for production, staging that serves others, or anything users hit.
  For those, use `ANTHROPIC_API_KEY` from the Console.

**Always state this boundary when you apply the skill, and leave the app's
API-key path intact** so switching back to production auth is one setting away.
If the user's target is a deployed/shared service, stop and recommend an API key
instead — don't wire subscription auth into it. And name the personal-account
risk: automating your own subscription auth is at *your* account's risk — keep
volume to a human-paced dev loop; if you need automation or scale, use an API key.

## Why this shape (and why it's cheap to remove)

Most LLM apps already have a small provider seam — a function like
`generate(prompt) -> str` (or a small `LLMProvider` class) with implementations
for OpenAI, Anthropic, Ollama, etc. The cleanest, most removable integration is
to add **one more provider** that adapts the Agent SDK's `query()` to that same
interface. Nothing else changes: callers still call `generate()`, and you flip
which provider is active. When you're done, delete the one module and flip back.

Put the whole thing in **its own module** with a couple of tiny, tagged hooks in
the core files (factory branch + provider registry/validation list). Deleting the
module and reverting the tags is the entire unwire. Resist rewriting features onto
the agent loop — you're using the SDK in a degenerate one-shot mode purely as a
credential + model bridge. Keep it that small.

## What you need to know about the SDK (verified)

- **Package:** `claude-agent-sdk` (Python 3.10+) / `@anthropic-ai/claude-agent-sdk`
  (Node 18+). **Self-contained** — the platform wheel bundles a native `claude`
  binary (the linux-x86-64 wheel is ~80 MB vs a 268 KB sdist). **No separate
  Node.js, no `@anthropic-ai/claude-code`, nothing to apt-get.** Verified on
  `python:3.11-slim` with **0.2.115** (installs, imports, and coexists with
  `anthropic`/`fastapi`/`pydantic`). Pin a floor — `claude-agent-sdk>=0.2.115` —
  since the bundled-binary / no-Node behavior and `setting_sources` are only
  guaranteed from a recent version.
- **Single-shot:** `query()` is an async generator. Cap it with `max_turns=1`,
  disable tools with `allowed_tools=[]`, and use `permission_mode="bypassPermissions"`
  + `setting_sources=[]` (skip CLAUDE.md / settings discovery). `bypassPermissions`
  is safe **only** because `allowed_tools=[]` leaves nothing to permit — never keep
  it if you re-enable any tools. Extract text **robustly** by duck-typing the
  stream: collect `.text` from any block on a message's `.content` list, and fall
  back to a final message's `.result` string. (Don't hard-depend on importing
  specific message classes — that's fragile across SDK versions.)
- **No output-token cap:** the single-shot path has no equivalent of `max_tokens`.
  If your provider contract takes one, accept it for signature parity and note it
  isn't enforced. This pattern sends a user prompt only; if you need a system
  prompt, set it via `ClaudeAgentOptions(system_prompt=...)`.
- **Model:** choose per call with `model=` (`"opus"`, `"sonnet"`, `"haiku"`, or a
  full model ID).
- **Auth precedence (highest first):** cloud-provider vars
  (`CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`) → `ANTHROPIC_AUTH_TOKEN` →
  **`ANTHROPIC_API_KEY`** → `apiKeyHelper` → **`CLAUDE_CODE_OAUTH_TOKEN`** →
  interactive login. The subscription token sits *below* `ANTHROPIC_API_KEY`, so
  **any higher-precedence source present in the env makes the token lose.** The #1
  failure mode is a stray/placeholder `ANTHROPIC_API_KEY` silently winning and
  re-triggering a 401 even with a valid token set. Scrub `ANTHROPIC_API_KEY` (see
  below); if a dev also has `ANTHROPIC_AUTH_TOKEN` or a Bedrock/Vertex var set,
  those must be unset too — the common-case scrub only covers `ANTHROPIC_API_KEY`.
- **`ClaudeAgentOptions.env` MERGES** onto the inherited process env — it can add
  or override keys but **cannot remove** an inherited `ANTHROPIC_API_KEY`. So the
  scrub can't be done via the SDK option; do it at the Python level.
- **Writable state dir:** the subprocess writes session transcripts under
  `~/.claude` (or `CLAUDE_CONFIG_DIR/projects` if set). On a read-only or
  awkward-HOME container this fails with a *filesystem* error, not a 401 — easy to
  misdiagnose. Pass `env={"CLAUDE_CONFIG_DIR": <existing writable dir>}` (create it
  first). Transcripts can contain prompt/response content, so on a shared machine
  don't point it at a world-readable location.
- **Async bridging:** the caller may already be inside a live event loop (a FastAPI
  async handler, a background task). `asyncio.run()` / `run_until_complete()` on
  that thread raises "loop already running." Drive the coroutine on a **dedicated
  worker thread with its own fresh loop** (below). (Node SDK only: don't wrap
  `query()` in an outer `AbortController`/`Promise.race` — it hangs.)
- **Cost model:** calls draw on the subscription's Claude Code usage and are
  **rate-limited** (Pro/Max limits), not billed per token. A human-paced dev loop is
  fine even on Opus — a single-section extraction (~300 words → 20 entities, 53
  relationships) returns in seconds without tripping limits. It's *bulk* sweeps
  (e.g. whole-manuscript extraction across dozens of sections on Opus) that bite —
  expose a model env-override so you can drop to `sonnet` for those.

## Steps

### 1. Mint a personal token
```bash
claude setup-token        # one interactive login → prints CLAUDE_CODE_OAUTH_TOKEN (≈1yr)
```
`claude setup-token` needs the Claude Code CLI installed and an active Pro/Max
login. Treat the token like a secret: put it in `.env` (and make sure `.env` is in
`.gitignore`), never commit it, never paste it into source or a chat transcript.
It's *your* token — not something you ship. It lasts ~1 year: a fresh 401 on a
previously-working token after about that long usually means it expired — re-run
`claude setup-token`.

### 2. Install the SDK
```bash
pip install 'claude-agent-sdk>=0.2.115'    # Python 3.10+ ; bundles the binary, no Node
```

### 3. Write the provider adapter (with the async→sync bridge)
Match the app's existing provider interface. The core is an async single-shot
query, driven synchronously through a worker thread so it's safe under a live
event loop. **Scrub `ANTHROPIC_API_KEY` on the CALLING thread, around
start()/join()** — never inside the worker — so it's always restored even if the
worker hangs past the join timeout (otherwise a single hung call leaves the key
popped and, with the lock held, wedges every later call). Note the scrub mutates
process-global env for the call's duration, so it assumes a single active provider
in dev — unsafe if other Anthropic-keyed calls run concurrently on other threads.

```python
import asyncio, os, threading
from pathlib import Path

_ENV_LOCK = threading.Lock()          # serialize the process-global env mutation
# Your app's per-call timeout (seconds); the worker join must exceed the longest
# single call so a slow-but-live call isn't abandoned.
REQUEST_TIMEOUT = int(os.environ.get("MY_APP_REQUEST_TIMEOUT", "180"))

def _config_dir() -> str:
    # Private dir for the SDK subprocess's session state. Transcripts can contain
    # prompt/response content, so avoid world-readable /tmp on shared machines.
    base = os.environ.get("MY_APP_CONFIG_DIR") or str(Path.home() / ".myapp")
    d = Path(base) / "agentsdk"
    d.mkdir(parents=True, exist_ok=True)   # must exist and be writable
    try:
        os.chmod(d, 0o700)                 # best-effort; no-op on Windows
    except OSError:
        pass
    return str(d)

def _options(model: str, system_prompt: str | None = None):
    from claude_agent_sdk import ClaudeAgentOptions
    kwargs = dict(
        model=model,                       # "opus" | "sonnet" | "haiku" | full id
        allowed_tools=[],                  # no tools — pure text
        max_turns=1,                       # one turn, no agent loop
        permission_mode="bypassPermissions",  # safe ONLY because allowed_tools=[]
        setting_sources=[],                # skip CLAUDE.md / settings discovery
        env={"CLAUDE_CONFIG_DIR": _config_dir()},
    )
    if system_prompt:
        kwargs["system_prompt"] = system_prompt   # if your provider contract needs one
    try:
        return ClaudeAgentOptions(**kwargs)
    except TypeError:                      # defensive — the >=0.2.115 pin already guarantees setting_sources
        kwargs.pop("setting_sources", None)
        return ClaudeAgentOptions(**kwargs)

def generate(prompt: str, model: str | None = None, max_tokens: int = 2000,
             system_prompt: str | None = None) -> str:
    # model: resolve from env so you can flip Opus↔Sonnet per-run to survive rate
    # limits (cheaper Sonnet as the generic default; Manuript defaults this to opus).
    model = model or os.environ.get("MY_APP_MODEL", "sonnet")
    # max_tokens: accepted for interface parity — the SDK single-shot has no
    # output-token cap, so it is not enforced. Return type here is str for
    # illustration; wrap it in your app's response object if the contract needs one.
    box = {}

    async def _agenerate() -> str:
        from claude_agent_sdk import query
        parts, result = [], None
        async for msg in query(prompt=prompt, options=_options(model, system_prompt)):
            content = getattr(msg, "content", None)
            if isinstance(content, list):
                parts += [b.text for b in content if getattr(b, "text", None)]
            r = getattr(msg, "result", None)
            if isinstance(r, str) and r:
                result = r
        return "".join(parts).strip() or (result or "").strip()

    def runner():
        loop = asyncio.new_event_loop()
        try:
            box["value"] = loop.run_until_complete(_agenerate())
        except BaseException as e:        # propagate to the caller thread
            box["error"] = e
        finally:
            loop.close()

    with _ENV_LOCK:
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)   # token must outrank the key
        try:
            t = threading.Thread(target=runner, daemon=True)
            t.start()
            t.join(timeout=REQUEST_TIMEOUT + 60)   # exceed your longest single call
            if t.is_alive():
                raise TimeoutError("Agent SDK call timed out")
        finally:
            if saved is not None:                  # always restored, even on timeout
                os.environ["ANTHROPIC_API_KEY"] = saved
    if "error" in box:
        raise box["error"]
    return box.get("value", "")
```

Slot it into the app's provider registry / factory like the existing providers, add
its name to whatever list validates provider names, and make the app's "provider
available?" check report it available when the token is set **and** the SDK is
importable (so any UI gate unlocks). Use a **lazy import** of the SDK in the factory
so the ~80 MB package only loads when this provider is selected.

### 4. Force the token to win (scrub the API key)
The step people miss. Because `ANTHROPIC_API_KEY` outranks the token and
`ClaudeAgentOptions.env` can't *remove* an inherited key, scrub it in Python — the
adapter above does it per-call (pop → run → restore), keeping the app's API-key
path intact. Also unset any *higher*-precedence source if present
(`ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`). Alternatively, if you
don't need the key in dev at all, just leave `ANTHROPIC_API_KEY` unset and set
`CLAUDE_CODE_OAUTH_TOKEN`. Either way: **no truthy `ANTHROPIC_API_KEY` (or higher
source) when the SDK subprocess spawns.**

### 5. Select the provider and verify
Flip the app to the new provider, then exercise a **real feature end-to-end** and
confirm output comes back with no 401 / no auth error. "It returned a plausible
answer" is the check — not "the process started." If you can, drive it via the
app's own API/UI so you exercise the actual call path (including whatever runs
`generate()` inside an event loop).

**Re-check your test fixture after any container recreate.** You typically recreate
the container to load the new token — and that can wipe non-persistent app data
(uploads, an in-container DB) that isn't on a mounted volume. So the manuscript /
record / fixture you planned to test against may be gone by the time you run the
feature: confirm it still exists (or re-create it) *after* the recreate, or you'll
misread a plain "not found" as a provider failure.

### 6. Document the unwire
Because it's dev-only, make removal trivial and write it down: flip the provider
setting back to the API-key provider, delete the adapter module + its tagged hooks,
and drop the SDK from the image/deps. One flip returns you to production auth.

## Docker / headless

**Still dev-only** — this image is for your local/CI dev loop, not a deployed or
shared service; for anything users hit, use `ANTHROPIC_API_KEY`. The SDK
containerizes with **no Node layer** (the wheel bundles the binary):
```dockerfile
FROM python:3.11-slim
RUN pip install 'claude-agent-sdk>=0.2.115'
# ... app ...
```
Run with `CLAUDE_CODE_OAUTH_TOKEN` in the environment and **no truthy**
`ANTHROPIC_API_KEY` (or higher-precedence source) at spawn. Point `CLAUDE_CONFIG_DIR`
at an existing writable dir — e.g. a mounted data volume — so the subprocess can
write session state. `setting_sources=[]` skips filesystem config discovery. If
that volume is shared or persisted, treat it as sensitive — session transcripts
can contain prompt/response content.

## Worked example — Manuript (implemented + E2E-verified)

Manuript (Python/FastAPI, `bookreview/`) has the ideal seam and this pattern is
wired there as a removable scaffold — and **verified end-to-end with a live
subscription token**: a real Knowledge-Graph extraction ran through the provider
on Opus and returned 20 entities / 53 relationships with clean 200s and zero 401s,
exercising the worker-thread bridge under an actual `BackgroundTasks` loop. The two
transferable lessons:

- **Your app's contract may return a response object, not a bare `str`.** Manuript's
  `LLMProvider.generate(prompt, max_tokens=2500)` returns an `LLMResponse` dataclass
  (`.text/.model/.provider`), so the adapter wraps the SDK text in that — match
  whatever your seam expects.
- **The worker-thread bridge is load-bearing when `generate()` runs on a thread
  with a live loop.** Manuript's KG extraction runs the *sync* analyzer inside an
  *async* `BackgroundTasks` coroutine, so `generate()` executes under a running loop
  — the exact case `asyncio.run()` can't handle.

Reference map (all under `# TEMP:agentsdk` tags, for a quick skim):
`bookreview/llm_provider_agentsdk.py` holds `AgentSdkProvider` + the bridge +
`ANTHROPIC_API_KEY` scrub + `CLAUDE_CONFIG_DIR` + `is_agentsdk_available()`; a lazy
factory branch in `llm_provider.py`; `"agentsdk"` added to
`VALID_PROVIDERS`/`LLMProviderType` and an availability entry in
`get_available_providers()` (settings.py); the UI gate flows via `api/main.py`
`enrichment_available` and `ensure_provider_available()` in `api/routes/utils.py`.
Flip with `set_llm_provider_setting('agentsdk')`, extract, confirm no 401; unwire by
deleting the module + reverting the tags + dropping `claude-agent-sdk`.

## Gotchas checklist

Each failure mode, once, terse:

- **`ANTHROPIC_API_KEY` (or a higher-precedence source) present → token ignored.**
  Scrub it; `ClaudeAgentOptions.env` merges and can't remove it for you.
- **`asyncio.run()` inside a live loop raises.** Drive the coroutine on a worker
  thread with its own loop.
- **Scrub on the CALLING thread, not the worker.** A hung call must not strand the
  popped key or the lock — restore in a `finally` the timeout can't skip.
- **`CLAUDE_CONFIG_DIR` must exist and be writable** (create it). Failure here is a
  filesystem error, not a 401.
- **`bypassPermissions` is safe only with `allowed_tools=[]`.** Never keep it if you
  re-enable tools.
- **Rate limits, not token bills.** Expose a model env-override to drop Opus→Sonnet.
- **Don't commit or paste the token.** Personal, long-lived; keep `.env` gitignored.
- **Keep it out of prod.** Deployed or serving anyone but you → use `ANTHROPIC_API_KEY`.
