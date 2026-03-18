# Validation Report

## Run
- Reference year: 1999, Measurement year: 2000, History: 5

## Status
- Overall: FAIL
- Sample-size check: FAIL (Panel A: 598 vs 598, Panel B: 1628 vs 1417)
- Mean-diff check: FAIL (tolerance: <= 20.0% absolute percent diff)
- Missing replicated means: 0

## Mean-Diff Summary
- Variables compared: 19
- Mean absolute percent diff (across variables): 19.914%
- Max absolute percent diff: 88.890%

## Largest Mean Gaps
| Panel | Variable | Paper Mean | Replicated Mean | Abs % Diff |
|---|---|---:|---:|---:|
| A | Value of options ($ m) | 29.47 | 55.6659 | 88.890% |
| B | Options (%) | 1.45 | 2.46358 | 69.902% |
| A | Options adjusted (%) | 1.22 | 2.0498 | 68.016% |
| A | Options (%) | 1.29 | 2.15168 | 66.797% |
| A | Stock (%) | 2.29 | 3.21566 | 40.422% |
| A | Value of stock ($ m) | 91.98 | 104.236 | 13.324% |
| B | Stock (%) | 2.97 | 3.18837 | 7.353% |
| B | Market value ($ m) | 8012 | 7486.21 | 6.563% |
| A | Maturity (years) | 5.89 | 5.53718 | 5.990% |
| B | Base salary ($'000) | 1718 | 1629.46 | 5.153% |

## Notes
- This report compares replicated Table I statistics against paper targets.
- If sample sizes fail first, prioritize filter/timing logic before tuning option or wealth calculations.
- If sample sizes pass but means fail, inspect units/scaling (`P0`, `W0`, `%` fields), then option and wealth steps.
