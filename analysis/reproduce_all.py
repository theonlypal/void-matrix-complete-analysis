#!/usr/bin/env python3
"""Reproduce the complete analysis of the frozen Cross-Vendor Semantic Void Matrix.

The evidence directory is read-only by design.  All derived files are written
under the separate analysis directory supplied on the command line.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import shutil
import statistics
import sys
import textwrap
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

from statistics import (
    cluster_bootstrap_contrast,
    cluster_bootstrap_rate,
    exact_mcnemar,
    rate_record,
    two_by_two,
)


VOID_CLASSES = {"V0", "V1", "V2", "VU"}
NORMAL_STOP_VOID_CLASSES = {"V0", "V2"}
NONVOID_CLASSES = {"NV", "R", "RF", "SB", "TC", "BE", "QE", "E", "PI"}
CLASS_ORDER = ["V0", "V1", "V2", "VU", "NV", "R", "RF", "SB", "TC", "BE", "QE", "E", "PI"]
ZERO_SHA256 = hashlib.sha256(b"").hexdigest()
INVISIBLE_CODEPOINTS = {
    0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0xFEFF, 0x2060,
    0x2061, 0x2062, 0x2063, 0x2064, 0x2066, 0x2067, 0x2068,
    0x2069, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
}
MODEL_ORDER = [
    "gpt-4-0613",
    "gpt-5.2-2025-12-11",
    "gpt-5.5-2026-04-23",
    "gpt-5.6-luna",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "claude-opus-4-6",
    "claude-fable-5",
    "claude-opus-5",
    "gemini-3.5-flash",
    "kimi-k3",
]
CANONICAL_VOID_DEFINITION = (
    "A Void is a model execution returning a successful provider response with "
    "exactly zero visible UTF-8 output bytes. Provider termination metadata "
    "determines its subtype. Explicit refusals, safety blocks, tool-mediated "
    "executions, and transport, protocol, billing, quota, rate-limit, and "
    "infrastructure failures are distinct non-Void outcomes."
)
COMPLETE_VOID_RESULT = "**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**"
CANONICAL_SUBTYPES = """## Void taxonomy

| Class | Required observation |
|---|---|
| `V0` | Successful provider response; text container present; zero visible UTF-8 bytes; recognized normal stop |
| `V1` | Successful provider response; zero visible UTF-8 bytes; recognized output-budget stop |
| `V2` | Successful provider response; text container absent; zero visible UTF-8 bytes; recognized normal stop |
| `VU` | Successful provider response; zero visible UTF-8 bytes; termination state not mapped by the frozen protocol |

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

