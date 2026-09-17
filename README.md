# AI/ML Systems Architecture Labs

Architecture-first labs exploring the design, operation and failure modes of
AI/ML systems in real-world, stateful environments.

## Focus

- explicit system boundaries and non-goals;
- state-driven and event-driven behaviour;
- determinism, observability and failure analysis;
- governed AI assistance with human authority;
- transferable engineering patterns rather than tutorials.

These labs are intentionally minimal and reference-oriented. They prioritise
clarity of system behaviour and testable claims over feature completeness.

## Labs

| Lab | Question | Status |
|---|---|---|
| [Lab 01 — Event vs State](labs/lab-01-event-vs-state/) | Can state be treated as a disposable projection of immutable events? | Reference implementation |
| [Lab 02 — Temporal Reconstruction](labs/lab-02-temporal-reconstruction/) | Can historical state be reconstructed and compared deterministically? | Reference implementation |
| [Lab 03 — Governed Evidence Agent](labs/lab-03-governed-evidence-agent/) | Can an AI-assisted system create useful synthesis without escaping its evidence boundary? | Architecture and evaluation contract |

## Evidence standard

A lab must state:

1. the system question and boundary;
2. invariants that can fail;
3. the reference implementation or experiment;
4. verification and adversarial cases;
5. limitations and claims deliberately excluded.

A model-generated demonstration is not sufficient evidence. Inputs, versions,
validation results and human authority must remain visible.
