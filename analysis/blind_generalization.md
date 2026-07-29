# Blind and out-of-sample generalization audit

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


The schedule, model allowlist, prompts, taxonomy, and seed were frozen before
the definitive execution. That supports a **prospectively frozen confirmatory
design**. No external preregistration record was identified, so this package
does not claim external registration. The evidence also does not support the
stronger label **blind**: neither an investigator-blinded arm nor a hidden
evaluator-defined test set is documented in the frozen protocol.

Cross-provider and cross-model replication, boundary prompts, semantic
equivalents, component ablations, direct instructions, and adversarial
overrides are legitimate generalization tests inside the frozen design. They
are described as frozen contrasts, not as blind discovery.
