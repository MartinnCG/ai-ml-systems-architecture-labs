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

The baseline does not evaluate semantic entailment, call a model, retrieve from
external systems or authorize an operational action. It establishes the control
path against which the M2 model adapter will be tested.
