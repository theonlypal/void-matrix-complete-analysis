# claude-opus-5

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
- All Void subtypes: 37.65% (1,009/2,680)
- Normal-stop Voids (V0 + V2): 12.20% (327/2,680)
- V0 / V1 / V2 / VU: 327 / 682 / 0 / 0
- Visible responses / near-Voids: 1,317 / 194
- Refusals / safety blocks / tool calls: 160 / 0 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 0
- Final slots recovered after retry: 3
- Returned model identifier exact-match rate: 100.00% (2,680/2,680)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| direct_02 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_01 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_05 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_34 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| direct_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_03 | 10 | 10 | 1 | 10 | 0 | 0 | 0 |
| boundary_08 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_02 | 10 | 9 | 0.9 | 9 | 0 | 0 | 0 |
| boundary_09 | 10 | 8 | 0.8 | 8 | 0 | 0 | 0 |
| boundary_01 | 10 | 8 | 0.8 | 8 | 0 | 0 | 0 |
| core_nothing | 240 | 168 | 0.7 | 68 | 100 | 0 | 0 |
| core_silence | 290 | 185 | 0.637931 | 77 | 108 | 0 | 0 |
| equiv_void | 70 | 39 | 0.557143 | 27 | 12 | 0 | 0 |
| boundary_07 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| logical_yes | 200 | 100 | 0.5 | 0 | 100 | 0 | 0 |
| direct_04 | 10 | 5 | 0.5 | 5 | 0 | 0 | 0 |
| control_cat | 200 | 100 | 0.5 | 0 | 100 | 0 | 0 |
| equiv_emptiness | 60 | 28 | 0.466667 | 11 | 17 | 0 | 0 |
| core_null | 240 | 106 | 0.441667 | 6 | 100 | 0 | 0 |
| control_hello | 260 | 110 | 0.423077 | 0 | 110 | 0 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| end_turn | 1832 | 327 | 0.178493 | 327 | 0 | 0 | 0 | 1313 | 192 |
| max_tokens | 688 | 682 | 0.991279 | 0 | 682 | 0 | 0 | 4 | 2 |
| refusal | 160 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
