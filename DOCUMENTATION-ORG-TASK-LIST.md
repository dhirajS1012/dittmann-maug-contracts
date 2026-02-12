# DOCUMENTATION ORGANIZATION - TASK LIST

**Date:** February 12, 2026  
**Status:** 📋 TASK LIST ONLY - NO IMPLEMENTATION  
**Based on:** Professor's instruction to organize docs better

---

## PROFESSOR'S INSTRUCTION (Summarized)

> "Organize docs better. docs/Core and Guay.md is a PDF dump for LLMs (good but should have special directory for PDF dumps so it's not confusing). References folder was supposed to be for parsed PDF dumps but has AI notes on Core and Guay. All these docs have to be organized - it's confusing for both us and Claude to search."

### Key Problems Identified:
1. **PDF dumps mixed with regular docs** - `Core and Guay.md` is a binary PDF stored as .md in docs/
2. **Unclear folder purposes** - `references/` doesn't clearly indicate what belongs there
3. **No clear distinction** between:
   - Raw PDF materials
   - Parsed/analyzed notes
   - Research papers
   - Implementation guides
4. **Searchability issues** - Both humans and Claude (AI) confused by unclear organization

---

## TASK LIST

### TASK 1: Audit Current Documentation Structure
**Description:** Understand what documentation exists and its current location  
**Subtasks:**
- [ ] List all .md files in docs/ directory with their purposes
- [ ] List all .md files in root directory with their purposes
- [ ] Identify file types:
  - Research papers (markdown conversions of articles)
  - PDF dumps (binary PDFs stored as .md files)
  - Parsed notes (AI-generated summaries/notes)
  - Implementation guides (how-to documents)
  - Project documentation (PRD, roadmaps, status)
  - Data reference materials (ExecuComp specs)
- [ ] Check if DROPBOX/ directory exists and what it contains
- [ ] Verify .gitignore settings for non-versioned files

---

### TASK 2: Identify PDF Dumps
**Description:** Find all binary PDF files masquerading as .md files  
**Subtasks:**
- [ ] Confirm `docs/Core and Guay.md` is a binary PDF (check file header: %PDF-1.2)
- [ ] Search for other potential PDF dumps in docs/
- [ ] Check what the correct source/title is for Core and Guay PDF
- [ ] Note any other PDFs that need to be separated

---

### TASK 3: Plan New Documentation Structure
**Description:** Design the ideal organization for all documentation  
**Subtasks:**
- [ ] Decide on folder structure (e.g., separate for PDFs vs. docs)
- [ ] Define purpose of each folder:
  - Where do raw PDFs go?
  - Where do parsed notes go?
  - Where do research papers go?
  - Where do implementation guides go?
  - Where do project docs go?
  - Where do data references go?
- [ ] Decide naming conventions for files and folders
- [ ] Ensure structure is intuitive for humans AND searchable for Claude

---

### TASK 4: Create Directory Structure
**Description:** Set up new folders for organized documentation  
**Subtasks:**
- [ ] Create `DROPBOX/pdf-dumps/` for raw PDF files (or decide on alternative location)
- [ ] Create subdirectories in docs/ for each documentation type
  - Example options:
    - `docs/RESEARCH/` for research papers
    - `docs/REFERENCES/` for data specs
    - `docs/IMPLEMENTATION/` for how-to guides
    - `docs/PROJECT/` for project management docs
    - `docs/ADMIN/` for internal documentation
- [ ] Ensure .gitignore properly ignores DROPBOX/ directory

---

### TASK 5: Move PDF Dumps
**Description:** Move binary PDF files to dedicated directory  
**Subtasks:**
- [ ] Move `docs/Core and Guay.md` to DROPBOX/pdf-dumps/ directory
- [ ] Rename with appropriate naming:
  - Change .md extension to .pdf
  - Use clear, searchable name (e.g., Core-and-Guay-2002.pdf)
- [ ] Move any other identified PDF dumps
- [ ] Verify they're in .gitignore (not tracked by git)

---

