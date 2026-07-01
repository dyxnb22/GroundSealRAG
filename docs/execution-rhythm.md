# Execution Rhythm

## Purpose

This document defines how GroundSeal RAG should be advanced over many work sessions. The project should use sustained agent work productively without spreading into unfocused code or vague documentation.

## Ideal Single Work Session

A good session should have one clear objective:

- refine one design document
- complete one phase artifact
- add one evaluation concept
- run one experiment
- analyze one failure class
- implement one small phase-aligned behavior after the design exists

A session should not try to build multiple layers at once.

## Session Start

At the beginning of a session:

1. Identify the roadmap phase.
2. Read the relevant project documents.
3. State the intended artifact.
4. Check whether the task is documentation, experiment, implementation, or reporting.
5. Confirm the exit criteria.

## Session End

At the end of a session, leave at least one visible artifact:

- updated document
- task list update
- note
- report
- evaluation case
- failure record
- small implementation with verification

Also record next steps when the work reveals them.

## When To Pause Implementation

Pause implementation and return to documents when:

- the task cannot be mapped to a roadmap phase
- the expected behavior is unclear
- permission behavior is undefined
- citation output is not traceable
- evaluation is missing
- a dependency is being added only for convenience
- failures repeat without a clear category

## When To Start Evaluation

Evaluation should begin before the system feels complete. Start evaluation when:

- candidate output exists or is defined
- query cases can name expected evidence
- permission context affects results
- citation packing decisions are being made
- a new retrieval method is compared to a baseline

Evaluation does not need a large dataset at first. It needs stable cases and honest reporting.

## Avoiding Code Without Conclusions

The project should avoid long stretches of code growth without findings. Every meaningful implementation should produce one of:

- a metric comparison
- a failure category
- a design correction
- a documented tradeoff
- a new evaluation case
- a decision to keep, change, or remove the approach

If code changes do not produce conclusions, the next session should focus on evaluation or reporting.

## Productive Long-Running Agent Work

GroundSeal RAG can use many agent cycles well because each cycle can deepen one layer:

- define the contract
- create examples
- implement the smallest behavior
- evaluate it
- record failures
- update tasks
- refine the roadmap

This rhythm lets the project consume sustained effort while keeping outputs useful. The goal is not to maximize file count. The goal is to accumulate decisions, evidence, and learning.

## Healthy Phase Loop

For each phase:

1. Scope the phase.
2. Update design documents.
3. Define artifacts and exit criteria.
4. Add minimal examples or cases.
5. Implement only if the phase calls for it.
6. Evaluate or review the result.
7. Record findings.
8. Update tasks and open questions.

This loop should continue even after implementation begins.
