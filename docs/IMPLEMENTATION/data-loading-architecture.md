# 📂 Dropbox Data Loading Architecture

## Quick Answer

**Main Files Involved in Dropbox Data Loading:**

| File | Purpose |
|------|---------|
| **`src/py/dittmann_maug/config.py`** | 🔧 Settings & environment variable reading |
| **`src/py/dittmann_maug/io/paths.py`** | 📍 Path resolution for ExecuComp files |
| **`src/py/dittmann_maug/io/loaders.py`** | 📥 Parquet/CSV file reading |
| **`src/py/dittmann_maug/pipeline.py`** | 🔄 Orchestration (uses all above) |

---

## Data Loading Flow

### Step 1: Read Settings (`config.py`)

```python
# Location: src/py/dittmann_maug/config.py

class Settings:
    repo_root: Path
    dropbox_dirname: str = ".DROPBOX"
    
    def dropbox_root(self) -> Path:
        # Priority order:
        # 1. Check environment variable DM_DROPBOX_ROOT
        env = os.getenv("DM_DROPBOX_ROOT")
        if env:
            return Path(env).expanduser().resolve()
        
        # 2. Check for .DROPBOX/ folder in project
        preferred = self.repo_root / ".DROPBOX"
        if preferred.exists():
            return preferred
        
        # 3. Fall back to DROPBOX/ folder
        fallback = self.repo_root / "DROPBOX"
        return fallback
```

**What it does:**
- Reads `DM_DROPBOX_ROOT` environment variable (set in ~/.zshrc)
- Falls back to `.DROPBOX/` or `DROPBOX/` in project if env var not set
- Returns the root path to your Dropbox data folder

**Your current setting:**
```bash
DM_DROPBOX_ROOT=/Users/dhirajs/Dropbox/2026-dittman-maug-replication/data
```

---

### Step 2: Resolve Paths (`paths.py`)

```python
# Location: src/py/dittmann_maug/io/paths.py

class ExecuCompPaths:
    root: Path  # Points to execucomp/ subdirectory
    
    @property
    def anncomp(self) -> Path:
        return self.root / "anncomp.parquet"
    
    @property
    def codirfin(self) -> Path:
        return self.root / "codirfin.parquet"
    
    @property
    def coperol(self) -> Path:
        return self.root / "coperol.parquet"
    
    @property
    def stgrttab(self) -> Path:
        return self.root / "stgrttab.parquet"

def resolve_execucomp_dir(dropbox_root: Path) -> Path:
    # Looks for execucomp/ or ExecuComp/ subdirectory
    # Returns first one that exists
```

**Expected folder structure:**
```
$DM_DROPBOX_ROOT/
├── execucomp/
│   ├── anncomp.parquet         ✅ Required
│   ├── codirfin.parquet        ✅ Required
│   ├── coperol.parquet         (Optional)
│   └── stgrttab.parquet        (Optional, needed for Stage 3)
└── out/
    ├── stage1_contract_inputs_1995.parquet
    ├── stage1_contract_inputs_2000.parquet
    └── ... (other generated outputs)
```

**Your actual structure:**
```
/Users/dhirajs/Dropbox/2026-dittman-maug-replication/data/
├── execucomp/
│   ├── anncomp.parquet         ✅
│   ├── codirfin.parquet        ✅
│   └── ... other files
└── out/
    └── ... stage outputs
```

---

### Step 3: Load Data (`loaders.py`)

```python
# Location: src/py/dittmann_maug/io/loaders.py

def read_parquet(path: Path, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Read a parquet file using PyArrow."""
    if not path.exists():
        raise FileNotFoundError(f"Missing parquet file: {path}")
    return pd.read_parquet(path, columns=...)

def read_table_auto(path: Path, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Read parquet or CSV automatically based on file extension."""
    if path.suffix.lower() == ".parquet":
        return read_parquet(path, columns=columns)
    if path.suffix.lower() == ".csv":
        return read_csv(path, usecols=...)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all column names to lowercase."""
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df
```

**What it does:**
- Reads parquet or CSV files
- Handles missing files with clear error messages
- Normalizes column names to lowercase
- Uses PyArrow backend for fast parquet reading

---

### Step 4: Orchestrate Pipeline (`pipeline.py`)

```python
# Location: src/py/dittmann_maug/pipeline.py

def run_stage1(year: int, rf: float):
    # 1. Get settings and path resolution
    settings = Settings.from_env()
    dropbox_root = settings.dropbox_root()
    execucomp_dir = resolve_execucomp_dir(dropbox_root)
    
    # 2. Load data tables
    anncomp = read_parquet(execucomp_dir / "anncomp.parquet")
    codirfin = read_parquet(execucomp_dir / "codirfin.parquet")
    
    # 3. Normalize column names
    anncomp = normalize_columns(anncomp)
    codirfin = normalize_columns(codirfin)
    
    # 4. Build contract inputs
    result = build_stage1_contract_inputs(anncomp, codirfin, year, rf)
    
    # 5. Save output
    output_path = dropbox_root / "out" / f"stage1_contract_inputs_{year}.parquet"
    result.to_parquet(output_path)
```

