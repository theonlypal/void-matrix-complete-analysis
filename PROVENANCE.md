# Provenance

## Frozen runner

- Repository: [`theonlypal/void-matrix`](https://github.com/theonlypal/void-matrix)
- Original preregistration tag: `void-matrix-preregistered-final`
- Definitive runner tag: `v1.0.0-definitive-runner`
- Definitive runner commit: `2dfe895bdafd35d23d6dab5f307ed560214a3843`
- Source-manifest state: `SOURCE_SEALED`

The definitive runner repository was clean, its `main` branch and definitive tag resolved to the exact commit above, and its source manifest passed offline tests before public-artifact construction.

## Completed experiment identity

The identified master evidence corpus verified as:

- 31,430 scheduled and completed slots
- 31,484 raw attempt records
- 62,968 chained events
- zero pending slots, incomplete attempts, orphan raw responses, or event-chain errors
- event-chain head `b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460`
- raw-file-set SHA-256 `cb8f43f0f97e6ed0893cd2f8358b94d30afc4e5a036354ee05ef65f694b7b839`
- events SHA-256 `acf4b13af758784f657075ee7a9dda3192ccba45d025d033bc443e4bbe4d18d9`

The source evidence location is intentionally described here only as the verified completed runner workspace. A private absolute filesystem path is not required for public verification.

## Analysis source

The completed analysis was regenerated from the immutable evidence corpus by the included analysis source. The resulting package contains 90 substantive files after excluding only OS metadata, bytecode/cache files, and editor temporary files. Every file controlled by `analysis/tables/generated_file_manifest.csv` was independently verified. The generated-analysis manifest SHA-256 is:

`1fc3e04733a49a2584f496dd1f449a8d0796af71dc3542348a615b21e3e238f5`

The deterministic analysis ZIP and the regenerated analysis folder are compared file-by-file during release verification and contain the same 90 substantive files with no missing, extra, or changed content.

## Public derivative construction

The evidence release archive was built directly from the verified master with stable path sorting, normalized ZIP timestamps, stable permissions, deterministic compression, and a single stable archive root. File bytes were preserved exactly.

Excluded categories were limited to:

- Git implementation metadata
- operating-system metadata (`.DS_Store`, `__MACOSX`)
- Python bytecode and cache directories
- test/linter/type-checker caches
- editor swap and unrelated temporary files
- credential files, authorization values, and `.env` files, if present

No actual credential was detected. No scientific outcome category was removed. Failed attempts, retries, refusals, safety blocks, billing outcomes, the operational error, control Voids, V1 outcomes, raw responses, event-chain records, schedules, frozen configuration, inventories, preflight records, request reconstructions, summaries, identifiers, termination metadata, reasoning metadata, and cryptographic hashes remain in the public evidence archive.

## Master immutability

Before publication work began, complete SHA-256 inventories were recorded for the evidence master, analysis master, and sealed analysis ZIP. They were recomputed after archive construction and again before publication. The original masters and frozen runner were not modified. All construction occurred in this separate artifact repository.
