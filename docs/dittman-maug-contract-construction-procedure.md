# AI Generated: Dittman and Maug (2007) CEO Compensation Contract Construction Procedure

This document provides a comprehensive description of the methodology used by Dittman and Maug (2007) to construct CEO compensation contracts from ExecuComp data. It is intended to be a detailed guide for replicating the dataset construction. This procedure is derived from the paper's "Empirical Methodology and Data" section (Section II), Appendix B, and is thoroughly informed by the logic in the `Dataset Construction Macro V4.sas` script.

## 1. CEO Compensation Formula

The core of the paper's analysis is a model of the CEO's end-of-period wealth (`WT`), which is a function of firm performance (end-of-period stock price `PT`). The contract is defined by a set of parameters: base salary (`phi`), number of shares (`ns`), and number of options (`no`).

**Formula for End-of-Period Wealth (`WT`):**

```
WT = (phi + W0) * e^(rf * T) + ns * PT + no * max(PT - K, 0)
```

Where:
*   `WT`: CEO's end-of-period wealth at time `T`.
*   `phi`: Base salary + bonus for the `considered year`.
*   `W0`: CEO's initial non-firm wealth.
*   `rf`: Risk-free rate of interest.
*   `T`: Maturity of the representative option.
*   `ns`: Number of shares held by the CEO (as a fraction of total shares).
*   `PT`: End-of-period market value of the firm.
*   `no`: Number of options held by the CEO (as a fraction of total shares).
*   `K`: Strike price of the representative option.

*(Source: Dittman & Maug (2007), Section I, Equation (2))*

## 2. Data Sources and Sample Selection

*   **Primary Data Source:** Compustat ExecuComp Database (1992-2000 for the original paper). The SAS script accesses these via a library named `dir`, referencing tables like `comptabl` (AnnComp), `coperol`, `codirfin`, and `stgrttab`.
*   **Sample:** The SAS macro is designed to be called as `%construct(year, history)`. For the paper, this was `%construct(1999, 5)`, which selects CEOs in the `considered year` 2000 who have a continuous data history from 1995-1999.
    *(Source: Dataset Construction Macro V4.sas, lines 3-4)*
*   **Exclusions:**
    *   CEOs with missing `salary` in the `considered year`. *(SAS script, line 68)*
    *   Observations where `shrown` (shares owned) is missing or `pinclopt='TRUE'` (shares and exercisable options are not separated). If `pinclopt` is true for any year, that executive's data for that year and all prior years are excluded. *(SAS script, lines 88-100)*
    *   CEOs who do not have the required `history` of data. *(SAS script, lines 105-139)*
    *   CEOs who appear as an executive for more than one company in the same year. *(SAS script, lines 144-159)*
    *   Final dataset excludes observations with missing `W0`, `W0 < 0`, missing `sigma` (`bs_volatility`), or errors during the option calculation. *(SAS script, lines 525-530, 545-546)*

## 3. Key Variable Definitions and Construction

For `%construct(year, history)`:
- **Reference year** = `year` (for `%construct(1999,5)`, this is 1999).
- **Measurement year** = `year + 1` (for `%construct(1999,5)`, this is 2000).

Most market/holdings inputs come from the **reference year**. `phi` comes from the **measurement year**.

### 3.0 Source tables used

- `comptabl`: compensation and holdings (`salary`, `bonus`, `othann`, `allothtot`, `ltip`, `shrown`, `rstkgrnt`, `soptexer`, `rstkhld`, `uexnumun`, `uexnumex`, `inmonun`, `inmonex`, `pinclopt`)
- `coperol`: identity and role (`execid`, `permid`, `year`, `ceoann`, `co_per_rol`)
- `codirfin`: firm market inputs (`prccf`, `ajex`, `divyield`, `shrsout`, `bs_volatility`, `fyr`)
- `stgrttab`: option grant details (`numsecur`, `expric`, `exdate`)

### 3.1 `P0` (Firm market value)

- `P0 = prccf_a * NumOfShares`
- `prccf_a = prccf / ajex`
- `NumOfShares = (shrsout * ajex) * 1000`
- Uses **reference-year** data.

### 3.2 `d` (Dividend yield)

- `d = divyield / 100`
- Uses **reference-year** `codirfin.divyield`.

### 3.3 `sigma` (Volatility)

- `sigma = bs_volatility`
- Uses **reference-year** `codirfin.bs_volatility`.

### 3.4 `rf` (Risk-free rate)

- `rf` is hardcoded by year in SAS (6-year Treasury for the measurement year).
- Example: for year 2000, `rf = 0.0664`.

### 3.5 `phi` (Fixed pay)

- `phi = salary + bonus + othann + allothtot`
- Uses **measurement-year** compensation row.
- `ltip` is **not** included in `phi`.

### 3.6 `W0` (Non-firm wealth)

- Built iteratively from the CEO history.
- First observed year:
  - `W0 = (total_salary + soptexer) * (1 - tau)`
  - `total_salary = salary + bonus + othann + ltip + allothtot` (includes `ltip`)
- Later years:
  - grow prior wealth by the 1-year Treasury series in SAS;
  - add after-tax income/dividends and restricted stock grants;
  - subtract net stock purchases;
  - apply company-switch logic exactly as in SAS.
- Final sample drops rows with missing/negative `W0`.

### 3.7 `ns` (Shares held as fraction of firm)

- `ns = shrown_a / (shrsout_a * 1000)`
- `shrown_a = shrown * ajex`
- `shrsout_a = shrsout * ajex`
- Uses **reference-year** holdings and shares outstanding.

### 3.8 `no`, `K`, `T` (Representative option)

- Start from current-year grants (`stgrttab`) plus two Core-Guay-style hypothetical grants (unexercisable and exercisable holdings).
- Apply maturity reduction factor `0.7`.
- Compute portfolio-average Black-Scholes value and delta, then solve for representative `K` and `T` by minimizing squared distance.
- `no` is total options held, normalized by shares outstanding.
- `K` is scaled to firm level (`K * NumOfShares`).
- If no options: set `K = P0` and `T = 10`.

All formulas in this section follow `Dataset Construction Macro V4.sas` (mainly IML block and final data steps).

## 4. Output Dataset and Final Variables

The final dataset (`CEO_YYYY_HYRS`) contains one row per CEO for the `considered year` with all the constructed variables, ready for the economic analysis part of the paper. All fractional ownership variables (`nS`, `nO`) and the total strike price `K` are scaled to represent the entire firm.

## 5. Considerations for Old vs. New ExecuComp Formats

This procedure is based entirely on the **pre-FAS 123 (1992 reporting format)**. Replicating this for **post-FAS 123 (2006 onwards) data** would require careful mapping of variables. For example, option details would need to be extracted from `PlanBasedAwards` and `OutstandingAwards` tables instead of `stgrttab`, and the logic for identifying exercisable vs. unexercisable options would need to adapt to the new data structure.
