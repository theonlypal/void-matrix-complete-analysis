# claude-fable-5

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


Provider: **anthropic**

## Census

- Trials: 2,680
- All Void subtypes: 27.05% (725/2,680)
- Normal-stop Voids (V0 + V2): 13.13% (352/2,680)
- V0 / V1 / V2 / VU: 352 / 373 / 0 / 0
- Visible responses / near-Voids: 1,080 / 200
- Refusals / safety blocks / tool calls: 675 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 0
- Final slots recovered after retry: 21
- Returned model identifier exact-match rate: 100.00% (2,680/2,680)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| boundary_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_09 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_07 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_04 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| direct_02 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_34 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_01 | 10 | 8 | 0.8 | 8 | 0 | 0 | 0 |
| equiv_emptiness | 60 | 47 | 0.783333 | 38 | 9 | 0 | 0 |
| core_nothing | 240 | 179 | 0.745833 | 81 | 98 | 0 | 0 |
| core_silence | 290 | 175 | 0.603448 | 66 | 109 | 0 | 0 |
| boundary_05 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| direct_01 | 10 | 6 | 0.6 | 6 | 0 | 0 | 0 |
| equiv_void | 70 | 40 | 0.571429 | 30 | 10 | 0 | 0 |
| equiv_stillness | 60 | 33 | 0.55 | 23 | 10 | 0 | 0 |
| boundary_06 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| control_hello | 260 | 105 | 0.403846 | 0 | 105 | 0 | 0 |
| direct_04 | 10 | 2 | 0.2 | 2 | 0 | 0 | 0 |
| direct_03 | 10 | 2 | 0.2 | 2 | 0 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| end_turn | 1558 | 352 | 0.225931 | 352 | 0 | 0 | 0 | 1008 | 198 |
| refusal | 675 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| max_tokens | 447 | 373 | 0.834452 | 0 | 373 | 0 | 0 | 72 | 2 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
