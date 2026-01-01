# Restore Context: Repo Minder Modernization

**Last Updated:** 2026-01-01
**Status:** Planning Complete, Ready to Execute
**Branch:** main

---

## Quick Start (30 seconds)

```bash
# Navigate to project
cd ~/github/mitre/repo-minder

# View project overview
bd show repo-minder-8lv

# See what to work on next
bd ready

# Start working on first task
bd show repo-minder-hxh.1
```

---

## Where We Are

### ✅ Completed
- **Beads board initialized** - 30 tasks across 5 epics, all dependencies set
- **Full planning done** - MODERNIZATION_PLAN.md (500+ lines of specs)
- **Research complete** - Analyzed mitre/vulcan, mitre/heimdall2, mitre/train-k8s-container
- **Template variables identified** - All new variables documented
- **Design decisions made** - External templates, multi-file support, unified LICENSE.md

### 🎯 Next: Start Epic 1 - Modernize to 2025 Python Standards

**Epic 1 has 5 unblocked tasks ready to work on NOW:**

1. `repo-minder-hxh.1` - Update pyproject.toml (remove black, add semantic-release)
2. `repo-minder-hxh.2` - Upgrade Python requirement to 3.12+
3. `repo-minder-hxh.3` - Create .pre-commit-config.yaml
4. `repo-minder-hxh.4` - Update CI workflow to match guide standards
5. `repo-minder-hxh.5` - Design: External template support (P1 - docs only)

---

## Project Context

**What is this project?**
- Tool that standardizes LICENSE.md files across 240+ MITRE SAF repositories
- Currently at v1.0.0 - working, tested, production-ready
- Goal: Modernize to 2025 Python standards + add multi-file support

**What we're doing:**
- Bringing repo-minder up to modern Python standards (Python 3.12+, ruff-only, pre-commit)
- Adding automated release/publishing (semantic-release, PyPI)
- Creating documentation infrastructure (MkDocs, GitHub Pages)
- Extending to support multiple file types (SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md)

**Timeline:** 4-6 working days (~22-32 hours)

---

## Key Documents

| Document | Purpose |
|----------|---------|
| **MODERNIZATION_PLAN.md** | Complete implementation specs (500+ lines) |
| **PYTHON_PROJECT_SETUP_GUIDE.md** | 2025 Python standards reference |
| **ROADMAP.md** | Future features (v1.1.0+) |
| **repo-minder-8lv** (beads) | Project overview card |

---

## Epic Structure & Dependencies

```
Epic 1: Modernize to 2025 Python Standards (repo-minder-hxh) ← START HERE
    ↓ (blocks)
Epic 2: Documentation Infrastructure (repo-minder-rpb) ──┐
                                                          ├─→ Epic 4
Epic 3: Release & Publishing Automation (repo-minder-3r0) ┘
    ↓ (blocks)
Epic 4: Community Health & Multi-File Support (repo-minder-bn7)
    ↓ (blocks)
Epic 5: Future Features (repo-minder-vcn) - v1.1.0+
```

**Work order:**
1. Complete Epic 1 (all tasks ready now)
2. Epic 2 & 3 can be done in parallel
3. Epic 4 requires all previous epics complete
4. Epic 5 is future work

---

## Essential Beads Commands

```bash
# View project overview (full context)
bd show repo-minder-8lv

# See what's ready to work on
bd ready

# Show all tasks
bd list

# Show task details
bd show repo-minder-hxh.1

# Add comment/note to task
bd comment repo-minder-hxh.1 "Starting work on this"

# Mark task complete
bd close repo-minder-hxh.1

# Show epic details with dependencies
bd show repo-minder-hxh

# Sync board with git
bd sync
```

---

## Key Design Decisions (Important!)

1. **LICENSE.md is unified** - Combines Apache 2.0 + NOTICE content in ONE file
   - We do NOT create separate NOTICE.md
   - The `## Notice` section in LICENSE.md IS the notice

2. **CODE_OF_CONDUCT.md is identical** across all MITRE repos
   - Uses Contributor Covenant v2.1
   - Only variable: `{{ team_email }}`

3. **CHANGELOG.md is auto-generated** by release-please
   - We create initial structure only
   - release-please maintains it after that

4. **External templates use ChoiceLoader** pattern
   - User templates → Config dir templates → Bundled templates
   - Standard Jinja2 ecosystem pattern

---

## Template Variables

### Already in Settings
- organization, team, case_number, copyright_org, copyright_year
- org_office, org_address, org_phone

