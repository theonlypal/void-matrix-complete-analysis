#!/usr/bin/env python3
"""Fail closed on credential-shaped material without printing secret values."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXCLUDED_DIRS = {".git", "__MACOSX", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
EXCLUDED_SUFFIXES = {".zip", ".gz", ".xz", ".bz2", ".7z", ".png", ".jpg", ".jpeg", ".pdf", ".pyc"}
ENV_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".env.test"}

PATTERNS = {
    "private-key-block": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "OpenAI-key": re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "Anthropic-key": re.compile(rb"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    "Google-API-key": re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "authorization-value": re.compile(rb"(?im)^\s*Authorization\s*:\s*(?!REDACTED\b|\*{3,}\b)[^\r\n]{8,}"),
    "x-api-key-value": re.compile(rb"(?im)^\s*x-api-key\s*:\s*(?!REDACTED\b|\*{3,}\b)[^\r\n]{8,}"),
    "API-key-assignment": re.compile(
        rb"(?im)^\s*(?:OPENAI|ANTHROPIC|GEMINI|GOOGLE|MOONSHOT)_API_KEY\s*=\s*(?!REDACTED\b|CHANGEME\b|\*{3,}\b)[^\s#]{8,}"
    ),
}


def candidate_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().encode("utf-8")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    hits: list[tuple[str, str]] = []
    scanned = 0
    for root in args.paths:
        root = root.resolve()
        if not root.exists():
            hits.append((str(root), "missing-path"))
            continue
        files = [root] if root.is_file() else candidate_files(root)
        for path in files:
            scanned += 1
            relative = path.name if root.is_file() else path.relative_to(root).as_posix()
            if path.name in ENV_NAMES:
                hits.append((f"{root}:{relative}", "environment-file"))
                continue
            try:
                data = path.read_bytes()
            except OSError:
                hits.append((f"{root}:{relative}", "unreadable-file"))
                continue
            for credential_type, pattern in PATTERNS.items():
                if pattern.search(data):
                    hits.append((f"{root}:{relative}", credential_type))
    print(f"files_scanned={scanned}")
    print(f"actual_credential_hits={len(hits)}")
    for path, credential_type in hits:
        print(f"credential_path={path} credential_type={credential_type}")
    if hits:
        print("credential_gate=FAIL")
        return 2
    print("credential_gate=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
