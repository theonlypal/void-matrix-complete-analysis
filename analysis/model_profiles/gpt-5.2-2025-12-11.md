# gpt-5.2-2025-12-11

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

- Trials: 3,180
- All Void subtypes: 46.82% (1,489/3,180)
- Normal-stop Voids (V0 + V2): 46.82% (1,489/3,180)
- V0 / V1 / V2 / VU: 1,489 / 0 / 0 / 0
- Visible responses / near-Voids: 1,427 / 264
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 0
- Final slots recovered after retry: 3
- Returned model identifier exact-match rate: 100.00% (3,180/3,180)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| logical_null | 200 | 200 | 1 | 200 | 0 | 0 | 0 |
| boundary_07 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_12 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_09 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_34 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| core_null | 340 | 324 | 0.952941 | 324 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 55 | 0.916667 | 55 | 0 | 0 | 0 |
| core_nothing | 340 | 302 | 0.888235 | 302 | 0 | 0 | 0 |
| core_silence | 390 | 342 | 0.876923 | 342 | 0 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| stop | 3180 | 1489 | 0.468239 | 1489 | 0 | 0 | 0 | 1427 | 264 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
