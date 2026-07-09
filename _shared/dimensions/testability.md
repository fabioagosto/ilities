*Can the behavior be verified, and is it?*
- **Signals:** new behavior is covered at the right level (unit / integration); tests
  assert behavior, not implementation details; code is structured to be tested in
  isolation (dependencies injectable, side effects isolated).
- **Smells:** untested new behavior; tests coupled to internals that break on refactor;
  logic that cannot be exercised without standing up the whole system.