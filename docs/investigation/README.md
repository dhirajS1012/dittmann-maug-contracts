# Investigation History

This folder tracks investigations into replication discrepancies, organized chronologically.

## Format

Each file follows this structure:
- **Date** and **hypothesis** being tested
- **Method** — what was checked or changed
- **Results** — before/after metrics from the 10% tolerance pytest
- **Conclusion** — data revision, code bug, or inconclusive

## Index

| File | Topic | Conclusion |
|------|-------|-----------|
| `2026-03-24-nS-mystery.md` | Why nS is 40% off but nSP0 is only 12% off | Data revision + negative correlation between nS and P0 |
