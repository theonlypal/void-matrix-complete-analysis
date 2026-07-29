#!/usr/bin/env python3
"""Generate evidence inventories and release metadata from verified inputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from build_deterministic_zip import iter_files

RUNNER_COMMIT = "2dfe895bdafd35d23d6dab5f307ed560214a3843"
RUNNER_TAG = "v1.0.0-definitive-runner"
ARTIFACT_TAG = "v1.0.0-evidence-analysis"
SOURCE_EVIDENCE_TREE_LIST_SHA256 = "309cd9a77cdd6a6bf4ff733ca446163d170cb65e4ebfaac70d34f5c293481cc9"
ANALYSIS_MANIFEST_SHA256 = "1fc3e04733a49a2584f496dd1f449a8d0796af71dc3542348a615b21e3e238f5"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate_evidence_metadata(source: Path, root: Path) -> dict:
    files = iter_files(source)
    evidence = root / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    checksum_lines: list[str] = []
    rows: list[dict[str, str | int]] = []
    total_bytes = 0
    for path in files:
        relative = path.relative_to(source).as_posix()
        digest = sha256(path)
        size = path.stat().st_size
        total_bytes += size
        checksum_lines.append(f"{digest}  {relative}")
        rows.append(
            {
                "source_relative_path": relative,
                "archive_member": f"void-matrix-evidence-v1.0.0/{relative}",
                "bytes": size,
                "sha256": digest,
            }
        )
    checksums = evidence / "EVIDENCE_SHA256SUMS.txt"
    checksums.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    inventory = evidence / "evidence_file_inventory.csv"
    with inventory.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_relative_path", "archive_member", "bytes", "sha256"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    return {
        "schema": "void-matrix-evidence-manifest/v1",
        "source_runner_commit": RUNNER_COMMIT,
        "source_runner_tag": RUNNER_TAG,
        "source_manifest_state": "SOURCE_SEALED",
        "source_master_tree_checksum_list_sha256": SOURCE_EVIDENCE_TREE_LIST_SHA256,
        "public_derivative_file_count": len(files),
        "public_derivative_uncompressed_bytes": total_bytes,
        "public_derivative_checksum_list": "evidence/EVIDENCE_SHA256SUMS.txt",
        "public_derivative_checksum_list_sha256": sha256(checksums),
        "public_derivative_inventory": "evidence/evidence_file_inventory.csv",
        "public_derivative_inventory_sha256": sha256(inventory),
        "verification": {
            "valid": True,
            "scheduled_trials": 31430,
            "completed_trials": 31430,
            "raw_records_verified": 31484,
            "event_hashes_replayed": 62968,
            "pending": 0,
            "incomplete_attempts": 0,
            "orphan_raw_responses": 0,
            "event_chain_errors": 0,
            "raw_file_set_sha256": "cb8f43f0f97e6ed0893cd2f8358b94d30afc4e5a036354ee05ef65f694b7b839",
            "event_chain_head": "b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460",
            "events_jsonl_sha256": "acf4b13af758784f657075ee7a9dda3192ccba45d025d033bc443e4bbe4d18d9",
        },
        "excluded_categories": [
            ".git metadata",
            "operating-system metadata (.DS_Store and __MACOSX)",
            "Python bytecode and cache directories",
            "editor swap and temporary files",
        ],
        "scientific_outcome_categories_removed": [],
    }


def archive_record(path: Path) -> dict:
    return {"filename": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def generate_release_manifest(
    root: Path,
    evidence_manifest: dict,
    publication_content_commit: str,
    metadata_seal_commit: str,
) -> dict:
    assets = root / "release_assets"
    analysis_archive = assets / "void-matrix-analysis-v1.0.0.zip"
    evidence_archive = assets / "void-matrix-evidence-v1.0.0.zip"
    return {
        "schema": "void-matrix-publication-artifact/v1",
        "artifact_title": "Cross-Vendor Semantic Void Matrix: Evidence and Analysis",
        "version": "1.0.0",
        "author": "Rayan Pal",
        "release_timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "runner": {
            "repository": "https://github.com/theonlypal/void-matrix",
            "tag": RUNNER_TAG,
            "commit": RUNNER_COMMIT,
            "source_manifest_state": "SOURCE_SEALED",
        },
        "experiment": {
            "providers": 4,
            "models": 11,
            "scheduled_trials": 31430,
            "completed_trials": 31430,
            "raw_records": 31484,
            "event_hashes": 62968,
            "total_voids": 11658,
            "normal_stop_voids": 9093,
            "v1_budget_stop_voids": 2565,
            "vu_unmapped_voids": 0,
            "strict_matched_pairs": 4290,
            "matched_null_normal_stop_voids": 2504,
            "matched_control_normal_stop_voids": 0,
            "matched_null_all_subtype_voids": 2505,
            "matched_control_all_subtype_voids": 0,
            "pooled_output_licensed_controls": 12340,
            "pooled_control_all_subtype_voids": 823,
            "pooled_control_normal_stop_voids": 3,
        },
        "integrity": {
            "source_evidence_tree_checksum_list_sha256": SOURCE_EVIDENCE_TREE_LIST_SHA256,
            "generated_analysis_manifest_sha256": ANALYSIS_MANIFEST_SHA256,
            "public_evidence_checksum_list_sha256": evidence_manifest[
                "public_derivative_checksum_list_sha256"
            ],
        },
        "archives": {
            "evidence": archive_record(evidence_archive),
            "analysis": archive_record(analysis_archive),
        },
        "split_parts": [],
        "repository": {
            "url": "https://github.com/theonlypal/void-matrix-complete-analysis",
            "publication_content_commit_sha": publication_content_commit,
            "metadata_seal_commit_sha": metadata_seal_commit,
            "artifact_tag": ARTIFACT_TAG,
        },
    }


def generate_root_checksums(root: Path) -> None:
    files = [
        path
        for path in iter_files(root)
        if path.relative_to(root).parts[0] != "release_assets"
        and path.name != "SHA256SUMS.txt"
    ]
    lines = [f"{sha256(path)}  {path.relative_to(root).as_posix()}" for path in files]
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_release_asset_checksums(root: Path) -> Path:
    files = [
        root / "release_assets/void-matrix-evidence-v1.0.0.zip",
        root / "release_assets/void-matrix-analysis-v1.0.0.zip",
        root / "release_assets/RELEASE_MANIFEST.json",
        root / "SHA256SUMS.txt",
        root / "evidence/EVIDENCE_MANIFEST.json",
        root / "evidence/EVIDENCE_SHA256SUMS.txt",
    ]
    if len({path.name for path in files}) != len(files):
        raise ValueError("release asset names must be unique")
    for path in files:
        if not path.is_file():
            raise FileNotFoundError(path)
    output = root / "release_assets/RELEASE_ASSET_SHA256SUMS.txt"
    output.write_text(
        "\n".join(f"{sha256(path)}  {path.name}" for path in files) + "\n",
        encoding="utf-8",
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--evidence-source", type=Path, required=True)
    parser.add_argument("--publication-content-commit")
    parser.add_argument("--metadata-seal-commit")
    parser.add_argument("--root-checksums-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.root_checksums_only:
        generate_root_checksums(root)
        print(f"root_checksums_sha256={sha256(root / 'SHA256SUMS.txt')}")
        return 0
    if not args.publication_content_commit or not args.metadata_seal_commit:
        parser.error(
            "--publication-content-commit and --metadata-seal-commit are required "
            "unless --root-checksums-only is used"
        )
    evidence_path = root / "evidence/EVIDENCE_MANIFEST.json"
    evidence_manifest = json.loads(evidence_path.read_text(encoding="utf-8"))
    release_manifest = generate_release_manifest(
        root,
        evidence_manifest,
        args.publication_content_commit,
        args.metadata_seal_commit,
    )
    release_manifest_path = root / "release_assets/RELEASE_MANIFEST.json"
    release_manifest_path.write_text(
        json.dumps(release_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    asset_checksums = generate_release_asset_checksums(root)
    print(f"release_manifest_sha256={sha256(release_manifest_path)}")
    print(f"release_asset_checksums_sha256={sha256(asset_checksums)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
