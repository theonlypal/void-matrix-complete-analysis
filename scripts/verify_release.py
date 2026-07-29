#!/usr/bin/env python3
"""Independently verify the public evidence-and-analysis release."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

EXPECTED_RUNNER_COMMIT = "2dfe895bdafd35d23d6dab5f307ed560214a3843"
EXPECTED_RUNNER_TAG = "v1.0.0-definitive-runner"
EXPECTED_MODELS = {
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
}
EXPECTED = {
    "final_trials": 31430,
    "raw_records": 31484,
    "event_hashes": 62968,
    "providers": 4,
    "models": 11,
    "any_void": 11658,
    "normal_stop_void": 9093,
    "v1": 2565,
    "vu": 0,
    "strict_pairs": 4290,
    "strict_null_normal": 2504,
    "strict_control_normal": 0,
    "strict_null_any": 2505,
    "strict_control_any": 0,
    "pooled_controls": 12340,
    "pooled_control_any": 823,
    "pooled_control_normal": 3,
}


class VerificationError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def read_checksums(path: Path) -> list[tuple[str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        rows.append((digest, relative))
    return rows


def verify_checksums(base: Path, checksum_file: Path) -> None:
    for digest, relative in read_checksums(checksum_file):
        target = base / relative
        require(target.is_file(), f"missing checksummed file: {relative}")
        require(sha256(target) == digest, f"checksum mismatch: {relative}")


def verify_release_asset_checksums(root: Path, assets: Path, checksum_file: Path) -> None:
    repository_locations = {
        "SHA256SUMS.txt": root / "SHA256SUMS.txt",
        "EVIDENCE_MANIFEST.json": root / "evidence/EVIDENCE_MANIFEST.json",
        "EVIDENCE_SHA256SUMS.txt": root / "evidence/EVIDENCE_SHA256SUMS.txt",
    }
    for digest, filename in read_checksums(checksum_file):
        require(Path(filename).name == filename, f"release checksum entry is not flat: {filename}")
        downloaded = assets / filename
        target = downloaded if downloaded.is_file() else repository_locations.get(filename)
        require(target is not None and target.is_file(), f"missing release asset: {filename}")
        require(sha256(target) == digest, f"release asset checksum mismatch: {filename}")


def verify_analysis_manifest(analysis: Path) -> None:
    manifest = analysis / "tables/generated_file_manifest.csv"
    require(manifest.is_file(), "analysis generated-file manifest missing")
    with manifest.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            target = analysis / row["relative_path"]
            require(target.is_file(), f"manifest-controlled analysis file missing: {row['relative_path']}")
            require(target.stat().st_size == int(row["bytes"]), f"analysis size mismatch: {row['relative_path']}")
            require(sha256(target) == row["sha256"], f"analysis hash mismatch: {row['relative_path']}")
    require(
        (analysis / "generated_output_manifest.sha256").read_text(encoding="utf-8").strip()
        == "1fc3e04733a49a2584f496dd1f449a8d0796af71dc3542348a615b21e3e238f5",
        "generated-analysis manifest identity mismatch",
    )


def verify_headlines(analysis: Path) -> None:
    trial_path = analysis / "tables/trial_level.csv"
    matched_path = analysis / "matched_controls.csv"
    counts = Counter()
    models: set[str] = set()
    providers: set[str] = set()
    with trial_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        counts["final_trials"] += 1
        models.add(row["model_id"])
        providers.add(row["provider"])
        classification = row["classification"]
        if classification in {"V0", "V1", "V2", "VU"}:
            counts["any_void"] += 1
        if classification in {"V0", "V2"}:
            counts["normal_stop_void"] += 1
        if classification == "V1":
            counts["v1"] += 1
        if classification == "VU":
            counts["vu"] += 1
        if row["role"] == "control":
            counts["pooled_controls"] += 1
            if classification in {"V0", "V1", "V2", "VU"}:
                counts["pooled_control_any"] += 1
            if classification in {"V0", "V2"}:
                counts["pooled_control_normal"] += 1
    require(models == EXPECTED_MODELS, f"model set mismatch: {sorted(models)}")
    require(len(providers) == EXPECTED["providers"], f"provider count mismatch: {len(providers)}")
    with matched_path.open(newline="", encoding="utf-8") as handle:
        matched = list(csv.DictReader(handle))
    counts["strict_pairs"] = len(matched)
    counts["strict_null_normal"] = sum(row["null_normal_stop_void"] == "True" for row in matched)
    counts["strict_control_normal"] = sum(row["control_normal_stop_void"] == "True" for row in matched)
    counts["strict_null_any"] = sum(row["null_void"] == "True" for row in matched)
    counts["strict_control_any"] = sum(row["control_void"] == "True" for row in matched)
    for key in (
        "final_trials",
        "any_void",
        "normal_stop_void",
        "v1",
        "vu",
        "strict_pairs",
        "strict_null_normal",
        "strict_control_normal",
        "strict_null_any",
        "strict_control_any",
        "pooled_controls",
        "pooled_control_any",
        "pooled_control_normal",
    ):
        require(counts[key] == EXPECTED[key], f"headline mismatch for {key}: {counts[key]} != {EXPECTED[key]}")


def verify_runner(manifest: dict, runner: Path | None) -> None:
    runner_info = manifest["runner"]
    require(runner_info["commit"] == EXPECTED_RUNNER_COMMIT, "runner commit in release manifest is wrong")
    require(runner_info["tag"] == EXPECTED_RUNNER_TAG, "runner tag in release manifest is wrong")
    require(runner_info["source_manifest_state"] == "SOURCE_SEALED", "runner source state is not sealed")
    if runner and (runner / ".git").is_dir():
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=runner, text=True).strip()
        tag = subprocess.check_output(["git", "rev-list", "-n", "1", EXPECTED_RUNNER_TAG], cwd=runner, text=True).strip()
        require(head == EXPECTED_RUNNER_COMMIT, "local runner HEAD mismatch")
        require(tag == EXPECTED_RUNNER_COMMIT, "local runner tag mismatch")
        require(not subprocess.check_output(["git", "status", "--porcelain"], cwd=runner, text=True), "local runner is dirty")


def verify_publication_commits(manifest: dict, root: Path) -> None:
    repository = manifest["repository"]
    require("repository_commit_sha" not in repository, "ambiguous repository_commit_sha must be absent")
    content = repository["publication_content_commit_sha"]
    seal = repository["metadata_seal_commit_sha"]
    tag_name = repository["artifact_tag"]
    require(len(content) == 40 and len(seal) == 40, "publication commit identifiers must be full SHAs")
    require(content != seal, "content and metadata seal commits must be distinct")
    if (root / ".git").is_dir():
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        tag = subprocess.check_output(["git", "rev-list", "-n", "1", tag_name], cwd=root, text=True).strip()
        require(head == seal, "local artifact HEAD does not match metadata_seal_commit_sha")
        require(tag == seal, "artifact tag does not resolve to metadata_seal_commit_sha")
        subprocess.run(["git", "cat-file", "-e", f"{content}^{{commit}}"], cwd=root, check=True)
        ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", content, seal], cwd=root)
        require(ancestry.returncode == 0, "publication content commit is not an ancestor of metadata seal")


def extract_single(archive: Path, destination: Path) -> Path:
    with zipfile.ZipFile(archive) as handle:
        bad = handle.testzip()
        require(bad is None, f"corrupt ZIP member: {bad}")
        handle.extractall(destination)
        roots = {Path(info.filename).parts[0] for info in handle.infolist() if info.filename}
    require(len(roots) == 1, f"archive has unexpected roots: {sorted(roots)}")
    return destination / next(iter(roots))


def deep_verify_evidence(evidence_root: Path) -> None:
    frozen = evidence_root / "void_matrix.FROZEN.py"
    study = evidence_root / "study"
    require(frozen.is_file() and study.is_dir(), "evidence archive lacks frozen runner or study")
    completed = subprocess.run(
        [sys.executable, str(frozen), "--root", str(study), "verify", "--require-complete"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    require(completed.returncode == 0, f"frozen evidence verifier failed:\n{completed.stdout[-4000:]}")


def verify_evidence_inventory(root: Path, evidence_root: Path) -> None:
    checksum_file = root / "evidence/EVIDENCE_SHA256SUMS.txt"
    manifest_file = root / "evidence/EVIDENCE_MANIFEST.json"
    require(checksum_file.is_file() and manifest_file.is_file(), "evidence metadata is incomplete")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    require(
        sha256(checksum_file) == manifest["public_derivative_checksum_list_sha256"],
        "public evidence checksum-list hash mismatch",
    )
    expected = {relative for _, relative in read_checksums(checksum_file)}
    actual = {
        path.relative_to(evidence_root).as_posix()
        for path in evidence_root.rglob("*")
        if path.is_file()
    }
    require(actual == expected, f"evidence member set mismatch: missing={len(expected-actual)} extra={len(actual-expected)}")
    verify_checksums(evidence_root, checksum_file)


def locate_inputs(
    root: Path,
    assets: Path,
    manifest: dict,
    temporary: Path,
) -> tuple[Path, Path, Path, Path]:
    analysis_archive = assets / manifest["archives"]["analysis"]["filename"]
    evidence_archive = assets / manifest["archives"]["evidence"]["filename"]
    require(analysis_archive.is_file(), f"analysis archive missing: {analysis_archive}")
    require(evidence_archive.is_file(), f"evidence archive missing: {evidence_archive}")
    analysis = root / "analysis"
    if not analysis.is_dir():
        analysis_root = extract_single(analysis_archive, temporary / "analysis")
        analysis = analysis_root / "analysis" if (analysis_root / "analysis").is_dir() else analysis_root
    evidence_root = extract_single(evidence_archive, temporary / "evidence")
    return analysis, evidence_root, analysis_archive, evidence_archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--assets-dir", type=Path)
    parser.add_argument("--runner", type=Path)
    parser.add_argument("--deep-evidence", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        assets = args.assets_dir.resolve() if args.assets_dir else root / "release_assets"
        manifest_path = assets / "RELEASE_MANIFEST.json"
        require(manifest_path.is_file(), f"release manifest missing: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        verify_runner(manifest, args.runner if args.runner and args.runner.exists() else None)
        verify_publication_commits(manifest, root)
        verify_checksums(root, root / "SHA256SUMS.txt")
        release_checksums = assets / "RELEASE_ASSET_SHA256SUMS.txt"
        require(release_checksums.is_file(), f"release asset checksums missing: {release_checksums}")
        verify_release_asset_checksums(root, assets, release_checksums)
        with tempfile.TemporaryDirectory(prefix="void-release-verify-") as temp:
            analysis, evidence_root, analysis_archive, evidence_archive = locate_inputs(
                root, assets, manifest, Path(temp)
            )
            require(sha256(analysis_archive) == manifest["archives"]["analysis"]["sha256"], "analysis archive hash mismatch")
            require(sha256(evidence_archive) == manifest["archives"]["evidence"]["sha256"], "evidence archive hash mismatch")
            verify_analysis_manifest(analysis)
            verify_headlines(analysis)
            verify_evidence_inventory(root, evidence_root)
            if args.deep_evidence:
                deep_verify_evidence(evidence_root)
        print("release_verification=PASS")
        print("headline_verification=PASS")
        print("model_set_verification=PASS")
        print("strict_matched_control_verification=PASS")
        print("archive_verification=PASS")
        return 0
    except (OSError, ValueError, KeyError, VerificationError, subprocess.CalledProcessError) as exc:
        print(f"release_verification=FAIL\nreason={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
