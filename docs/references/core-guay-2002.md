# Core and Guay (2002): Option Portfolio Aggregation

## Citation

Core, John E., and Wayne R. Guay. 2002. "Estimating the value of employee stock option portfolios and their sensitivities to price and volatility." *Journal of Accounting Research* 40(3): 613–630.

**DOI:** 10.1111/1475-679X.00064

**PDF Location:** `/Users/dhirajs/Dropbox/2026-dittman-maug-replication/references/core-guay-2002-estimating-option-portfolios.pdf`

---

## Overview

This paper presents a methodology for aggregating complex option portfolios held by corporate executives into a single **representative option** characterized by three parameters:
- **Number of options** (`no`): Normalized by total shares outstanding
- **Strike price** (`K`): Dollar amount per share
- **Time to maturity** (`T`): Years until expiration

This aggregation is critical for valuing executive compensation packages and calculating option sensitivities without losing material information about portfolio risk.

---

## Core Algorithm

### Problem Statement

Given a portfolio of $m$ option grants with different strike prices, maturities, and quantities, find a single representative option that:
1. Preserves the **portfolio value** (Black-Scholes valuation)
2. Preserves the **portfolio delta** (sensitivity to stock price changes)

### Mathematical Formulation

**Portfolio Characteristics (actual):**
- For option grant $i$: quantity $n_i$, strike $K_i$, maturity $T_i$
- Black-Scholes value: $BS_i = \text{BS}(S, K_i, T_i, \sigma, r, d)$
- Delta: $\Delta_i = N(d1)_i$ (where $N(d1)$ is the cumulative normal at $d1$)

**Portfolio Aggregates:**
$$\text{BS}_q = \frac{\sum_i n_i \cdot BS_i}{\sum_i n_i} \quad \text{(value-weighted average)}$$

$$N(d1)_q = \frac{\sum_i n_i \cdot N(d1)_i}{\sum_i n_i} \quad \text{(delta-weighted average)}$$

**Representative Option:**
Find $K^*$ and $T^*$ such that a single option with these parameters produces:
$$BS^* = \text{BS}(S, K^*, T^*, \sigma, r, d) \approx BS_q$$
$$N(d1)^* = N(d1) \text{ for the option with } K^*, T^* \approx N(d1)_q$$

### Optimization Procedure

**Objective Function:**
$$\min_{K, T} \left[ \left(\frac{BS^* - BS_q}{BS_q}\right)^2 + \left(\frac{N(d1)^* - N(d1)_q}{N(d1)_q}\right)^2 \right]$$

**Method:** Nelder-Mead simplex algorithm (unconstrained nonlinear optimization)

**Constraints (implicit):**
- $K > 0$ (strike must be positive)
- $T > 0$ (maturity must be positive)

---

## Implementation in Dittman & Maug (2007)

The Core & Guay algorithm is used in **Stage 3** of our replication to construct the representative option (`no`, `K`, `T`) from each CEO's complete option portfolio.

### Portfolio Composition

For a given measurement year, the CEO's option portfolio includes:

1. **Newly granted options** from `stgrttab`:
   - Grant date, quantity, strike price, maturity
   - Takes these values directly

2. **Previously granted options** (approximated as two synthetic grants):
   - **Unexercisable options**: `uexnumun_a` options at strike `S - realizable_value_unex / uexnumun_a`
   - **Exercisable options**: `uexnumex_a` options at strike `S - realizable_value_ex / uexnumex_a`

### Maturity Adjustment

Before aggregation, all option maturities are multiplied by a **reduction factor**:
$$T_{adjusted} = T_{original} \times 0.7$$

This accounts for the tendency of executives to exercise options early (approximately 70% of the remaining time until expiration).

**Source:** SAS script line 235; based on empirical evidence in Core & Guay (2002)

### Aggregation Steps (Pseudocode)

```
1. INPUT: Portfolio of m option grants {(n_i, K_i, T_i) for i = 1...m}
           Current stock price S, volatility σ, dividend yield d, risk-free rate r

2. FOR EACH option i:
   - Calculate BS_i = BlackScholes(S, K_i, T_i, σ, r, d)
   - Calculate N(d1)_i = NormDist(d1_i) where d1 = (ln(S/K) + (r-d+σ²/2)*T) / (σ*√T)

3. Calculate portfolio aggregates:
   - BS_q = SUM(n_i * BS_i) / SUM(n_i)
   - N(d1)_q = SUM(n_i * N(d1)_i) / SUM(n_i)

4. OPTIMIZATION: Find K*, T* minimizing:
   error(K, T) = [(BS(S,K,T,...) - BS_q)/BS_q]² + [(N(d1) - N(d1)_q)/N(d1)_q]²

5. OUTPUT: Representative option (no, K*, T*)
          where no = total_option_quantity / total_shares_outstanding
```

