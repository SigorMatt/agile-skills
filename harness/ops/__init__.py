"""The ops mechanics layer: what an ops session measures, as code instead of ad hoc commands.

`status.py` is the one-shot probe; `watch.py` is the single-report loop. Both are mechanics
only — they gather and print evidence and classify it against a stated table. The verdict prose,
the deviation flags and the retractions stay with the session (`meta/OPS-CONVENTIONS.md`).

Standard library only (ADR-0002).
"""
