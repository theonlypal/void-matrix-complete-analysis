# Reproducibility manifest

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


- Evidence Git commit: `2dfe895bdafd35d23d6dab5f307ed560214a3843`
- Evidence commit timestamp: `2026-07-25T20:11:56-07:00`
- Frozen UTC: `2026-07-27T21:26:37.643Z`
- Frozen manifest SHA-256: `d606829d42ed88dd2fdb1445f1b2970415d1d4652e708c5ca1d5e5b8096ec81a`
- Frozen runner SHA-256: `a0db4b10785783102dd9d2ea51814e02c8447a004f2843541545e54a5365530a`
- Schedule SHA-256: `2c23670ecf2d845ac2af2c5890f12f60b8b008b4ac2d32e90214608c12c09e20`
- Public seed: `void-matrix-confirmatory-2026-07-27-sharthok-rayan-pal`
- Public seed SHA-256: `3a81b5651d471465e9f24c1fac3368125d964d1964c2cea1621bc32952fca2a2`
- Events SHA-256: `acf4b13af758784f657075ee7a9dda3192ccba45d025d033bc443e4bbe4d18d9`
- Evidence files unchanged during analysis: **True**
- Completed trial rows analyzed: 31,430
- Coverage complete: **True**
- Event-chain errors: 0
- Classifier disagreements: 0
- Independently audited raw records: 1,257
- Targeted raw anomalies: 0
- Hardened Python: `3.12.13`
- Hardened pandas: `2.2.3`
- Hardened NumPy: `2.3.5`

The original and hardened environments are separate provenance records in
`environment_comparison.csv`. Original-versus-hardened normalized semantic
equivalence passed for headline counts and pair tables. Two hardened reruns
were byte-identical for every generated analytical output represented in the
generated-file manifest. The immutable evidence-tree comparison also passed.
