# Report outline — complete in your own words after running the programs

1. Problem statement and synchronization objective.
2. Semaphore Readers-Writers: explain `count_lock`, `resource`, reader-count transitions, and the reader-starvation limitation.
3. Monitor Readers-Writers: explain the condition lock, predicate loops, active-reader count, and waiting-writer preference.
4. Semaphore Dining Philosophers: explain four fork semaphores and why `Semaphore(3)` breaks circular wait.
5. Monitor Dining Philosophers: explain the `Hungry` state, neighbor test, condition wait, and atomic transition to `Eating`.
6. HTML trace generation: explain that `record()` captures events during concurrent execution and `make_html()` embeds those events for replay.
7. Race conditions, mutual exclusion, deadlock and starvation.
8. Compare semaphores and monitor-style condition variables.
9. Add screenshots of all four generated pages and your observed execution traces.
10. AI usage summary, references, and academic-integrity declaration required by your course handout.

Do not submit this outline as a completed report; add your own observations and cite resources you actually used.
