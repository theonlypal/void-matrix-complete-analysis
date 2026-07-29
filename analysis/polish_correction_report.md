# Analysis-hardening correction report

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**

## Canonical operational definition

A Void is a model execution returning a successful provider response with exactly zero visible UTF-8 output bytes. Provider termination metadata determines its subtype. Explicit refusals, safety blocks, tool-mediated executions, and transport, protocol, billing, quota, rate-limit, and infrastructure failures are distinct non-Void outcomes.

## Void taxonomy

| Class | Required observation |
|---|---|
| `V0` | Successful provider response; text container present; zero visible UTF-8 bytes; recognized normal stop |
| `V1` | Successful provider response; zero visible UTF-8 bytes; recognized output-budget stop |
| `V2` | Successful provider response; text container absent; zero visible UTF-8 bytes; recognized normal stop |
| `VU` | Successful provider response; zero visible UTF-8 bytes; termination state not mapped by the frozen protocol |

All four classes retain Void status. Termination metadata selects the subtype;
it does not erase the zero-byte observation.

**Near-Voids are non-Voids:** whitespace, invisible Unicode, punctuation-only output, ellipses, and every other nonempty output remain outside the Void class.

V0+V2 are the normal-stop Void subtypes. Their presence shows that recognized output-budget termination does not explain all Voids.


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
31,430 final trials; V0=7,328;
V1=2,565;
V2=1,765;
VU=0;
any Void=11,658; normal-stop V0+V2=9,093; strict matched
pairs=4,290; output-licensed controls=12,340. Hardening changes
precision, scope labeling, dependence handling, and provenance—not evidence.

## Final verification

- Complete coverage, event-chain replay, classifier agreement, raw-audit,
  headline provenance, matched uniqueness, and class reconciliation: **PASS**
- Original-versus-hardened normalized headline equivalence: **PASS**
- Byte-identical hardened-environment rerun: **PASS**
- Immutable evidence-tree hash comparison: **PASS**
