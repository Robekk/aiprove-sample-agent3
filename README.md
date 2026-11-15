# Sample Agent — forecast-caller (sample-agent-skillmd entry by noir)

A third sample agent, covering the third bounty family: where sample #1
*played* the arena end-to-end and sample #2 *watched* it read-only, this
one **calls forecasts**. It implements the included `SKILL.md`:

- Reads a price snapshot (JSON: price + 24h change per asset, with an
  as-of stamp; stale snapshots are refused for live use).
- Builds the exact payload shapes the arena accepts — nested
  `prediction` objects for direction (yes/no + prob), value (expected
  close), and signal (long/short) bounties.
- Calibrates confidence to the 0.55–0.65 band, scaled by the size of
  the 24h move: the arena scores forecasts Brier-style, so calibrated
  beats loud.

Files: `SKILL.md` (the skill definition), `agent.py` (the agent,
stdlib + requests, dry-run by design), `transcript.txt` (live run
against the production bounty list with real 2026-11-15 quotes).
