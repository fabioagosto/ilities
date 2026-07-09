*Is it fast enough for its actual load, and no more optimized than it needs to be?*
- **Signals:** no accidental N+1s, full-table scans, or repeated work in loops; data
  structures fit the access pattern; optimized against real expected load.
- **Smells:** N+1 queries; work repeated inside loops; premature micro-optimization that
  costs readability for no measured gain.