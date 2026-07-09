Answer these first. A "no" on the four **blockers** below stops the merge, and the
finding is the "no" itself. The fifth is a **flag**, not a blocker.

Blockers:

- **Intent is stated.** The change has a clear, one-sentence goal. If you cannot write
  that sentence, the change is not ready to review: that is itself the finding.
- **The change matches the intent.** It solves the stated problem, not an adjacent or
  larger one.
- **Scope is contained.** No unrelated refactors, drive-by edits, or "while I was here"
  additions. Those are not free; they belong in a separate change where they can be
  reviewed on their own terms.
- **The problem is actually solved at the goal level.** Not partially patched, not worked
  around in a way that reintroduces the problem elsewhere. (This is the *goal*-level
  question: "did it address the stated problem." Edge-case correctness is scored
  separately under the Correctness dimension.)

Flag (raise, do not block):

- **Is the intent worth doing?** Ideally it maps to a real bug, backlog item, or user
  need. But judging product value usually needs context an agent does not have, so raise
  this as a question ("this does not obviously map to a stated need, intended?") rather
  than blocking the merge on it. Only treat it as a blocker when the waste is unambiguous
  (dead code, a feature the change itself shows is unreachable).