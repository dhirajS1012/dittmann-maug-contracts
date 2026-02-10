# Setup & Installation Guide

## ✅ Installation Complete

The project is now properly set up. Here's what was done:

### Installation Steps

1. **Updated `pyproject.toml`** with:
   - Build system configuration (hatchling)
   - CLI script entry point
   - Package path configuration for `src/py/` layout

2. **Synced uv environment**:
   ```bash
   uv sync
   ```
   This installed the package and all dependencies

3. **Verified CLI works**:
   ```bash
   uv run python -m dittmann_maug.cli check-data
   ```

---

## 🎯 Current Status

✅ **Package installed and CLI functional**

The error you see is **expected** - it's telling you that the ExecuComp data files are missing:

```
FileNotFoundError: Missing required files:
- DROPBOX/execucomp/anncomp.parquet
- DROPBOX/execucomp/codirfin.parquet
```

This is normal! You need to add the ExecuComp data files to proceed.

---

## 📊 How to Use

### Option 1: Using `uv run` (Recommended)

```bash
# Navigate to project root
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts

# Run any command with uv
uv run python -m dittmann_maug.cli check-data
uv run python -m dittmann_maug.cli inspect
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

### Option 2: Using the venv directly

```bash
# Activate the venv
source .venv/bin/activate

# Then run directly
python -m dittmann_maug.cli check-data
python -m dittmann_maug.cli inspect
python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

### Option 3: Using the console script

Once you have data files set up:

```bash
uv run dittmann-maug check-data
uv run dittmann-maug inspect
uv run dittmann-maug stage1 --year 2000 --rf 0.0664
```

---

## 📁 Data Setup

### Option 1: Local DROPBOX Folder (Simple)

Place ExecuComp parquet files at:

```
DROPBOX/execucomp/
├── anncomp.parquet       # Annual compensation data
├── codirfin.parquet      # Company director/financial data
├── coperol.parquet       # (Optional) CEO role data
└── stgrttab.parquet      # (Optional, for Stage 3) Stock grant table
```

### Option 2: Dropbox Folder + Environment Variable (Recommended) ✅

This is more convenient if your data is in Dropbox. It keeps data in one place and syncs automatically.

#### Step 1: Set Up Dropbox Environment Variable

**For zsh (if you use `zsh`):**

```bash
# Add this line to your ~/.zshrc file
echo 'export DM_DROPBOX_ROOT="$HOME/Dropbox/path-to-your-execucomp-data"' >> ~/.zshrc

# Reload your shell
source ~/.zshrc
```

**For bash (if you use `bash`):**

```bash
# Add this line to your ~/.bashrc file
echo 'export DM_DROPBOX_ROOT="$HOME/Dropbox/path-to-your-execucomp-data"' >> ~/.bashrc

# Reload your shell
source ~/.bashrc
```

#### Step 2: Update the Path

Replace `path-to-your-execucomp-data` with your actual Dropbox path:

```bash
# Example: If your data is in ~/Dropbox/Research/ExecuComp
export DM_DROPBOX_ROOT="$HOME/Dropbox/Research/ExecuComp"

# Or with full path
export DM_DROPBOX_ROOT="/Users/dhirajs/Dropbox/Research/ExecuComp"
```

#### Step 3: Verify Setup

```bash
# Reload terminal to apply changes
source ~/.zshrc   # or ~/.bashrc

# Test it
uv run python -m dittmann_maug.cli check-data

# You should see the paths of your data files, or a helpful error message
```

#### Step 4: Expected Dropbox Structure

Your Dropbox folder should have this structure:

```
~/Dropbox/Research/ExecuComp/          (or your chosen path)
├── execucomp/
│   ├── anncomp.parquet               # Annual compensation
│   ├── codirfin.parquet              # Company/director/financial data
│   ├── coperol.parquet               # (Optional)
│   └── stgrttab.parquet              # (Optional, needed for Stage 3)
└── out/
    ├── stage1_contract_inputs_2000.parquet
    ├── stage1_contract_inputs_1999.parquet
    └── ... (outputs saved here)
```

---

### Comparison: Local vs Dropbox

| Feature | Local `DROPBOX/` | Dropbox + Env Var |
|---------|------------------|-------------------|
| **Setup time** | 2 minutes | 3 minutes |
| **Data backup** | Manual | Automatic ✅ |
| **Disk usage** | ~5GB locally | Only in Dropbox |
| **Multi-machine** | Copy to each | Works everywhere ✅ |
| **Data sync** | Manual | Auto-sync ✅ |
| **Simplicity** | Simpler | Better for teams ✅ |

---

### Troubleshooting

**If you get "ModuleNotFoundError":**
```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts
uv run python -m dittmann_maug.cli check-data
```

**If you get "Missing required files":**
- Check that `DM_DROPBOX_ROOT` is set correctly
- Verify parquet files exist in `$DM_DROPBOX_ROOT/execucomp/`
- Verify Dropbox is syncing (check Dropbox app)

**To check your environment variable:**
```bash
echo $DM_DROPBOX_ROOT
# Should print your Dropbox path
```

**To temporarily override:**
```bash
export DM_DROPBOX_ROOT="/different/path"
uv run python -m dittmann_maug.cli check-data
```

---

## 🧪 Test Commands

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

## 🐛 Troubleshooting

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

## 📦 Dependencies Installed

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

## ✨ What's Next?

1. ✅ **CLI working** - Can run check-data/inspect/stage1 commands
2. ⏭️ **Add data files** - Place ExecuComp parquet files in `DROPBOX/execucomp/`
3. ⏭️ **Test Stage 1** - Run with real data and verify outputs
4. ⏭️ **Implement Stage 2 & 3** - W0 calculation and option aggregation

---

**Generated:** February 10, 2026  
**Status:** Setup complete, ready for data integration
