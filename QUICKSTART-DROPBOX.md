# 🚀 Quick Start: Dropbox Setup

## Easiest Way: Use the Setup Script

The project includes an automated setup script that configures your Dropbox path. Just run it once!

### Step 1: Run the Setup Script

```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts

# Run the setup script
./setup-dropbox-env.sh
```

### Step 2: Enter Your Dropbox Path

The script will ask you for your Dropbox path. For example:

```
Enter your Dropbox path to ExecuComp data:
/Users/dhirajs/Dropbox/Research/ExecuComp
```

Or just press **Enter** to use the default:
```
/Users/dhirajs/Dropbox/dittmann-maug-execucomp
```

### Step 3: Reload Your Shell

```bash
# If using zsh
source ~/.zshrc

# If using bash
source ~/.bashrc
```

### Step 4: Verify It Worked

```bash
# Check the environment variable
echo $DM_DROPBOX_ROOT

# Should print your Dropbox path
# /Users/dhirajs/Dropbox/Research/ExecuComp
```

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

