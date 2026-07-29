# Evidence Archive

The complete raw evidence corpus is distributed as the deterministic GitHub release asset:

[`void-matrix-evidence-v1.0.0.zip`](https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/void-matrix-evidence-v1.0.0.zip)

It is not committed as tens of thousands of individual Git objects. The archive contains the frozen runner and completed study workspace needed to replay offline verification, including all raw attempt records, retries, failed attempts, event-chain records, schedules, frozen configuration, provider inventory and preflight records, request reconstructions, summaries, provider identifiers, termination metadata, and retained reasoning metadata.

For byte-reproducible packaging, all ZIP member modification timestamps are normalized to 1980-01-01, the earliest conventional ZIP timestamp. These are archive metadata, not experiment timestamps; authoritative times are preserved inside the event records, manifests, raw responses, Git history, and release metadata.

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**

All four classes retain Void status. Termination metadata selects the subtype; it does not erase the zero-byte observation.

V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized output-budget termination does not explain all Voids.

Verification anchors:

- Archive SHA-256: `04d79ddb0f961729369da8ae46c58f7293e42dfd278d2e9b703edc0cec6455d2`
- Original evidence-tree checksum-list SHA-256: `309cd9a77cdd6a6bf4ff733ca446163d170cb65e4ebfaac70d34f5c293481cc9`
- Raw-file-set SHA-256: `cb8f43f0f97e6ed0893cd2f8358b94d30afc4e5a036354ee05ef65f694b7b839`
- Event-chain head: `b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460`

The archive’s portable, source-relative file checksums are in [`EVIDENCE_SHA256SUMS.txt`](EVIDENCE_SHA256SUMS.txt), with sizes and archive member names in [`evidence_file_inventory.csv`](evidence_file_inventory.csv).

After extraction:

```bash
python3 void-matrix-evidence-v1.0.0/void_matrix.FROZEN.py \
  --root void-matrix-evidence-v1.0.0/study \
  verify --require-complete
```

This command performs no provider API calls.