### TASK 6: Organize Research Papers
**Description:** Move markdown conversions of research papers to RESEARCH folder  
**Subtasks:**
- [ ] Identify which files are research paper conversions
  - dittman-maug-2007.md (appears to be in docs/references/)
  - dittman-maug-zhang-2011.md (appears to be in docs/references/)
- [ ] Move to docs/RESEARCH/ or designated research folder
- [ ] Verify file organization is clear

---

### TASK 7: Organize Reference Materials
**Description:** Move data specifications and reference materials to REFERENCES folder  
**Subtasks:**
- [ ] Move ExecuComp documentation to docs/REFERENCES/ or similar
  - Execucomp_Data_Definitions.md
  - Execucomp_changes_2006_FAS_123_.md
- [ ] Ensure folder name clearly indicates these are DATA/REFERENCE materials
- [ ] Keep these in version control (unlike PDFs)

---

### TASK 8: Organize Implementation Guides
**Description:** Move how-to guides and architecture docs to IMPLEMENTATION folder  
**Subtasks:**
- [ ] Move implementation guides to docs/IMPLEMENTATION/ or similar:
  - dittman-maug-contract-construction-procedure.md
  - DATA-CONSTRUCTION-MANUAL.md
  - DATA-LOADING-ARCHITECTURE.md
- [ ] Ensure folder name clearly indicates these are IMPLEMENTATION guides
- [ ] Keep these in version control

---

### TASK 9: Organize Project Documentation
**Description:** Move project management and planning docs to PROJECT folder  
**Subtasks:**
- [ ] Move project documentation to docs/PROJECT/ or similar:
  - prd.md (Project Requirements Document)
  - implementation-roadmap.md
  - PROJECT-STATUS.md
  - TODOS-HUMAN.md
- [ ] Ensure folder name clearly indicates these are PROJECT docs
- [ ] Keep these in version control

---

### TASK 10: Organize Admin/Internal Docs
**Description:** Move internal documentation to ADMIN folder  
**Subtasks:**
- [ ] Move internal/admin docs to docs/ADMIN/ or similar:
  - SETUP.md
  - STAGE1-OUTPUT-SUMMARY.md
  - code-review files
  - PYPROJECT-EXPLAINED.md
- [ ] Ensure folder name clearly indicates these are internal
- [ ] Keep these in version control

---

### TASK 11: Clean Up Empty Folders
**Description:** Remove old folder structures that are no longer needed  
**Subtasks:**
- [ ] Remove old `docs/references/` if all files have been moved
- [ ] Remove old `docs/execucomp-docs/` if all files have been moved
- [ ] Verify no empty folders remain (except new structure)

---

### TASK 12: Rename Files for Consistency
**Description:** Apply consistent naming conventions across all documentation  
**Subtasks:**
- [ ] Decide on naming convention:
  - Lowercase? Uppercase? Mixed?
  - Hyphens for spacing? Underscores?
- [ ] Rename files to follow convention (e.g., `SETUP.md` → `setup.md`)
- [ ] Ensure rename doesn't break any internal links/references

---

### TASK 13: Update Documentation Links
**Description:** Fix any internal references that point to moved files  
**Subtasks:**
- [ ] Check README.md for links to moved files
- [ ] Check agents.md for links to moved files
- [ ] Check any other docs that reference specific file paths
- [ ] Update all broken links to point to new locations

---

### TASK 14: Create Index/Navigation Files
**Description:** Add README files to help navigate the new structure  
**Subtasks:**
- [ ] Create `docs/README.md` explaining the structure:
  - What's in each folder
  - When to look in each folder
  - How to add new documentation
- [ ] Create `DROPBOX/README.md` explaining:
  - This is for raw PDFs and unprocessed materials
  - Not version controlled
  - How to add new PDFs
- [ ] Create folder-level README files if helpful

---

### TASK 15: Update agents.md
**Description:** Update agent responsibilities to reflect new documentation structure  
**Subtasks:**
- [ ] Add "Documentation Organization" section to agents.md
- [ ] Document the new folder structure
- [ ] Explain where different types of docs belong
- [ ] Update any references to old DROPBOX/ locations
- [ ] Clarify DROPBOX/ is only for PDFs, not processed docs

---

