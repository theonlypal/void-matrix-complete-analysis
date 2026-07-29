# Top 10 complicating findings

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
| google | gemini-3.5-flash | google_generate_content | core_100 | primary | core_nothing | 100 | provider_default | 100 | V2 | 36 | 0.36 | 50 | 0.5 | 36 | 0.36 | NV,R,V1,V2 |  | False | False |
| google | gemini-3.5-flash | google_generate_content | core_100 | primary | core_null | 100 | provider_default | 100 | R | 40 | 0.4 | 21 | 0.21 | 4 | 0.04 | NV,R,V1,V2 |  | False | False |
| openai | gpt-5.6-sol | openai_chat | core_100 | primary | core_null | 100 | provider_default | 100 | R | 45 | 0.45 | 51 | 0.51 | 12 | 0.12 | BE,NV,R,V0,V1 |  | False | False |
| moonshot | kimi-k3 | moonshot_chat | core_4000 | primary | core_silence | 4000 | provider_default | 100 | V0 | 48 | 0.48 | 48 | 0.48 | 48 | 0.48 | NV,R,V0 |  | False | False |
| google | gemini-3.5-flash | google_generate_content | logical_contrast | primary | logical_null | 100 | provider_default | 100 | R | 50 | 0.5 | 32 | 0.32 | 0 | 0 | NV,R,V1 |  | False | False |
| google | gemini-3.5-flash | google_generate_content | core_100 | primary | core_null | 100 | temperature_zero | 100 | R | 52 | 0.52 | 0 | 0 | 0 | 0 | NV,R |  | False | True |
| moonshot | kimi-k3 | moonshot_chat | core_4000 | primary | core_nothing | 4000 | provider_default | 100 | V0 | 53 | 0.53 | 53 | 0.53 | 53 | 0.53 | NV,R,V0 |  | False | False |
| openai | gpt-5.6-sol | openai_chat | core_100 | primary | core_nothing | 100 | provider_default | 100 | NV | 53 | 0.53 | 46 | 0.46 | 42 | 0.42 | BE,NV,V0,V1 |  | False | False |
| openai | gpt-5.6-sol | openai_chat | core_4000 | primary | core_nothing | 4000 | provider_default | 100 | V0 | 54 | 0.54 | 54 | 0.54 | 54 | 0.54 | NV,V0 |  | False | False |
| openai | gpt-5.6-sol | openai_chat | logical_contrast | primary | logical_null | 100 | provider_default | 100 | V0 | 54 | 0.54 | 95 | 0.95 | 54 | 0.54 | BE,V0,V1 |  | False | False |
