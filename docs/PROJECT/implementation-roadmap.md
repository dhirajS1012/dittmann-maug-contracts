# Implementation Roadmap: Completing the Contract Construction Pipeline
**Date:** February 10, 2026  
**Status:** AI-generated roadmap (model)

---

## Overview

The current codebase has successfully implemented **Stage 1** (basic contract inputs). To complete the Dittmann-Maug contract construction replication, three major stages remain:

| Stage | Component | Status | Effort |
|-------|-----------|--------|--------|
| 1 | Basic inputs (phi, ns, p0, d, sigma, rf) | ✅ Done | - |
| 2 | W0 (non-firm wealth accumulation) | ❌ To-do | ~40 hours |
| 3 | Option portfolio aggregation | ❌ To-do | ~50 hours |
| 4 | Visualization & testing | ❌ To-do | ~30 hours |

---

## Stage 2: W0 (Non-Firm Wealth) Implementation

### Objective
Calculate each CEO's accumulated non-firm wealth (`W0`), which represents cash and investments outside of firm holdings. This is calculated iteratively from the CEO's first appearance in the database.

### Data Required
- Historical anncomp data (5+ years back from measurement year)
- Historical codirfin data (for investment returns)
- Tax rate schedule (1992-2000)
- Historical stock price and dividends

### Implementation Plan

**File:** `src/py/dittmann_maug/contracts/stage2_wealth.py`

#### 2.1 Tax Rate Lookup Module
```python
def get_tax_rate(year: int) -> float:
    """Return personal tax rate for the given year."""
    # SAS script reference: hardcoded rates
    return {
        1992: 0.31,
        1993: 0.396,
        1994: 0.42, 1995: 0.42, ..., 2000: 0.42
    }.get(year, 0.42)  # Default to 1994+ rate
```

#### 2.2 Risk-Free Rate Lookup
```python
def get_risk_free_rate(year: int) -> float:
    """Return 1-year risk-free rate for the given year."""
    # SAS script hardcoded values
    return {...}  # Build full 1992-2000 table
```

#### 2.3 Wealth Accumulation Loop
```python
def calculate_w0(
    ceo_data: pd.DataFrame,  # Historical rows for one CEO, sorted by year
    tax_rates: dict,
    rf_rates: dict,
) -> pd.DataFrame:
    """
    Calculate W0 iteratively for each year in CEO's history.
    
    Formula:
    1. Initial W0 (first year tE):
       W0_tE = (total_salary_tE + soptexer_tE) * (1 - tax_tE)
       where total_salary includes ltip
    
    2. Subsequent years:
       Growth: W0' = W0_prev * (1 + R_year)
       Add income: W0' += (salary + options_exercised) * (1 - tax)
       Adjust shares: W0' -= (new_shares - old_shares) * price
    """
```

#### 2.4 Column Requirements
**Input (anncomp):**
- `salary`, `bonus`, `othann`, `ltip`, `allothtot` (compensation)
- `soptexer` (realized option exercise value)
- `shrown` (shares owned)
- `year`

**Input (codirfin):**
- `prccf_a` (adjusted stock price)
- `divyield`
- Risk-free rate lookup (from hardcoded table)

**Output:**
- `w0`: Non-firm wealth at end of measurement year
- `w0_calc_history`: Optional detail rows for debugging

#### 2.5 Edge Cases
- Missing `soptexer` → treat as 0
- First year in database → W0 = 0 initially
- CEO with data gaps → skip or flag
- Negative W0 → exclude from final dataset (per SAS exclusion)

### Pseudocode
```
FOR each CEO:
  FOR each year in history (sorted ascending):
    IF first year:
      W0 = (total_salary + soptexer) * (1 - tax)
    ELSE:
      W0 = W0_prev * (1 + rf_rate)  # Growth
      W0 += (salary + soptexer + dividends) * (1 - tax)  # Add income
      W0 -= (shrown - shrown_prev) * price  # Subtract new share costs
      
  Store W0 for measurement_year
```

---

## Stage 3: Option Portfolio Aggregation

### Objective
Aggregate CEO's entire option portfolio (newly granted + outstanding) into a single "representative option" with three parameters: number of options (`no`), strike price (`K`), and maturity (`T`).

### Data Required
- Stock grant table (`stgrttab`): Newly granted options with strike, maturity, and count
- Outstanding option counts (`uexnumun`, `uexnumex`) from previous years
- Current stock price and volatility
- Black-Scholes valuation capability

### Implementation Plan

**File:** `src/py/dittmann_maug/contracts/stage3_options.py`

#### 3.1 Black-Scholes Valuation Module
**File:** `src/py/dittmann_maug/math/blackscholes.py`

```python
from scipy.stats import norm

def black_scholes_value(
    S: float,         # Current stock price
    K: float,         # Strike price
    T: float,         # Time to maturity (years)
    r: float,         # Risk-free rate
    sigma: float,     # Volatility
    d: float = 0.0,   # Dividend yield
) -> tuple[float, float]:
    """
    Calculate Black-Scholes value and delta N(d1).
    
    Returns: (value, delta)
    """
    d1 = (log(S/K) + (r - d + 0.5*sigma**2)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    
    value = S*exp(-d*T)*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    delta = exp(-d*T)*norm.cdf(d1)
    
    return value, delta

def black_scholes_delta(S, K, T, r, sigma, d=0.0):
    """Wrapper for delta only."""
    _, delta = black_scholes_value(S, K, T, r, sigma, d)
    return delta
```

