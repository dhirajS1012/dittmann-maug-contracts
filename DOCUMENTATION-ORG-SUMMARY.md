# DOCUMENTATION ORGANIZATION - QUICK SUMMARY

**Status:** 📋 TASK LIST CREATED - NO IMPLEMENTATION  

---

## PROFESSOR'S INSTRUCTION (One Sentence)

> "Organize docs better - PDFs should have a special directory separate from parsed notes/guides, making it clear for both humans and Claude what each document is."

---

## MAIN PROBLEMS

1. **PDF dumps mixed with docs** - `Core and Guay.md` is a binary PDF stored in docs/
2. **Unclear purposes** - references/ folder doesn't clearly say what goes there
3. **No distinction** between:
   - Raw PDFs (unprocessed)
   - Parsed notes (processed)
   - Research papers (markdown versions)
   - Implementation guides (how-to docs)
   - Project docs (status, roadmaps)
   - Data reference (specs)
4. **Confusing for search** - Humans and Claude both confused

---

## SOLUTION APPROACH

**Create organized structure:**
- `DROPBOX/pdf-dumps/` → Raw PDF files (not in git)
- `docs/RESEARCH/` → Research papers (markdown)
- `docs/REFERENCES/` → Data specifications
- `docs/IMPLEMENTATION/` → Implementation guides
- `docs/PROJECT/` → Project planning & status
- `docs/ADMIN/` → Internal documentation

---

## 18 TASKS (High Level)

| # | Task | What It Does |
|---|------|------------|
| 1 | Audit current structure | Understand what docs exist and where |
| 2 | Identify PDF dumps | Find binary PDFs stored as .md files |
| 3 | Plan new structure | Design the ideal organization |
| 4 | Create directories | Set up new folder structure |
| 5-10 | Move files | Organize docs by type into folders |
| 11 | Clean up | Remove empty old folders |
| 12 | Rename for consistency | Apply consistent naming conventions |
| 13 | Update links | Fix broken references in docs |
| 14 | Create README files | Add navigation/explanation files |
| 15 | Update agents.md | Document new structure |
| 16 | Update .gitignore | Ensure proper version control |
| 17 | Git commit | Save changes to repository |
| 18 | Verify | Confirm everything is correct |

---

## TIMELINE

- **Total time estimate:** 2.5-3 hours
- **Can be done in one session** (or split into multiple sessions)
- **Low risk** - Only file moves and renames (can be reverted if needed)

---

## CRITICAL DECISIONS NEEDED

Before I implement, I need your input on:

1. **Folder structure** - Agree with proposed 5-folder structure?
2. **Naming** - UPPERCASE folders or lowercase?
3. **PDF location** - DROPBOX/pdf-dumps/ is correct?
4. **Git handling** - Should DROPBOX/ be completely ignored?
5. **Any breaking changes?** - Scripts/imports that reference old paths?

---

## NEXT ACTION

1. ✅ **Task list created** - DOCUMENTATION-ORG-TASK-LIST.md
2. 👉 **Your review** - Read the task list and decide on the 5 decision points
3. ⏳ **My implementation** - Once you approve, I execute all 18 tasks

---

**File:** `DOCUMENTATION-ORG-TASK-LIST.md` (detailed task breakdown)  
**This file:** Quick summary reference

