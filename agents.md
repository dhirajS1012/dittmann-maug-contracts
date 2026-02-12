# Agents (AI Generated)

This file will document the roles and responsibilities of various agents involved in the project, including human and AI agents, their specific tasks, and interaction protocols.

## AI Agent (Current Instance)

*   **Role:** Facilitator for project setup, documentation generation, code analysis, and future implementation.
*   **Responsibilities:**
    *   Generate initial project documentation and plan drafts.
    *   Analyze existing research papers and code to extract methodologies.
    *   Translate methodologies into detailed procedural documents.
    *   Assist in setting up the Python development environment.
    *   Implement Python code for data processing and contract construction.
    *   Develop and execute tests to ensure replication accuracy.
    *   Maintain adherence to project conventions (e.g., file paths, naming, style).
    *   Provide clear and concise communication regarding progress, challenges, and proposed solutions.
*   **Operating Principles:**
    *   Prioritize thorough planning and reporting before action.
    *   Flag all AI-generated documentation at the top.
    *   Flag all AI-generated commit messages with "(model)" at the end.
    *   **Code Location:** Python files are located in `src/py/`.
    *   **Script Execution:** All scripts are run from the project root directory.
    *   **Data Storage:** 
        *   Input data: `data/raw/execucomp/` (local, .gitignore'd)
        *   Generated outputs: `output/` (local, .gitignore'd)
        *   Raw PDFs: `DROPBOX/pdf-dumps/` (local, .gitignore'd)
    *   **Documentation Organization:** See "Documentation Structure" section below for folder organization
    *   Utilize `uv` for Python package management.
    *   Strive for replication accuracy and code quality.

## Important Project Documentation

*   `docs/README.md`: Documentation index and navigation guide
*   `docs/PROJECT/prd.md`: Project Requirement Document (draft)
*   `agents.md`: Roles and responsibilities for human and AI agents
*   `docs/RESEARCH/dittman-maug-2007.md`: Markdown version of the core research paper
*   `docs/REFERENCES/Execucomp_Data_Definitions.md`: Detailed definitions of ExecuComp data items
*   `docs/REFERENCES/Execucomp_changes_2006_FAS_123_.md`: Information on changes in ExecuComp reporting
*   `docs/IMPLEMENTATION/dittman-maug-contract-construction-procedure.md`: CEO compensation contract construction procedure
*   `DROPBOX/pdf-dumps/Core-and-Guay-2002.pdf`: Raw PDF of Core and Guay research article

---

## Documentation Structure

The project documentation is organized by purpose into 5 main folders:

**docs/RESEARCH/** - Research papers (markdown conversions)
- `dittman-maug-2007.md` - Primary research paper
- `dittman-maug-zhang-2011.md` - Extended research paper

**docs/REFERENCES/** - Data specifications and reference materials
- ExecuComp database documentation
- Data item definitions and changes

**docs/IMPLEMENTATION/** - Implementation guides and architecture
- Contract construction procedures
- Data construction manuals
- System architecture documentation

**docs/PROJECT/** - Project planning and status
- Project requirements document (prd.md)
- Implementation roadmap
- Project status tracking
- Human task lists

**docs/ADMIN/** - Internal documentation
- Setup instructions
- Code reviews
- Configuration explanations

**DROPBOX/pdf-dumps/** - Raw PDF materials (not version controlled)
- Original research articles
- Reference PDFs
- Non-processed materials

### Principles

- **Raw PDFs:** Stored in `DROPBOX/pdf-dumps/`, not in version control (.gitignore'd)
- **Processed docs:** Stored in `docs/` subdirectories, version controlled (in git)
- **Clear naming:** Folder names indicate content purpose
- **Searchability:** Organization supports both human navigation and AI (Claude) semantic search
- **Future:** Will use rclone to sync DROPBOX/ with cloud Dropbox

For detailed documentation, see `docs/README.md`.

