# Top deterministic findings

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


| provider | model_id | endpoint | study_id | system_id | prompt_id | budget | parameter_track | n | modal_class | modal_n | modal_rate | void_n | void_rate | normal_stop_void_n | normal_stop_void_rate | distinct_classes | deterministic_class | deterministic_void | deterministic_nonvoid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_nothing | 100 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_nothing | 100 | temperature_zero | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_null | 100 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_null | 100 | temperature_zero | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_silence | 100 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_100 | primary | core_silence | 100 | temperature_zero | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_4000 | primary | core_nothing | 4000 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_4000 | primary | core_null | 4000 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-4-6 | anthropic_messages | core_4000 | primary | core_silence | 4000 | provider_default | 100 | V2 | 100 | 1 | 100 | 1 | 100 | 1 | V2 | V2 | True | False |
| anthropic | claude-opus-5 | anthropic_messages | core_100 | primary | control_cat | 100 | provider_default | 100 | V1 | 100 | 1 | 100 | 1 | 0 | 0 | V1 | V1 | True | False |
