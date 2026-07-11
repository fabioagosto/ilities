# evals

Reproducible test cases for the **companion** skills (`ilities-opord`, `ilities-pontoon`).
The review lenses are graded by human judgment against the rubric; the companions produce
objectively checkable artifacts (a PR description, wired-in or removed code), so they get
eval fixtures here.

Each skill has a directory with an `evals.json` (prompts + assertions) and a `fixtures/`
directory holding the inputs the prompts refer to. Everything here is committed and
stable — the transient run outputs (per-run generations, gradings, benchmark numbers) are
**not** stored in the repo; they're regenerated each time you run.

```
evals/
├── ilities-opord/
│   ├── evals.json                  # 2 evals: write a PR description, retrofit a bad one
│   └── fixtures/
│       └── companion-tier.diff     # the real change the PR-description evals describe
└── ilities-pontoon/
    ├── evals.json                  # 2 evals: wire a removable scaffold, unwire an existing one
    └── fixtures/
        ├── notifier-app/           # clean app with a provider seam (wire target)
        └── payments-app/           # app with an untagged 'fakepay' scaffold (unwire target)
```

## How to run

These use the [`skill-creator`](https://github.com/anthropics/skills) eval harness, but the
files are harness-agnostic — an `evals.json` is just prompts and assertions. To run one eval
by hand:

1. **Pick an eval** from a skill's `evals.json`.
2. **Run it two ways** — once with the skill's `SKILL.md` in context (the "with-skill" arm),
   once without (the baseline) — each in a fresh agent, so the skill's contribution is
   visible as the delta. For `pontoon` evals, have the agent copy the named `fixture/` into a
   scratch working directory and operate only on the copy, so the fixture stays pristine.
3. **Grade** each output against that eval's `assertions` (each is an objectively checkable
   statement). Several `pontoon` assertions are mechanical — e.g. `grep -ri fakepay` returning
   nothing, or checking that `checkout.py` calls `run_fraud_check` unconditionally — so prefer
   a script over eyeballing.

## What these evals are watching for

- **opord** — the discriminating assertions are `explicit_scope_out` and `honest_verification`.
  A capable agent writes a decent PR description *without* the skill; what it tends to skip is
  an explicit "what this does NOT do" list and an honest "here's what I did not verify." Those
  are the OPORD-specific moves.
- **pontoon** — the wire/unwire mechanics (own module, greppable tag, permanent path intact,
  written unwire) are the check. Note the caveat in `ilities-pontoon/evals.json`: both current
  prompts hint at removability, which is exactly what the skill injects, so a strong baseline
  can also pass. The skill's sharpest value is on prompts that *don't* ask for removability —
  a good candidate for a future eval.
