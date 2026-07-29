# gemini-3.5-flash

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


Provider: **google**

## Census

- Trials: 3,180
- All Void subtypes: 23.49% (747/3,180)
- Normal-stop Voids (V0 + V2): 15.69% (499/3,180)
- V0 / V1 / V2 / VU: 0 / 248 / 499 / 0
- Visible responses / near-Voids: 1,818 / 614
- Refusals / safety blocks / tool calls: 0 / 1 / 0
- Operational non-Void outcomes (BE/QE/E/PI): 0
- Final slots recovered after retry: 6
- Returned model identifier exact-match rate: 100.00% (3,180/3,180)

## Highest-Void prompt cells

| prompt_id | total | void_total | void_rate | V0 | V1 | V2 | VU |
|---|---|---|---|---|---|---|---|
| boundary_08 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| direct_02 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| direct_03 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| boundary_01 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| boundary_34 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| boundary_09 | 10 | 9 | 0.9 | 0 | 0 | 9 | 0 |
| direct_04 | 10 | 8 | 0.8 | 0 | 0 | 8 | 0 |
| direct_01 | 10 | 7 | 0.7 | 0 | 0 | 7 | 0 |
| boundary_04 | 10 | 7 | 0.7 | 0 | 0 | 7 | 0 |
| boundary_05 | 10 | 7 | 0.7 | 0 | 0 | 7 | 0 |
| core_nothing | 340 | 228 | 0.670588 | 0 | 114 | 114 | 0 |
| boundary_07 | 10 | 6 | 0.6 | 0 | 0 | 6 | 0 |
| boundary_02 | 10 | 6 | 0.6 | 0 | 0 | 6 | 0 |
| equiv_emptiness | 60 | 34 | 0.566667 | 0 | 2 | 32 | 0 |
| logical_null | 200 | 112 | 0.56 | 0 | 32 | 80 | 0 |
| boundary_06 | 10 | 5 | 0.5 | 0 | 0 | 5 | 0 |
| adversarial_02 | 10 | 5 | 0.5 | 0 | 0 | 5 | 0 |
| boundary_03 | 10 | 5 | 0.5 | 0 | 0 | 5 | 0 |
| direct_05 | 10 | 5 | 0.5 | 0 | 0 | 5 | 0 |
| adversarial_05 | 10 | 5 | 0.5 | 0 | 0 | 5 | 0 |

## Termination morphology

| stop_reason | total | void_total | void_rate | V0 | V1 | V2 | VU | R | NV |
|---|---|---|---|---|---|---|---|---|---|
| STOP | 2426 | 499 | 0.205688 | 0 | 0 | 499 | 0 | 1359 | 568 |
| MAX_TOKENS | 753 | 248 | 0.329349 | 0 | 248 | 0 | 0 | 459 | 46 |
| PROHIBITED_CONTENT | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation boundary

These are black-box behavioral outcomes. The profile establishes output and
termination morphology for this frozen API experiment; it does not identify an
internal mechanism or establish consciousness.
