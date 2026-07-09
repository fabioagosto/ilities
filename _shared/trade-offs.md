- **One failing gate stops the merge.** The score is a diagnostic, not an average to
  game.
- **Simplicity and flexibility trade off.** Every abstraction added for flexibility
  costs simplicity. Decide which one *this specific code* should optimize for; do not
  try to max both.
- **Performance trades against readability and portability.** Spend that trade only
  against measured load, not imagined load.
- **Security and robustness caps trade against convenience.** Usually worth it on
  anything crossing a trust boundary; note the cost rather than pretending there is
  none.
- **Correctness is assumed, so it is easy to skip. Don't.**
- **Review the change, not the author.** Findings describe the code and its failure
  mode, never the person.