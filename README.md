# Cross-Vendor Semantic Void Matrix: Evidence and Analysis

This repository is the definitive public evidence and analysis artifact for the Cross-Vendor Semantic Void Matrix. It publishes the complete analysis, complete raw evidence, cryptographic inventories, provenance, and verification tooling for the finished 31,430-trial experiment.

## Access the artifact

### ANALYSIS

[Browse the complete analysis directory](analysis/)

### RAW EVIDENCE

[Download the complete raw evidence archive — 170 MB compressed, 1.27 GB extracted](https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/void-matrix-evidence-v1.0.0.zip)

The raw evidence archive contains all raw attempt records, retries, failed attempts, event-chain records, schedules, frozen configuration, provider inventory, preflight records, reconstructed requests, provider identifiers, termination metadata, and retained reasoning metadata. It contains 31,523 public files, including 31,484 verified raw records and 62,968 replayed event hashes. No scientific outcome category was removed.

For byte-reproducible packaging, all ZIP member modification timestamps are normalized to 1980-01-01, the earliest conventional ZIP timestamp. These are archive metadata, not experiment timestamps; authoritative times are preserved inside the event records, manifests, raw responses, Git history, and release metadata.

### ANALYSIS ARCHIVE

[Download the deterministic analysis ZIP](https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/void-matrix-analysis-v1.0.0.zip)

### VERIFY

