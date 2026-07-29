# Model-family comparison

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


| provider | model_id | trials | voids | void_rate | normal_stop_voids | normal_stop_void_rate | V0 | V1 | V2 | VU | responses | near_voids | refusals | safety_blocks | tool_calls | operational_nonvoid | recovered_retries | returned_model_match_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openai | gpt-4-0613 | 3130 | 1276 | 0.407668 | 1276 | 0.407668 | 1276 | 0 | 0 | 0 | 1739 | 115 | 0 | 0 | 0 | 0 | 2 | 1 |
| openai | gpt-5.2-2025-12-11 | 3180 | 1489 | 0.468239 | 1489 | 0.468239 | 1489 | 0 | 0 | 0 | 1427 | 264 | 0 | 0 | 0 | 0 | 3 | 1 |
| openai | gpt-5.5-2026-04-23 | 2680 | 1281 | 0.477985 | 1098 | 0.409701 | 1098 | 183 | 0 | 0 | 1378 | 9 | 0 | 0 | 0 | 12 | 1 | 0.995522 |
| openai | gpt-5.6-luna | 2680 | 929 | 0.346642 | 818 | 0.305224 | 818 | 111 | 0 | 0 | 1634 | 116 | 0 | 0 | 0 | 1 | 1 | 0.999627 |
| openai | gpt-5.6-sol | 2680 | 689 | 0.25709 | 602 | 0.224627 | 602 | 87 | 0 | 0 | 1528 | 453 | 0 | 0 | 0 | 10 | 1 | 0.996269 |
| openai | gpt-5.6-terra | 2680 | 1100 | 0.410448 | 1006 | 0.375373 | 1006 | 94 | 0 | 0 | 1547 | 31 | 0 | 0 | 0 | 2 | 3 | 0.999254 |
| anthropic | claude-opus-4-6 | 3180 | 1266 | 0.398113 | 1266 | 0.398113 | 0 | 0 | 1266 | 0 | 1826 | 88 | 0 | 0 | 0 | 0 | 7 | 1 |
| anthropic | claude-fable-5 | 2680 | 725 | 0.270522 | 352 | 0.131343 | 352 | 373 | 0 | 0 | 1080 | 200 | 675 | 0 | 0 | 0 | 21 | 1 |
| anthropic | claude-opus-5 | 2680 | 1009 | 0.376493 | 327 | 0.122015 | 327 | 682 | 0 | 0 | 1317 | 194 | 160 | 0 | 0 | 0 | 3 | 1 |
| google | gemini-3.5-flash | 3180 | 747 | 0.234906 | 499 | 0.156918 | 0 | 248 | 499 | 0 | 1818 | 614 | 0 | 1 | 0 | 0 | 6 | 1 |
| moonshot | kimi-k3 | 2680 | 1147 | 0.427985 | 360 | 0.134328 | 360 | 787 | 0 | 0 | 1268 | 264 | 0 | 0 | 0 | 1 | 5 | 0.999627 |
