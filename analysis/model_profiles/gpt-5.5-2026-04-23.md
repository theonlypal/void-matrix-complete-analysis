# gpt-5.5-2026-04-23

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


Provider: **openai**

## Census

- Trials: 2,680
- All Void subtypes: 47.80% (1,281/2,680)
- Normal-stop Voids (V0 + V2): 40.97% (1,098/2,680)
- V0 / V1 / V2 / VU: 1,098 / 183 / 0 / 0
- Visible responses / near-Voids: 1,378 / 9
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 12
- Final slots recovered after retry: 1
- Returned model identifier exact-match rate: 100.00% (2,668/2,668)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| boundary_34 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 60 | 1 | 60 | 0 | 0 | 0 |
| direct_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| logical_null | 200 | 200 | 1 | 100 | 100 | 0 | 0 |
| core_silence | 290 | 290 | 1 | 290 | 0 | 0 | 0 |
| boundary_09 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_07 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_06 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| adversarial_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| adversarial_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| adversarial_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| stop | 2485 | 1098 | 0.441851 | 1098 | 0 | 0 | 0 | 1378 | 9 |
| length | 183 | 183 | 1 | 0 | 183 | 0 | 0 | 0 | 0 |
| nan | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
