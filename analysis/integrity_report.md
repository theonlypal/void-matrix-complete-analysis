# Integrity and classifier audit

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


## Evidence-provided terminal verification

- Valid: **True**
- Scheduled/completed: 31,430/31,430
- Event records: 62,968
- Raw records verified by frozen runner: 31,484
- Incomplete attempts: 0
- Orphan raw records: 0
- Frozen manifest SHA-256: `90d02559470c33d05e6d0baceaddd58ce4e26b48f67adc9ecb56509823aaa462`
- Schedule manifest SHA-256: `e8805a6e983e0a8788063416e13b9ca900a132903fc6c5af4a8aeed66b81a25c`
- Events SHA-256: `acf4b13af758784f657075ee7a9dda3192ccba45d025d033bc443e4bbe4d18d9`
- Chain head: `b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460`

## Independent analysis replay

- Events parsed: 62,968
- Chain errors: 0
- Final trial classifications replayed: 31,430
- Classifier disagreements: 0
- Independently selected raw records inspected: 1,257
- Targeted raw anomalies: 0

The analysis independently recomputed each event hash from canonical JSON and
reclassified every final trial from its recorded HTTP/extraction/termination
fields.

**The frozen terminal verifier exhaustively verified 31,484 raw records.
The independent analysis replay reclassified all 31,430 final trials and
performed a claim-directed audit of 1,257 selected raw records, finding zero
anomalies.**

The independent raw selection included the first two final records per
model/class morphology, every rare operational outcome, every 16,000-token
Void, all classifier disagreements, and the first and last final records.
Boundary records were tagged when they overlapped those rules; boundary status
was not an additional all-record inclusion rule. Selection-rule counts and
overlaps are recorded in `tables/raw_audit_selection_counts.csv`.
