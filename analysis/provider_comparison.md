# Provider comparison

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


| provider | total | V0 | V1 | V2 | VU | NV | R | RF | SB | TC | BE | QE | E | PI | void_total | normal_stop_void_total | budget_stop_void_total | void_rate | normal_stop_void_rate | successful_http |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| moonshot | 2680 | 360 | 787 | 0 | 0 | 264 | 1268 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1147 | 360 | 787 | 0.427985 | 0.134328 | 2679 |
| openai | 17030 | 6289 | 475 | 0 | 0 | 988 | 9253 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 6764 | 6289 | 475 | 0.397181 | 0.369289 | 17005 |
| anthropic | 8540 | 679 | 1055 | 1266 | 0 | 482 | 4223 | 835 | 0 | 0 | 0 | 0 | 0 | 0 | 3000 | 1945 | 1055 | 0.351288 | 0.227752 | 8540 |
| google | 3180 | 0 | 248 | 499 | 0 | 614 | 1818 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 747 | 499 | 248 | 0.234906 | 0.156918 | 3180 |
