---
name: ilities-lensatic
description: >-
  Decide which code-quality dimensions to concentrate effort on for a given change and
  which need only enough to clear the bar, since attention is finite and not every
  dimension deserves equal investment. Given the context
  (prototype vs production, library vs app, hot path, security boundary, one-off
  script), it returns a ranked shortlist of the 2 to 4 dimensions that matter most
  here, the ones safe to deprioritize, and the specific trade-offs to make. Use
  this whenever the user asks "what should I optimize for," "is it worth
  abstracting this," "how much error handling does this need," "should I write
  tests for this," or is weighing simplicity against flexibility, speed against
  readability, or robustness against shipping speed. Pairs with ilities-azimuth
  (which then builds to the chosen priorities) and ilities (which scores
  against them).
---

# ilities Lensatic

Pick what this change should be *great* at, and where merely clearing the bar is fine.
The rubric has 11 dimensions, and while every dimension that applies should still be
met, spreading equal effort across all of them is how you get code that is
over-engineered in the places that did not need it and thin in the places that did.
This skill turns context into a short, honest priority list: where the extra care goes,
not which dimensions to neglect. (If a change genuinely can be strong on every applicable
dimension without contortion, that is a fine answer. Say so, and just flag where the
effort concentrates.)

Read `references/rubric.md` for the dimension definitions and the trade-off principles.
The definitions matter here because the whole exercise is deciding *between* dimensions,
so you need to know precisely what each one is.

## When to use this

Use it when the right engineering trade-off is genuinely unclear and the answer depends
on context: "is it worth abstracting this," "how much error handling does this need,"
"should I write tests for a throwaway script," "do I optimize this or ship it,"
"simplicity or flexibility here." Also use it as the first step of `ilities-azimuth` when
you are about to build something and want to choose priorities before writing.

If the priorities are already obvious for the change at hand, skip this and just build.

## The method

1. **Characterize the change** along the axes that actually move the trade-offs:
   - **Lifespan:** throwaway / prototype / production / long-lived foundation.
   - **Blast radius:** private helper / internal module / public API / shared library.
   - **Exposure:** internal-only / crosses a trust boundary / handles secrets or
     untrusted input.
   - **Load:** cold path / hot path / grows with users or data.
   - **Change rate:** frozen / occasionally touched / a known extension point.

2. **Derive the top 2 to 4 dimensions** that context makes load-bearing, and name the ones
   it makes safe to deprioritize. Be decisive: a priority list where everything is
   important is not a priority list.

3. **Call the specific trade-offs**, especially the pairs that pull against each other:
   - **Simplicity vs Flexibility**: abstract only where change is genuinely expected;
     otherwise the plain version wins.
   - **Performance vs Readability/Portability**: spend this only against measured or
     clearly expected load, never imagined load.
   - **Robustness/Security vs Shipping speed**: non-negotiable across a trust boundary;
     often deferrable for an internal throwaway.
   - **Testability investment vs one-off value**: match test depth to lifespan and blast
     radius.

4. **State what "good enough" looks like** for the deprioritized dimensions, so
   deprioritizing does not become ignoring.

## Output format

```
## Change in one line
<what it is + the context that drives the trade-offs>

## Optimize for (in order)
1. <dimension>: why context makes it load-bearing here
2. <dimension>: why
   (2 to 4 total)

## Enough to clear the bar
- <dimension>: what "good enough" looks like here, so it is deprioritized, not ignored

## The calls
- <trade-off>: <the decision and the one-line reason>

## Bottom line
<one sentence a developer can act on immediately>
```

## Worked examples

**Example 1: one-off data migration script, run once, internal.**
Optimize for: Correctness (it must not corrupt data), Robustness (idempotent/re-runnable
if it dies halfway), Observability (log what it touched). Spend down: Flexibility (no
future variants), Testability (a dry-run mode beats a test suite), Performance (as long
as it finishes). Call: do not abstract anything; write it linearly and readably.

**Example 2: new public function in a shared library.**
Optimize for: Consistency (match the library's conventions exactly), Flexibility (callers
you will never meet), Testability, Readability. Spend down: raw Performance unless it is a
known hot path. Call: invest in the interface and its tests; a breaking change later is
far more expensive than getting the shape right now.

**Example 3: endpoint accepting untrusted user input on a hot path.**
Optimize for: Security (validate/escape, cap caller-controlled sizes), Correctness,
Performance (no N+1, structures fit the access pattern), Robustness. Spend down:
Flexibility (do not abstract a speculative second endpoint). Call: security and the load
budget are non-negotiable; resist the temptation to generalize.

## Principles

- **A priority list that includes everything is worthless.** The value is in what you are
  willing to *not* optimize.
- **Deprioritized is not ignored.** Always say what "good enough" means for the dimensions
  you spend down.
- **The default when unsure is Simplicity.** Under-abstraction is cheap to fix later;
  over-abstraction has to be torn out first. See the rubric's trade-off principles.
