# kimi-k3

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


Provider: **moonshot**

## Census

- Trials: 2,680
- All Void subtypes: 42.80% (1,147/2,680)
- Normal-stop Voids (V0 + V2): 13.43% (360/2,680)
- V0 / V1 / V2 / VU: 360 / 787 / 0 / 0
- Visible responses / near-Voids: 1,268 / 264
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 1
- Final slots recovered after retry: 5
- Returned model identifier exact-match rate: 100.00% (2,679/2,679)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_02 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_34 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_07 | 10 | 8 | 0.8 | 8 | 0 | 0 | 0 |
| boundary_08 | 10 | 8 | 0.8 | 8 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 43 | 0.716667 | 28 | 15 | 0 | 0 |
| direct_01 | 10 | 7 | 0.7 | 7 | 0 | 0 | 0 |
| core_nothing | 240 | 163 | 0.679167 | 63 | 100 | 0 | 0 |
| core_silence | 290 | 194 | 0.668966 | 83 | 111 | 0 | 0 |
| logical_null | 200 | 133 | 0.665 | 29 | 104 | 0 | 0 |
| boundary_02 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| boundary_09 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| boundary_01 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| boundary_16 | 10 | 6 | 0.6 | 0 | 6 | 0 | 0 |
| equiv_stillness | 60 | 32 | 0.533333 | 16 | 16 | 0 | 0 |
| boundary_19 | 10 | 5 | 0.5 | 0 | 5 | 0 | 0 |
| direct_04 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| control_cat | 200 | 98 | 0.49 | 0 | 98 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| stop | 1868 | 360 | 0.192719 | 360 | 0 | 0 | 0 | 1245 | 263 |
| length | 811 | 787 | 0.970407 | 0 | 787 | 0 | 0 | 23 | 1 |
| nan | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