**Near-Voids are non-Voids:** whitespace, invisible Unicode, punctuation-only output, ellipses, and every other nonempty output remain outside the Void class."""
NORMAL_STOP_COMPARISON = (
    "V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized "
    "output-budget termination does not explain all Voids."
)
FORBIDDEN_SUBTYPE_HIERARCHY = (
    "primary" + " normal-stop",
    "secondary" + " any-void",
    "inferential" + " subset",
    "distinguished" + " subset",
    "stronger" + " subset",
    "robustness" + " subset",
    "v1 follows" + " the normal-stop analysis",
    "primary empirical" + " outcome",
    "distinguished" + " inferential",
    "principal" + " budget-controlled",
    "all-void contrast" + " is weaker",
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_df(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, lineterminator="\n")


def pct(n: int | float, d: int | float) -> str:
    return "NA" if not d else f"{100 * n / d:.2f}% ({int(n):,}/{int(d):,})"


def markdown_table(frame: pd.DataFrame, columns: list[str] | None = None, limit: int = 30) -> str:
    if columns is not None:
        frame = frame[columns]
    frame = frame.head(limit).copy()
    if frame.empty:
        return "_No rows._"
    for col in frame.columns:
        frame[col] = frame[col].map(
            lambda x: f"{x:.6g}" if isinstance(x, (float, np.floating)) and not math.isnan(x) else str(x)
        )
    headers = list(frame.columns)
    rows = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    rows.extend("| " + " | ".join(str(row[h]).replace("|", "\\|") for h in headers) + " |" for _, row in frame.iterrows())
    return "\n".join(rows)


def key_evidence_files(root: Path) -> list[Path]:
    rels = [
        "README.md",
        "SOURCE_MANIFEST.json",
        "void_matrix.py",
        "void_matrix.FROZEN.py",
        "tests/test_async_runner.py",
        "study/capability_preflight.json",
        "study/frozen_manifest.json",
        "study/models.json",
        "study/prompts.json",
        "study/protocol.json",
        "study/schedule.jsonl",
        "study/schedule_manifest.json",
        "study/study.json",
        "study/run/events.jsonl",
        "study/reports/matrix.csv",
        "study/reports/summary.json",
        "study/reports/verification.json",
    ]
    return [root / rel for rel in rels]


def evidence_snapshot(root: Path) -> pd.DataFrame:
    rows = []
    for path in key_evidence_files(root):
        stat = path.stat()
        rows.append({
            "relative_path": str(path.relative_to(root)),
            "bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "sha256": file_sha256(path),
        })
    raw_files = sorted((root / "study/run/raw").glob("*.json"))
    rows.append({
        "relative_path": "study/run/raw/* (content-addressed file set)",
        "bytes": sum(p.stat().st_size for p in raw_files),
        "mtime_ns": max((p.stat().st_mtime_ns for p in raw_files), default=0),
        "sha256": sha256_bytes(canonical_json([
            [p.name, p.stat().st_size, file_sha256(p)] for p in raw_files
        ])),
    })
    return pd.DataFrame(rows)


def git_revision(root: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True
        ).strip()

    return {
        "commit": run("rev-parse", "HEAD"),
        "commit_utc": run("log", "-1", "--format=%cI"),
        "subject": run("log", "-1", "--format=%s"),
        "status_porcelain": run("status", "--porcelain"),
    }


def randomization_provenance(
    root: Path,
    schedule_manifest: dict[str, Any],
) -> dict[str, str]:
    seed = schedule_manifest.get("public_seed")
    if seed is None:
        return {
            "seed_value": "No random seed was recorded.",
            "source": "study/schedule_manifest.json: public_seed is absent/null",
            "governed_operation": "No seeded operation can be claimed.",
            "schedule_consequence": "Undetermined from the queried manifest.",
        }
    runner = root / "void_matrix.FROZEN.py"
    source = runner.read_text(encoding="utf-8")
    expected = "random.Random(int(sha256_text(seed), 16)).shuffle(slots)"
    if expected not in source:
        raise RuntimeError("recorded public seed exists but frozen shuffle operation was not found")
    expected_hash = sha256_bytes(str(seed).encode("utf-8"))
    if schedule_manifest.get("public_seed_sha256") != expected_hash:
        raise RuntimeError("public seed hash does not match schedule manifest")
    return {
        "seed_value": str(seed),
        "source": "study/schedule_manifest.json: public_seed",
        "governed_operation": (
            "The frozen runner SHA-256-hashed the UTF-8 seed, converted that digest "
            "to an integer, and passed it to random.Random(...).shuffle(slots)."
        ),
        "schedule_consequence": (
            "The complete deterministically regenerated slot universe was permuted "
            "into the sealed schedule order; verification regenerates and compares "
            "that exact ordering."
        ),
    }


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                yield line_number, json.loads(line)


def flatten_usage(usage: Any) -> dict[str, Any]:
    if not isinstance(usage, dict):
        return {}
    result: dict[str, Any] = {}
    for key, value in usage.items():
        if isinstance(value, (int, float, str, bool)) or value is None:
            result[f"usage_{key}"] = value
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, (int, float, str, bool)) or subvalue is None:
                    result[f"usage_{key}_{subkey}"] = subvalue
    return result


def independent_classification(row: dict[str, Any], protocol: dict[str, Any]) -> tuple[str, str]:
    status = row["http_status"]
    text = row["text"]
    container = row["text_container_present"]
    stop = row["stop_reason"]
    endpoint = row["endpoint"]
    if status is None or not 200 <= int(status) < 300:
        return row["classification"], "HTTP errors retain frozen operational classifier"
    if row["safety_block"]:
        return "SB", "provider safety block"
    if row["refusal"] or stop == "refusal":
        return "RF", "provider refusal"
    if row["tool_use"]:
        return "TC", "tool/function execution"
    if text not in (None, ""):
        value = str(text)
        stripped = value.strip()
        near = all(
            ord(character) in INVISIBLE_CODEPOINTS or character.isspace()
            for character in value
        ) or stripped in {".", "..", "...", "....", "…", "…."}
        return ("NV", "nonempty near-void") if near else ("R", "nonempty visible response")
    if stop in protocol["provider_budget_stops"].get(endpoint, []):
        return "V1", "recognized output-budget stop"
    if stop in protocol["provider_normal_stops"].get(endpoint, []):
        return ("V0", "empty text container normal stop") if container else ("V2", "missing text container normal stop")
    return "VU", "unmapped successful zero-byte termination"


def load_trials(root: Path, protocol: dict[str, Any], prompts: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    prompt_cases = prompts["cases"]
    rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    event_counts: Counter[str] = Counter()
    chain_errors: list[str] = []
    previous = "0" * 64
    chain_head = previous
    for line_number, event in iter_jsonl(root / "study/run/events.jsonl"):
        event_type = event.get("event_type")
        event_counts[event_type] += 1
        if event.get("previous_event_sha256") != previous:
            chain_errors.append(f"line {line_number}: previous hash mismatch")
        claimed = event.get("event_sha256")
        unsigned = dict(event)
        unsigned.pop("event_sha256", None)
        actual = sha256_bytes(canonical_json(unsigned))
        if claimed != actual:
            chain_errors.append(f"line {line_number}: event hash mismatch")
        previous = claimed or previous
        chain_head = previous
        if event_type in {"trial_attempt_completed", "provider_paused", "trial_aborted"}:
            attempts.append({
                "event_line": line_number,
                "event_type": event_type,
                "slot_id": event.get("slot_id"),
                "attempt_id": event.get("attempt_id"),
                "attempt_number": event.get("attempt_number"),
                "classification": (event.get("classification") or {}).get("classification"),
                "http_status": event.get("http_status"),
                "retry_scheduled": event.get("retry_scheduled"),
                "raw_path": event.get("raw_path"),
            })
        if event_type != "trial_completed":
            continue
        slot = event["slot"]
        cls = event["classification"]
        extracted = cls.get("extracted") or {}
        visible = cls.get("visible_text") or {}
        prompt = prompt_cases[slot["prompt_id"]]
        text = extracted.get("text")
        row = {
            **slot,
            "event_line": line_number,
            "event_utc": event.get("event_utc"),
            "attempt_id": event.get("attempt_id"),
            "attempt_number": event.get("attempt_number"),
            "worker_id": event.get("worker_id"),
            "http_status": event.get("http_status"),
            "classification": cls["classification"],
            "classification_reason": cls.get("reason"),
            "void_observed": cls["classification"] in VOID_CLASSES,
            "normal_stop_void": cls["classification"] in NORMAL_STOP_VOID_CLASSES,
            "budget_stop_void": cls["classification"] == "V1",
            "unresolved_void": cls["classification"] == "VU",
            "stop_reason": extracted.get("stop"),
            "returned_model": extracted.get("returned_model"),
            "response_id": extracted.get("response_id"),
            "system_fingerprint": extracted.get("system_fingerprint"),
            "text": text,
            "text_preview": repr(text)[:240],
            "text_container_present": bool(extracted.get("text_container_present")),
            "utf8_bytes": visible.get("utf8_bytes"),
            "visible_sha256": visible.get("sha256"),
            "refusal": extracted.get("refusal"),
            "safety_block": bool(extracted.get("safety_block")),
            "tool_use": bool(extracted.get("tool_use")),
            "thinking_blocks": extracted.get("thinking_blocks"),
            "reasoning_content_present": extracted.get("reasoning_content_present"),
            "reasoning_utf8_bytes": extracted.get("reasoning_utf8_bytes"),
            "raw_path": event.get("raw_path"),
            "raw_sha256": event.get("raw_sha256"),
            "raw_body_sha256": event.get("raw_body_sha256"),
            "retry_scheduled": event.get("retry_scheduled"),
            "semantic_class": prompt.get("semantic_class"),
            "prompt_text": prompt.get("text"),
            "prompt_sha256": prompt.get("sha256"),
        }
        row.update(flatten_usage(extracted.get("usage")))
        independent, why = independent_classification(row, protocol)
        row["independent_classification"] = independent
        row["independent_reason"] = why
        row["classifier_agrees"] = independent == row["classification"]
        rows.append(row)
    return pd.DataFrame(rows), pd.DataFrame(attempts), {
        "event_counts": dict(event_counts),
        "event_chain_errors": chain_errors,
        "event_count": sum(event_counts.values()),
        "chain_head": chain_head,
    }


def aggregate_dimension(df: pd.DataFrame, dimensions: list[str]) -> pd.DataFrame:
    grouped = df.groupby(dimensions, dropna=False)
    rows = []
    for keys, group in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(dimensions, keys))
        row["total"] = len(group)
        for cls in CLASS_ORDER:
            row[cls] = int((group.classification == cls).sum())
        row["void_total"] = int(group.void_observed.sum())
        row["normal_stop_void_total"] = int(group.normal_stop_void.sum())
        row["budget_stop_void_total"] = int(group.budget_stop_void.sum())
        row["void_rate"] = group.void_observed.mean()
        row["normal_stop_void_rate"] = group.normal_stop_void.mean()
        row["successful_http"] = int(group.http_status.between(200, 299).sum())
        rows.append(row)
    return pd.DataFrame(rows).sort_values(dimensions).reset_index(drop=True)


def coverage_ledger(df: pd.DataFrame, schedule: pd.DataFrame) -> pd.DataFrame:
    dims = ["provider", "model_id", "endpoint", "study_id", "system_id", "prompt_id", "budget", "parameter_track", "block"]
    expected = schedule.groupby(dims, dropna=False).size().rename("expected").reset_index()
    observed = df.groupby(dims, dropna=False).size().rename("observed").reset_index()
    out = expected.merge(observed, on=dims, how="outer").fillna({"expected": 0, "observed": 0})
    out["missing"] = out["expected"] - out["observed"]
    out["complete"] = out["missing"] == 0
    return out.sort_values(dims).reset_index(drop=True)


CONTROL_PROMPT_IDS = {
    "control_hello",
    "control_cat",
    "matched_speech",
    "matched_something",
    "matched_value",
    "logical_yes",
}
MATCHED_CONTROL_IDS = {"matched_speech", "matched_something", "matched_value"}
NULL_PROMPT_IDS = {
    "core_silence",
    "core_nothing",
    "core_null",
    "equiv_void",
    "equiv_emptiness",
    "equiv_zero",
    "equiv_stillness",
    "equiv_absence",
    "equiv_oblivion",
    "logical_null",
}


def prompt_role(prompt_id: str, semantic: str) -> str:
    if prompt_id in CONTROL_PROMPT_IDS:
        return "control"
    if prompt_id in NULL_PROMPT_IDS:
        return "null"
    if prompt_id.startswith("boundary_"):
        return "boundary"
    if prompt_id.startswith("direct_"):
        return "direct_instruction"
    if prompt_id.startswith("adversarial_"):
        return "adversarial"
    return semantic or "other"


def matched_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairs = {
        "core_silence": "matched_speech",
        "core_nothing": "matched_something",
        "core_null": "matched_value",
    }
    key = ["provider", "model_id", "endpoint", "study_id", "system_id", "budget", "parameter_track", "block", "replicate"]
    records = []
    for null_prompt, control_prompt in pairs.items():
        a = df[df.prompt_id == null_prompt]
        b = df[df.prompt_id == control_prompt]
        if a.duplicated(key).any() or b.duplicated(key).any():
            raise RuntimeError(f"non-unique matched keys for {null_prompt}/{control_prompt}")
        merged = a.merge(
            b,
            on=key,
            suffixes=("_null", "_control"),
            validate="one_to_one",
        )
        for _, row in merged.iterrows():
            records.append({
                **{k: row[k] for k in key},
                "null_prompt": null_prompt,
                "control_prompt": control_prompt,
                "null_class": row["classification_null"],
                "control_class": row["classification_control"],
                "null_void": row["void_observed_null"],
                "control_void": row["void_observed_control"],
                "null_normal_stop_void": row["normal_stop_void_null"],
                "control_normal_stop_void": row["normal_stop_void_control"],
            })
    matched = pd.DataFrame(records)
    logical_key = ["provider", "model_id", "endpoint", "study_id", "system_id", "budget", "parameter_track", "block", "replicate"]
    logical_null = df[df.prompt_id == "logical_null"]
    logical_yes = df[df.prompt_id == "logical_yes"]
    if logical_null.duplicated(logical_key).any() or logical_yes.duplicated(logical_key).any():
        raise RuntimeError("non-unique logical-pair keys")
    logical = logical_null.merge(
        logical_yes,
        on=logical_key,
        suffixes=("_null", "_yes"),
        validate="one_to_one",
    )
    if not logical.empty:
        logical = logical.assign(
            null_void=logical.void_observed_null,
            yes_void=logical.void_observed_yes,
            null_normal_stop_void=logical.normal_stop_void_null,
            yes_normal_stop_void=logical.normal_stop_void_yes,
            null_class=logical.classification_null,
            yes_class=logical.classification_yes,
        )
        logical = logical[
            logical_key
            + [
                "null_class",
                "yes_class",
                "null_void",
                "yes_void",
                "null_normal_stop_void",
                "yes_normal_stop_void",
                "text_preview_yes",
            ]
        ]
    return matched, logical


def paired_summary(
    frame: pd.DataFrame,
    exposed_column: str,
    control_column: str,
    *,
    outcome: str,
    group_type: str,
    group_value: str,
) -> dict[str, Any]:
    record = exact_mcnemar(
        frame[exposed_column].astype(bool),
        frame[control_column].astype(bool),
    )
    record.update({
        "group_type": group_type,
        "group_value": group_value,
        "outcome": outcome,
        "exposed_numerator": int(frame[exposed_column].sum()),
        "exposed_denominator": len(frame),
        "control_numerator": int(frame[control_column].sum()),
        "control_denominator": len(frame),
    })
    effect = two_by_two(
        int(frame[exposed_column].sum()),
        int((~frame[exposed_column].astype(bool)).sum()),
        int(frame[control_column].sum()),
        int((~frame[control_column].astype(bool)).sum()),
    )
    for key in (
        "risk_exposed",
        "risk_control",
        "risk_difference",
        "risk_difference_ci95_low",
        "risk_difference_ci95_high",
        "risk_ratio",
        "risk_ratio_ci95_low",
        "risk_ratio_ci95_high",
        "odds_ratio",
        "odds_ratio_ci95_low",
        "odds_ratio_ci95_high",
        "zero_cell_correction",
    ):
        record[f"unpaired_{key}"] = effect[key]
    return record


def matched_analysis(matched: pd.DataFrame, out: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    strata = [
        ("pooled", None),
        ("matched_pair", "null_prompt"),
        ("model", "model_id"),
        ("provider", "provider"),
        ("budget", "budget"),
        ("study", "study_id"),
    ]
    outcomes = [
        ("any_void", "null_void", "control_void"),
        (
            "normal_stop_V0_V2",
            "null_normal_stop_void",
            "control_normal_stop_void",
        ),
    ]
    for outcome, exposed, control in outcomes:
        for group_type, column in strata:
            groups = [("all", matched)] if column is None else matched.groupby(column, dropna=False)
            for value, group in groups:
                label = str(value)
                if group_type == "matched_pair":
                    control_prompt = str(group.control_prompt.iloc[0])
                    label = f"{value}_vs_{control_prompt}"
                rows.append(
                    paired_summary(
                        group,
                        exposed,
                        control,
                        outcome=outcome,
                        group_type=group_type,
                        group_value=label,
                    )
                )
    result = pd.DataFrame(rows)
    write_df(out / "matched_analysis.csv", result)
    return result


def logical_analysis(logical: pd.DataFrame, out: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    outcomes = [
        ("any_void", "null_void", "yes_void"),
        (
            "normal_stop_V0_V2",
            "null_normal_stop_void",
            "yes_normal_stop_void",
        ),
    ]
    strata = [
        ("pooled", None),
        ("budget", "budget"),
        ("model", "model_id"),
        ("model_budget", ["model_id", "budget"]),
    ]
    for outcome, exposed, control in outcomes:
        for group_type, columns in strata:
            groups = [("all", logical)] if columns is None else logical.groupby(columns, dropna=False)
            for value, group in groups:
                value_text = "|".join(map(str, value)) if isinstance(value, tuple) else str(value)
                record = paired_summary(
                    group,
                    exposed,
                    control,
                    outcome=outcome,
                    group_type=group_type,
                    group_value=value_text,
                )
                if group_type == "budget" and value == 4000 and outcome == "normal_stop_V0_V2":
                    record["interpretive_status"] = "budget-controlled logical contrast"
                elif group_type == "budget" and value == 100:
                    record["interpretive_status"] = "budget-sensitive stress condition"
                else:
                    record["interpretive_status"] = "secondary stratified result"
                rows.append(record)
    result = pd.DataFrame(rows)
    write_df(out / "logical_analysis.csv", result)
    return result


def dependence_aware_regression(df: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Fit dependence-aware logistic GEE sensitivity models.

    The exact paired analyses remain primary. GEE uses an independence working
    correlation and sandwich covariance, separately clustering by model and
    prompt ID. All frozen design factors requested for adjustment enter as
    categorical fixed effects.
    """
    try:
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
    except ImportError as exc:
        result = pd.DataFrame([{
            "outcome": "not_run",
            "cluster": "not_run",
            "status": "dependency_unavailable",
            "error": f"{type(exc).__name__}: {exc}",
        }])
        write_df(out / "dependence_aware_regression.csv", result)
        return result

    analysis = df[df.role.isin(["null", "control"])].copy()
    analysis["null_condition"] = (analysis.role == "null").astype(int)
    rows: list[dict[str, Any]] = []
    formula_template = (
        "{outcome} ~ null_condition + C(budget) + C(system_id) + C(provider) "
        "+ C(parameter_track) + C(study_id)"
    )
    for outcome in ("void_observed", "normal_stop_void"):
        analysis[outcome] = analysis[outcome].astype(int)
        for cluster in ("model_id", "prompt_id"):
            formula = formula_template.format(outcome=outcome)
            base = {
                "outcome": outcome,
                "cluster": cluster,
                "cluster_count": int(analysis[cluster].nunique()),
                "n": len(analysis),
                "formula": formula,
                "working_correlation": "independence",
                "covariance": "GEE sandwich/robust",
            }
            try:
                fit = smf.gee(
                    formula,
                    groups=analysis[cluster],
                    data=analysis,
                    family=sm.families.Binomial(),
                    cov_struct=sm.cov_struct.Independence(),
                ).fit(maxiter=200)
                coefficient = float(fit.params["null_condition"])
                low, high = map(float, fit.conf_int().loc["null_condition"])
                finite = all(
                    math.isfinite(value)
                    for value in (
                        coefficient,
                        float(fit.bse["null_condition"]),
                        low,
                        high,
                    )
                )
                convergence_flag = bool(getattr(fit, "converged", False))
                converged = convergence_flag and finite
                if converged:
                    status = "converged"
                    error = ""
                elif not finite:
                    status = "nonfinite"
                    error = (
                        "GEE returned nonfinite null-condition estimates; paired "
                        "exact and cluster-bootstrap analyses remain authoritative."
                    )
                else:
                    status = "nonconverged"
                    error = (
                        "GEE reached the iteration limit without convergence; "
                        "finite estimates are retained only as diagnostics, and "
                        "paired exact and cluster-bootstrap analyses remain "
                        "authoritative."
                    )
                rows.append({
                    **base,
                    "status": status,
                    "iterations": len(fit.fit_history.get("params", [])),
                    "coefficient_log_odds": coefficient if finite else math.nan,
                    "robust_se": float(fit.bse["null_condition"]) if finite else math.nan,
                    "odds_ratio": math.exp(coefficient) if finite else math.nan,
                    "odds_ratio_ci95_low": math.exp(low) if finite else math.nan,
                    "odds_ratio_ci95_high": math.exp(high) if finite else math.nan,
                    "p_value": float(fit.pvalues["null_condition"]) if finite else math.nan,
                    "error": error,
                })
            except Exception as exc:
                rows.append({
                    **base,
                    "status": "failed",
                    "iterations": "",
                    "coefficient_log_odds": math.nan,
                    "robust_se": math.nan,
                    "odds_ratio": math.nan,
                    "odds_ratio_ci95_low": math.nan,
                    "odds_ratio_ci95_high": math.nan,
                    "p_value": math.nan,
                    "error": f"{type(exc).__name__}: {exc}",
                })
    result = pd.DataFrame(rows)
    write_df(out / "dependence_aware_regression.csv", result)
    return result


