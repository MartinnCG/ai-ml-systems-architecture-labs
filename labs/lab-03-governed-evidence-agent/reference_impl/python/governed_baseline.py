"""Deterministic evidence-to-decision baseline for Lab 03 M1.

The baseline deliberately contains no model integration.  It demonstrates the
control envelope that a later probabilistic adapter must obey.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


CONTRACT_VERSION = "1.0"
BASELINE_VERSION = "m1.0"
ALLOWED_CLASSIFICATIONS = {"public", "sanitised"}
ALLOWED_PURPOSES = {"historical_replay_qualification"}
FORBIDDEN_KEYS = {
    "credentials",
    "deployment_path",
    "personal_schedule",
    "precise_location",
    "private_key",
    "raw_telemetry",
}
AUTHORITY_PATTERNS = (
    re.compile(r"\bapprove(?:d|s)?\b", re.IGNORECASE),
    re.compile(r"\bdispatch(?:ed|es)?\b", re.IGNORECASE),
    re.compile(r"\bactuat(?:e|ed|es|ion)\b", re.IGNORECASE),
    re.compile(r"\bsafe to operate\b", re.IGNORECASE),
)


class ContractError(ValueError):
    """Input cannot cross the governed evidence boundary."""


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    evidence_id: str
    kind: str
    facts: Mapping[str, Any]
    observed_at: str
    classification: str = "sanitised"
    expires_at: str | None = None
    content: str = ""


@dataclass(frozen=True, slots=True)
class EvidencePacket:
    packet_id: str
    purpose: str
    as_of: str
    evidence: tuple[EvidenceItem, ...]
    schema_version: str = CONTRACT_VERSION


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: str
    text: str
    evidence_ids: tuple[str, ...]
    confidence: str
    limitation: str | None = None


@dataclass(frozen=True, slots=True)
class DecisionBrief:
    status: str
    claims: tuple[Claim, ...] = ()
    limitations: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    human_review_required: bool = True


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class AuditRecord:
    packet_id: str
    packet_sha256: str
    purpose: str
    baseline_version: str
    validator_version: str
    evidence_ids: tuple[str, ...]
    brief_sha256: str
    disposition: str
    findings: tuple[ValidationFinding, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class RunResult:
    brief: DecisionBrief
    audit: AuditRecord


def _canonical(value: Any) -> bytes:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def canonical_digest(value: Any) -> str:
    """Return the stable digest used by control-plane audit records."""
    return _digest(value)


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ContractError("timestamps must use RFC 3339 UTC") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ContractError("timestamps must use UTC")
    return parsed.astimezone(timezone.utc)


def _forbidden_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_KEYS:
                findings.append(child_path)
            findings.extend(_forbidden_keys(child, child_path))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, child in enumerate(value):
            findings.extend(_forbidden_keys(child, f"{path}[{index}]"))
    return findings


def packet_from_mapping(value: Mapping[str, Any]) -> EvidencePacket:
    forbidden = _forbidden_keys(value)
    if forbidden:
        raise ContractError("excluded private fields: " + ", ".join(forbidden))
    required = {"packet_id", "purpose", "as_of", "evidence"}
    missing = sorted(required - set(value))
    if missing:
        raise ContractError("missing packet fields: " + ", ".join(missing))
    if value.get("schema_version", CONTRACT_VERSION) != CONTRACT_VERSION:
        raise ContractError("unsupported schema_version")
    if not isinstance(value["evidence"], list):
        raise ContractError("evidence must be a list")

    _parse_utc(value["as_of"])
    items: list[EvidenceItem] = []
    seen: set[str] = set()
    for raw in value["evidence"]:
        if not isinstance(raw, Mapping):
            raise ContractError("evidence items must be objects")
        item = EvidenceItem(
            evidence_id=str(raw.get("evidence_id", "")),
            kind=str(raw.get("kind", "")),
            facts=raw.get("facts", {}),
            observed_at=str(raw.get("observed_at", "")),
            classification=str(raw.get("classification", "sanitised")),
            expires_at=raw.get("expires_at"),
            content=str(raw.get("content", "")),
        )
        if not item.evidence_id or not item.kind or not isinstance(item.facts, Mapping):
            raise ContractError("evidence_id, kind and object facts are required")
        if item.evidence_id in seen:
            raise ContractError(f"duplicate evidence_id: {item.evidence_id}")
        if item.classification not in ALLOWED_CLASSIFICATIONS:
            raise ContractError(f"classification is not allowlisted: {item.evidence_id}")
        _parse_utc(item.observed_at)
        if item.expires_at is not None:
            _parse_utc(item.expires_at)
        seen.add(item.evidence_id)
        items.append(item)

    return EvidencePacket(
        packet_id=str(value["packet_id"]),
        purpose=str(value["purpose"]),
        as_of=str(value["as_of"]),
        evidence=tuple(items),
        schema_version=str(value.get("schema_version", CONTRACT_VERSION)),
    )


def _stale(item: EvidenceItem, as_of: datetime) -> bool:
    return item.expires_at is not None and _parse_utc(item.expires_at) < as_of


def build_brief(packet: EvidencePacket) -> DecisionBrief:
    """Build a brief from explicit structured facts; free text is never executed."""
    if packet.purpose not in ALLOWED_PURPOSES:
        return DecisionBrief(
            status="abstained",
            limitations=("The requested purpose is outside the M1 allowlist.",),
            missing_evidence=("allowlisted_purpose",),
        )

    by_kind: dict[str, list[EvidenceItem]] = {}
    for item in packet.evidence:
        by_kind.setdefault(item.kind, []).append(item)

    required = {"qualification_summary", "replay_check"}
    missing = tuple(sorted(required - set(by_kind)))
    if missing:
        return DecisionBrief(
            status="abstained",
            limitations=("Evidence is insufficient for the requested conclusion.",),
            missing_evidence=missing,
        )

    summaries = by_kind["qualification_summary"]
    replays = by_kind["replay_check"]
    summary_values = {
        (
            item.facts.get("accepted_records"),
            item.facts.get("rejected_records"),
            item.facts.get("source_streams"),
        )
        for item in summaries
    }
    replay_values = {item.facts.get("independent_replay_match") for item in replays}
    conflicts: list[str] = []
    if len(summary_values) != 1:
        conflicts.append("qualification_summary")
    if len(replay_values) != 1:
        conflicts.append("replay_check")
    if conflicts:
        return DecisionBrief(
            status="qualified",
            limitations=("Conflicting evidence requires human resolution.",),
            conflicts=tuple(conflicts),
        )

    accepted, rejected, streams = next(iter(summary_values))
    replay_match = next(iter(replay_values))
    if not isinstance(accepted, int) or not isinstance(rejected, int) or not isinstance(streams, int):
        return DecisionBrief(status="abstained", missing_evidence=("valid_qualification_counts",))
    if replay_match is not True or accepted <= 0 or rejected != 0:
        return DecisionBrief(
            status="qualified",
            limitations=("The supplied evidence does not satisfy the clean replay rule.",),
            conflicts=("qualification_result",),
        )

    as_of = _parse_utc(packet.as_of)
    used = tuple(summaries + replays)
    stale_ids = tuple(sorted(item.evidence_id for item in used if _stale(item, as_of)))
    ids = tuple(sorted(item.evidence_id for item in used))
    claims = (
        Claim(
            claim_id="claim-record-qualification",
            text=f"{accepted} records were accepted with {rejected} rejections across {streams} source streams.",
            evidence_ids=tuple(sorted(item.evidence_id for item in summaries)),
            confidence="qualified" if stale_ids else "supported",
            limitation="Evidence freshness requires review." if stale_ids else None,
        ),
        Claim(
            claim_id="claim-replay-consistency",
            text="Independent replay produced a matching final state.",
            evidence_ids=tuple(sorted(item.evidence_id for item in replays)),
            confidence="qualified" if stale_ids else "supported",
            limitation="Evidence freshness requires review." if stale_ids else None,
        ),
    )
    limitations = [
        "Historical qualification does not demonstrate current hardware operation, live transport latency or safety suitability."
    ]
    if stale_ids:
        limitations.append("Expired evidence: " + ", ".join(stale_ids))
    return DecisionBrief(
        status="qualified" if stale_ids else "supported",
        claims=claims,
        limitations=tuple(limitations),
    )


def validate_brief(packet: EvidencePacket, brief: DecisionBrief) -> tuple[ValidationFinding, ...]:
    findings: list[ValidationFinding] = []
    known_ids = {item.evidence_id for item in packet.evidence}
    if not brief.human_review_required:
        findings.append(ValidationFinding("human_authority_missing", "Human review must be required."))
    if brief.status not in {"supported", "qualified", "abstained", "rejected"}:
        findings.append(ValidationFinding("invalid_status", "Unknown brief status."))
    for claim in brief.claims:
        if not claim.evidence_ids:
            findings.append(ValidationFinding("uncited_claim", claim.claim_id))
        unknown = sorted(set(claim.evidence_ids) - known_ids)
        if unknown:
            findings.append(ValidationFinding("unknown_citation", f"{claim.claim_id}: {', '.join(unknown)}"))
        if claim.confidence not in {"supported", "qualified"}:
            findings.append(ValidationFinding("invalid_confidence", claim.claim_id))
        if any(pattern.search(claim.text) for pattern in AUTHORITY_PATTERNS):
            findings.append(ValidationFinding("authority_escalation", claim.claim_id))
    if brief.status == "abstained" and brief.claims:
        findings.append(ValidationFinding("abstention_with_claims", "Abstained briefs cannot assert factual claims."))
    return tuple(findings)


def run(packet: EvidencePacket) -> RunResult:
    brief = build_brief(packet)
    findings = validate_brief(packet, brief)
    disposition = "rejected" if findings else brief.status
    if findings:
        brief = DecisionBrief(
            status="rejected",
            limitations=("Deterministic validation rejected the proposed brief.",),
        )
    audit = AuditRecord(
        packet_id=packet.packet_id,
        packet_sha256=_digest(packet),
        purpose=packet.purpose,
        baseline_version=BASELINE_VERSION,
        validator_version=CONTRACT_VERSION,
        evidence_ids=tuple(sorted(item.evidence_id for item in packet.evidence)),
        brief_sha256=_digest(brief),
        disposition=disposition,
        findings=findings,
    )
    return RunResult(brief=brief, audit=audit)


def result_to_mapping(result: RunResult) -> dict[str, Any]:
    return asdict(result)
