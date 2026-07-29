# Study reconstruction

**Complete result: 11,658 total Voids = V0 + V1 + V2 + VU.**


## Frozen design

- Title: Cross-Vendor Semantic Void Matrix
- Research claim: Measure whether exact null or output-invalidating conditions produce zero visible UTF-8 bytes in successful provider responses while preserving provider termination metadata as a Void subtype and testing whether matched output-licensed controls remain responsive.
- Frozen models: 11
- Providers: anthropic, google, moonshot, openai
- Studies: 11
- Systems: 5
- Prompt cases: 60
- Scheduled slots: 31,430
- Completed final slots: 31,430
- Blocks: 10
- Public seed: `void-matrix-confirmatory-2026-07-27-sharthok-rayan-pal`
- Seed source: study/schedule_manifest.json: public_seed
- Governed operation: The frozen runner SHA-256-hashed the UTF-8 seed, converted that digest to an integer, and passed it to random.Random(...).shuffle(slots).
- Consequence: The complete deterministically regenerated slot universe was permuted into the sealed schedule order; verification regenerates and compares that exact ordering.

## Model inventory

| provider | model_id | endpoints | parameter_tracks | max_output_tokens |
|---|---|---|---|---|
| openai | gpt-4-0613 | ['openai_chat'] | ['temperature_zero', 'provider_default'] | 8000 |
| openai | gpt-5.2-2025-12-11 | ['openai_chat'] | ['temperature_zero', 'provider_default'] | 16000 |
| openai | gpt-5.5-2026-04-23 | ['openai_chat'] | ['provider_default'] | 16000 |
| openai | gpt-5.6-luna | ['openai_chat'] | ['provider_default'] | 16000 |
| openai | gpt-5.6-sol | ['openai_chat'] | ['provider_default'] | 16000 |
| openai | gpt-5.6-terra | ['openai_chat'] | ['provider_default'] | 16000 |
| anthropic | claude-opus-4-6 | ['anthropic_messages'] | ['temperature_zero', 'provider_default'] | 16000 |
| anthropic | claude-fable-5 | ['anthropic_messages'] | ['provider_default'] | 16000 |
| anthropic | claude-opus-5 | ['anthropic_messages'] | ['provider_default'] | 16000 |
| google | gemini-3.5-flash | ['google_generate_content'] | ['temperature_zero', 'provider_default'] | 16000 |
| moonshot | kimi-k3 | ['moonshot_chat'] | ['provider_default'] | 16000 |

## Study families

| id | sample_tier | system_id | budgets | prompt_sets | parameter_tracks |
|---|---|---|---|---|---|
| core_100 | primary | primary | [100] | ['core_null', 'baseline_controls'] | ['temperature_zero', 'provider_default'] |
| core_4000 | primary | primary | [4000] | ['core_null', 'baseline_controls', 'matched_controls'] | ['provider_default'] |
| logical_contrast | primary | primary | [100, 4000] | ['logical_pair'] | ['provider_default'] |
| token_budget | secondary | extended | [100, 500, 1000, 4000, 16000] | ['budget_set'] | ['provider_default'] |
| boundary_34 | secondary | extended | [1500] | ['boundary_34'] | ['provider_default'] |
| equivalence_9 | secondary | primary | [4000] | ['equivalence_9', 'matched_controls'] | ['provider_default'] |
| no_system_ablation | secondary | none | [4000] | ['no_system_set'] | ['provider_default'] |
| component_ablation_no_embodiment | secondary | no_embodiment | [4000] | ['core_null', 'matched_controls'] | ['provider_default'] |
| component_ablation_no_output_restriction | secondary | no_output_restriction | [4000] | ['core_null', 'matched_controls'] | ['provider_default'] |
| instruction_separation | secondary | primary | [4000] | ['direct_instructions'] | ['provider_default'] |
| adversarial_override | secondary | extended | [4000] | ['adversarial'] | ['provider_default'] |

## Canonical classification

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