---

## Key Insights

### Why This Works

1. **Preserves Value:** The representative option values the CEO's compensation correctly
2. **Preserves Risk Sensitivity:** Delta matching ensures the option's sensitivity to price changes matches the actual portfolio
3. **Simplifies Calculation:** Single option easier to work with than portfolio of 10-20+ individual grants
4. **Empirically Validated:** Tested on large samples of executive option portfolios

### Important Assumptions

1. Options are exercised according to historical patterns (captured in the 0.7 maturity factor)
2. Black-Scholes pricing model is appropriate for executive options
3. Delta (alone) is sufficient to characterize portfolio sensitivity; other Greeks (gamma, vega) are less critical
4. Strike and maturity can vary continuously (smooth optimization surface)

### Limitations

1. **Information Loss:** Aggregation discards details about grant timing, vesting schedules, etc.
2. **Early Exercise:** The 0.7 reduction factor is an approximation; actual early exercise patterns vary
3. **No Vesting Cliffs:** Assumes continuous exercise opportunities rather than cliff vesting
4. **Liquidity:** Ignores trading restrictions on executive stock options

---

## Implementation in Our Python Code

### Stage 3 Implementation Plan

```python
# Expected location: src/py/dittmann_maug/contracts/stage3_options.py

class OptionPortfolio:
    """Represents a CEO's complete option portfolio from one year."""
    
    def __init__(self, grants: List[OptionGrant]):
        """grants: List of OptionGrant(quantity, strike, maturity, type)"""
        self.grants = grants
    
    def aggregate_to_representative(self, 
                                     stock_price: float,
                                     volatility: float,
                                     dividend_yield: float,
                                     risk_free_rate: float) -> RepresentativeOption:
        """
        Use Core & Guay algorithm to find representative option.
        
        Returns: RepresentativeOption(quantity, strike, maturity)
        """
        # 1. Calculate BS value and delta for each grant
        # 2. Compute portfolio aggregates (BS_q, N(d1)_q)
        # 3. Minimize error function using scipy.optimize
        # 4. Return K*, T* parameters
        pass
```

### Validation Strategy

```python
def test_core_guay_matches_original():
    """
    For each CEO-year in the sample:
    1. Load option portfolio from ExecuComp
    2. Aggregate using Core & Guay algorithm
    3. Compare to Dittman & Maug original output
    4. Assert error < 1% in both value and delta
    """
    pass
```

---

## References to This Algorithm

- **Dittman & Maug (2007):** Section II.C, Appendix B
- **DM & Maug (2007) SAS code:** Lines 235, 273-370 (aggregation logic)
- **Zhang & DM (2011):** Uses same algorithm for option aggregation
- **Original Core & Guay paper:** Sections 1-3 for algorithm; Section 4 for validation

---

## Related Literature

**Other Option Valuation Methods:**
- Hall & Murphy (2002): Alternative approach with closed-form approximations
- Brenner, Sundaram & Damodaran (1997): Early exercise modeling
- Carpenter (1998): Executive option exercise behavior

**Executive Compensation Context:**
- Murphy (1999): Survey of executive pay practices
- Jensen & Murphy (1990): Pay-performance sensitivity
- Hubbard & Palia (1995): Executive incentives and firm performance

---

## Notes for Implementation

1. **Black-Scholes Module Required:** Need robust BS implementation with all Greeks
2. **Optimization:** Use `scipy.optimize.minimize` with multiple starting points to avoid local minima
3. **Constraints:** Ensure K, T > 0; may need to reparameterize or add bounds
4. **Numerical Stability:** Use log-space calculations for very small/large stock prices
5. **Testing:** Validate against published examples; compare to original SAS output

---

## Questions for Next Meeting

- Have you reviewed the actual option portfolios in ExecuComp? How many options per CEO-year?
- Do we want to implement full Core & Guay or simplified approach (e.g., use weighted-average strike)?
- Any computational constraints we should be aware of?

---

*Last Updated: February 10, 2026*
*Document Type: Reference | AI-Generated Markdown*
