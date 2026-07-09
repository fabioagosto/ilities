---
name: ilities-security
description: >-
  Security-only review of a change: run the intent gate first, then judge one thing
  deeply, could this be misused? Use when the user wants a security review ("is this safe
  to ship", "review this for vulnerabilities", "check this endpoint for
  injection/authz/secrets", "any security holes in this diff"), or when a change touches a
  security-sensitive surface even if they just said "review this": auth, user or network
  input, SQL/shell/path construction, file uploads, deserialization, secrets, CORS, rate
  limits. Checks validation and escaping at the trust boundary, authz on mutating paths, no
  secrets in source, least privilege, and caps on caller-controlled limits. For a full
  11-dimension review use ilities; for line-by-line vulnerability hunting,
  /security-review and /code-review are sharper and run alongside. Intent-first: a
  secure-looking change that solves the wrong problem still fails here.
---

# ilities: Security

A security-only review. Confirm the change does what it set out to do, then judge one
thing: could this be misused? Run the intent gate first. A change that is airtight against
injection but quietly solves a different problem, or smuggles in an unrelated refactor, is
not mergeable no matter how secure the code is. Intent is the gate; security is the lens
once it passes.

Read `references/rubric.md` for the intent gate, the scoring scale, the Security dimension
definition, and the trade-off principles. Load it before scoring so you assess against the
written definition, not your gut.

## When to use this

Use it when the user wants the security question answered specifically, or when the change
touches a security-sensitive surface even if they only said "review this": authentication
or authorization, user- or network-supplied input, SQL/shell/path construction, file
uploads, deserialization, secrets and credentials, CORS, rate limits, or anything that
reads or mutates data across a trust boundary.

For a full review across all 11 dimensions, use `ilities`; it runs the whole rubric
and this same gate. For line-by-line vulnerability hunting, `/security-review` and
`/code-review` are sharper and can run alongside. This skill is intent-first: it asks
whether the change should exist in this shape at all, not only whether a line has a flaw.

## The process

Work in this order. The ordering is the method.

1. **State the intent in one sentence.** What is this change supposed to accomplish? Pull
   it from the PR, commit, ticket, or user. If you cannot write that sentence, stop and say
   so: the change is not reviewable yet, and that is your first finding.

2. **Run the intent gate** (rubric Part 1). The four blockers each stop the merge on a
   "no"; the worth-doing item is a flag. Report a gate failure before, and more prominently
   than, the security score. A clean solution to the wrong problem fails even a
   security-only look.

3. **Assess Security, deeply.** Do not stop at the first issue; walk the whole trust
   boundary the change touches. Is every input from outside it validated or escaped
   (injection, XSS, path traversal)? Is there an authn/authz check on everything that reads
   or mutates data, including the mutating path that is easy to miss? Are there secrets in
   source? Is least privilege honored? Is everything a caller controls (page size, batch
   size, rate) capped? Score it 0 to 3 on the rubric scale, and attach a concrete finding
   for anything below 3: the location, the failure mode, and what would raise it.

4. **Verify, do not just inspect.** A security verdict from reading alone is dangerous.
   Where you can, exercise the path: send the malformed input, call the endpoint without a
   token, try the traversal, grep the diff for hardcoded secrets. Let what you observe set
   the score. Where you cannot (bare diff, no repo, missing deps), say so and list what you
   could not verify.

5. **Write the verdict**, scoped to security: Ship, Ship with follow-ups, or Needs work,
   plus the single most important thing to fix. A Security score of 0, or a failed gate, is
   Needs work no matter how clean the rest looks. Never say Ship on inspection alone; either
   you verified the boundary, or the verdict names what stays unverified.

## Scale the review to the change

A two-line change does not need a five-paragraph write-up. For a small diff, run the gate,
note what you probed, give the Security score, and land a one-line verdict. Save the fuller
treatment for a change with real security surface. The gate and the verification step
always run; only the depth flexes.

## Output format

```
## Intent
<one sentence: what this change is supposed to accomplish>

## Intent gate
<Pass, or the specific blocker(s); include any worth-doing flag as a question>

## Security (0 to 3)
- <file:line>: <failure mode> -> <what would fix it>
- ...

## Verification
<what you exercised and observed, or what you could not verify and why>

## Verdict (security)
<Ship | Ship with follow-ups | Needs work>
Most important fix: <one thing>
```

## Principles

- **Intent before security, always.** A locked-down change that solves the wrong problem
  still fails. Lead with the gate, not the score.
- **Probe the boundary; do not admire the code.** Most holes live on the failure and edge
  paths: the malformed input, the missing authz check, the uncapped limit. Go looking there.
- **A finding names the code and its failure mode, never the author.** "This interpolates
  the request path into the query, so a crafted `id` reads other tenants' rows," not "you
  forgot to sanitize the input."
- **Say what you could not verify.** If you could not run the exploit path, the verdict
  names that gap rather than implying a safety you did not confirm.
