# Project Brief

## Project

GroundSeal RAG is a permission-aware hybrid retrieval project for grounded enterprise agents. It studies and builds the retrieval layer that decides which evidence can be used, how evidence is ranked, how permissions shape accessible context, and how citations make downstream answers inspectable.

The project is intentionally retrieval-first. It treats retrieval as an engineering system with contracts, measurements, failure modes, and security-sensitive behavior. A future generation layer may use the retrieval output, but generation is not the center of the project.

## What It Is

- A long-running engineering project for understanding retrieval and RAG internals.
- A grounded context assembly system where evidence identity and source traceability are explicit.
- A permission-aware retrieval project that models access scope as part of candidate selection.
- A citation-first project that treats references as required output of retrieval.
- An evaluation-first project where quality is measured with repeatable cases.

## What It Is Not

- It is not a chatbot demo.
- It is not a UI-first product prototype.
- It is not a thin wrapper around a model API.
- It is not a generic document search project with no permission model.
- It is not a benchmark-chasing project detached from practical engineering constraints.
- It is not a place to create broad package scaffolding before behavior is defined.

## Why This Project Exists

Many RAG projects begin with a chat screen and then try to improve retrieval after the system already appears to work. That order hides the hard parts. The hard parts include source identity, chunk boundaries, metadata quality, permission constraints, candidate ranking, citation fidelity, and failure analysis. GroundSeal RAG reverses the order: it starts by defining the retrieval system that a grounded agent would need.

This makes the project useful as both a learning vehicle and a portfolio artifact. It demonstrates understanding of the infrastructure beneath grounded AI systems rather than only the surface interaction.

## Why Not Start From A Chatbot

A chatbot can make weak retrieval look acceptable because fluent generation masks missing evidence. Starting with chat encourages premature prompt tuning, UI work, and model-provider decisions before the retrieval problem is understood.

GroundSeal RAG should first answer lower-level questions:

- Which sources are registered?
- Which chunks are eligible?
- Which permissions apply to a requester?
- Which evidence was retrieved?
- Which citations support a response?
- Which queries fail, and why?

Only after those questions have disciplined answers should a generation layer be considered.

## Why Permission-Aware Retrieval Is Core

Enterprise agents do not retrieve from a neutral pile of text. They retrieve from sources with ownership, visibility, sensitivity, tenant boundaries, department boundaries, and user-specific access. A retrieval system that ignores permissions can return correct-looking but unauthorized context.

Permission-aware retrieval is therefore not a later security patch. It is part of the retrieval contract. GroundSeal RAG should make permission scope visible at source registration, metadata design, candidate filtering, evaluation, and failure analysis.

## Why Citation-First Matters

Generated answers are only useful in grounded workflows if users can inspect the evidence. Citations help show whether the system used the right source, whether the source was allowed, and whether the answer faithfully reflects retrieved material.

Citation-first design also improves engineering feedback. When a retrieval result is wrong, missing, stale, overbroad, or unauthorized, citation records give the project a concrete object to debug.

## Why Evaluation-First Matters

Retrieval quality cannot be judged only by whether a demo response sounds plausible. Evaluation-first work creates repeatable cases for measuring recall, precision, ranking, permission correctness, citation coverage, and failure patterns.

This matters for learning because it forces tradeoffs to become visible. It matters for a resume because it shows disciplined engineering judgment: baselines, metrics, ablations, reports, and conclusions rather than only a running demo.

## Target Users

- A platform engineer studying retrieval systems for grounded AI applications.
- An enterprise AI team that needs an evidence layer before agent workflows.
- A security-conscious product team exploring permission-aware RAG.
- A future project maintainer who wants clear contracts before adding code.
- A reviewer or interviewer evaluating whether the project demonstrates real retrieval understanding.

## Learning Value

The project is designed to build practical understanding of:

- ingestion boundaries and source metadata
- chunking strategy tradeoffs
- lexical retrieval and ranking behavior
- semantic retrieval and embedding tradeoffs
- hybrid retrieval design
- metadata and permission filtering
- citation packing and evidence budgeting
- reranking experiments
- retrieval evaluation and failure analysis
- grounded context assembly for agents

## Engineering Value

GroundSeal RAG emphasizes engineering practices that matter in production-like retrieval systems:

- explicit contracts before implementation
- small phase exits with artifacts
- measurable retrieval quality
- permission correctness as system behavior
- traceable citations
- failure reports that create future work
- restrained use of dependencies
- implementation choices tied to documented goals

## Resume Value

The project can become resume-ready when it includes a working retrieval pipeline, permission filtering, citation output, and an evaluation suite with documented findings. The strongest resume version would show comparison across lexical, semantic, hybrid, and reranked retrieval while preserving permission correctness and citation traceability.

The project should not be described as a generic RAG chatbot. Its differentiators are retrieval-first architecture, permission-aware filtering, citation-first context assembly, and evaluation-driven iteration.

## Long-Term Direction

The project may evolve into an enterprise-oriented retrieval layer that can support agents, search workflows, compliance-sensitive assistants, and internal knowledge systems. Future extensions could include multi-tenant permissions, source freshness tracking, policy-aware retrieval, audit logs, connector abstractions, and role-specific evaluation sets.

Each extension must remain connected to the core purpose: better grounded retrieval under real-world constraints.

## Non-Goals

- Build a chatbot before retrieval quality is understood.
- Add a web app or API before the retrieval contract is stable.
- Integrate model providers during the framing phase.
- Create large package scaffolding without implemented behavior.
- Optimize for broad feature lists instead of measurable learning.
- Claim enterprise-grade quality without permission and evaluation evidence.
- Hide failures or only document successful examples.
- Treat citations as decorative output.
- Treat permission filtering as a UI concern instead of retrieval behavior.