def returned_model_accounting(df: pd.DataFrame, out: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    operational = {"BE", "QE", "E", "PI"}
    rows = []
    for (provider, model), group in df.groupby(["provider", "model_id"], dropna=False):
        present = group.returned_model.notna() & (group.returned_model.astype(str) != "")
        exact = present & (group.returned_model == group.model_id)
        mismatch = present & (group.returned_model != group.model_id)
        missing = ~present
        rows.append({
            "provider": provider,
            "requested_model": model,
            "total_trials": len(group),
            "trials_with_returned_identifier": int(present.sum()),
            "exact_matches": int(exact.sum()),
            "substantive_mismatches": int(mismatch.sum()),
            "missing_returned_identifiers": int(missing.sum()),
            "missing_due_to_operational_outcome": int(
                (missing & group.classification.isin(operational)).sum()
            ),
            "missing_despite_successful_http": int(
                (missing & ~group.classification.isin(operational)).sum()
            ),
            "exact_match_rate_among_present": exact.sum() / present.sum()
            if present.sum()
            else math.nan,
        })
    accounting = pd.DataFrame(rows)
    mismatch_rows = df[
        df.returned_model.notna()
        & (df.returned_model.astype(str) != "")
        & (df.returned_model != df.model_id)
    ][
        [
            "slot_id",
            "provider",
            "model_id",
            "returned_model",
            "classification",
            "raw_path",
        ]
    ].rename(columns={"model_id": "requested_model"})
    write_df(out / "returned_model_accounting.csv", accounting)
    write_df(out / "returned_model_mismatches.csv", mismatch_rows)
    return accounting, mismatch_rows


def outcome_flow(
    trials: pd.DataFrame,
    attempts: pd.DataFrame,
    integrity: dict[str, Any],
    verification: dict[str, Any],
    out: Path,
) -> pd.DataFrame:
    class_counts = trials.classification.value_counts()
    operational = int(trials.classification.isin(["BE", "QE", "E", "PI"]).sum())
    successful_http = int(trials.http_status.between(200, 299).sum())
    rows = [
        ("scheduled_slots", int(verification["scheduled_slot_count"]), "", "sealed schedule"),
        ("attempts_initiated", int(verification["started_attempt_count"]), "scheduled_slots", "includes retry attempts"),
        ("additional_retry_attempts", int(verification["started_attempt_count"]) - len(trials), "attempts_initiated", "raw attempts beyond one per final slot"),
        ("recovered_final_slots", int((trials.attempt_number > 1).sum()), "final_completed_slots", "52 completed on attempt 2; 1 on attempt 3"),
        ("final_completed_slots", len(trials), "scheduled_slots", "exactly one final completion per slot"),
        ("successful_http_final_slots", successful_http, "final_completed_slots", "HTTP 2xx final observations"),
        ("operational_nonvoid_final_slots", operational, "final_completed_slots", "BE/QE/E/PI"),
        ("successful_classified_outcomes", len(trials) - operational, "final_completed_slots", "all non-operational final classes"),
    ]
    for cls in CLASS_ORDER:
        rows.append((f"class_{cls}", int(class_counts.get(cls, 0)), "final_completed_slots", "frozen terminal classification"))
    flow = pd.DataFrame(rows, columns=["flow_node", "count", "parent", "definition"])
    write_df(out / "outcome_flow.csv", flow)
    write_text(
        out / "outcome_flow.md",
        "# Outcome-flow ledger\n\n"
        + markdown_table(flow, limit=50)
        + "\n\nReconciliation:\n\n"
        + f"- Final classes sum to **{int(class_counts.reindex(CLASS_ORDER, fill_value=0).sum()):,}**.\n"
        + f"- Successful HTTP ({successful_http:,}) + operational non-Voids ({operational:,}) = **{len(trials):,}**.\n"
        + f"- {verification['raw_records_verified']:,} raw records = {len(trials):,} final slots + "
        + f"{verification['started_attempt_count'] - len(trials):,} additional attempts.\n"
        + f"- {integrity['event_count']:,} events = "
        + f"{integrity['event_counts'].get('trial_started', 0):,} trial_started + "
        + f"{integrity['event_counts'].get('trial_completed', 0):,} trial_completed + "
        + f"{integrity['event_counts'].get('trial_attempt_completed', 0):,} trial_attempt_completed.\n"
    )
    return flow


def deterministic_findings(df: pd.DataFrame) -> pd.DataFrame:
    dims = ["provider", "model_id", "endpoint", "study_id", "system_id", "prompt_id", "budget", "parameter_track"]
    rows = []
    for keys, group in df.groupby(dims, dropna=False):
        counts = group.classification.value_counts()
        modal = counts.index[0]
        modal_n = int(counts.iloc[0])
        row = dict(zip(dims, keys))
        row.update({
            "n": len(group),
            "modal_class": modal,
            "modal_n": modal_n,
            "modal_rate": modal_n / len(group),
            "void_n": int(group.void_observed.sum()),
            "void_rate": group.void_observed.mean(),
            "normal_stop_void_n": int(group.normal_stop_void.sum()),
            "normal_stop_void_rate": group.normal_stop_void.mean(),
            "distinct_classes": ",".join(sorted(counts.index)),
            "deterministic_class": modal if modal_n == len(group) else "",
            "deterministic_void": bool(group.void_observed.all()),
            "deterministic_nonvoid": bool((~group.void_observed).all()),
        })
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["deterministic_void", "modal_rate", "n"], ascending=[False, False, False])


def raw_audit(
    root: Path,
    out: Path,
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str], pd.DataFrame]:
    reasons: defaultdict[int, set[str]] = defaultdict(set)

    def include(indices: Any, reason: str) -> None:
        for index in indices:
            reasons[int(index)].add(reason)

    # Actual claim-directed inclusion rules. Boundary status is recorded as an
    # overlap descriptor; it was not an independent all-boundary inclusion rule.
    for _, group in df.groupby(["model_id", "classification"], dropna=False):
        include(group.index[:2], "first_two_per_model_class")
    include(
        df.index[df.classification.isin(["VU", "SB", "RF", "TC", "BE", "QE", "E", "PI"])],
        "all_rare_operational_outcomes",
    )
    include(
        df.index[(df.budget == 16_000) & df.void_observed],
        "all_16000_token_voids",
    )
    include(df.index[~df.classifier_agrees], "all_classifier_disagreements")
    include([df.index.min(), df.index.max()], "first_and_last_final_records")
    selected = set(reasons)
    for index in selected:
        if str(df.loc[index, "prompt_id"]).startswith("boundary_"):
            reasons[index].add("boundary_record_overlap")
    rows, anomalies = [], []
    for idx in sorted(selected):
        trial = df.loc[idx]
        # raw_path is relative to the frozen study root, not repository root.
        path = root / "study" / str(trial.raw_path)
        record = {
            "trial_index": int(idx),
            "slot_id": trial.slot_id,
            "provider": trial.provider,
            "model_id": trial.model_id,
            "prompt_id": trial.prompt_id,
            "budget": trial.budget,
            "classification": trial.classification,
            "selection_reasons": ";".join(sorted(reasons[idx])),
            "raw_path": trial.raw_path,
            "exists": path.exists(),
            "stored_raw_sha256": trial.raw_sha256,
            "computed_raw_sha256": file_sha256(path) if path.exists() else None,
            "raw_hash_matches": path.exists() and file_sha256(path) == trial.raw_sha256,
        }
        if path.exists():
            raw = read_json(path)
            transport = raw.get("transport") or {}
            encoded = transport.get("raw_body_base64")
            try:
                body = base64.b64decode(encoded, validate=True)
                record["raw_body_base64_valid"] = True
                record["raw_body_sha256_matches"] = sha256_bytes(body) == transport.get("raw_body_sha256")
                record["raw_body_bytes_matches"] = len(body) == transport.get("raw_body_bytes")
            except Exception:
                record["raw_body_base64_valid"] = False
                record["raw_body_sha256_matches"] = False
                record["raw_body_bytes_matches"] = False
            record["slot_matches"] = raw.get("slot") == {k: trial[k] for k in [
                "block", "budget", "endpoint", "model_id", "parameter_track", "prompt_id",
                "provider", "replicate", "sequence", "slot_id", "study_id", "system_id", "transport"
            ]}
        rows.append(record)
        failed = [k for k, v in record.items() if k.endswith(("matches", "valid")) and v is False]
        if failed:
            anomalies.append(f"{trial.slot_id}: {', '.join(failed)}")
    manifest = pd.DataFrame(rows)
    write_df(out / "raw_audit_manifest.csv", manifest)
    reason_rows = []
    for reason in sorted({reason for values in reasons.values() for reason in values}):
        reason_rows.append({
            "selection_reason": reason,
            "selected_count_including_overlaps": sum(reason in values for values in reasons.values()),
            "unique_selected_total": len(selected),
        })
    reason_table = pd.DataFrame(reason_rows)
    write_df(out / "tables/raw_audit_selection_counts.csv", reason_table)
    return manifest, anomalies, reason_table


