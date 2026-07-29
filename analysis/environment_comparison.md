# Environment comparison

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


The original analysis environment and hardened robustness environment are distinct provenance records. No byte-identical claim is made across different Python/package versions. Original headline numerators, denominators, class totals, matched-pair tables, and logical-pair tables passed normalized semantic equivalence. Added GEE output requires statsmodels and belongs only to the hardened environment. Two hardened replays were also byte-identical.

| package | original_version | hardened_version | reason_for_change | affected_outputs | baseline_results_identical |
|---|---|---|---|---|---|
| Python | 3.9.6 | 3.12.13 | Isolated hardened-analysis runtime supplied by workspace tooling. | serialization/runtime metadata; core counts must remain semantically identical | PASS — normalized semantic equivalence verified by verify_analysis.sh |
| NumPy | 2.0.2 | 2.3.5 | Dependency resolution for the isolated robustness environment. | bootstrap implementation; core counts and exact pair tables unaffected | PASS — normalized semantic equivalence verified by verify_analysis.sh |
| pandas | 2.3.3 | 2.2.3 | Dependency resolution for the isolated robustness environment. | CSV serialization and table assembly; core counts must remain identical | PASS — normalized semantic equivalence verified by verify_analysis.sh |
| SciPy | 1.13.1 | 1.16.1 | Dependency resolution for the isolated robustness environment. | Clopper-Pearson and Fisher float value; exact log10 display independently recomputed | PASS — normalized semantic equivalence verified by verify_analysis.sh |
| statsmodels | not installed | 0.14.5 | Added only for GEE sandwich-covariance sensitivity models. | tables/dependence_aware_regression.csv only | PASS — normalized semantic equivalence verified by verify_analysis.sh |
| mpmath | not required by original headline pipeline | 1.3.0 | Not used by the hardened generator; exact log10 probabilities use Python Decimal and integer combinatorics. | none | PASS — normalized semantic equivalence verified by verify_analysis.sh |
