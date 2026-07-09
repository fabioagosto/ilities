*Does it degrade gracefully?*
- **Signals:** fails loudly and early on programmer error, safely on user/environment
  error; no unbounded resource use; idempotent and retry-safe where the context calls
  for it.
- **Smells:** unbounded loops/queries/memory; silent failure; non-idempotent operations
  on a retry path.
- *Absorbs scalability; flag it by name when growth in load or data is the specific
  concern.*