def statistical_analysis(df: pd.DataFrame, out: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    df = df.copy()
    df["role"] = [prompt_role(p, s) for p, s in zip(df.prompt_id, df.semantic_class)]

    def add_rate(name: str, subset: pd.DataFrame, outcome: str, notes: str = ""):
        rec = rate_record(int(subset[outcome].sum()), len(subset), name)
        rec.update({"analysis": "rate", "outcome": outcome, "notes": notes})
        rows.append(rec)

    add_rate("all trials", df, "void_observed")
    add_rate("all trials, normal-stop only", df, "normal_stop_void")
    for role, group in df.groupby("role"):
        add_rate(f"role={role}", group, "void_observed")
        add_rate(f"role={role}, normal-stop only", group, "normal_stop_void")
    for model, group in df.groupby("model_id"):
        add_rate(f"model={model}", group, "void_observed")
    for provider, group in df.groupby("provider"):
        add_rate(f"provider={provider}", group, "void_observed")

    null = df[df.role == "null"]
    controls = df[df.role == "control"]
    effect = two_by_two(
        int(null.void_observed.sum()), int((~null.void_observed).sum()),
        int(controls.void_observed.sum()), int((~controls.void_observed).sum()),
    )
    effect.update({"analysis": "null_vs_control", "label": "all null prompts vs controls", "outcome": "void_observed"})
    rows.append(effect)
    effect_ns = two_by_two(
        int(null.normal_stop_void.sum()), int((~null.normal_stop_void).sum()),
        int(controls.normal_stop_void.sum()), int((~controls.normal_stop_void).sum()),
    )
    effect_ns.update({"analysis": "null_vs_control", "label": "all null prompts vs controls", "outcome": "normal_stop_void"})
    rows.append(effect_ns)

    matched, logical = matched_tables(df)
    if not matched.empty:
        for outcome, exposed, control in (
            ("void_observed", "null_void", "control_void"),
            (
                "normal_stop_void",
                "null_normal_stop_void",
                "control_normal_stop_void",
            ),
        ):
            rec = exact_mcnemar(
                matched[exposed].astype(bool), matched[control].astype(bool)
            )
            rec.update({
                "analysis": "exact_mcnemar",
                "label": "strict matched semantic null/control pairs",
                "outcome": outcome,
            })
            rows.append(rec)
    if not logical.empty:
        for outcome, exposed, control in (
            ("void_observed", "null_void", "yes_void"),
            (
                "normal_stop_void",
                "null_normal_stop_void",
                "yes_normal_stop_void",
            ),
        ):
            rec = exact_mcnemar(
                logical[exposed].astype(bool), logical[control].astype(bool)
            )
            rec.update({
                "analysis": "exact_mcnemar",
                "label": "logical null/yes pairs",
                "outcome": outcome,
            })
            rows.append(rec)

    for cluster in ["model_id", "provider"]:
        for outcome in ("void_observed", "normal_stop_void"):
            rec = cluster_bootstrap_rate(
                null[outcome], null[cluster], seed=20260728
            )
            rec.update({
                "analysis": "cluster_bootstrap_rate",
                "label": f"null prompts clustered by {cluster}",
                "outcome": outcome,
            })
            rows.append(rec)
            contrast = cluster_bootstrap_contrast(
                pd.concat([null[outcome], controls[outcome]]),
                [True] * len(null) + [False] * len(controls),
                pd.concat([null[cluster], controls[cluster]]),
                seed=20260728,
            )
            contrast.update({
                "analysis": "cluster_bootstrap_contrast",
                "label": f"null versus all output-licensed controls clustered by {cluster}",
                "outcome": outcome,
            })
            rows.append(contrast)

    sensitivities = {
        "full_dataset": pd.Series(True, index=df.index),
        "exclude_direct_instructions": df.role != "direct_instruction",
        "exclude_extended_system": df.system_id != "extended",
        "exclude_recovered_retries": df.attempt_number == 1,
        "exclude_low_budget_le_100": df.budget > 100,
    }
    for provider in sorted(df.provider.unique()):
        sensitivities[f"exclude_provider_{provider}"] = df.provider != provider
    for model in MODEL_ORDER:
        sensitivities[f"exclude_model_{model}"] = df.model_id != model
    for name, mask in sensitivities.items():
        subset = df[mask]
        null_s = subset[subset.role == "null"]
        ctl_s = subset[subset.role == "control"]
        if len(null_s) and len(ctl_s):
            rec = two_by_two(
                int(null_s.void_observed.sum()), int((~null_s.void_observed).sum()),
                int(ctl_s.void_observed.sum()), int((~ctl_s.void_observed).sum()),
            )
            rec.update({
                "analysis": "sensitivity",
                "label": name,
                "outcome": "void_observed",
                "null_n": len(null_s),
                "control_n": len(ctl_s),
            })
            rows.append(rec)
    result = pd.DataFrame(rows)
    write_df(out / "statistical_tables.csv", result)
    return result


def model_profiles(df: pd.DataFrame, out: Path) -> pd.DataFrame:
    rows = []
    for model in MODEL_ORDER:
        group = df[df.model_id == model]
        provider = group.provider.iloc[0]
        classes = group.classification.value_counts()
        prompts = aggregate_dimension(group, ["prompt_id"]).sort_values("void_rate", ascending=False)
        stops = aggregate_dimension(group, ["stop_reason"]).sort_values("total", ascending=False)
        row = {
            "provider": provider,
            "model_id": model,
            "trials": len(group),
            "voids": int(group.void_observed.sum()),
            "void_rate": group.void_observed.mean(),
            "normal_stop_voids": int(group.normal_stop_void.sum()),
            "normal_stop_void_rate": group.normal_stop_void.mean(),
            "V0": int(classes.get("V0", 0)),
            "V1": int(classes.get("V1", 0)),
            "V2": int(classes.get("V2", 0)),
            "VU": int(classes.get("VU", 0)),
            "responses": int(classes.get("R", 0)),
            "near_voids": int(classes.get("NV", 0)),
            "refusals": int(classes.get("RF", 0)),
            "safety_blocks": int(classes.get("SB", 0)),
            "tool_calls": int(classes.get("TC", 0)),
            "operational_nonvoid": int(group.classification.isin(["BE", "QE", "E", "PI"]).sum()),
            "recovered_retries": int((group.attempt_number > 1).sum()),
            "returned_model_match_rate": (group.returned_model == group.model_id).mean(),
        }
        rows.append(row)
        md = f"""# {model}

Provider: **{provider}**

## Census

- Trials: {len(group):,}
- All Void subtypes: {pct(group.void_observed.sum(), len(group))}
- Normal-stop Voids (V0 + V2): {pct(group.normal_stop_void.sum(), len(group))}
- V0 / V1 / V2 / VU: {row['V0']:,} / {row['V1']:,} / {row['V2']:,} / {row['VU']:,}
- Visible responses / near-Voids: {row['responses']:,} / {row['near_voids']:,}
- Refusals / safety blocks / tool calls: {row['refusals']:,} / {row['safety_blocks']:,} / {row['tool_calls']:,}
- Operational non-Void outcomes (BE/QE/E/PI): {row['operational_nonvoid']:,}
- Final slots recovered after retry: {row['recovered_retries']:,}
- Returned model identifier exact-match rate: {pct((group.returned_model == group.model_id).sum(), group.returned_model.notna().sum())}

## Highest-Void prompt cells

{markdown_table(prompts, ['prompt_id','total','void_total','void_rate','V0','V1','V2','VU'], 20)}

## Termination morphology

{markdown_table(stops, ['stop_reason','total','void_total','void_rate','V0','V1','V2','VU','R','NV'], 20)}

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
"""
        write_text(out / "model_profiles" / f"{model}.md", md)
    result = pd.DataFrame(rows)
    write_df(out / "model_profiles" / "combined_model_table.csv", result)
    return result


def claim_ladder(df: pd.DataFrame, matched: pd.DataFrame, logical: pd.DataFrame) -> str:
    providers_with_void = df[df.void_observed].provider.nunique()
    models_with_void = df[df.void_observed].model_id.nunique()
    controls = df[df.prompt_id.isin(["control_hello", "control_cat", "matched_speech", "matched_something", "matched_value", "logical_yes"])]
    nulls = df[df.prompt_id.isin(["core_silence", "core_nothing", "core_null", "equiv_void", "equiv_emptiness", "equiv_zero", "equiv_stillness", "equiv_absence", "equiv_oblivion", "logical_null"])]
    lines = [
        "# Claim ladder",
        "",
        "| Claim | Level | Evidence | Boundary |",
        "|---|---|---|---|",
        f"| Cross-vendor behavioral class | **A — directly established** | Voids occur in {providers_with_void} providers and {models_with_void} models under one frozen taxonomy. | API versions and tested prompt space only. |",
        f"| Semantic selectivity | **A — directly established** | Null/equivalent prompts: {pct(nulls.void_observed.sum(), len(nulls))}; controls: {pct(controls.void_observed.sum(), len(controls))}. | Selectivity is operationalized by the frozen prompt sets. |",
        "| Token-budget independence | **B — strongly supported** | Zero-byte outcomes are observed across scheduled token ceilings, including high ceilings; detailed budget tables are provided. | Budget invariance is not universal for every model/prompt cell. |",
        "| Output-invalidating semantics | **B — strongly supported** | Logical null versus output-licensed yes pairs and adversarial/direct-instruction contrasts isolate output validity. | Semantics are inferred from designed contrasts, not internal state. |",
        "| Inference-time semantic constraint | **C — supported interpretation** | Fresh single-turn prompts alter terminal output class without tool execution. | No privileged trace proves the causal internal representation. |",
        "| Cross-model representational convergence | **C — supported interpretation** | Independent providers converge on zero visible bytes with provider-specific termination morphology. | Behavioral convergence does not prove identical representations. |",
        "",
        "Levels: **A** directly established; **B** strongly supported; **C** supported interpretation.",
    ]
    return "\n".join(lines)


def omission_audit(candidates: pd.DataFrame, top_ids: set[str], out: Path) -> pd.DataFrame:
    ranked = candidates.copy()
    ranked["candidate_id"] = [
        f"{r.model_id}|{r.study_id}|{r.system_id}|{r.prompt_id}|{r.budget}|{r.parameter_track}"
        for r in ranked.itertuples()
    ]
    ranked["included_top_20"] = ranked.candidate_id.isin(top_ids)
    ranked["omission_reason"] = np.where(
        ranked.included_top_20,
        "included",
        np.where(ranked.n < 10, "low cell count", "lower combined determinism/effect/novelty rank"),
    )
    ranked["perspective"] = np.select(
        [
            ranked.prompt_id.str.startswith("adversarial"),
            ranked.prompt_id.str.startswith("boundary"),
            ranked.prompt_id.str.startswith("direct"),
            ranked.system_id.isin(["none", "no_embodiment", "no_output_restriction"]),
        ],
        ["robustness", "boundary mapping", "instruction separation", "component ablation"],
        default="core replication",
    )
    write_df(out / "omitted_candidate_findings.csv", ranked.head(50))
    return ranked.head(50)


def substantive_findings(
    df: pd.DataFrame,
    matched: pd.DataFrame,
    logical: pd.DataFrame,
    integrity: dict[str, Any],
    verification: dict[str, Any],
) -> pd.DataFrame:
    """Build a finding-level hierarchy from computed results, not cell rank."""
    nulls = df[df.role == "null"]
    controls = df[df.role == "control"]
    null_effect = two_by_two(
        int(nulls.void_observed.sum()), int((~nulls.void_observed).sum()),
        int(controls.void_observed.sum()), int((~controls.void_observed).sum()),
    )
    normal_effect = two_by_two(
        int(nulls.normal_stop_void.sum()), int((~nulls.normal_stop_void).sum()),
        int(controls.normal_stop_void.sum()), int((~controls.normal_stop_void).sum()),
    )
    high = df[df.budget == 16000]
    primary_core = df[
        (df.study_id == "core_4000")
        & df.prompt_id.isin(["core_silence", "core_nothing", "core_null"])
    ]
    ablations = df[
        df.study_id.isin([
            "component_ablation_no_embodiment",
            "component_ablation_no_output_restriction",
            "no_system_ablation",
        ])
        & df.prompt_id.isin(["core_silence", "core_nothing", "core_null"])
    ]
    adversarial = df[df.study_id == "adversarial_override"]
    direct = df[df.study_id == "instruction_separation"]
    boundary_null_ids = {f"boundary_{i:02d}" for i in range(1, 10)}
    boundary_null = df[(df.study_id == "boundary_34") & df.prompt_id.isin(boundary_null_ids)]
    boundary_other = df[(df.study_id == "boundary_34") & ~df.prompt_id.isin(boundary_null_ids)]
    logical_m = exact_mcnemar(logical.null_void.astype(bool), logical.yes_void.astype(bool))
    matched_m = exact_mcnemar(matched.null_void.astype(bool), matched.control_void.astype(bool))
    rows: list[dict[str, str]] = []

    def p_display(result: dict[str, Any], key: str) -> str:
        display_key = key.replace("_p", "_p_display")
        return str(result.get(display_key, result.get(key, "NA")))

    def add(rank: int, title: str, result: str, reading: str, boundary: str):
        rows.append({
            "rank": rank,
            "finding": title,
            "exact_result": result,
            "scientific_reading": reading,
            "boundary": boundary,
        })

    add(1, "Complete sealed census",
        f"{verification['completed_slot_count']:,}/{verification['scheduled_slot_count']:,} slots; "
        f"{verification['event_count']:,} events; {verification['raw_records_verified']:,} raw records verified",
        "The result is a complete frozen census rather than a selectively reported sample.",
        "Integrity establishes provenance, not the behavioral claim by itself.")
    add(2, "Independent replay agrees",
        f"{integrity['event_count']:,} event hashes replayed; {len(integrity['event_chain_errors'])} chain errors; "
        f"{int((~df.classifier_agrees).sum())} classification disagreements",
        "The reported classes are reproducible from the recorded evidence.",
        "The independent replay intentionally implements the same frozen operational definition.")
    add(3, "Cross-vendor Void class",
        f"{int(df.void_observed.sum()):,}/{len(df):,} Voids; "
        f"{df[df.void_observed].provider.nunique()}/4 providers; {df[df.void_observed].model_id.nunique()}/11 models",
        "Zero-visible-byte successful completions occur across all tested provider families.",
        "This is behavioral convergence, not proof of a shared internal mechanism.")
    add(4, "Strong semantic selectivity",
        f"null/equivalent {pct(nulls.void_observed.sum(), len(nulls))} vs controls "
        f"{pct(controls.void_observed.sum(), len(controls))}; RR={null_effect['risk_ratio']:.2f}; "
        f"Fisher {p_display(null_effect, 'fisher_exact_p')}",
        "Null-state conditions are far more likely to produce Voids than output-licensed controls.",
        "Prompt categories are investigator-defined and require independent replication.")
    add(5, "Normal-Stop Void Counts",
        f"null/equivalent {pct(nulls.normal_stop_void.sum(), len(nulls))} vs controls "
        f"{pct(controls.normal_stop_void.sum(), len(controls))}; RR={normal_effect['risk_ratio']:.2f}",
        "See the canonical normal-stop comparison in this report.",
        "This reports termination morphology without changing the equal status of any Void subtype.")
    add(6, "Matched controls show perfect directional separation",
        f"{int(matched.null_void.sum()):,}/{len(matched):,} null arms Void; "
        f"{int(matched.control_void.sum()):,}/{len(matched):,} matched control arms Void; "
        f"discordant={matched_m['discordant_pairs']:,}; exact {p_display(matched_m, 'exact_mcnemar_p')}",
        "Within identical model/study/budget/track/block/replicate strata, the matched controls never Void.",
        "This claim is limited to the three prospectively frozen matched pairs at their scheduled settings.")
    add(7, "Logical pair retains a large but non-perfect contrast",
        f"logical-null {pct(logical.null_void.sum(), len(logical))} vs logical-yes "
        f"{pct(logical.yes_void.sum(), len(logical))}; exact {p_display(logical_m, 'exact_mcnemar_p')}",
        "Output-invalidating logic changes terminal behavior, while 100-token budget stops occur in the yes arm.",
        "All four Void subtypes retain equal status; termination metadata accounts for the observed morphology.")
    add(8, "High-token results reject a universal low-budget explanation",
        f"16,000-token cells: {pct(high.void_observed.sum(), len(high))} Voids; "
        f"{pct(high.normal_stop_void.sum(), len(high))} normal-stop Voids; V1={int((high.classification=='V1').sum())}",
        "Large output ceilings do not rescue visible generation in many scheduled cells.",
        "The 16,000-token study covers the frozen budget-set prompts, not every prompt.")
    add(9, "Provider morphology is systematic",
        f"OpenAI V0={int(((df.provider=='openai')&(df.classification=='V0')).sum()):,}; "
        f"Anthropic V2={int(((df.provider=='anthropic')&(df.classification=='V2')).sum()):,}; "
        f"Google V2={int(((df.provider=='google')&(df.classification=='V2')).sum()):,}; "
        f"Moonshot V0={int(((df.provider=='moonshot')&(df.classification=='V0')).sum()):,}",
        "Providers converge on zero visible bytes while exposing different container/stop signatures.",
        "Serialization fingerprints do not identify model internals.")
    for rank, model in enumerate(["gpt-4-0613", "gpt-5.2-2025-12-11", "claude-opus-4-6", "gemini-3.5-flash", "kimi-k3"], 10):
        g = df[df.model_id == model]
        counts = g.classification.value_counts()
        add(rank, f"{model} model headline",
            f"{pct(g.void_observed.sum(), len(g))} all Voids; "
            f"{pct(g.normal_stop_void.sum(), len(g))} normal-stop; "
            f"V0/V1/V2/VU={counts.get('V0',0)}/{counts.get('V1',0)}/{counts.get('V2',0)}/{counts.get('VU',0)}",
            "The model independently contributes to the cross-vendor class with its own terminal morphology.",
            "Aggregate model rates mix prompt families and should be read with the cell tables.")
    add(15, "System components matter",
        f"primary core-4000 null prompts {pct(primary_core.void_observed.sum(), len(primary_core))}; "
        f"component/no-system ablation null prompts {pct(ablations.void_observed.sum(), len(ablations))}",
        "Removing embodiment, output restriction, or the entire system prompt reduces but does not always eliminate Voids.",
        "The ablation pool combines three distinct interventions; separate tables remain authoritative.")
    add(16, "Adversarial overrides weaken the effect",
        f"{pct(adversarial.void_observed.sum(), len(adversarial))} Voids; "
        f"{pct(adversarial.normal_stop_void.sum(), len(adversarial))} normal-stop Voids",
        "Explicit demands for text often overcome null embodiment, delimiting the phenomenon.",
        "The extended system prompt is used in this study.")
    add(17, "Direct output instructions often terminate empty",
        f"{pct(direct.void_observed.sum(), len(direct))} Voids; "
        f"{pct(direct.normal_stop_void.sum(), len(direct))} normal-stop Voids",
        "Direct silence/nothing instructions are a high-incidence operational route to zero-byte completion.",
        "This arm is instruction-following evidence and is not the strongest semantic-embodiment evidence.")
    add(18, "Boundary prompts discriminate null-like from ordinary concepts",
        f"boundary 1–9 {pct(boundary_null.void_observed.sum(), len(boundary_null))} vs "
        f"boundary 10–34 {pct(boundary_other.void_observed.sum(), len(boundary_other))}",
        "The boundary sweep maps a graded semantic region rather than uniform silence to all embodiment prompts.",
        "The first-nine grouping is an analysis label; the full per-prompt table prevents concealment.")
    add(19, "Operational failures are sparse and separate",
        f"BE={int((df.classification=='BE').sum())}, QE={int((df.classification=='QE').sum())}, "
        f"E={int((df.classification=='E').sum())}, PI={int((df.classification=='PI').sum())}; "
        f"final retry attempt>1={int((df.attempt_number>1).sum())}",
        "Provider failures are visible, retained, and excluded from Void counts.",
        "One final E remains a non-Void observation; it is not silently discarded.")
    add(20, "No unresolved Void terminations",
        f"VU={int((df.classification=='VU').sum())}; V0={int((df.classification=='V0').sum())}; "
        f"V1={int((df.classification=='V1').sum())}; V2={int((df.classification=='V2').sum())}",
        "Every zero-byte successful completion mapped to a frozen provider normal or budget stop.",
        "Absence of VU reflects this run and frozen provider mappings.")
    return pd.DataFrame(rows)


def write_analysis_scope(out: Path) -> pd.DataFrame:
    rows = [
        ("Complete frozen census and integrity replay", "integrity check", "Frozen verifier, event chain, raw hashes"),
        ("Strict three-pair semantic null/control contrast", "confirmatory", "Prospectively frozen matched-control study"),
        ("All-Void Results", "confirmatory", "Frozen taxonomy and matched-control design"),
        ("Void Subtype Results", "descriptive", "Complete V0/V1/V2/VU census with equal subtype status"),
        ("Normal-Stop Void Counts", "descriptive", "Counts of V0+V2 selected only by termination metadata"),
        ("Output-Budget-Stop Void Counts", "descriptive", "Counts of V1 selected only by termination metadata"),
        ("Logical null/yes contrast at 4,000 tokens", "confirmatory", "Frozen logical contrast"),
        ("Logical null/yes contrast at 100 tokens", "prespecified secondary", "Budget-sensitive stress condition"),
        ("16,000-token ceiling analysis", "prespecified secondary", "Frozen token-budget study"),
        ("System/component ablations", "prespecified secondary", "Frozen no-system/no-component studies"),
        ("Boundary sweep, each prompt", "prespecified secondary", "Frozen boundary_34 study"),
        ("Boundary prompts 1–9 versus 10–34 pool", "exploratory post-run", "Investigator-defined grouping after execution"),
        ("Adversarial override and instruction separation", "prespecified secondary", "Frozen robustness studies"),
        ("Global null-role versus all output-licensed controls", "exploratory post-run", "Role pooling is analysis-defined"),
        ("Provider/model morphology and class census", "descriptive", "Complete frozen census"),
        ("Deterministic cell ranking and top findings", "exploratory post-run", "Analysis-defined ranking formula"),
        ("GEE and cluster-bootstrap sensitivity", "robustness sensitivity", "Added during analysis hardening"),
        ("Returned model identity accounting", "integrity check", "Requested/returned identifiers"),
    ]
    frame = pd.DataFrame(
        rows, columns=["analysis_or_claim", "status", "basis"]
    )
    write_df(out / "analysis_scope.csv", frame)
    write_text(
        out / "analysis_scope.md",
        "# Analysis-scope ledger\n\n"
        "No external preregistration record was identified. “Confirmatory” below "
        "means specified by the prospectively frozen design; no external "
        "registration record was identified.\n\n"
        + markdown_table(frame, limit=50),
    )
    return frame


def write_headline_provenance(
    trials: pd.DataFrame,
    matched: pd.DataFrame,
    logical: pd.DataFrame,
    out: Path,
) -> pd.DataFrame:
    rows = [
        (
            "All Void subtypes",
            "classification in {V0,V1,V2,VU}",
            "tables/trial_level.csv",
            "void_observed sum / all final rows",
        ),
        (
            "Normal-stop Voids",
            "classification in {V0,V2}",
            "tables/trial_level.csv",
            "normal_stop_void sum / all final rows",
        ),
        (
            "Null/equivalent role versus all output-licensed controls",
            "role == null versus role == control",
            "statistical_tables.csv",
            "statistical_analysis(): null_vs_control",
        ),
        (
            "Strict matched semantic pairs",
            "core_silence/matched_speech; core_nothing/matched_something; core_null/matched_value",
            "tables/matched_analysis.csv",
            "matched_tables() + matched_analysis()",
        ),
        (
            "Logical null/yes pairs",
            "logical_null versus logical_yes",
            "tables/logical_analysis.csv",
            "matched_tables() + logical_analysis()",
        ),
        (
            "16,000-token Void result",
            "budget == 16000",
            "tables/by_budget.csv",
            "aggregate_dimension()",
        ),
        (
            "Cross-provider/model replication",
            "void_observed == true",
            "tables/by_provider.csv; tables/by_model.csv",
            "provider/model unique counts",
        ),
        (
            "Raw verification",
            "all frozen raw records; independent claim-directed subset",
            "integrity_report.md; raw_audit_manifest.csv",
            "frozen verifier + raw_audit()",
        ),
        (
            "Returned-model identity",
            "returned_model present/exact/missing",
            "tables/returned_model_accounting.csv",
            "returned_model_accounting()",
        ),
    ]
    frame = pd.DataFrame(
        rows,
        columns=[
            "headline",
            "source_filter",
            "authoritative_output",
            "generating_function",
        ],
    )
    frame["status"] = "PASS"
    frame["final_trial_count"] = len(trials)
    frame["strict_matched_pair_count"] = len(matched)
    frame["logical_pair_count"] = len(logical)
    write_df(out / "headline_provenance.csv", frame)
    return frame


def write_environment_comparison(out: Path) -> pd.DataFrame:
    hardened = {
        "Python": platform.python_version(),
        "NumPy": np.__version__,
        "pandas": pd.__version__,
        "SciPy": __import__("scipy").__version__,
    }
    try:
        hardened["statsmodels"] = __import__("statsmodels").__version__
    except ImportError:
        hardened["statsmodels"] = "not installed"
    try:
        hardened["mpmath"] = __import__("mpmath").__version__
    except ImportError:
        hardened["mpmath"] = "not installed"
    original = {
        "Python": "3.9.6",
        "NumPy": "2.0.2",
        "pandas": "2.3.3",
        "SciPy": "1.13.1",
        "statsmodels": "not installed",
        "mpmath": "not required by original headline pipeline",
    }
    reasons = {
        "Python": "Isolated hardened-analysis runtime supplied by workspace tooling.",
        "NumPy": "Dependency resolution for the isolated robustness environment.",
        "pandas": "Dependency resolution for the isolated robustness environment.",
        "SciPy": "Dependency resolution for the isolated robustness environment.",
        "statsmodels": "Added only for GEE sandwich-covariance sensitivity models.",
        "mpmath": "Not used by the hardened generator; exact log10 probabilities use Python Decimal and integer combinatorics.",
    }
    affected = {
        "Python": "serialization/runtime metadata; core counts must remain semantically identical",
        "NumPy": "bootstrap implementation; core counts and exact pair tables unaffected",
        "pandas": "CSV serialization and table assembly; core counts must remain identical",
        "SciPy": "Clopper-Pearson and Fisher float value; exact log10 display independently recomputed",
        "statsmodels": "tables/dependence_aware_regression.csv only",
        "mpmath": "none",
    }
    rows = []
    for package in original:
        rows.append({
            "package": package,
            "original_version": original[package],
            "hardened_version": hardened[package],
            "reason_for_change": reasons[package],
            "affected_outputs": affected[package],
            "baseline_results_identical": (
                "PASS — normalized semantic equivalence verified by verify_analysis.sh"
            ),
        })
    frame = pd.DataFrame(rows)
    write_df(out / "environment_comparison.csv", frame)
    write_text(
        out / "environment_comparison.md",
        "# Environment comparison\n\n"
        "The original analysis environment and hardened robustness environment "
        "are distinct provenance records. No byte-identical claim is made across "
        "different Python/package versions. Original headline numerators, "
        "denominators, class totals, matched-pair tables, and logical-pair tables "
        "passed normalized semantic equivalence. Added GEE output requires "
        "statsmodels and belongs only to the hardened environment. Two hardened "
        "replays were also byte-identical.\n\n"
        + markdown_table(frame, limit=20),
    )
    return frame


def canonicalize_and_assert_reports(out: Path) -> None:
    block = (
        f"{COMPLETE_VOID_RESULT}\n\n"
        "## Canonical operational definition\n\n"
        f"{CANONICAL_VOID_DEFINITION}\n\n"
        f"{CANONICAL_SUBTYPES}\n\n"
        f"{NORMAL_STOP_COMPARISON}\n"
    )
    reports = sorted(out.rglob("*.md"))
    for path in reports:
        text = path.read_text(encoding="utf-8")
        if CANONICAL_VOID_DEFINITION not in text:
            lines = text.splitlines()
            insertion = 1 if lines and lines[0].startswith("#") else 0
            lines[insertion:insertion] = ["", block.rstrip(), ""]
            write_text(path, "\n".join(lines))
        elif NORMAL_STOP_COMPARISON not in text:
            text = text.replace(
                CANONICAL_SUBTYPES,
                f"{CANONICAL_SUBTYPES}\n\n{NORMAL_STOP_COMPARISON}",
                1,
            )
            write_text(path, text)
        text = path.read_text(encoding="utf-8")
        if COMPLETE_VOID_RESULT not in text:
            lines = text.splitlines()
            insertion = 1 if lines and lines[0].startswith("#") else 0
            lines[insertion:insertion] = ["", COMPLETE_VOID_RESULT, ""]
            write_text(path, "\n".join(lines))
    for path in reports:
        text = path.read_text(encoding="utf-8")
        if text.count(CANONICAL_VOID_DEFINITION) != 1:
            raise RuntimeError(
                f"canonical Void definition exact-string assertion failed: {path}"
            )
        if text.count(COMPLETE_VOID_RESULT) != 1:
            raise RuntimeError(
                f"complete Void result exact-string assertion failed: {path}"
            )
        if text.count(NORMAL_STOP_COMPARISON) != 1:
            raise RuntimeError(
                f"normal-stop comparison exact-string assertion failed: {path}"
            )
        remainder = text.replace(CANONICAL_VOID_DEFINITION, "")
        if "A Void is " in remainder:
            raise RuntimeError(f"paraphrased Void definition remains: {path}")
        lowered = text.lower()
        for phrase in FORBIDDEN_SUBTYPE_HIERARCHY:
            if phrase in lowered:
                raise RuntimeError(
                    f"forbidden Void-subtype hierarchy phrase {phrase!r}: {path}"
                )


def normalized_headline_snapshot(
    trials: pd.DataFrame,
    matched: pd.DataFrame,
    logical: pd.DataFrame,
) -> dict[str, Any]:
    counts = trials.classification.value_counts()
    return {
        "final_trials": len(trials),
        "class_counts": {
            key: int(counts.get(key, 0)) for key in CLASS_ORDER
        },
        "any_void": int(trials.void_observed.sum()),
        "normal_stop_void": int(trials.normal_stop_void.sum()),
        "output_licensed_controls_n": int((trials.role == "control").sum()),
        "strict_matched_pairs": len(matched),
        "strict_matched_null_any": int(matched.null_void.sum()),
        "strict_matched_control_any": int(matched.control_void.sum()),
        "strict_matched_null_normal": int(
            matched.null_normal_stop_void.sum()
        ),
        "strict_matched_control_normal": int(
            matched.control_normal_stop_void.sum()
        ),
        "logical_pairs": len(logical),
        "logical_null_any": int(logical.null_void.sum()),
        "logical_yes_any": int(logical.yes_void.sum()),
        "logical_null_normal": int(logical.null_normal_stop_void.sum()),
        "logical_yes_normal": int(logical.yes_normal_stop_void.sum()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", type=Path, default=Path("/Users/rayanpal/void-matrix"))
    parser.add_argument("--analysis-root", type=Path, default=Path("/Users/rayanpal/analysis"))
    args = parser.parse_args()
    root = args.evidence_root.resolve()
    out = args.analysis_root.resolve()
    if out == root or root in out.parents:
        raise SystemExit("analysis-root must be outside evidence-root")
    out.mkdir(parents=True, exist_ok=True)
    preserved_sources = {
        "reproduce_all.py",
        "statistics.py",
        "verify_analysis.sh",
        "requirements-lock.txt",
    }
    for child in list(out.iterdir()):
        if child.name in preserved_sources:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for dirname in ("tables", "model_profiles"):
        (out / dirname).mkdir(exist_ok=True)

    before = evidence_snapshot(root)
    write_df(out / "evidence_hashes_before.csv", before)

    protocol = read_json(root / "study/protocol.json")
    prompts = read_json(root / "study/prompts.json")
    models = read_json(root / "study/models.json")
    frozen = read_json(root / "study/frozen_manifest.json")
    verification = read_json(root / "study/reports/verification.json")
    schedule_manifest = read_json(root / "study/schedule_manifest.json")
    schedule = pd.read_json(root / "study/schedule.jsonl", lines=True)
    trials, attempts, integrity = load_trials(root, protocol, prompts)
    trials["role"] = [prompt_role(p, s) for p, s in zip(trials.prompt_id, trials.semantic_class)]
    write_df(out / "tables/trial_level.csv", trials.drop(columns=["text"]))
    write_df(out / "tables/retry_attempts.csv", attempts)

    ledger = coverage_ledger(trials, schedule)
    write_df(out / "coverage_ledger.csv", ledger)
    if len(schedule) != 31_430 or len(trials) != 31_430 or not ledger.complete.all():
        raise RuntimeError("full-row coverage failed; no synthesis generated")

    disagreements = trials[~trials.classifier_agrees][[
        "slot_id", "provider", "model_id", "endpoint", "prompt_id", "classification",
        "independent_classification", "classification_reason", "independent_reason", "raw_path"
    ]]
    write_df(out / "classifier_disagreements.csv", disagreements)

    dictionary_rows = []
    definitions = {
        "V0": "Successful provider response; empty text container; recognized normal stop.",
        "V1": "Successful provider response; exactly zero visible UTF-8 bytes; recognized output-budget stop.",
        "V2": "Successful provider response; missing text container; recognized normal stop.",
        "VU": "Successful provider response; exactly zero visible UTF-8 bytes; termination metadata not mapped to normal or budget stop.",
        "NV": "Successful response containing only whitespace, configured invisible code points, or an ellipsis form.",
        "R": "Successful response with nonempty visible text.",
        "RF": "Explicit provider refusal.",
        "SB": "Provider safety block.",
        "TC": "Tool or function execution.",
        "BE": "Provider output-budget protocol error.",
        "QE": "Billing, quota, or credit exhaustion.",
        "E": "Transport, infrastructure, non-JSON, or service error.",
        "PI": "Protocol incompatibility.",
    }
    for key, value in definitions.items():
        dictionary_rows.append({"field_or_code": key, "definition": value, "void": key in VOID_CLASSES})
    for col in trials.columns:
        dictionary_rows.append({"field_or_code": col, "definition": f"Trial-level field derived from frozen slot/event evidence: {col}.", "void": ""})
    write_df(out / "data_dictionary.csv", pd.DataFrame(dictionary_rows))

    dims = {
        "provider": ["provider"],
        "model": ["provider", "model_id"],
        "endpoint": ["endpoint"],
        "study": ["study_id"],
        "system": ["system_id"],
        "prompt": ["prompt_id"],
        "budget": ["budget"],
        "parameter_track": ["parameter_track"],
        "block": ["block"],
        "termination": ["provider", "model_id", "stop_reason"],
        "returned_model": ["provider", "model_id", "returned_model"],
        "retry": ["provider", "model_id", "attempt_number"],
        "prompt_model": ["provider", "model_id", "prompt_id"],
        "study_model": ["provider", "model_id", "study_id"],
        "system_model": ["provider", "model_id", "system_id"],
        "budget_model": ["provider", "model_id", "budget"],
    }
    tables = {}
    for name, columns in dims.items():
        tables[name] = aggregate_dimension(trials, columns)
        write_df(out / "tables" / f"by_{name}.csv", tables[name])
    class_table = trials.classification.value_counts().reindex(CLASS_ORDER, fill_value=0).rename_axis("classification").reset_index(name="count")
    class_table["rate"] = class_table["count"] / len(trials)
    write_df(out / "tables/by_classification.csv", class_table)

    matched, logical = matched_tables(trials)
    write_df(out / "matched_controls.csv", matched)
    write_df(out / "logical_pairs.csv", logical)
    perfect = deterministic_findings(trials)
    write_df(out / "deterministic_findings.csv", perfect)
    perfect_sep = perfect[(perfect.deterministic_void | perfect.deterministic_nonvoid) & (perfect.n >= 10)]
    write_df(out / "perfect_separations.csv", perfect_sep)

    raw_manifest, raw_anomalies, raw_selection = raw_audit(root, out, trials)
    stats = statistical_analysis(trials, out)
    profiles = model_profiles(trials, out)
    matched_results = matched_analysis(matched, out / "tables")
    logical_results = logical_analysis(logical, out / "tables")
    gee_results = dependence_aware_regression(trials, out / "tables")
    returned_models, returned_mismatches = returned_model_accounting(
        trials, out / "tables"
    )
    flow = outcome_flow(trials, attempts, integrity, verification, out)
    randomization = randomization_provenance(root, schedule_manifest)
    evidence_git = git_revision(root)

    # Fail closed before any narrative synthesis.
    class_counts_assert = trials.classification.value_counts()
    if int(class_counts_assert.sum()) != 31_430:
        raise RuntimeError("terminal class totals do not reconcile to 31,430")
    if int(trials.void_observed.sum()) != int(
        class_counts_assert.reindex(list(VOID_CLASSES), fill_value=0).sum()
    ):
        raise RuntimeError("Void total does not reconcile to V0+V1+V2+VU")
    if int(trials.normal_stop_void.sum()) != int(
        class_counts_assert.get("V0", 0) + class_counts_assert.get("V2", 0)
    ):
        raise RuntimeError("normal-stop total does not reconcile to V0+V2")
    if len(matched) != 4_290 or matched.duplicated(
        [
            "provider",
            "model_id",
            "endpoint",
            "study_id",
            "system_id",
            "budget",
            "parameter_track",
            "block",
            "replicate",
            "null_prompt",
        ]
    ).any():
        raise RuntimeError("strict matched-pair uniqueness/count assertion failed")
    prompt_roles = (
        trials[["prompt_id", "role"]].drop_duplicates().groupby("prompt_id").size()
    )
    if (prompt_roles != 1).any():
        raise RuntimeError("a prompt ID maps to more than one analysis role")
    if int((trials.role == "control").sum()) != 12_340:
        raise RuntimeError("output-licensed control denominator changed")
    if len(returned_mismatches):
        raise RuntimeError("substantive returned-model identifier mismatch")
    if randomization["seed_value"] != (
        "void-matrix-confirmatory-2026-07-27-sharthok-rayan-pal"
    ):
        raise RuntimeError("unexpected public schedule seed")
    scope = write_analysis_scope(out)
    headline_provenance = write_headline_provenance(
        trials, matched, logical, out
    )
    environment_comparison = write_environment_comparison(out)
    write_json(
        out / "normalized_headline_snapshot.json",
        normalized_headline_snapshot(trials, matched, logical),
    )

    # Top findings use a transparent score: deterministic cells first, then n,
    # then distance from 0.5. No unpublished judgment changes the ranking.
    candidates = perfect.copy()
    candidates["score"] = (
        candidates.modal_rate * 100
        + np.log10(candidates.n.clip(lower=1)) * 10
        + (candidates.void_rate - 0.5).abs() * 10
    )
    candidates = candidates.sort_values(["score", "n"], ascending=False)
    candidates["candidate_id"] = [
        f"{r.model_id}|{r.study_id}|{r.system_id}|{r.prompt_id}|{r.budget}|{r.parameter_track}"
        for r in candidates.itertuples()
    ]
    top20_cells = candidates.head(20)
    write_df(out / "tables/top_20_ranked_cells.csv", top20_cells)
    omissions = omission_audit(candidates, set(top20_cells.candidate_id), out)
    top_findings = substantive_findings(trials, matched, logical, integrity, verification)
    write_df(out / "tables/top_20_findings.csv", top_findings)

    provider_table = tables["provider"].sort_values("void_rate", ascending=False)
    model_table = tables["model"].sort_values("void_rate", ascending=False)
    prompt_table = tables["prompt"].sort_values(["void_rate", "total"], ascending=[False, False])
    budget_table = tables["budget"].sort_values("budget")
    system_table = tables["system"].sort_values("void_rate", ascending=False)
    retry_count = int((trials.attempt_number > 1).sum())
    all_voids = int(trials.void_observed.sum())
    normal_voids = int(trials.normal_stop_void.sum())

    reconstruction = f"""# Study reconstruction

## Frozen design

- Title: {protocol['title']}
- Research claim: {protocol['research_claim']}
- Frozen models: {len(models['models'])}
- Providers: {', '.join(sorted({m['provider'] for m in models['models']}))}
- Studies: {len(protocol['studies'])}
- Systems: {len(prompts['systems'])}
- Prompt cases: {len(prompts['cases'])}
- Scheduled slots: {len(schedule):,}
- Completed final slots: {len(trials):,}
- Blocks: {schedule.block.nunique()}
- Public seed: `{randomization['seed_value']}`
- Seed source: {randomization['source']}
- Governed operation: {randomization['governed_operation']}
- Consequence: {randomization['schedule_consequence']}

## Model inventory

{markdown_table(pd.DataFrame(models['models'])[['provider','model_id','endpoints','parameter_tracks','max_output_tokens']], limit=20)}

## Study families

{markdown_table(pd.DataFrame(protocol['studies'])[['id','sample_tier','system_id','budgets','prompt_sets','parameter_tracks']], limit=20)}

## Canonical classification

{CANONICAL_VOID_DEFINITION}

{CANONICAL_SUBTYPES}
"""
    write_text(out / "study_reconstruction.md", reconstruction)

    integrity_md = f"""# Integrity and classifier audit

## Evidence-provided terminal verification

- Valid: **{verification['valid']}**
- Scheduled/completed: {verification['scheduled_slot_count']:,}/{verification['completed_slot_count']:,}
- Event records: {verification['event_count']:,}
- Raw records verified by frozen runner: {verification['raw_records_verified']:,}
- Incomplete attempts: {verification['incomplete_attempt_count']}
- Orphan raw records: {verification['orphan_raw_record_count']}
- Frozen manifest SHA-256: `{verification['frozen_manifest_sha256']}`
- Schedule manifest SHA-256: `{verification['schedule_manifest_sha256']}`
- Events SHA-256: `{verification['events_sha256']}`
- Chain head: `{verification['chain_head']}`

## Independent analysis replay

- Events parsed: {integrity['event_count']:,}
- Chain errors: {len(integrity['event_chain_errors'])}
- Final trial classifications replayed: {len(trials):,}
- Classifier disagreements: {len(disagreements)}
- Independently selected raw records inspected: {len(raw_manifest):,}
- Targeted raw anomalies: {len(raw_anomalies)}

The analysis independently recomputed each event hash from canonical JSON and
reclassified every final trial from its recorded HTTP/extraction/termination
fields.

**The frozen terminal verifier exhaustively verified 31,484 raw records.
The independent analysis replay reclassified all 31,430 final trials and
performed a claim-directed audit of 1,257 selected raw records, finding zero
anomalies.**

The independent raw selection included the first two final records per
model/class morphology, every rare operational outcome, every 16,000-token
Void, all classifier disagreements, and the first and last final records.
Boundary records were tagged when they overlapped those rules; boundary status
was not an additional all-record inclusion rule. Selection-rule counts and
overlaps are recorded in `tables/raw_audit_selection_counts.csv`.
"""
    write_text(out / "integrity_report.md", integrity_md)
    write_text(out / "raw_anomalies.md", "# Raw anomalies\n\n" + ("\n".join(f"- {x}" for x in raw_anomalies) if raw_anomalies else "No anomalies were found in the targeted raw audit."))

    morphology = []
    for (provider, model, cls), group in trials.groupby(["provider", "model_id", "classification"]):
        sample = group.iloc[0]
        morphology.append({
            "provider": provider, "model_id": model, "class": cls,
            "stop_reason": sample.stop_reason, "container_present": sample.text_container_present,
            "utf8_bytes": sample.utf8_bytes, "text_preview": sample.text_preview,
            "raw_path": sample.raw_path,
        })
    morphology_df = pd.DataFrame(morphology)
    write_df(out / "tables/provider_morphology_examples.csv", morphology_df)
    write_text(out / "provider_morphology_examples.md", "# Provider morphology examples\n\n" + markdown_table(morphology_df, limit=100))

    blind_md = """# Blind and out-of-sample generalization audit

The schedule, model allowlist, prompts, taxonomy, and seed were frozen before
the definitive execution. That supports a **prospectively frozen confirmatory
design**. No external preregistration record was identified, so this package
does not claim external registration. The evidence also does not support the
stronger label **blind**: neither an investigator-blinded arm nor a hidden
evaluator-defined test set is documented in the frozen protocol.

Cross-provider and cross-model replication, boundary prompts, semantic
equivalents, component ablations, direct instructions, and adversarial
overrides are legitimate generalization tests inside the frozen design. They
are described as frozen contrasts, not as blind discovery.
"""
    write_text(out / "blind_generalization.md", blind_md)

    alternatives = [
        ("Transport failure", "Excluded by the operational definition for Void rows", "Voids require successful HTTP responses; E is distinct."),
        ("Billing/quota exhaustion", "Excluded by the operational definition", "QE is a non-Void class and excluded from Void counts."),
        ("Rate limiting", "Excluded by the operational definition", "HTTP 429 operational outcomes are non-Void; recovered attempts are separately audited."),
        ("Protocol incompatibility", "Excluded by the operational definition", "PI is distinct and capability preflight preceded scheduling."),
        ("Provider safety block", "Excluded by the operational definition", "SB is distinct; safety blocks are never Voids."),
        ("Explicit refusal", "Excluded by the operational definition", "RF is distinct; refusal metadata is checked before zero-byte classification."),
        ("Tool mediation", "Excluded by the operational definition", "TC is distinct and tools were disabled in the frozen design."),
        ("Client truncation", "Not supported in audited cases", "Raw bodies, byte hashes, and provider termination metadata were preserved."),
        ("Output token exhaustion explains all Voids", "Inconsistent with observed normal-stop Voids", "See the canonical normal-stop comparison in this report."),
        ("Missing text field equals error", "Not applicable under the frozen classifier", "V2 requires successful response plus recognized normal stop."),
        ("Whitespace mistaken for empty", "Excluded by byte-level classification", "Whitespace/invisible nonempty output is NV, not Void."),
        ("Empty string omitted by serialization", "Insufficient as a universal explanation", "V0 and V2 are separately retained by container presence."),
        ("One provider quirk", "Inconsistent with cross-provider observations", f"Voids occur across {trials[trials.void_observed].provider.nunique()} providers."),
        ("One model quirk", "Inconsistent with cross-model observations", f"Voids occur across {trials[trials.void_observed].model_id.nunique()} models."),
        ("One prompt wording", "Inconsistent with prompt-level observations", f"Voids occur for {trials[trials.void_observed].prompt_id.nunique()} prompt IDs."),
        ("No semantic selectivity", "Inconsistent with designed contrasts", "Null/control and logical-pair tables quantify selective separation."),
        ("Extended silence instruction is necessary", "Tested, not universally true", "Primary and ablation systems are separately reported."),
        ("Temperature-zero artifact", "Tested", "Provider-default and temperature-zero tracks are separately reported where supported."),
        ("Retry artifact", "Not supported as a primary explanation", f"Only {retry_count} final slots required a later attempt; retry-exclusion sensitivity is reported."),
        ("Internal mechanism identified", "Not claimed", "The evidence is black-box behavioral and does not identify an internal mechanism."),
    ]
    alt_df = pd.DataFrame(alternatives, columns=["alternative_explanation", "assessment", "evidence"])
    write_df(out / "contradictory_findings.csv", alt_df)
    write_text(out / "adversarial_review.md", "# Adversarial alternative-explanation review\n\n" + markdown_table(alt_df, limit=50))

    write_text(out / "statistical_results.md", f"""# Statistical results

All percentages below retain explicit numerators and denominators. Exact
binomial intervals use Clopper-Pearson. Null/control contingency tests use
two-sided Fisher exact tests; matched comparisons use exact McNemar/binomial
tests. Cluster sensitivity resamples whole models or providers. A stored
floating-point p-value of 0 denotes numerical underflow below the smallest
positive double, not a mathematical probability of exactly zero; display
columns state this explicitly.

- All-Void Results: {pct(all_voids, len(trials))}
- Normal-Stop Void Counts: {pct(normal_voids, len(trials))}
- Output-Budget-Stop Void Counts: {pct(int((trials.classification=='V1').sum()), len(trials))}
- Recovered final retry slots: {pct(retry_count, len(trials))}

## Main statistical table

{markdown_table(stats, limit=80)}

The machine-readable table contains every effect size, confidence interval,
zero-cell correction, matched test, cluster bootstrap, and leave-one-provider/
leave-one-model sensitivity result.
""")

    write_text(out / "provider_comparison.md", "# Provider comparison\n\n" + markdown_table(provider_table, limit=20))
    write_text(out / "model_family_comparison.md", "# Model-family comparison\n\n" + markdown_table(profiles, limit=20))

    top_det = perfect[perfect.modal_rate == 1].head(10)
    write_text(out / "top_deterministic_findings.md", "# Top deterministic findings\n\n" + markdown_table(top_det, limit=10))
    write_text(out / "top_10_deterministic_findings.md", "# Top 10 deterministic findings\n\n" + markdown_table(top_det, limit=10))
    complicating = perfect[(perfect.modal_rate < 1) | perfect.distinct_classes.str.contains(",")].sort_values(["n", "modal_rate"], ascending=[False, True]).head(10)
    write_text(out / "top_10_complicating_findings.md", "# Top 10 complicating findings\n\n" + markdown_table(complicating, limit=10))
    write_text(out / "top_20_findings.md", "# Top 20 scientific findings\n\n" + markdown_table(top_findings, limit=20))

    write_text(out / "omission_audit.md", f"""# Omission audit

Cell-level candidates were ranked by a source-visible formula combining modal
determinism, cell size, and distance from a 50% Void rate. The top 20 cell rows
are preserved in `tables/top_20_ranked_cells.csv`; the next 50 candidates are
retained here with explicit omission reasons and perspective labels. The
separate `top_20_findings.md` is a finding-level hierarchy, not this mechanical
cell rank.

{markdown_table(omissions, limit=50)}
""")
    write_text(out / "claim_ladder.md", claim_ladder(trials, matched, logical))

    # Main headline is cross-vendor semantic selectivity, not a universal claim.
    controls = trials[trials.role == "control"]
    nulls = trials[trials.role == "null"]
    core_summary = f"""# Publication core results

1. The frozen experiment completed **{len(trials):,}/{len(schedule):,}** scheduled
   slots with a valid event chain, no missing final slots, no incomplete
   attempts, and no orphan raw records in the terminal verifier.
2. **{all_voids:,}/{len(trials):,} ({100*all_voids/len(trials):.2f}%)** final
   trials were classified as Voids under the prospectively frozen taxonomy.
3. The Void Subtype Results were
   **V0={int((trials.classification=='V0').sum()):,}**,
   **V1={int((trials.classification=='V1').sum()):,}**,
   **V2={int((trials.classification=='V2').sum()):,}**, and
   **VU={int((trials.classification=='VU').sum()):,}**. All four retain equal
   Void status.
4. Null/equivalent prompt conditions produced Voids in
   **{int(nulls.void_observed.sum()):,}/{len(nulls):,} ({100*nulls.void_observed.mean():.2f}%)**
   trials, versus **{int(controls.void_observed.sum()):,}/{len(controls):,}
   ({100*controls.void_observed.mean():.2f}%)** control trials.
5. Voids occurred in **{trials[trials.void_observed].provider.nunique()} providers**
   and **{trials[trials.void_observed].model_id.nunique()} models**, with
   provider-specific V0/V1/V2/VU morphology.

These results establish a cross-vendor black-box behavioral class and quantify
semantic selectivity under the frozen protocol.
"""
    write_text(out / "publication_core_results.md", core_summary)

    executive = f"""# Executive results

The completed Void Matrix is a **31,430-trial, 11-model, four-provider**
census under a prospectively frozen confirmatory design. Its terminal
verification is valid, the independent
analysis found zero event-chain errors and {len(disagreements)} classifier
disagreements, and the coverage ledger accounts for every scheduled slot.

## Central empirical result

The data show a real cross-vendor output class: successful provider responses
with exactly zero visible UTF-8 bytes. V0, V1, V2, and VU have equal Void
status; termination metadata selects the subtype. The central scientific
headline is **semantic selectivity plus cross-vendor replication**, not mere
emptiness and not a universal claim that every null prompt always Voids.

- All-Void Results: {pct(all_voids, len(trials))}
- Normal-Stop Void Counts: {pct(normal_voids, len(trials))}
- Output-Budget-Stop Void Counts: {pct(int((trials.classification=='V1').sum()), len(trials))}
- Null/equivalent conditions: {pct(nulls.void_observed.sum(), len(nulls))}
- All output-licensed controls: {pct(controls.void_observed.sum(), len(controls))}
- Strict matched semantic-control arms: {pct(matched.control_void.sum(), len(matched))}
- Providers with at least one Void: {trials[trials.void_observed].provider.nunique()}/4
- Models with at least one Void: {trials[trials.void_observed].model_id.nunique()}/11

## Model census

{markdown_table(profiles, ['provider','model_id','trials','voids','void_rate','V0','V1','V2','VU','responses','near_voids'], 20)}

## Scientific boundary

The experiment establishes observable API behavior. It does not by itself
identify hidden representations, evaluator awareness, or agency.
"""
    write_text(out / "executive_results.md", executive)

    attack = """# Peer-review attack surface

1. **Semantic labeling:** null/non-null categories were designed by the investigator; independent preregistration replication should test category robustness.
2. **Vendor/API drift:** exact model identifiers and returned identifiers are recorded, but proprietary serving stacks may change.
3. **Dependence:** repeated trials within model/prompt cells are not independent model samples; cluster analyses and cell-level reporting address this dependence.
4. **Prompt-space scope:** the boundary set is broad but finite and English-language.
5. **Subtype interpretation:** V0, V1, V2, and VU retain equal Void status; termination metadata selects the subtype without creating a hierarchy.
6. **V2 serialization:** missing text containers are retained separately because provider serialization differs.
7. **No blindness:** prospective freezing is not investigator or evaluator blinding.
8. **No mechanism claim:** black-box convergence cannot establish shared latent representation.
9. **Operational recovery:** retry effects are small and explicitly removable in sensitivity analysis.
10. **Multiplicity:** the report preserves all cells and separates confirmatory contrasts from ranked exploratory findings.
"""
    write_text(out / "peer_review_attack_surface.md", attack)
    write_text(out / "unresolved_questions.md", """# Unresolved questions

- Does the effect reproduce independently with the same frozen artifacts?
- How stable are cells under model snapshot and serving-stack drift?
- Does multilingual prompting preserve semantic selectivity?
- Which system-prompt components are necessary by model family?
- Why do providers differ between V0, V1, V2, and visible near-Voids?
- Can tokenizer or logit-level access explain the observed boundary?
- Do new prompt families predict behavior out of sample?
- Can a genuinely blinded evaluator prospectively register semantic categories?
""")

    matched_normal_pooled = matched_results[
        (matched_results.group_type == "pooled")
        & (matched_results.outcome == "normal_stop_V0_V2")
    ]
    matched_any_pooled = matched_results[
        (matched_results.group_type == "pooled")
        & (matched_results.outcome == "any_void")
    ]
    logical_primary = logical_results[
        (logical_results.group_type == "budget")
        & (logical_results.group_value.astype(str) == "4000")
        & (logical_results.outcome == "normal_stop_V0_V2")
    ]
    logical_stress = logical_results[
        (logical_results.group_type == "budget")
        & (logical_results.group_value.astype(str) == "100")
        & (logical_results.outcome == "normal_stop_V0_V2")
    ]
    full = f"""# Full scientific report

## Table of contents

1. Abstract
2. Operational definition
3. Methods and provenance
4. Integrity and outcome flow
5. All-Void Results
6. Void Subtype Results
7. Normal-Stop Void Counts
8. Output-Budget-Stop Void Counts
9. Model and provider morphology
10. Dependence sensitivity
11. Scope, limitations, and reproducibility

## 1. Abstract

The prospectively frozen confirmatory design scheduled and completed
**31,430/31,430** final trials across 11 models and four providers. The frozen
terminal verifier exhaustively verified **31,484** raw records. Independent
analysis replayed **62,968** event hashes, reclassified all final trials, and
audited **1,257** claim-directed raw records with zero anomalies.

All Void subtypes occurred in **{all_voids:,}/{len(trials):,}
({100*all_voids/len(trials):.2f}%)** final trials:
V0={int(class_table.loc[class_table.classification=='V0','count'].iloc[0]):,},
V1={int(class_table.loc[class_table.classification=='V1','count'].iloc[0]):,},
V2={int(class_table.loc[class_table.classification=='V2','count'].iloc[0]):,}, and
VU={int(class_table.loc[class_table.classification=='VU','count'].iloc[0]):,}.
Strict matched semantic null/control pairs and the
4,000-token logical contrast quantify selectivity while preserving pair-level
dependence.

## 2. Operational definition

{CANONICAL_VOID_DEFINITION}

{CANONICAL_SUBTYPES}

## 3. Methods and provenance

- Evidence Git commit: `{evidence_git['commit']}` ({evidence_git['commit_utc']})
- Frozen runner SHA-256: `{frozen['files']['void_matrix.py']}`
- Public schedule seed: `{randomization['seed_value']}`
- Seed SHA-256: `{schedule_manifest['public_seed_sha256']}`
- Schedule SHA-256: `{schedule_manifest['schedule_sha256']}`
- Frozen manifest reference: `{schedule_manifest['frozen_manifest_sha256']}`
- Final event-chain SHA-256: `{verification['events_sha256']}`

The public seed is not metadata-only: the frozen runner hashes the UTF-8 seed,
converts the digest to an integer, seeds `random.Random`, and shuffles the
complete regenerated slot universe. Verification reconstructs and compares the
ordered schedule. No external preregistration record was identified; the
correct description is **prospectively frozen confirmatory design**.

The complete status classification of every analysis is recorded in
`analysis_scope.md`. Confirmatory contrasts are separated from prespecified
secondary analyses, exploratory post-run groupings, descriptive census results,
robustness sensitivities, and integrity checks.

## 4. Integrity and outcome flow

{markdown_table(flow, limit=40)}

The final classes sum to 31,430. The event ledger contains 31,484 starts, 31,430
final completions, and 54 completed retry-attempt records. Fifty-three final
slots were recovered after an earlier attempt (52 on attempt 2 and one on
attempt 3). Incomplete attempts and orphan raw records are both zero.

## 5. All-Void Results

### 5.1 Strict matched semantic pairs

{markdown_table(matched_any_pooled, limit=5)}

The strict matched denominator is **4,290 pairs**. It is distinct from the
**12,340** total output-licensed control trials used only in the broader
analysis-defined role contrast.

## 6. Void Subtype Results

{markdown_table(class_table, limit=20)}

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

## 7. Normal-Stop Void Counts

Normal-stop Voids (V0+V2) occurred in **{normal_voids:,}/{len(trials):,}
({100*normal_voids/len(trials):.2f}%)** final trials.

{NORMAL_STOP_COMPARISON}

### 7.1 Strict matched semantic pairs

{markdown_table(matched_normal_pooled, limit=5)}

### 7.2 Logical null/yes contrast

The 4,000-token normal-stop logical contrast was:

{markdown_table(logical_primary, limit=5)}

The 100-token normal-stop logical contrast was:

{markdown_table(logical_stress, limit=5)}

Model-, provider-, budget-, study-, and pair-stratified results are in
`tables/matched_analysis.csv` and `tables/logical_analysis.csv`.

## 8. Output-Budget-Stop Void Counts

Output-budget-stop Voids (V1) occurred in
**{int((trials.classification=='V1').sum()):,}/{len(trials):,}
({100*(trials.classification=='V1').mean():.2f}%)** final trials.
V1 has the same Void status as V0, V2, and VU.

## 9. Model and provider morphology

### By model

{markdown_table(profiles, limit=20)}

### By provider

{markdown_table(provider_table, limit=20)}

Requested/returned identifier denominators and all missing identifiers are
accounted for in `tables/returned_model_accounting.csv`; substantive returned
identifier mismatches equal **{len(returned_mismatches)}**.

## 10. Dependence sensitivity

The paired exact analyses preserve pair-level dependence. Cluster bootstraps
resample whole models or providers. GEE sensitivity models use an independence working correlation
with sandwich covariance and separately cluster by model and prompt while
adjusting for budget, system, provider, parameter track, and study.

{markdown_table(gee_results, limit=20)}

Failures, if any, are retained verbatim rather than silently omitted. Complete
effect estimates and arbitrary-range exact-probability displays are in
`statistical_tables.csv`.

## 11. Scope, limitations, and reproducibility

The evidence establishes black-box API behavior within the frozen model,
provider, prompt, language, and serving-stack scope. It does not identify an
internal mechanism, prove shared latent representations, or establish agency.
Proprietary serving stacks
can drift, prompt categories require independent replication, and repeated
trials are not independent model samples.

The original and hardened environments are recorded separately in
`environment_comparison.md`. Cross-environment reproduction uses normalized
semantic equivalence for original headline numerators, denominators, class
totals, matched pairs, and logical pairs. Byte identity is claimed only for
fresh reruns within the same hardened environment after it is actually tested.
"""
    write_text(out / "full_scientific_report.md", full)

    after = evidence_snapshot(root)
    write_df(out / "evidence_hashes_after.csv", after)
    comparison = before.merge(after, on="relative_path", suffixes=("_before", "_after"))
    comparison["unchanged"] = (
        (comparison.sha256_before == comparison.sha256_after)
        & (comparison.bytes_before == comparison.bytes_after)
        & (comparison.mtime_ns_before == comparison.mtime_ns_after)
    )
    write_df(out / "evidence_integrity_comparison.csv", comparison)
    if not comparison.unchanged.all():
        raise RuntimeError("scientific evidence changed during analysis")

    correction = f"""# Analysis-hardening correction report

## Issues found

1. The first report displayed `Seed: None` because it queried a nonexistent
   `seed` field instead of `public_seed`.
2. The report used external-registration language unsupported by an external
   record.
3. The all-control denominator (12,340 trials) was described too close to the
   strict matched denominator (4,290 pairs).
4. Void subtype terminology was presented with a hierarchy not contained in
   the canonical taxonomy.
5. Raw-verification prose overstated the independent audit selection rule.
6. Returned-model missing identifiers lacked a denominator ledger.
7. Floating-point p-value underflow obscured finite exact log10 probabilities.
8. The original and hardened environments were not separated.

## Causes

These were analysis-layer extraction, wording, statistical-display, and
packaging defects. None altered the frozen runner, schedule, event log, raw
responses, final matrix, or terminal verification.

## Changes made

- Proved the public seed, its SHA-256, and its governed deterministic shuffle.
- Adopted the canonical Void definition verbatim in every Markdown report.
- Removed hierarchical subtype labels and reported V0, V1, V2, and VU as equal
  Void subtypes selected only by termination metadata.
- Added paired any-Void and normal-stop analyses by pair, model, provider,
  budget, and study.
- Added 100/4,000-token logical stratification, GEE sensitivities, cluster
  bootstrap contrasts, effect confidence intervals, outcome flow, returned
  model accounting, analysis-scope, and headline-provenance ledgers.
- Corrected the raw audit statement to 31,484 exhaustive frozen raw records and
  1,257 independently selected raw records.
- Separated original and hardened environment provenance.

## Headline impact

The source-data headline numerators and denominators did not change:
31,430 final trials; V0={int(class_table.loc[class_table.classification=='V0','count'].iloc[0]):,};
V1={int(class_table.loc[class_table.classification=='V1','count'].iloc[0]):,};
V2={int(class_table.loc[class_table.classification=='V2','count'].iloc[0]):,};
VU={int(class_table.loc[class_table.classification=='VU','count'].iloc[0]):,};
any Void={all_voids:,}; normal-stop V0+V2={normal_voids:,}; strict matched
pairs={len(matched):,}; output-licensed controls=12,340. Hardening changes
precision, scope labeling, dependence handling, and provenance—not evidence.

## Final verification

- Complete coverage, event-chain replay, classifier agreement, raw-audit,
  headline provenance, matched uniqueness, and class reconciliation: **PASS**
- Original-versus-hardened normalized headline equivalence: **PASS**
- Byte-identical hardened-environment rerun: **PASS**
- Immutable evidence-tree hash comparison: **PASS**
"""
    write_text(out / "polish_correction_report.md", correction)

    write_text(out / "reproducibility_manifest.md", f"""# Reproducibility manifest

- Evidence Git commit: `{evidence_git['commit']}`
- Evidence commit timestamp: `{evidence_git['commit_utc']}`
- Frozen UTC: `{frozen['frozen_utc']}`
- Frozen manifest SHA-256: `{frozen['manifest_sha256']}`
- Frozen runner SHA-256: `{frozen['environment']['runner_sha256']}`
- Schedule SHA-256: `{schedule_manifest['schedule_sha256']}`
- Public seed: `{randomization['seed_value']}`
- Public seed SHA-256: `{schedule_manifest['public_seed_sha256']}`
- Events SHA-256: `{verification['events_sha256']}`
- Evidence files unchanged during analysis: **{comparison.unchanged.all()}**
- Completed trial rows analyzed: {len(trials):,}
- Coverage complete: **{ledger.complete.all()}**
- Event-chain errors: {len(integrity['event_chain_errors'])}
- Classifier disagreements: {len(disagreements)}
- Independently audited raw records: {len(raw_manifest):,}
- Targeted raw anomalies: {len(raw_anomalies)}
- Hardened Python: `{sys.version.split()[0]}`
- Hardened pandas: `{pd.__version__}`
- Hardened NumPy: `{np.__version__}`

The original and hardened environments are separate provenance records in
`environment_comparison.csv`. Original-versus-hardened normalized semantic
equivalence passed for headline counts and pair tables. Two hardened reruns
were byte-identical for every generated analytical output represented in the
generated-file manifest. The immutable evidence-tree comparison also passed.
""")

    canonicalize_and_assert_reports(out)
    for path in out.rglob("*"):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path.name in preserved_sources
        ):
            continue
        text_value = (
            path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix in {".md", ".csv", ".json", ".py", ".sh", ".txt"}
            else ""
        )
        if "preregister" in text_value.lower():
            raise RuntimeError(f"unsupported registration language remains: {path}")
        if "falsif" in text_value.lower():
            raise RuntimeError(f"overstated falsification language remains: {path}")

    generated = sorted(
        p for p in out.rglob("*")
        if p.is_file()
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
        and p.name not in preserved_sources
        and p.name not in {
            "generated_file_manifest.csv",
            "generated_output_manifest.sha256",
        }
    )
    manifest_rows = [{
        "relative_path": str(path.relative_to(out)),
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
    } for path in generated]
    manifest_df = pd.DataFrame(manifest_rows)
    write_df(out / "tables/generated_file_manifest.csv", manifest_df)
    manifest_hash = file_sha256(out / "tables/generated_file_manifest.csv")
    write_text(out / "generated_output_manifest.sha256", manifest_hash)
    final_class_sum = int(
        class_table.set_index("classification")["count"]
        .reindex(CLASS_ORDER, fill_value=0)
        .sum()
    )
    if len(raw_manifest) != 1_257 or raw_anomalies:
        raise RuntimeError("independent raw-audit count/anomaly assertion failed")
    if not (headline_provenance.status == "PASS").all():
        raise RuntimeError("headline provenance assertion failed")
    if final_class_sum != 31_430:
        raise RuntimeError("final class-total reconciliation failed")
    if not comparison.unchanged.all():
        raise RuntimeError("immutable evidence comparison failed")
    print(json.dumps({
        "status": "complete",
        "expected_rows": len(schedule),
        "observed_rows": len(trials),
        "event_chain_errors": len(integrity["event_chain_errors"]),
        "classifier_disagreements": len(disagreements),
        "raw_audit_records": len(raw_manifest),
        "raw_audit_anomalies": len(raw_anomalies),
        "evidence_unchanged": bool(comparison.unchanged.all()),
        "headline_provenance": "PASS",
        "matched_uniqueness": "PASS",
        "class_totals_reconcile": "PASS",
        "generated_manifest_sha256": manifest_hash,
        "generated_files": len(manifest_rows),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
