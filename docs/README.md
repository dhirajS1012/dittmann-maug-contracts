# Documentation Index

This directory contains all project documentation organized by purpose and type.

---

## Structure Overview

```
docs/
├── RESEARCH/          ← Research papers (markdown conversions)
├── REFERENCES/        ← Data specifications and reference materials
├── IMPLEMENTATION/    ← Implementation guides, procedures, architecture
├── PROJECT/           ← Project planning, requirements, status, tasks
└── ADMIN/             ← Internal documentation, setup, reviews
```

---

## Folder Descriptions

### 📚 docs/RESEARCH/

**Purpose:** Original research papers converted to markdown  
**Contents:** Academic papers and theoretical foundations  
**Examples:**
- `dittman-maug-2007.md` - Core research paper on CEO compensation
- `dittman-maug-zhang-2011.md` - Extended research paper

**When to use:** Understanding the theoretical basis and methodology

---

### 📖 docs/REFERENCES/

**Purpose:** Data specifications and reference materials  
**Contents:** ExecuComp database documentation and data definitions  
**Examples:**
- `Execucomp_Data_Definitions.md` - Field definitions and data items
- `Execucomp_changes_2006_FAS_123_.md` - Changes in data reporting

**When to use:** Understanding data structures and specifications

---

### 🛠️ docs/IMPLEMENTATION/

**Purpose:** Implementation guides, procedures, and architecture  
**Contents:** How-to guides, step-by-step procedures, technical architecture  
**Examples:**
- `dittman-maug-contract-construction-procedure.md` - Contract construction steps
- `data-construction-manual.md` - Data processing manual
- `data-loading-architecture.md` - System architecture overview

**When to use:** Implementing features, understanding the system architecture

---

### 📋 docs/PROJECT/

**Purpose:** Project planning, requirements, status tracking  
**Contents:** Project-level documentation and task tracking  
**Examples:**
- `prd.md` - Project Requirement Document
- `implementation-roadmap.md` - Project timeline and phases
- `project-status.md` - Current project status and progress
- `todos-human.md` - Tasks for human team members

**When to use:** Planning work, tracking progress, understanding requirements

---

### ⚙️ docs/ADMIN/

**Purpose:** Internal documentation, configuration, reviews  
**Contents:** Setup guides, configuration notes, code reviews  
**Examples:**
- `setup.md` - Project setup instructions
- `stage1-output-summary.md` - Stage 1 implementation summary
- `code-review-20260210.md` - Code review notes
- `pyproject-explained.md` - Configuration explanation

**When to use:** Setting up environment, reviewing code, understanding configuration

---

## Document Types

### Research Papers
- Location: `docs/RESEARCH/`
- Format: Markdown (.md)
- Purpose: Theoretical foundation
- Version controlled: ✅ Yes (in git)

### Data Specifications
- Location: `docs/REFERENCES/`
- Format: Markdown (.md)
- Purpose: Reference information
- Version controlled: ✅ Yes (in git)

### Implementation Guides
- Location: `docs/IMPLEMENTATION/`
- Format: Markdown (.md)
- Purpose: How-to and procedures
- Version controlled: ✅ Yes (in git)

### Project Documentation
- Location: `docs/PROJECT/`
- Format: Markdown (.md)
- Purpose: Planning and tracking
- Version controlled: ✅ Yes (in git)

### Internal Documentation
- Location: `docs/ADMIN/`
- Format: Markdown (.md)
- Purpose: Setup and configuration
- Version controlled: ✅ Yes (in git)

### Raw PDFs
- Location: `DROPBOX/pdf-dumps/`
- Format: PDF (.pdf)
- Purpose: Raw reference materials
- Version controlled: ❌ No (.gitignore)

---

## Quick Navigation

**I need to...**
- Understand the theory → See `docs/RESEARCH/`
- Look up data fields → See `docs/REFERENCES/`
- Implement a feature → See `docs/IMPLEMENTATION/`
- Check project status → See `docs/PROJECT/`
- Set up my environment → See `docs/ADMIN/setup.md`

---

## Adding New Documentation

When adding documentation, place it in the appropriate folder:

| Document Type | Folder | Example |
|---|---|---|
| Research paper | RESEARCH/ | `my-paper.md` |
| Data specification | REFERENCES/ | `new-data-spec.md` |
| Implementation guide | IMPLEMENTATION/ | `feature-guide.md` |
| Project status/plan | PROJECT/ | `quarterly-plan.md` |
| Internal notes | ADMIN/ | `review-notes.md` |
| Raw PDF | DROPBOX/pdf-dumps/ | `Author-Year.pdf` |

---

## Naming Conventions

- **Folders:** UPPERCASE (RESEARCH, REFERENCES, IMPLEMENTATION, PROJECT, ADMIN)
- **Files:** lowercase-with-hyphens.md (except for files with existing names)
- **PDFs:** lowercase-with-hyphens-year.pdf (e.g., core-and-guay-2002.pdf)

---

## Version Control

**In git (version controlled):**
- ✅ docs/RESEARCH/
- ✅ docs/REFERENCES/
- ✅ docs/IMPLEMENTATION/
- ✅ docs/PROJECT/
- ✅ docs/ADMIN/

**Not in git (.gitignore):**
- ❌ DROPBOX/ (raw materials, not shared via git)
- ❌ output/ (generated results)
- ❌ data/raw/ (data files)

---

## Future Enhancements

- **rclone sync:** Will synchronize DROPBOX/ with actual Dropbox cloud
- **Wiki generation:** May generate HTML wiki from markdown docs
- **Full-text search:** Will implement searchable documentation index
- **Versioning:** Will track documentation changes over time

---

For questions about document organization, refer to `agents.md` "Documentation Organization" section.

