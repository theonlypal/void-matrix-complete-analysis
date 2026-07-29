#!/usr/bin/env python3
"""Build a byte-reproducible ZIP archive from a directory tree."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import zipfile
from pathlib import Path, PurePosixPath

FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
EXCLUDED_DIRS = {
    ".git",
    "__MACOSX",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".swp", ".swo", ".tmp"}


def excluded(relative: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return True
    if relative.name in EXCLUDED_NAMES or relative.name.endswith("~"):
        return True
    return relative.suffix.lower() in EXCLUDED_SUFFIXES


def iter_files(source: Path) -> list[Path]:
    return sorted(
        (path for path in source.rglob("*") if path.is_file() and not excluded(path.relative_to(source))),
        key=lambda path: path.relative_to(source).as_posix().encode("utf-8"),
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(source: Path, output: Path, prefix: str) -> None:
    source = source.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix_path = PurePosixPath(prefix.strip("/"))
    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in iter_files(source):
            relative = PurePosixPath(path.relative_to(source).as_posix())
            member = str(prefix_path / relative) if prefix_path.parts else str(relative)
            info = zipfile.ZipInfo(member, FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800
            with path.open("rb") as handle:
                archive.writestr(info, handle.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    os.utime(output, (315532800, 315532800))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source is not a directory: {args.source}")
    build(args.source, args.output, args.prefix)
    print(f"{sha256(args.output)}  {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
