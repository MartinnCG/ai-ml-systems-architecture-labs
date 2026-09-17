# Lab 03 — Governed Evidence-to-Decision Agent

## Purpose

This lab tests whether an AI-assisted system can turn verified operational
evidence into a concise decision brief while preserving traceability,
uncertainty, abstention and human authority.

The objective is not to build a general chatbot. It is to isolate and test the
boundary between trusted evidence, probabilistic generation and an accountable
human decision.

## Core question

Can a model produce useful operational synthesis without introducing unsupported
claims, obeying instructions embedded in evidence or acting beyond the supplied
evidence boundary?

## Inputs

The lab accepts an allowlisted evidence packet containing:

- stable evidence identifiers;
- source and observation metadata;
- structured facts or already-sanitised excerpts;
- freshness and scope declarations;
- integrity information where available.

Initial fixtures are synthetic or derived only from public, sanitised results.
Private telemetry, identities, credentials, locations and deployment paths are
excluded.

## Output

The agent produces a structured decision brief containing:

- answer status: supported, qualified or abstained;
- factual claims with evidence identifiers;
- uncertainty and conflicts;
- explicit limitations;
- suggested questions for human review;
- no command or actuator instruction.

Each run also produces an audit record covering the evidence set, prompt
template, model/configuration, validator version and final disposition.

## Invariants

- **G1 — Evidence closure:** every factual claim cites an identifier present in
  the supplied evidence packet.
- **G2 — No instruction inheritance:** evidence content is data, never executable
  instruction.
- **G3 — Honest insufficiency:** missing or conflicting support produces
  qualification or abstention.
- **G4 — Human authority:** the system cannot approve, dispatch or actuate.
- **G5 — Auditable execution:** a brief can be connected to its exact evidence,
  configuration and validation result.
- **G6 — Privacy preservation:** outputs cannot reveal fields excluded at the
  evidence boundary.
- **G7 — Accurate reproducibility claim:** evidence inputs and validation are
  reproducible; natural-language generation is not described as deterministic.

## Non-goals

- autonomous control;
- safety, maintenance or compliance authorization;
- diagnosis or calibrated prediction;
- unrestricted retrieval from private repositories;
- hiding uncertainty behind fluent language;
- claiming that identical prompts guarantee identical model text.

## Delivery sequence

1. **M0 — Contracts:** architecture, threat model and evaluation contract.
2. **M1 — Deterministic baseline:** rule-based brief and validator with no model.
3. **M2 — Provider-neutral model adapter:** structured generation behind the same
   contracts.
4. **M3 — Adversarial evaluation:** unsupported, conflicting, stale, injected and
   out-of-scope evidence cases.
5. **M4 — Portfolio demonstration:** sanitised operational evidence first;
   geospatial evidence may follow through the same boundary.

M9B hardware work is not a dependency for this lab.
