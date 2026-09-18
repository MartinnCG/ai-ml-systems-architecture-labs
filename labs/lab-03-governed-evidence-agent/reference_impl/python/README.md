# Lab 03 M1 — Deterministic baseline

This reference implementation creates and validates an evidence-grounded
decision brief without an LLM or external dependency.

## Run

```bash
cd labs/lab-03-governed-evidence-agent/reference_impl/python
python -m unittest -v
python run_demo.py
```

## What is deterministic

- evidence-boundary validation;
- rule-based claim construction;
- citation membership checks;
- abstention and qualification rules;
- privacy-key rejection;
- packet, brief and audit digests.

Free-text evidence is never interpreted as instruction. The baseline reads only
the allowlisted structured facts needed by the selected purpose.

## What this does not prove

The baseline does not evaluate semantic entailment, retrieve from external
systems or authorize an operational action.

## M2 provider-neutral boundary


`model_adapter.py` adds a minimal provider protocol without importing a vendor
SDK or exposing tools. Deterministic fake adapters exercise the boundary:

- proposals must match the decision-brief schema;
- citations and authority language are validated by M1;
- adapter errors fail closed;
- prompt, request, provider/model, configuration, proposal and brief are
  represented by audit digests;
- secret-like configuration keys are rejected.

M2 does not yet establish that a cited claim is semantically entailed by its
evidence. That adversarial support evaluation remains M3.
