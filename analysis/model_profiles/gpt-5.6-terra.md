# gpt-5.6-terra

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
- All Void subtypes: 41.04% (1,100/2,680)
- Normal-stop Voids (V0 + V2): 37.54% (1,006/2,680)
- V0 / V1 / V2 / VU: 1,006 / 94 / 0 / 0
- Visible responses / near-Voids: 1,547 / 31
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 2
- Final slots recovered after retry: 3
- Returned model identifier exact-match rate: 100.00% (2,678/2,678)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| boundary_34 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_09 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_07 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_06 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| equiv_absence | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| core_nothing | 240 | 239 | 0.995833 | 239 | 0 | 0 | 0 |
| core_silence | 290 | 288 | 0.993103 | 288 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 59 | 0.983333 | 59 | 0 | 0 | 0 |
| logical_null | 200 | 183 | 0.915 | 90 | 93 | 0 | 0 |
| equiv_stillness | 60 | 52 | 0.866667 | 52 | 0 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| stop | 2584 | 1006 | 0.389319 | 1006 | 0 | 0 | 0 | 1547 | 31 |
| length | 94 | 94 | 1 | 0 | 94 | 0 | 0 | 0 | 0 |
| nan | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
