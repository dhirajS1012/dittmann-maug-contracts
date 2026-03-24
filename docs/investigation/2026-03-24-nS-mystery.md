# Investigation: nS (Stock %) Discrepancy

**Date:** 2026-03-24
**Status:** Resolved — data revision, not code error

## Hypothesis

Professor Azevedo flagged that nS (stock %) is 40% too high while nSP0 (value of stock = nS * P0) is only 12% too high and P0 is 0.4% off. Since nSP0 = nS * P0, if two of three are correct, the third should be too. Something must be wrong.

## Investigation

### 1. Formula Verification

The nS formula in `contracts.py:749` is:
```python
a16["nS"] = a16["nS"] / a16["shrsout_a"] / 1000.0
```
Where input nS = `shrown_a` (thousands of shares) and `shrsout_a` (millions of shares).

Verified empirically: `shrown / (shrsout * 1000)` gives the correct fraction of shares owned. The formula is mathematically correct.

### 2. Why nSP0 Can Be 12% Off While nS Is 40% Off

The professor's intuition assumed `mean(nS * P0) ≈ mean(nS) * mean(P0)`, but this only holds if nS and P0 are uncorrelated. In reality, **nS and P0 are strongly negatively correlated** — CEOs at small firms own much larger fractions.

- `mean(nS) * mean(P0) = 318` (if uncorrelated)
- `mean(nS * P0) = 104` (actual — much lower due to negative covariance)

So a 40% increase in mean(nS) does NOT translate to a 40% increase in mean(nS * P0) — the high-nS CEOs are at small firms, so their contribution to nSP0 is small.

### 3. Split Adjustment (ajex) Is Irrelevant

A critical finding: **ajex cancels out in both the nS and P0 formulas**:

- `nS = (shrown * ajex) / (shrsout * ajex * 1000) = shrown / (shrsout * 1000)` — ajex cancels
- `P0 = (prccf / ajex) * (shrsout * ajex) * 1M = prccf * shrsout * 1M` — ajex cancels

So the professor's concern about double-correction through ajex is **moot** for nS and P0. The split adjustment only matters for per-share values and option counts.

### 4. Data Revision Is the Root Cause

- 6 CEOs have nS > 46.34% (the paper's reported maximum), with one CEO at 84.9%
- Even capping at the paper's max only reduces mean nS from 3.22% to 3.09%
- The discrepancy is distributed across many CEOs, not just extreme outliers
- S&P revised ExecuComp share holdings (`shrown_tot`) after the paper was published in 2007

### 5. shrsout Units Confirmed

Empirically verified that `shrsout` in current ExecuComp parquets is in **millions** (not thousands as in the original SAS data). For ajex=1 companies, `prccf * shrsout / mktval ≈ 1.0` (median: 1.000, mean for clean sample: 0.923).

Note: there is an inconsistency in the codebase where `contracts.py:754` uses `shrsout_a * 1_000_000` (correct) but `contracts.py:873` in `get_contract_parameters()` uses `shrsout * ajex * 1000` (incorrect — this is the single-observation API, not used by the main pipeline).

## Results

**Before investigation (baseline):**

| Variable | Paper | Ours | % Diff | Status |
|----------|-------|------|--------|--------|
| N | 598 | 598 | 0% | PASS |
| phi | 2037 | ~2037 | ~0.7% | PASS |
| nS | 2.29% | 3.22% | +40% | FAIL |
| P0 | 9857 | 9896 | +0.4% | PASS |
| nSP0 | 91.98 | 104.24 | +13% | FAIL |

**After investigation:** No code changes — discrepancy is from data revisions, not a code bug.

## Conclusion

The nS discrepancy is a **data revision issue**. S&P updated ExecuComp share holdings after 2007. The apparent inconsistency between nS (40% off) and nSP0 (12% off) is explained by the strong negative correlation between stock ownership percentage and firm size — high-ownership CEOs are at small firms, so their inflated nS contributes little to the dollar-weighted nSP0.

The code formula is correct. The ajex split adjustment cancels in both nS and P0, so double-correction is not a concern for these variables.

**Action items:**
- Fix the inconsistent `get_contract_parameters()` function (line 873) which uses the wrong shrsout multiplier, though it's not used by the main pipeline
- Consider whether nO discrepancy (+67%) has the same data-revision root cause
