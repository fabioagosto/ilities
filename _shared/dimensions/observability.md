*When it breaks in production, can we tell what happened?*
- **Signals:** meaningful logs / metrics / errors at the boundaries that matter; error
  messages are actionable (say what failed and, ideally, what to do next).
- **Smells:** silent boundaries; `catch` blocks that lose the cause; error messages that
  give the reader nothing to act on.