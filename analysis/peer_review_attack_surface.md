# Peer-review attack surface

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


1. **Semantic labeling:** null/non-null categories were designed by the investigator; independent preregistration replication should test category robustness.
2. **Vendor/API drift:** exact model identifiers and returned identifiers are recorded, but proprietary serving stacks may change.
3. **Dependence:** repeated trials within model/prompt cells are not independent model samples; cluster analyses and cell-level reporting address this dependence.
4. **Prompt-space scope:** the boundary set is broad but finite and English-language.
5. **Subtype interpretation:** V0, V1, V2, and VU retain equal Void status; termination metadata selects the subtype without creating a hierarchy.
6. **V2 serialization:** missing text containers are retained separately because provider serialization differs.
7. **No blindness:** prospective freezing is not investigator or evaluator blinding.
8. **No mechanism claim:** black-box convergence cannot establish shared latent representation.
9. **Operational recovery:** retry effects are small and explicitly removable in sensitivity analysis.
10. **Multiplicity:** the report preserves all cells and separates confirmatory contrasts from ranked exploratory findings.