---

## Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User's Environment                                          │
│ ~/.zshrc: export DM_DROPBOX_ROOT=/Users/dhirajs/Dropbox/...│
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ config.py                                                   │
│ - Read DM_DROPBOX_ROOT env variable                        │
│ - Return: /Users/dhirajs/Dropbox/2026.../data             │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ paths.py                                                    │
│ - Look for execucomp/ subdirectory                         │
│ - Return: /Users/dhirajs/Dropbox/2026.../data/execucomp   │
└──────────┬──────────────────────────────────────────────────┘
           │
           ├─────────────────┬──────────────────┐
           ▼                 ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ anncomp.pq   │  │ codirfin.pq  │  │ stgrttab.pq  │
    │  (370K rows) │  │  (137K rows) │  │ (needed for  │
    │              │  │              │  │  Stage 3)    │
    └──────────────┘  └──────────────┘  └──────────────┘
           │                 │                  │
           └────────┬────────┴──────────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ loaders.py             │
         │ - read_parquet()       │
         │ - normalize_columns()  │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ pipeline.py            │
         │ - run_stage1()         │
         │ - build_stage1_contract_inputs()
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Output: Parquet        │
         │ stage1_contract_inputs │
         │ _YYYY.parquet          │
         └────────────────────────┘
```

---

## How to Verify It's Working

### Test 1: Check Environment Variable
```bash
echo $DM_DROPBOX_ROOT
# Should output: /Users/dhirajs/Dropbox/2026-dittman-maug-replication/data
```

### Test 2: Check Data Files Exist
```bash
ls -lh $DM_DROPBOX_ROOT/execucomp/
# Should show: anncomp.parquet and codirfin.parquet
```

### Test 3: Run the Pipeline
```bash
cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts

# Check data loads correctly
uv run python -m dittmann_maug.cli check-data

# Inspect a year
uv run python -m dittmann_maug.cli inspect --year 2000

# Run Stage 1
uv run python -m dittmann_maug.cli stage1 --year 2000 --rf 0.0664
```

### Test 4: Verify Output Created
```bash
ls -lh $DM_DROPBOX_ROOT/out/
# Should show: stage1_contract_inputs_YYYY.parquet files
```

---

## Key Code Locations

### Loading Entry Point (CLI)
**File:** `src/py/dittmann_maug/cli.py`
```python
def stage1_command(args):
    pipeline.run_stage1(year=args.year, rf=args.rf)
```

### Stage 1 Pipeline
**File:** `src/py/dittmann_maug/pipeline.py`
- `run_stage1()` - Main orchestration
- Uses `config.py` for settings
- Uses `paths.py` for path resolution
- Uses `loaders.py` for data reading

### Contract Input Builder
**File:** `src/py/dittmann_maug/contracts/stage1_inputs.py`
- `build_stage1_contract_inputs()` - Constructs the 8 contract parameters
- Filters data (CEO exclusions, missing values)
- Calculates φ, nₛ, P₀, d, σ, rf, W₀, nₒ/K/T

---

## Troubleshooting

### "FileNotFoundError: Missing parquet file"
```
Problem: Data file not found
Solution:
  1. Check DM_DROPBOX_ROOT is set: echo $DM_DROPBOX_ROOT
  2. Check file exists: ls $DM_DROPBOX_ROOT/execucomp/anncomp.parquet
  3. Reload shell: source ~/.zshrc
```

### "Permission denied"
```
Problem: Can't read Dropbox folder
Solution:
  1. Check folder permissions: ls -ld $DM_DROPBOX_ROOT
  2. Make sure Dropbox is synced
  3. Check if path is correct
```

### "Parquet file corruption"
```
Problem: Data file is corrupted
Solution:
  1. Check file size: ls -lh $DM_DROPBOX_ROOT/execucomp/*.parquet
  2. Try reading with pandas: 
     pandas.read_parquet('path/to/file')
  3. Re-download from source if needed
```

---

## Summary

| Component | File | Role |
|-----------|------|------|
| **Environment** | `~/.zshrc` | Sets `DM_DROPBOX_ROOT` |
| **Settings** | `config.py` | Reads env variable, resolves path |
| **Path Resolution** | `paths.py` | Finds `execucomp/` subdirectory |
| **File Loading** | `loaders.py` | Reads parquet/CSV files |
| **Orchestration** | `pipeline.py` | Coordinates the flow |
| **CLI Entry** | `cli.py` | User-facing commands |

**Current Status:** ✅ All files configured and operational for Dropbox data loading

---

*Last Updated: February 10, 2026*
*Document Type: Technical Reference | AI-Generated*
