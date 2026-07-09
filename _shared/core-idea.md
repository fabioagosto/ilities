A normal code review asks *"is this code good?"* An **intent review** asks first
*"does this change do what it set out to do, no more and no less?"* That ordering is
the whole point. Scope creep, half-solved problems, and clean solutions to the wrong
problem are all failures even when the code itself is spotless. You cannot judge
quality until you know what the change was trying to be, so intent is a gate you pass
before the quality dimensions even open.

So intent is the **first lens**, not one score among many: a change can fail here no
matter how clean its code. But treat the gate as a scope-and-goal check, not a back-door
into the quality dimensions. "Does it solve the stated problem *at all*" is a gate
question; "is it correct at the edges" is the Correctness dimension. Keep them separate
so the gate stays about *what the change is*, not *how well it is built*.

This is why the rubric is **not an average**. A change can be a 3 on ten dimensions
and still be unmergeable because it quietly solved a different problem, or smuggled in
an unrelated refactor. One failing gate stops the merge. The scores are a diagnostic
that tells you *where* the work is weak, not a number to optimize.