### New Variables to Add (Epic 4)
- `team_email` (saf@mitre.org) - General contact
- `security_email` (saf-security@mitre.org) - Security reporting
- `project_name` (auto-detect from pyproject.toml)
- `project_description` (auto-detect from pyproject.toml)

---

## Current State

### Git Status
- Branch: `main`
- Last commit: `205a475` - Remove Python bytecode files from tracking
- Status: Clean, all changes committed and pushed
- Beads: Synced with 30 tasks

### Files
- ✅ `.beads/` - Task tracker (30 tasks, git-tracked)
- ✅ `MODERNIZATION_PLAN.md` - Full implementation specs
- ✅ `PYTHON_PROJECT_SETUP_GUIDE.md` - 2025 standards reference
- ✅ `.gitignore` - Updated (ignores .claude/, CLAUDE.md, SESSION*.md, __pycache__)
- ✅ `AGENTS.md` - Beads workflow guide

### Tests
- 69 tests passing
- Coverage: Good
- CI: Passing (Python 3.8-3.12)

---

## When You Return

### Step 1: Get Context (2 minutes)
```bash
cd ~/github/mitre/repo-minder
bd show repo-minder-8lv          # Read overview
cat MODERNIZATION_PLAN.md        # Skim implementation details
```

### Step 2: Check What's Ready (30 seconds)
```bash
bd ready                         # See unblocked tasks
```

### Step 3: Start Working (Pick a task)
```bash
# Option A: Start with pyproject.toml update
bd show repo-minder-hxh.1
bd comment repo-minder-hxh.1 "Starting work"

# Option B: Start with Python version upgrade
bd show repo-minder-hxh.2
bd comment repo-minder-hxh.2 "Starting work"

# Option C: Start with pre-commit hooks
bd show repo-minder-hxh.3
bd comment repo-minder-hxh.3 "Starting work"
```

### Step 4: Reference Implementation Details
- Open `MODERNIZATION_PLAN.md`
- Go to "Phase 1: Epic 1" section (line ~280)
- Follow the detailed implementation specs

---

## Success Criteria (How to Know You're Done)

### Epic 1 Complete When:
- [ ] black removed from dependencies
- [ ] python-semantic-release added to build-system
- [ ] requires-python = ">=3.12"
- [ ] .pre-commit-config.yaml created and working
- [ ] CI updated (setup-uv@v7, ruff format, Python 3.12+3.13)
- [ ] All tests pass
- [ ] Pre-commit hooks pass

### Project Complete When:
- [ ] All 4 priority epics done (Epic 1-4)
- [ ] v1.1.0 released to PyPI
- [ ] Documentation live on GitHub Pages
- [ ] Community health files generated using repo-minder itself
- [ ] Close `repo-minder-8lv` overview card

---

## Contact Info (for generated files)

From analyzed MITRE repos:
- **Team email:** saf@mitre.org
- **Security email:** saf-security@mitre.org
- **Organization:** The MITRE Corporation
- **Case number:** 18-3678
- **Office:** Contracts Management Office
- **Address:** 7515 Colshire Drive, McLean, VA 22102-7539
- **Phone:** (703) 983-6000

---

## Troubleshooting

### "I forgot what we're doing"
→ Read `bd show repo-minder-8lv`

### "Where should I start?"
→ Run `bd ready` - Start with any task from Epic 1

### "What are the implementation details?"
→ Open `MODERNIZATION_PLAN.md`, go to Phase 1 section

### "How do I close a task?"
→ `bd close repo-minder-XXX`

### "How do I see dependencies?"
→ `bd show repo-minder-hxh` (shows what blocks this epic)

### "I need to sync the board"
→ `bd sync` (exports to git, pulls, imports)

---

## Quick Reference: Epic IDs

- **Epic 1:** repo-minder-hxh (Modernize to 2025 standards)
- **Epic 2:** repo-minder-rpb (Documentation)
- **Epic 3:** repo-minder-3r0 (Release automation)
- **Epic 4:** repo-minder-bn7 (Community health & multi-file)
- **Epic 5:** repo-minder-vcn (Future features)
- **Overview:** repo-minder-8lv (Project context)

---

## Remember

- **The board is the source of truth** - Everything tracked in beads
- **Documents are references** - MODERNIZATION_PLAN.md has full specs
- **Work order matters** - Epic 1 first, then 2+3 parallel, then 4
- **Close overview when done** - repo-minder-8lv stays open until project complete

---

**Ready to start? Run:** `bd ready`