### TASK 16: Update .gitignore
**Description:** Ensure proper version control of organized files  
**Subtasks:**
- [ ] Verify DROPBOX/ is in .gitignore (PDFs should not be versioned)
- [ ] Verify docs/ is NOT ignored (markdown docs should be versioned)
- [ ] Verify any temporary files/folders are ignored

---

### TASK 17: Create Git Commit
**Description:** Commit the reorganization to version control  
**Subtasks:**
- [ ] Stage all moved/renamed files
- [ ] Create clear commit message explaining the reorganization
- [ ] Commit with message like: "docs: Reorganize documentation by purpose and type (model)"
- [ ] Push to GitHub

---

### TASK 18: Verify Final Organization
**Description:** Confirm the reorganization is complete and correct  
**Subtasks:**
- [ ] List final directory structure
- [ ] Verify all files are in correct locations
- [ ] Verify no files are missing
- [ ] Verify no orphaned empty folders remain
- [ ] Test that Claude can search docs effectively
- [ ] Get team feedback if needed

---

## SUMMARY TABLE

| Task # | Task Name | Complexity | Time | Dependencies |
|--------|-----------|-----------|------|--------------|
| 1 | Audit Current Structure | Low | 10 min | None |
| 2 | Identify PDF Dumps | Low | 5 min | Task 1 |
| 3 | Plan New Structure | Medium | 15 min | Task 1, 2 |
| 4 | Create Directory Structure | Low | 5 min | Task 3 |
| 5 | Move PDF Dumps | Low | 5 min | Task 3, 4 |
| 6 | Organize Research Papers | Low | 5 min | Task 3, 4 |
| 7 | Organize Reference Materials | Low | 5 min | Task 3, 4 |
| 8 | Organize Implementation Guides | Low | 5 min | Task 3, 4 |
| 9 | Organize Project Documentation | Low | 5 min | Task 3, 4 |
| 10 | Organize Admin/Internal Docs | Low | 5 min | Task 3, 4 |
| 11 | Clean Up Empty Folders | Low | 3 min | Task 5-10 |
| 12 | Rename Files for Consistency | Medium | 10 min | Task 5-11 |
| 13 | Update Documentation Links | Medium | 10 min | Task 12 |
| 14 | Create Index/Navigation Files | Medium | 15 min | Task 3, 13 |
| 15 | Update agents.md | Low | 10 min | Task 3, 14 |
| 16 | Update .gitignore | Low | 5 min | Task 5 |
| 17 | Create Git Commit | Low | 5 min | Task 5-16 |
| 18 | Verify Final Organization | Low | 10 min | Task 17 |
| **TOTAL** | | | **~168 min (2.8 hrs)** | |

---

## ESTIMATED EFFORT

- **Simple Tasks (1-2, 4-11, 16):** ~45 minutes
- **Medium Tasks (3, 12-15, 18):** ~70 minutes
- **Buffer for issues:** ~15 minutes
- **TOTAL:** ~2.5-3 hours

---

## DECISION POINTS NEEDED

Before implementation, clarify:

1. **Folder Structure?**
   - Should DROPBOX/ be in project root or elsewhere?
   - Should docs have 5 subfolders (RESEARCH, REFERENCES, IMPLEMENTATION, PROJECT, ADMIN)?
   - Or different structure?

2. **Naming Convention?**
   - Uppercase folder names (RESEARCH, ADMIN)?
   - Lowercase file names (setup.md, not SETUP.md)?
   - Hyphens or underscores?

3. **PDF Location?**
   - DROPBOX/pdf-dumps/?
   - docs/pdf-dumps/?
   - Different location?

4. **Version Control?**
   - Should DROPBOX/ be completely ignored by git?
   - Or selectively ignored?

5. **Backward Compatibility?**
   - Any scripts/code that reference old file paths?
   - Need to update imports or references?

---

## NEXT STEPS

1. ✅ **This task list** - Provided without implementation
2. ⏳ **Review & Approve** - You review and provide decisions on decision points above
3. ⏳ **Implementation** - Once approved, execute all 18 tasks in order
4. ⏳ **Verification** - Confirm final organization is correct

---

**Status:** 📋 TASK LIST COMPLETE - AWAITING APPROVAL TO PROCEED

