# How to use the workflow

## Start

For a direct explanation, answer without creating a task. For persistent work, choose one objective and state its scope, constraints, and completion criteria in BRIEF.md. Resume only by an exact task path.

## Investigate

Read the generated ACTIVE_CONTEXT.md and the current WORKING_NOTE.md. Choose the next step based on the bottleneck: a derivation, counterexample, numerical diagnostic, source check, or focused search of wiki/. Record what changed your understanding, why the evidence supports it, and what remains open.

Human decisions are required for material priority changes, changes to frozen definitions, formal promotion of conclusions, external publication, and expanded AI authority. Temporary labeled assumptions within an authorized investigation are allowed. Existing valid authorization does not need repeated confirmation.

## Evidence

| Label | Meaning |
|---|---|
| external_unverified | Retrieved or generated material awaiting local checks |
| conjectural | Proposed claim without sufficient support |
| conditional | Conclusion depends on explicitly stated assumptions or an unresolved bridge |
| exact_finite | Exact result for a specified finite instance or range |
| numerical | Computational evidence with stated settings and limits |
| proved | Complete argument under explicit assumptions and scope |
| refuted | A valid counterexample or contradiction refutes the stated claim |
| open | The required conclusion remains unresolved |

A failed conjecture can be a completed investigation. Successful file checks do not establish a scientific conclusion. These labels are prose conventions; the script does not certify them.

## Preserve

Task files hold the detailed working record. Wiki summaries preserve reusable understanding: decisions, stable results, useful failures, and unresolved bridges. History holds completed task directories for selective retrieval. refresh rebuilds the active view from the brief and note; close copies a supplied summary to wiki/ and archives the task.

## Exact artifacts and delivery

The lightweight script does not implement exact checkpoints. When code, data, or a document needs exact preservation:

1. Select the files and record versions, dependencies, reproduction commands, failures, and open items.
2. Verify the selected result from a clean directory.
3. Record file hashes; if using Git, commit only the selected files and create a unique tag.
4. Create a ZIP only when delivery is needed. Check paths, checksums, extraction, and the documented reproduction command.
5. Obtain any required external publication authority. Integrity checks are not scientific proof or publication approval.

The full parent workflow has optional certification, dispatch, and Auto machinery. They are not included in this starter.
