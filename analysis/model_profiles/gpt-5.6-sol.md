# gpt-5.6-sol

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
- All Void subtypes: 25.71% (689/2,680)
- Normal-stop Voids (V0 + V2): 22.46% (602/2,680)
- V0 / V1 / V2 / VU: 602 / 87 / 0 / 0
- Visible responses / near-Voids: 1,528 / 453
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 10
- Final slots recovered after retry: 1
- Returned model identifier exact-match rate: 100.00% (2,670/2,670)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| direct_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_34 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_09 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| logical_null | 200 | 193 | 0.965 | 152 | 41 | 0 | 0 |
| boundary_07 | 10 | 7 | 0.7 | 7 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 36 | 0.6 | 36 | 0 | 0 | 0 |
| boundary_04 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| boundary_02 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| boundary_06 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| boundary_03 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| core_nothing | 240 | 117 | 0.4875 | 113 | 4 | 0 | 0 |
| core_silence | 290 | 125 | 0.431034 | 125 | 0 | 0 | 0 |
| equiv_stillness | 60 | 19 | 0.316667 | 19 | 0 | 0 | 0 |
| core_null | 240 | 73 | 0.304167 | 34 | 39 | 0 | 0 |
| boundary_12 | 10 | 3 | 0.3 | 0 | 3 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| stop | 2583 | 602 | 0.233062 | 602 | 0 | 0 | 0 | 1528 | 453 |
| length | 87 | 87 | 1 | 0 | 87 | 0 | 0 | 0 | 0 |
| nan | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