#### 3.2 Option Portfolio Construction
```python
def build_option_portfolio(
    ceo_row: pd.Series,         # Row from Stage 1 output
    stgrttab: pd.DataFrame,     # Stock grant table
    cfg: Stage3Config,
) -> dict:
    """
    Build portfolio of individual option grants.
    
    Portfolio consists of:
    1. Newly granted options (from stgrttab for measurement year)
    2. Hypothetical unexercisable options (approximating old grants)
    3. Hypothetical exercisable options (approximating old grants)
    
    For each, calculate:
    - Number of options (n_i)
    - Strike price (K_i)
    - Maturity (T_i)
    - Black-Scholes value (BS_i)
    - Delta (N(d1)_i)
    """
```

#### 3.3 Representative Option Calculation
```python
def optimize_representative_option(
    portfolio: list[dict],  # Individual option grants
    S: float,               # Current stock price
    r: float,
    sigma: float,
    d: float,
) -> tuple[float, float]:
    """
    Use Nelder-Mead optimization to find representative strike K* and maturity T*.
    
    Minimize: f(K, T) = ((BS_rep - BSq)/BSq)^2 + ((Nd1_rep - Nd1q)/Nd1q)^2
    
    where:
    - BS_rep = Black-Scholes value of single option (K, T)
    - BSq = value-weighted average BS of portfolio
    - Nd1q = value-weighted average delta of portfolio
    """
    from scipy.optimize import minimize
    
    def objective(x):
        K_test, T_test = x
        if K_test <= 0 or T_test <= 0:
            return 1e9
        
        bs_rep, n_d1_rep = black_scholes_value(S, K_test, T_test, r, sigma, d)
        
        error_bs = ((bs_rep - portfolio_bs_avg) / portfolio_bs_avg) ** 2
        error_nd1 = ((n_d1_rep - portfolio_nd1_avg) / portfolio_nd1_avg) ** 2
        
        return error_bs + error_nd1
    
    result = minimize(objective, [S, 6.0], method='Nelder-Mead')
    return result.x  # [K*, T*]
```

#### 3.4 Maturity Reduction Factor
```python
# From SAS script: Account for early exercise
MAT_RED = 0.7
# Apply: T_portfolio = T_original * 0.7
```

### Data Flow Pseudocode

```
FOR each CEO in Stage 1 output:
  # Gather option portfolio
  new_grants = Get grants from stgrttab for measurement_year
  old_grants = Approximate from uexnumun, uexnumex counts
  
  # For each grant: calculate BS value and delta
  portfolio = []
  FOR grant in [new_grants, old_grants]:
    BS_i, Nd1_i = black_scholes_value(P0, K_i, T_i*0.7, rf, sigma, d)
    portfolio.append({n: count, K: strike, T: maturity, BS: BS_i, Nd1: Nd1_i})
  
  # Calculate portfolio averages (value-weighted)
  BSq = sum(n_i * BS_i) / sum(n_i)
  Nd1q = sum(n_i * Nd1_i) / sum(n_i)
  
  # Optimize representative option
  K_opt, T_opt = optimize_representative_option(portfolio, ...)
  
  # Output
  no = sum(all option counts)
  K = K_opt
  T = T_opt
```

### Configuration
```python
@dataclass(frozen=True)
class Stage3Config:
    measurement_year: int
    considered_year: int
    maturity_reduction: float = 0.7  # Early exercise factor
    optimization_method: str = 'Nelder-Mead'
```

---

## Stage 4: Testing & Validation

### 4.1 Unit Tests

**File:** `tests/test_stage1.py`
- Test Stage 1 with sample data
- Verify phi, ns, p0, d, sigma, rf calculations
- Check filtering logic

**File:** `tests/test_stage2.py`
- Test W0 accumulation with known CEO history
- Verify tax rate lookups
- Test edge cases (missing data, first year, etc.)

**File:** `tests/test_stage3.py`
- Test Black-Scholes calculations
- Test portfolio aggregation
- Test optimization convergence

**File:** `tests/test_blackscholes.py`
- Black-Scholes value vs. known results
- Delta validation
- Dividend yield effects

### 4.2 Integration Tests

**Test:** Replicate example CEO from paper
- Take a known CEO-year from Dittmann & Maug (2007)
- Run full pipeline
- Compare contract parameters (phi, ns, no, K, T) to paper's reported values
- Flag any discrepancies

### 4.3 Regression Tests

Create a "golden dataset" from paper's results (or SAS script) and verify outputs match.

---

## Recommended Implementation Order

1. **Week 1:** Black-Scholes module + Stage 2 (W0) basic structure
2. **Week 2:** Stage 2 wealth accumulation logic + tax/RF lookups
3. **Week 3:** Stage 3 option portfolio + optimization
4. **Week 4:** Testing, debugging, and paper validation
5. **Week 5:** Visualization tool (Streamlit) + interactive testing

---

## Dependencies to Add

```toml
# pyproject.toml
scipy = ">=1.13.0"  # For optimization and statistical functions
```

---

## Success Criteria

- [ ] All three stages produce output matching Stage 1 schema + new columns
- [ ] `w0`, `no`, `K`, `T` calculated for sample CEOs
- [ ] At least one example CEO fully validated against paper
- [ ] Unit test coverage > 80%
- [ ] Visualization tool allows interactive inspection

---

## References

- `docs/dittman-maug-contract-construction-procedure.md` (comprehensive spec)
- `DROPBOX/dittman-maug-replication-materials/SAS/1 dataset construction/Dataset Construction Macro V4.sas` (original SAS code)
- Core & Guay (2002) (referenced in procedure doc; need to download per TODO)

