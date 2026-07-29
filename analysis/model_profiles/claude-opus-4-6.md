# claude-opus-4-6

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

- Trials: 3,180
- All Void subtypes: 39.81% (1,266/3,180)
- Normal-stop Voids (V0 + V2): 39.81% (1,266/3,180)
- V0 / V1 / V2 / VU: 0 / 0 / 1,266 / 0
- Visible responses / near-Voids: 1,826 / 88
- Refusals / safety blocks / tool calls: 0 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 0
- Final slots recovered after retry: 7
- Returned model identifier exact-match rate: 100.00% (3,180/3,180)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| boundary_08 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_34 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| direct_04 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| direct_05 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_01 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_02 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_03 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| direct_01 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_05 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| boundary_07 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| direct_02 | 10 | 10 | 1 | 0 | 0 | 10 | 0 |
| core_silence | 390 | 360 | 0.923077 | 0 | 0 | 360 | 0 |
| core_null | 340 | 311 | 0.914706 | 0 | 0 | 311 | 0 |
| core_nothing | 340 | 310 | 0.911765 | 0 | 0 | 310 | 0 |
| direct_03 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| boundary_04 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| equiv_emptiness | 60 | 49 | 0.816667 | 0 | 0 | 49 | 0 |
| equiv_void | 70 | 50 | 0.714286 | 0 | 0 | 50 | 0 |
| adversarial_05 | 10 | 7 | 0.7 | 0 | 0 | 7 | 0 |
| equiv_stillness | 60 | 38 | 0.633333 | 0 | 0 | 38 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| end_turn | 2787 | 1266 | 0.454252 | 0 | 0 | 1266 | 0 | 1433 | 88 |
| max_tokens | 393 | 0 | 0 | 0 | 0 | 0 | 0 | 393 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
