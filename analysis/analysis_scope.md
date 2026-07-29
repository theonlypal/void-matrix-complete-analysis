# Analysis-scope ledger

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


No external preregistration record was identified. “Confirmatory” below means specified by the prospectively frozen design; no external registration record was identified.

| analysis_or_claim | status | basis |
|---|---|---|
| Complete frozen census and integrity replay | integrity check | Frozen verifier, event chain, raw hashes |
| Strict three-pair semantic null/control contrast | confirmatory | Prospectively frozen matched-control study |
| All-Void Results | confirmatory | Frozen taxonomy and matched-control design |
| Void Subtype Results | descriptive | Complete V0/V1/V2/VU census with equal subtype status |
| Normal-Stop Void Counts | descriptive | Counts of V0+V2 selected only by termination metadata |
| Output-Budget-Stop Void Counts | descriptive | Counts of V1 selected only by termination metadata |
| Logical null/yes contrast at 4,000 tokens | confirmatory | Frozen logical contrast |
| Logical null/yes contrast at 100 tokens | prespecified secondary | Budget-sensitive stress condition |
| 16,000-token ceiling analysis | prespecified secondary | Frozen token-budget study |
| System/component ablations | prespecified secondary | Frozen no-system/no-component studies |
| Boundary sweep, each prompt | prespecified secondary | Frozen boundary_34 study |
| Boundary prompts 1–9 versus 10–34 pool | exploratory post-run | Investigator-defined grouping after execution |
| Adversarial override and instruction separation | prespecified secondary | Frozen robustness studies |
| Global null-role versus all output-licensed controls | exploratory post-run | Role pooling is analysis-defined |
| Provider/model morphology and class census | descriptive | Complete frozen census |
| Deterministic cell ranking and top findings | exploratory post-run | Analysis-defined ranking formula |
| GEE and cluster-bootstrap sensitivity | robustness sensitivity | Added during analysis hardening |
| Returned model identity accounting | integrity check | Requested/returned identifiers |
