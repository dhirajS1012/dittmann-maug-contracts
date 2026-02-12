# Dittmann-Maug (2007) CEO Compensation Replication

Replicating the contract construction methodology from "Optimal Incentive Contracts When Executives Manage Earnings" (Dittmann and Maug, 2007).

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/dhirajS1012/dittmann-maug-contracts.git
cd dittmann-maug-contracts
```

### 2. Copy ExecuComp Data
Get the ExecuComp database from your Dropbox and copy the data files:
```bash
# Create the data directory
mkdir -p data/raw/execucomp

# Copy your ExecuComp files here:
# - anncomp.parquet (annual compensation)
# - codirfin.parquet (financial data)
cp /path/to/anncomp.parquet data/raw/execucomp/
cp /path/to/codirfin.parquet data/raw/execucomp/
```

### 3. Run the Pipeline
```bash
# Install dependencies (first time only)
uv pip install -e .

# Verify data files are present
uv run python -m dittmann_maug.cli check-data

# Inspect the data
uv run python -m dittmann_maug.cli inspect

# Build Stage 1 contract inputs for a specific year
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

### 4. View Results
Output files are saved to the `output/` directory:
```bash
ls -la output/
# stage1_contract_inputs_2000.parquet
# stage1_contract_inputs_1995.parquet
# ... etc
```

---

## Commands

### `check-data`
Verify that required ExecuComp input files exist.
```bash
uv run python -m dittmann_maug.cli check-data
```

### `inspect`
Print summary statistics about input tables.
```bash
uv run python -m dittmann_maug.cli inspect
```

### `stage1`
Build Stage 1 contract inputs (phi, ns, p0, d, sigma, rf).
```bash
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

**Arguments:**
- `--year` (required): Considered year, e.g. 2000
- `--rf` (optional): Risk-free rate in decimals, e.g. 0.0664 (default: None)
- `--repo-root` (optional): Repository root directory (default: current directory)

---

## Project Structure

```
dittmann-maug-contracts/
├── data/
│   └── raw/
│       └── execucomp/          ← Copy your data files here
│           ├── anncomp.parquet
│           └── codirfin.parquet
├── output/                      ← Generated output files
├── src/py/
│   └── dittmann_maug/
│       ├── cli.py               ← Command-line interface
│       ├── pipeline.py          ← Data processing pipeline
│       ├── contracts/           ← Business logic
│       │   └── stage1_inputs.py
│       ├── io/                  ← File I/O
│       │   └── loaders.py
│       └── util/                ← Utilities
│           └── log.py
├── docs/                        ← Documentation
│   ├── prd.md                   ← Project requirements
│   ├── FLOW-ANALYSIS.md         ← Architecture overview
│   ├── EMAIL-TO-PROFESSOR.md    ← Project status email
│   ├── DATA-CONSTRUCTION-MANUAL.md
│   └── DATA-LOADING-ARCHITECTURE.md
└── pyproject.toml               ← Project configuration

```

---

## Development

### Environment Setup
```bash
# Install in editable mode
uv pip install -e .

# Run linter/formatter
uv run black src/py

# Check types
uv run pyright src/py
```

### Running Tests
```bash
uv run pytest tests/
```

---

## Implementation Status

### ✅ Stage 1: Contract Inputs (Complete)
Calculates 8 contract parameters:
- φ (phi): CEO compensation
- nₛ (ns): CEO ownership fraction
- P₀ (p0): Firm market value
- d: Dividend yield
- σ (sigma): Stock volatility
- rf: Risk-free rate

**Verified outputs:**
- Year 1995: 67 CEOs
- Year 2000: 36 CEOs

### 🚧 Stage 2: Wealth Accumulation (Coming Soon)
Accumulate CEO wealth from historical compensation.

### 🚧 Stage 3: Option Valuation (Coming Soon)
Apply Black-Scholes model to executive stock options.

---

## Notes

- **Data Storage:** Currently requires manual copy of ExecuComp data. Future versions will use `rclone` for automated Dropbox sync.
- **No Environment Variables:** All configuration is hardcoded with defaults. No setup needed beyond copying data.
- **Output Location:** All generated files go to `output/` directory (gitignored, safe to delete).

---

## References

- Dittmann, I., & Maug, E. (2007). Optimal Incentive Contracts When Executives Manage Earnings. *Journal of Financial Economics*, 84(1), 126-154.
- Core, J. E., & Guay, W. R. (2002). Estimating the value of employee stock option portfolios. *Journal of Accounting Research*, 40(3), 613-630.

---

## Contributing

This is an educational replication project. For questions or suggestions, please open an issue.

---

*Last Updated: February 11, 2026*
