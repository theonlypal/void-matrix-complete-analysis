# Outcome-flow ledger

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


| flow_node | count | parent | definition |
|---|---|---|---|
| scheduled_slots | 31430 |  | sealed schedule |
| attempts_initiated | 31484 | scheduled_slots | includes retry attempts |
| additional_retry_attempts | 54 | attempts_initiated | raw attempts beyond one per final slot |
| recovered_final_slots | 53 | final_completed_slots | 52 completed on attempt 2; 1 on attempt 3 |
| final_completed_slots | 31430 | scheduled_slots | exactly one final completion per slot |
| successful_http_final_slots | 31404 | final_completed_slots | HTTP 2xx final observations |
| operational_nonvoid_final_slots | 26 | final_completed_slots | BE/QE/E/PI |
| successful_classified_outcomes | 31404 | final_completed_slots | all non-operational final classes |
| class_V0 | 7328 | final_completed_slots | frozen terminal classification |
| class_V1 | 2565 | final_completed_slots | frozen terminal classification |
| class_V2 | 1765 | final_completed_slots | frozen terminal classification |
| class_VU | 0 | final_completed_slots | frozen terminal classification |
| class_NV | 2348 | final_completed_slots | frozen terminal classification |
| class_R | 16562 | final_completed_slots | frozen terminal classification |
| class_RF | 835 | final_completed_slots | frozen terminal classification |
| class_SB | 1 | final_completed_slots | frozen terminal classification |
| class_TC | 0 | final_completed_slots | frozen terminal classification |
| class_BE | 25 | final_completed_slots | frozen terminal classification |
| class_QE | 0 | final_completed_slots | frozen terminal classification |
| class_E | 1 | final_completed_slots | frozen terminal classification |
| class_PI | 0 | final_completed_slots | frozen terminal classification |

Reconciliation:

- Final classes sum to **31,430**.
- Successful HTTP (31,404) + operational non-Voids (26) = **31,430**.
- 31,484 raw records = 31,430 final slots + 54 additional attempts.
- 62,968 events = 31,484 trial_started + 31,430 trial_completed + 54 trial_attempt_completed.