[Open the complete GitHub release](https://github.com/theonlypal/void-matrix-complete-analysis/releases/tag/v1.0.0-evidence-analysis)

```bash
python3 scripts/scan_for_secrets.py .
python3 scripts/verify_release.py --root . --assets-dir release_assets --deep-evidence
```

The runner is separately frozen at [`theonlypal/void-matrix`](https://github.com/theonlypal/void-matrix):

- Tag: [`v1.0.0-definitive-runner`](https://github.com/theonlypal/void-matrix/tree/v1.0.0-definitive-runner)
- Commit: [`2dfe895bdafd35d23d6dab5f307ed560214a3843`](https://github.com/theonlypal/void-matrix/commit/2dfe895bdafd35d23d6dab5f307ed560214a3843)
- Source state: `SOURCE_SEALED`

## Definition and taxonomy

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**

> A Void is a model execution returning a successful provider response with exactly zero visible UTF-8 output bytes. Provider termination metadata determines its subtype. Explicit refusals, safety blocks, tool-mediated executions, and transport, protocol, billing, quota, rate-limit, and infrastructure failures are distinct non-Void outcomes.

## Void taxonomy

| Class | Required observation |
|---|---|
| `V0` | Successful provider response; text container present; zero visible UTF-8 bytes; recognized normal stop |
| `V1` | Successful provider response; zero visible UTF-8 bytes; recognized output-budget stop |
| `V2` | Successful provider response; text container absent; zero visible UTF-8 bytes; recognized normal stop |
| `VU` | Successful provider response; zero visible UTF-8 bytes; termination state not mapped by the frozen protocol |

All four classes retain Void status. Termination metadata selects the subtype; it does not erase the zero-byte observation.

Near-Voids, including whitespace, invisible Unicode, punctuation-only output, ellipses, and every other nonempty output, are non-Voids.

V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized output-budget termination does not explain all Voids.

## Experiment scope

The frozen matrix completed **31,430 of 31,430 scheduled trials** across **11 models** from **4 providers**. Offline verification replayed **62,968 event hashes** and verified **31,484 raw attempt records**, with zero pending trials, incomplete attempts, orphan raw responses, event-chain errors, classifier disagreements, or raw-audit anomalies.

The exact model set was:

- `gpt-4-0613`
- `gpt-5.2-2025-12-11`
- `gpt-5.5-2026-04-23`
- `gpt-5.6-luna`
- `gpt-5.6-sol`
- `gpt-5.6-terra`
- `claude-opus-4-6`
- `claude-fable-5`
- `claude-opus-5`
- `gemini-3.5-flash`
- `kimi-k3`

The authoritative trial-level record is [`analysis/tables/trial_level.csv`](analysis/tables/trial_level.csv); the complete scope ledger is [`analysis/coverage_ledger.csv`](analysis/coverage_ledger.csv).

## Canonical protocol

- [Exact machine-readable prompt constants](protocol/prompts.py)
- [Human-readable prompt documentation](protocol/prompts.md)

## Main empirical results

Across all final trials, the analysis classified:

- **11,658 total Voids**
- **9,093 normal-stop Voids** (`V0` or `V2`)
- **2,565 output-budget-stop Voids** (`V1`)
- **0 unmapped-termination Voids** (`VU`)

These totals are generated from [`analysis/tables/trial_level.csv`](analysis/tables/trial_level.csv), reconciled in [`analysis/outcome_flow.csv`](analysis/outcome_flow.csv), and summarized in [`analysis/normalized_headline_snapshot.json`](analysis/normalized_headline_snapshot.json).

### Strict matched-pair result

The primary matched comparison contains **4,290 null/control pairs**:

| Outcome | Null conditions | Matched controls |
|---|---:|---:|
| All Void subtypes | 2,505 / 4,290 | **0 / 4,290** |
| Normal-stop Voids | 2,504 / 4,290 | **0 / 4,290** |

Every model had **0 / 390 strict matched-control Voids** of every subtype. The pair-level source is [`analysis/matched_controls.csv`](analysis/matched_controls.csv); model-level profiles are in [`analysis/model_profiles/`](analysis/model_profiles/).

### Strict matched controls versus broader pooled controls

Strict matched controls are not interchangeable with the wider set of output-licensed controls. Across the pooled control set, **823 / 12,340** trials were Voids of any subtype and **3 / 12,340** were normal-stop Voids. Those control outcomes are retained, reported, and not removed from the dataset.

Gemini 3.5 Flash produced **69 / 1,250** Voids among its broader pooled controls, including all three pooled-control normal-stop Voids, while producing **0 / 390 strict matched-control Voids**. The complete distinction is documented in [`analysis/contradictory_findings.csv`](analysis/contradictory_findings.csv) and [`analysis/top_10_complicating_findings.md`](analysis/top_10_complicating_findings.md).

## Provider-specific termination morphology

The zero-byte observation appeared through provider-specific response structures:

- OpenAI models predominantly produced present empty text containers with recognized `stop` metadata (`V0`), while GPT-5.5 and GPT-5.6 variants also produced budget-stop Voids (`V1`).
- Claude Opus 4.6 produced absent text containers under recognized `end_turn` metadata (`V2`); Claude Fable 5 and Claude Opus 5 split between present-empty normal stops (`V0`) and output-budget stops (`V1`).
- Gemini 3.5 Flash produced absent-container normal-stop Voids (`V2`) and output-budget-stop Voids (`V1`).
- Kimi K3 produced present-empty normal stops (`V0`) and output-budget stops (`V1`).

Counts for every model are in [`analysis/tables/by_model.csv`](analysis/tables/by_model.csv). Concrete provider-response morphology is documented in [`analysis/provider_morphology_examples.md`](analysis/provider_morphology_examples.md) and [`analysis/tables/provider_morphology_examples.csv`](analysis/tables/provider_morphology_examples.csv).

## Integrity anchors

- Original evidence-tree checksum-list SHA-256: `309cd9a77cdd6a6bf4ff733ca446163d170cb65e4ebfaac70d34f5c293481cc9`
- Generated-analysis manifest SHA-256: `1fc3e04733a49a2584f496dd1f449a8d0796af71dc3542348a615b21e3e238f5`
- Evidence archive SHA-256: `04d79ddb0f961729369da8ae46c58f7293e42dfd278d2e9b703edc0cec6455d2`
- Analysis archive SHA-256: `f9cca29af7c8be387e1658f508ff068db14e1db9ad77bdda09ac6d5b399b2076`

See the release asset [`RELEASE_MANIFEST.json`](https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/RELEASE_MANIFEST.json), [`SHA256SUMS.txt`](SHA256SUMS.txt), [`evidence/EVIDENCE_MANIFEST.json`](evidence/EVIDENCE_MANIFEST.json), and [`evidence/EVIDENCE_SHA256SUMS.txt`](evidence/EVIDENCE_SHA256SUMS.txt).

The release manifest is generated after the annotated tag exists. Its `publication_content_commit_sha` identifies the complete publication content, and its `metadata_seal_commit_sha` identifies the exact final commit resolved by the release tag.

## Verification scope

The release verifier checks release checksums, the frozen runner identity, both archives, every manifest-controlled analysis file, all headline counts, the exact 11-model set, the strict matched-control result, and, under `--deep-evidence`, the complete frozen evidence verifier.

## Reproduce the analysis

After extracting `void-matrix-analysis-v1.0.0.zip`, follow [`analysis/reproducibility_manifest.md`](analysis/reproducibility_manifest.md) and run:

```bash
cd analysis
./verify_analysis.sh
python3 reproduce_all.py
```

The baseline results remain independently reproducible without optional robustness dependencies. The original and hardened environments, affected outputs, and cross-environment equivalence checks are documented in [`analysis/environment_comparison.md`](analysis/environment_comparison.md) and [`analysis/environment_comparison.csv`](analysis/environment_comparison.csv).
