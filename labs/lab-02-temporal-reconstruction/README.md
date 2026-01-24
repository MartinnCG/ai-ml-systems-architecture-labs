# Lab 02 — Temporal Reconstruction & Deterministic Replay

## Purpose

This lab explores how an operational system can reconstruct its state at any point in time using only an immutable event history.

The focus is not on architectural patterns, but on **operational guarantees**:
- explainability of system behavior,
- reproducible debugging,
- post-incident analysis,
- safe reasoning about time.

This lab is designed for engineers building long-lived systems that must survive failures, audits, and ownership transfer.

---

## Problem Statement

In real systems, failures are rarely about the current state alone.

They are about:
- how the system reached a condition,
- what happened right before an incident,
- whether a behavior can be reproduced,
- whether historical decisions can be explained.

Systems that cannot reason about their own history cannot be reliably debugged or trusted.

---

## Core Idea

The system’s source of truth is an **immutable, ordered event timeline**.

From this timeline:
- operational state is derived,
- historical states can be reconstructed,
- incidents can be replayed deterministically.

Time is treated as a **first-class system dimension**, not as metadata.

---

## Scope

### In Scope
- immutable event timeline
- deterministic replay
- temporal reconstruction (rebuild until a given point)
- equivalence between live and replayed state
- side-effect-free replay

### Out of Scope
- snapshots or checkpoints
- databases or persistence layers
- distribution or concurrency
- performance optimization
- machine learning models

This lab intentionally avoids premature complexity.

---

## Relationship to Lab 01

Lab 01 establishes the boundary between **events** and **state**.

Lab 02 builds on that boundary by introducing **time-aware reasoning**:
- events are treated as historical facts,
- state becomes a temporal view,
- system behavior becomes explainable over time.

Without Lab 01, this lab would not be possible.

---

## What This Lab Demonstrates

- how systems can reconstruct past states without guesswork,
- why deterministic replay is essential for debugging,
- why explainability is an architectural concern,
- how time-aware design increases system trustworthiness.

---

## What This Lab Does Not Attempt

This lab does not attempt to:
- be production-ready,
- scale horizontally,
- cover all edge cases.

Its purpose is clarity, not completeness.
