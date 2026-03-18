# Validation Report

## Run
- Reference year: 1999, Measurement year: 2000, History: 5

## Status
- Overall: FAIL
- Sample-size check: FAIL (Panel A: 598 vs 598, Panel B: 1400 vs 1417)
- Mean-diff check: PASS (mean abs % diff across variables: 19.656%, tolerance: <= 20.0%)
- Missing replicated means: 0

## Mean-Diff Summary
- Variables compared: 19
- Mean absolute percent diff (across variables): 19.656%
- Max absolute percent diff: 88.890%

## Largest Mean Gaps
| Panel | Variable | Paper Mean | Replicated Mean | Abs % Diff |
|---|---|---:|---:|---:|
| A | Value of options ($ m) | 29.47 | 55.6659 | 88.890% |
| B | Options (%) | 1.45 | 2.55773 | 76.395% |
| A | Options adjusted (%) | 1.22 | 2.0498 | 68.016% |
| A | Options (%) | 1.29 | 2.15168 | 66.797% |
| A | Stock (%) | 2.29 | 3.21566 | 40.422% |
| A | Value of stock ($ m) | 91.98 | 104.236 | 13.324% |
| A | Maturity (years) | 5.89 | 5.53718 | 5.990% |
| B | Value of stock ($ m) | 132.44 | 128.077 | 3.294% |
| B | Base salary ($'000) | 1718 | 1662.67 | 3.221% |
| B | Market value ($ m) | 8012 | 7850.22 | 2.019% |

## Notes
- This report compares replicated Table I statistics against paper targets.
- Panel A sample size (598) matches the paper exactly.
- Panel B sample size (1,400) is 17 below the paper's 1,417. The paper reports losing 103 CEOs for missing stock volatility or adjustment factor (from an initial 1,696 CEOs). Our sigma.notna() filter removes 228 from 1,628, yielding 1,400. The larger drop likely reflects S&P expanding historical ExecuComp coverage after 2006; the newly added records often lack 1999 volatility data, causing our filter to be more aggressive.
- nO (%) and nS (%) are systematically high relative to the paper. Investigation shows this is driven by a minority of CEOs with very large option/share holdings. These CEOs have the same execids as in the paper sample, suggesting S&P revised ExecuComp option counts upward after the paper was published (2007). Excluding the top ~56 CEOs by nO brings the mean to ~1.26% (paper: 1.29%).
- Phi (base salary), W0 (wealth), and P0 (market value) all replicate within 7%.
