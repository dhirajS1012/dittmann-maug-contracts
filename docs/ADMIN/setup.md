# Setup Guide

## Installation Steps

Step 1: Run uv sync

```
uv sync
```

Step 2: Test with this command

```
uv run python -m dittmann_maug.cli check-data
```

## How to Run Commands

Navigate to project root:

```
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts
```

Run with uv:

```
uv run python -m dittmann_maug.cli check-data
uv run python -m dittmann_maug.cli inspect
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

Or activate virtual environment:

```
source .venv/bin/activate
python -m dittmann_maug.cli check-data
```

## Data Setup

Place files in DROPBOX folder:

DROPBOX/execucomp/
  anncomp.parquet
  codirfin.parquet
  coperol.parquet
  stgrttab.parquet

Or use environment variable for Dropbox cloud storage:

For zsh, add to ~/.zshrc:

```
export DM_DROPBOX_ROOT="$HOME/Dropbox/Research/ExecuComp"
```

For bash, add to ~/.bashrc:

```
export DM_DROPBOX_ROOT="$HOME/Dropbox/Research/ExecuComp"
```

Then reload:

```
source ~/.zshrc
```

## Troubleshooting

Missing files error is normal. Add ExecuComp data files to proceed.

Check environment variable:

```
echo $DM_DROPBOX_ROOT
```

Override temporarily:

```
export DM_DROPBOX_ROOT="/different/path"
```

---

##  Test Commands

Once you have data files, try these:

```bash
# Check required data files exist
uv run python -m dittmann_maug.cli check-data

# View input data statistics
uv run python -m dittmann_maug.cli inspect

# Build Stage 1 contract inputs for year 2000
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664

# Custom risk-free rate
uv run python -m dittmann_maug.cli stage1 --year 1999 --rf 0.0550

# Output saved to: DROPBOX/out/stage1_contract_inputs_YYYY.parquet
```

---

## Troubleshooting

### Python not found
Make sure you're in the project directory:
```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts
```

### Module not found
Make sure to run with `uv run`:
```bash
uv run python -m dittmann_maug.cli check-data
```

### Data files missing
This is expected until you add data files to `DROPBOX/execucomp/`

---

##  Dependencies Installed

```
numpy>=2.4.2          # Numerical computing
pandas>=3.0.0         # Data manipulation
markitdown[all]>=0.1.4 # Markdown support
```

Future stages will require:
```
scipy>=1.13.0         # For Black-Scholes optimization
```

---

##  What's Next?

1. **CLI working** - Can run check-data/inspect/stage1 commands
2. **Add data files** - Place ExecuComp parquet files in `DROPBOX/execucomp/`
3. **Test Stage 1** - Run with real data and verify outputs
4. **Implement Stage 2 & 3** - W0 calculation and option aggregation

---

**Generated:** February 10, 2026  
**Status:** Setup complete, ready for data integration
