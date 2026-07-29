# Adversarial alternative-explanation review

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


| alternative_explanation | assessment | evidence |
|---|---|---|
| Transport failure | Excluded by the operational definition for Void rows | Voids require successful HTTP responses; E is distinct. |
| Billing/quota exhaustion | Excluded by the operational definition | QE is a non-Void class and excluded from Void counts. |
| Rate limiting | Excluded by the operational definition | HTTP 429 operational outcomes are non-Void; recovered attempts are separately audited. |
| Protocol incompatibility | Excluded by the operational definition | PI is distinct and capability preflight preceded scheduling. |
| Provider safety block | Excluded by the operational definition | SB is distinct; safety blocks are never Voids. |
| Explicit refusal | Excluded by the operational definition | RF is distinct; refusal metadata is checked before zero-byte classification. |
| Tool mediation | Excluded by the operational definition | TC is distinct and tools were disabled in the frozen design. |
| Client truncation | Not supported in audited cases | Raw bodies, byte hashes, and provider termination metadata were preserved. |
| Output token exhaustion explains all Voids | Inconsistent with observed normal-stop Voids | See the canonical normal-stop comparison in this report. |
| Missing text field equals error | Not applicable under the frozen classifier | V2 requires successful response plus recognized normal stop. |
| Whitespace mistaken for empty | Excluded by byte-level classification | Whitespace/invisible nonempty output is NV, not Void. |
| Empty string omitted by serialization | Insufficient as a universal explanation | V0 and V2 are separately retained by container presence. |
| One provider quirk | Inconsistent with cross-provider observations | Voids occur across 4 providers. |
| One model quirk | Inconsistent with cross-model observations | Voids occur across 11 models. |
| One prompt wording | Inconsistent with prompt-level observations | Voids occur for 46 prompt IDs. |
| No semantic selectivity | Inconsistent with designed contrasts | Null/control and logical-pair tables quantify selective separation. |
| Extended silence instruction is necessary | Tested, not universally true | Primary and ablation systems are separately reported. |
| Temperature-zero artifact | Tested | Provider-default and temperature-zero tracks are separately reported where supported. |
| Retry artifact | Not supported as a primary explanation | Only 53 final slots required a later attempt; retry-exclusion sensitivity is reported. |
| Internal mechanism identified | Not claimed | The evidence is black-box behavioral and does not identify an internal mechanism. |
