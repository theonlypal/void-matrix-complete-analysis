#!/bin/bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
EVIDENCE_ROOT="${EVIDENCE_ROOT:-/Users/rayanpal/void-matrix}"
HARDENED_PYTHON="${HARDENED_PYTHON:-/tmp/void-analysis-venv-20260728/bin/python}"
ORIGINAL_PYTHON="${ORIGINAL_PYTHON:-/usr/bin/python3}"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/void-analysis-verify.XXXXXX")"
trap 'rm -rf "$TMP_ROOT"' EXIT

hash_evidence() {
  local destination="$1"
  (
    cd "$EVIDENCE_ROOT"
    find . -type f -not -path './.git/*' -print0 \
      | LC_ALL=C sort -z \
      | xargs -0 shasum -a 256
  ) > "$destination"
}

compare_generated_manifests() {
  local first="$1"
  local second="$2"
  cmp "$first/tables/generated_file_manifest.csv" \
      "$second/tables/generated_file_manifest.csv"
  while IFS=, read -r relative_path bytes digest; do
    [ "$relative_path" = "relative_path" ] && continue
    [ -f "$first/$relative_path" ]
    [ -f "$second/$relative_path" ]
    [ "$(shasum -a 256 "$first/$relative_path" | awk '{print $1}')" = "$digest" ]
    [ "$(shasum -a 256 "$second/$relative_path" | awk '{print $1}')" = "$digest" ]
    cmp "$first/$relative_path" "$second/$relative_path"
  done < "$first/tables/generated_file_manifest.csv"
}

hash_evidence "$TMP_ROOT/evidence-before.sha256"

"$ORIGINAL_PYTHON" "$SOURCE_DIR/reproduce_all.py" \
  --evidence-root "$EVIDENCE_ROOT" \
  --analysis-root "$TMP_ROOT/original-environment"

"$HARDENED_PYTHON" "$SOURCE_DIR/reproduce_all.py" \
  --evidence-root "$EVIDENCE_ROOT" \
  --analysis-root "$TMP_ROOT/hardened-a"

"$HARDENED_PYTHON" "$SOURCE_DIR/reproduce_all.py" \
  --evidence-root "$EVIDENCE_ROOT" \
  --analysis-root "$TMP_ROOT/hardened-b"

cmp "$TMP_ROOT/original-environment/normalized_headline_snapshot.json" \
    "$TMP_ROOT/hardened-a/normalized_headline_snapshot.json"
compare_generated_manifests "$TMP_ROOT/hardened-a" "$TMP_ROOT/hardened-b"

hash_evidence "$TMP_ROOT/evidence-after.sha256"
cmp "$TMP_ROOT/evidence-before.sha256" "$TMP_ROOT/evidence-after.sha256"

echo "normalized cross-environment headline equivalence: PASS"
echo "byte-identical hardened rerun: PASS"
echo "immutable evidence hash comparison: PASS"
