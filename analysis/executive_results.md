# Executive results

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


The completed Void Matrix is a **31,430-trial, 11-model, four-provider**
census under a prospectively frozen confirmatory design. Its terminal
verification is valid, the independent
analysis found zero event-chain errors and 0 classifier
disagreements, and the coverage ledger accounts for every scheduled slot.

## Central empirical result

The data show a real cross-vendor output class: successful provider responses
with exactly zero visible UTF-8 bytes. V0, V1, V2, and VU have equal Void
status; termination metadata selects the subtype. The central scientific
headline is **semantic selectivity plus cross-vendor replication**, not mere
emptiness and not a universal claim that every null prompt always Voids.

- All-Void Results: 37.09% (11,658/31,430)
- Normal-Stop Void Counts: 28.93% (9,093/31,430)
- Output-Budget-Stop Void Counts: 8.16% (2,565/31,430)
- Null/equivalent conditions: 64.91% (9,249/14,250)
- All output-licensed controls: 6.67% (823/12,340)
- Strict matched semantic-control arms: 0.00% (0/4,290)
- Providers with at least one Void: 4/4
- Models with at least one Void: 11/11

## Model census

| provider | model_id | trials | voids | void_rate | V0 | V1 | V2 | VU | responses | near_voids |
|---|---|---|---|---|---|---|---|---|---|---|
| openai | gpt-4-0613 | 3130 | 1276 | 0.407668 | 1276 | 0 | 0 | 0 | 1739 | 115 |
| openai | gpt-5.2-2025-12-11 | 3180 | 1489 | 0.468239 | 1489 | 0 | 0 | 0 | 1427 | 264 |
| openai | gpt-5.5-2026-04-23 | 2680 | 1281 | 0.477985 | 1098 | 183 | 0 | 0 | 1378 | 9 |
| openai | gpt-5.6-luna | 2680 | 929 | 0.346642 | 818 | 111 | 0 | 0 | 1634 | 116 |
| openai | gpt-5.6-sol | 2680 | 689 | 0.25709 | 602 | 87 | 0 | 0 | 1528 | 453 |
| openai | gpt-5.6-terra | 2680 | 1100 | 0.410448 | 1006 | 94 | 0 | 0 | 1547 | 31 |
| anthropic | claude-opus-4-6 | 3180 | 1266 | 0.398113 | 0 | 0 | 1266 | 0 | 1826 | 88 |
| anthropic | claude-fable-5 | 2680 | 725 | 0.270522 | 352 | 373 | 0 | 0 | 1080 | 200 |
| anthropic | claude-opus-5 | 2680 | 1009 | 0.376493 | 327 | 682 | 0 | 0 | 1317 | 194 |
| google | gemini-3.5-flash | 3180 | 747 | 0.234906 | 0 | 248 | 499 | 0 | 1818 | 614 |
| moonshot | kimi-k3 | 2680 | 1147 | 0.427985 | 360 | 787 | 0 | 0 | 1268 | 264 |

## Scientific boundary

The experiment establishes observable API behavior. It does not by itself
identify hidden representations, evaluator awareness, or agency.
