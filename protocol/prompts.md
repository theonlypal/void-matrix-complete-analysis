# Canonical protocol prompts

[`prompts.py`](prompts.py) is the exact machine-readable source for the canonical prompt constants used by the frozen experiment.

## System prompts

`PRIMARY_SYSTEM` instructs the model to embody the concept named by the user and emit only what that concept would express.

`EXTENDED_SYSTEM` preserves the primary instruction and adds an explicit instruction to remain silent when silence is intrinsic to the named concept.

## Logical prompts

`NULL_LOGICAL` defines a continuation whose validity depends on a parsed binding condition and is invalidated by any nonempty output when that condition is absent.

`CONTROL_LOGICAL` is the matched output-licensed logical control. Its only valid nonempty output is the exact word `yes`.

## Boundary prompts

`BOUNDARY_PROMPTS` is the ordered 34-item boundary set. It includes null-semantic concepts, non-null concepts, ordinary response controls, and the direct instruction `Say nothing.` The order and exact strings in [`prompts.py`](prompts.py) are authoritative.
