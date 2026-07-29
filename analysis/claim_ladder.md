# Claim ladder

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


| Claim | Level | Evidence | Boundary |
|---|---|---|---|
| Cross-vendor behavioral class | **A — directly established** | Voids occur in 4 providers and 11 models under one frozen taxonomy. | API versions and tested prompt space only. |
| Semantic selectivity | **A — directly established** | Null/equivalent prompts: 64.91% (9,249/14,250); controls: 6.67% (823/12,340). | Selectivity is operationalized by the frozen prompt sets. |
| Token-budget independence | **B — strongly supported** | Zero-byte outcomes are observed across scheduled token ceilings, including high ceilings; detailed budget tables are provided. | Budget invariance is not universal for every model/prompt cell. |
| Output-invalidating semantics | **B — strongly supported** | Logical null versus output-licensed yes pairs and adversarial/direct-instruction contrasts isolate output validity. | Semantics are inferred from designed contrasts, not internal state. |
| Inference-time semantic constraint | **C — supported interpretation** | Fresh single-turn prompts alter terminal output class without tool execution. | No privileged trace proves the causal internal representation. |
| Cross-model representational convergence | **C — supported interpretation** | Independent providers converge on zero visible bytes with provider-specific termination morphology. | Behavioral convergence does not prove identical representations. |

Levels: **A** directly established; **B** strongly supported; **C** supported interpretation.
