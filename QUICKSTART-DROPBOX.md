# 🚀 Quick Start: Dropbox Setup

⚠️ **Note:** Dropbox is already set up and operational! This guide is for reference if you need to change the path.

**Current Status:**
- ✅ Dropbox path configured: `/Users/dhirajs/Dropbox/2026-dittman-maug-replication/data`
- ✅ Environment variable: `DM_DROPBOX_ROOT` (in ~/.zshrc)
- ✅ Pipeline working (67 CEOs from 1995, 36 CEOs from 2000)

---

## If You Need to Change the Dropbox Path

### Easiest Way: Use the Setup Script

The project includes an automated setup script that reconfigures your Dropbox path if needed.

```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts
./setup-dropbox-env.sh
```

Then reload: `source ~/.zshrc` (or `~/.bashrc`)

---

## Now You're Ready!

### Test the CLI:

```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts

# Check data files
uv run python -m dittmann_maug.cli check-data

# Run Stage 1 when data is ready
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

---

## Manual Setup (If You Prefer)

If you don't want to use the script, here's the manual way:

### For zsh users:

```bash
# Open/edit your shell config
nano ~/.zshrc

# Add this line at the end:
export DM_DROPBOX_ROOT="/Users/dhirajs/Dropbox/your-path-here"

# Save and reload
source ~/.zshrc
```

### For bash users:

```bash
# Open/edit your shell config
nano ~/.bashrc

# Add this line at the end:
export DM_DROPBOX_ROOT="/Users/dhirajs/Dropbox/your-path-here"

# Save and reload
source ~/.bashrc
```

---

## Expected Data Structure

Your Dropbox folder should have this structure:

```
/Users/dhirajs/Dropbox/Research/ExecuComp/
├── execucomp/
│   ├── anncomp.parquet               # ✅ Required
│   ├── codirfin.parquet              # ✅ Required
│   ├── coperol.parquet               # Optional
│   └── stgrttab.parquet              # Optional (needed for Stage 3)
└── out/
    ├── stage1_contract_inputs_2000.parquet
    └── ... (generated outputs)
```

---

## Troubleshooting

### "DM_DROPBOX_ROOT not set"

```bash
# Check if environment variable is set
echo $DM_DROPBOX_ROOT

# If empty, run:
source ~/.zshrc   # or ~/.bashrc
```

### "Missing required files"

```bash
# Check if path is correct
ls -la $DM_DROPBOX_ROOT/execucomp/

# Should see:
# anncomp.parquet
# codirfin.parquet
```

### "Dropbox is syncing"

The files might not be downloaded yet. Check your Dropbox app to ensure they're syncing.

---

## Done! ✅

Your Dropbox is now configured. The project will automatically use it for all data operations!

Run any command from the project directory:

```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts
uv run python -m dittmann_maug.cli stage1 --year 2000
```

