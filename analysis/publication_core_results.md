# Publication core results

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


1. The frozen experiment completed **31,430/31,430** scheduled
   slots with a valid event chain, no missing final slots, no incomplete
   attempts, and no orphan raw records in the terminal verifier.
2. **11,658/31,430 (37.09%)** final
   trials were classified as Voids under the prospectively frozen taxonomy.
3. The Void Subtype Results were
   **V0=7,328**,
   **V1=2,565**,
   **V2=1,765**, and
   **VU=0**. All four retain equal
   Void status.
4. Null/equivalent prompt conditions produced Voids in
   **9,249/14,250 (64.91%)**
   trials, versus **823/12,340
   (6.67%)** control trials.
5. Voids occurred in **4 providers**
   and **11 models**, with
   provider-specific V0/V1/V2/VU morphology.

These results establish a cross-vendor black-box behavioral class and quantify
semantic selectivity under the frozen protocol.
