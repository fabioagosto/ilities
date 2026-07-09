*Does it do the right thing, including at the edges?*
- **Signals:** handles empty, null, boundary, and malformed inputs; error and failure
  paths are handled, not swallowed; concurrency, ordering, and race assumptions are
  sound where relevant.
- **Smells:** happy-path-only logic; off-by-one and boundary gaps; swallowed
  exceptions; unstated timing assumptions.
- *Correctness is assumed, so it is the easiest dimension to skip and the most common
  thing a clean-looking change gets wrong. Do not skip it.*