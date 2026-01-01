# Repo Minder Modernization Plan

**Project:** repo-minder (formerly license-standardizer)
**Date:** 2026-01-01
**Status:** Planning Phase
**Tracked in:** beads (.beads/)

---

## Executive Summary

This document consolidates the complete modernization plan for repo-minder, bringing it up to 2025 Python standards while adding multi-file community health support. The work is organized into 4 priority epics with clear dependencies and work order.

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Gap Analysis](#gap-analysis)
3. [Template Variables & Patterns](#template-variables--patterns)
4. [Epic Structure & Work Order](#epic-structure--work-order)
5. [Implementation Details](#implementation-details)
6. [Success Criteria](#success-criteria)

---

## Current State Analysis

### What We Have (v1.0.0)

**Working Features:**
- ✅ LICENSE.md standardization across 240+ MITRE SAF repos
- ✅ Three template types (CIS, DISA, Plain) with Jinja2 inheritance
- ✅ Automatic template detection based on repo naming
- ✅ Interactive CLI with Typer + Rich + Questionary
- ✅ 5 safety layers (validation, confirmation, backup, analysis, sanity checks)
- ✅ 69 passing tests (contract/component levels)
- ✅ Modern Python stack (uv, Typer, Rich, Jinja2, Pydantic Settings)
- ✅ CI/CD with uv (all passing)
- ✅ Parallel verification (20 workers)

**Unique Design Decision:**
- ✅ **Unified LICENSE.md** - Combines Apache 2.0 license + NOTICE content in single file
  - `## License` - Apache 2.0 text
  - `## Redistribution Terms` - Distribution conditions
  - `## Notice` - Government contract info (replaces separate NOTICE.md)
  - `## Third-Party Content` - CIS/DISA acknowledgments (for applicable repos)

**Current Files:**
- `repo_minder.py` (880 lines, main CLI)
- `pyproject.toml` (uv-based packaging)
- `.github/workflows/ci.yml` (test/lint/security)
- `templates/` (LICENSE templates: base.j2, cis.j2, disa.j2, plain.j2)
- `tests/` (69 tests, comprehensive coverage)
- `README.md`, `LICENSE.md`, `ROADMAP.md`

### Research: MITRE Repo Patterns

**Repos Analyzed:**
- mitre/vulcan (SECURITY, CODE_OF_CONDUCT, CONTRIBUTING, CHANGELOG)
- mitre/heimdall2 (CODE_OF_CONDUCT, CHANGELOG)
- mitre/train-k8s-container (ALL 5 FILES - complete reference)

**Key Findings:**
1. **CODE_OF_CONDUCT.md** - 100% identical across all repos (Contributor Covenant v2.1)
2. **SECURITY.md** - Highly similar structure (reporting, timeline, recommendations)
3. **CONTRIBUTING.md** - Similar structure, varies by tech stack (Ruby/Python/JS)
4. **NOTICE.md** - **NOT NEEDED** (we unified it into LICENSE.md)
5. **CHANGELOG.md** - **AUTO-GENERATED** (release-please, not templated)

---

## Gap Analysis

### Missing: Modern Python Standards

**From PYTHON_PROJECT_SETUP_GUIDE.md:**

1. ❌ **Black still present** - Should remove, use ruff-only for formatting
2. ❌ **Python 3.8 minimum** - Should be 3.12+ (2025 standard)
3. ❌ **No pre-commit hooks** - Missing `.pre-commit-config.yaml`
4. ❌ **CI workflow outdated** - Uses `black --check`, should use `ruff format --check`
5. ❌ **CI references wrong file** - `standardize_licenses.py` → should be `repo_minder.py`
6. ❌ **Missing setup-uv@v7** - Currently using v5

### Missing: Documentation Infrastructure

1. ❌ **No docs/ directory** - Need MkDocs documentation
2. ❌ **No mkdocs.yml** - Need Material theme configuration
3. ❌ **No docs workflow** - Need `.github/workflows/docs.yml`
4. ❌ **No GitHub Pages** - Need deployment configuration

### Missing: Release Automation

1. ❌ **Manual versioning** - `version = "1.0.0"` in pyproject.toml
2. ❌ **No semantic-release** - Need python-semantic-release configuration
3. ❌ **No release workflow** - Need `.github/workflows/release.yml`
4. ❌ **No PyPI publishing** - Need trusted publisher setup
5. ❌ **No CHANGELOG automation** - Need release-please integration

### Missing: Community Health Files

1. ❌ **No SECURITY.md** - Security policy and vulnerability reporting
2. ❌ **No CODE_OF_CONDUCT.md** - Community standards
3. ❌ **No CONTRIBUTING.md** - Developer workflow and guidelines
4. ❌ **README.md needs badges** - PyPI, Python version, CI, coverage, license

### Opportunity: Multi-File Support

**Roadmap v1.1.0 Feature** - Extend tool beyond LICENSE to all community health files

**Dog-fooding opportunity:** Use repo-minder itself to create/maintain these files!

---

## Template Variables & Patterns

### Existing Variables (Already in Settings)

```python
# From current repo_minder.py Settings class
organization: str = "mitre"                    # GitHub org
team: str = "saf"                              # Team name
case_number: str = "18-3678"                   # Public release case number
copyright_org: str = "The MITRE Corporation"   # Copyright holder
copyright_year: int = 2025                     # Current year (auto)
org_office: str = "Contracts Management Office"
org_address: str = "7515 Colshire Drive, McLean, VA 22102-7539"
org_phone: str = "(703) 983-6000"
```

### New Variables Needed

```python
# Contact Information
team_email: str = Field(
    default="saf@mitre.org",
    description="General team contact email"
)
security_email: str = Field(
    default="saf-security@mitre.org",
    description="Security vulnerability reporting email"
)

# Project Information (extract from pyproject.toml)
project_name: str = Field(
    default=None,  # Auto-detect from pyproject.toml
    description="Project name"
)
project_description: str = Field(
    default=None,  # Auto-detect from pyproject.toml
    description="Project description"
)
github_url: str = Field(
    default=None,  # Construct from organization + project_name
    description="GitHub repository URL"
)

# Optional: Federal Contract Info
contract_number: Optional[str] = Field(
    default=None,
    description="Federal contract number (if applicable)"
)
```

### Template Structure

#### Current (LICENSE only)
```
templates/
└── LICENSE/
    ├── base.j2          # Apache 2.0 + Notice
    ├── cis.j2           # Extends base, adds CIS acknowledgment
    ├── disa.j2          # Extends base, adds DISA acknowledgment
    └── plain.j2         # Extends base, no third-party content
```

#### Proposed (Multi-file support)
```
templates/
├── LICENSE/
│   ├── base.j2
│   ├── cis.j2
│   ├── disa.j2
│   └── plain.j2
├── CODE_OF_CONDUCT.md          # Static (identical across all MITRE repos)
├── SECURITY.md.j2              # Template with {{ security_email }}, {{ team_email }}
├── CONTRIBUTING/
│   ├── base.md.j2              # Common sections
│   ├── python.md.j2            # Python-specific workflow
│   ├── ruby.md.j2              # Ruby-specific workflow
│   └── javascript.md.j2        # JS-specific workflow
└── CHANGELOG.md.j2             # Initial structure only (release-please updates)
```

### Template Patterns Discovered

#### 1. CODE_OF_CONDUCT.md - Static (No Variables)

**100% identical** across all MITRE repos analyzed.

```markdown
# Contributor Covenant Code of Conduct

[Standard Contributor Covenant v2.1 text]

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project team at {{ team_email }}.

[Full text: https://www.contributor-covenant.org/version/2/1/code_of_conduct/]
```

**Template variables:**
- `{{ team_email }}` - Contact for violations

**Implementation:** Single static template with one variable.

#### 2. SECURITY.md - Structured Template

**Highly similar** structure across repos with these sections:

```markdown
# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities to {{ security_email }}.

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- Acknowledgment: 48 hours
- Initial assessment: 7 days
- Fix timeline: Based on severity

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| {{ current_major }}.x.x | :white_check_mark: |
| < {{ current_major }}.0.0 | :x:              |

## Security Best Practices

[Project-specific recommendations]

## Contact

Security issues: {{ security_email }}
General questions: {{ team_email }}
```

**Template variables:**
- `{{ security_email }}`
- `{{ team_email }}`
- `{{ current_major }}` - Current major version (from pyproject.toml)
- `{{ project_name }}`

**Implementation:** Single template with optional sections.

#### 3. CONTRIBUTING.md - Tech Stack Dependent

**Base structure** (common to all):
- Getting Started
- How to Contribute
- Code Standards
- Testing Requirements
- Pull Request Process
- Community Standards

**Tech-specific sections** (varies):
- **Python:** pytest, ruff, black/ruff-format, mypy
- **Ruby:** RSpec, RuboCop, bundle install
- **JavaScript:** npm/yarn, ESLint, Jest/Mocha

```markdown
# Contributing to {{ project_name }}

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch

## Development Setup

{% block setup %}
# Python projects
pip install -e ".[dev]"
pytest

# Ruby projects
bundle install
bundle exec rspec
{% endblock %}

## Code Standards

{% block linting %}
# Python
ruff check .
ruff format .

# Ruby
bundle exec rubocop
{% endblock %}

## Testing

{% block testing %}
# Project-specific test commands
{% endblock %}

## Pull Request Process

1. Update documentation
2. Add tests
3. Run linting and tests
4. Push and create PR

## Commit Message Format

Use conventional commits:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Tests
- chore: Maintenance

## Contact

Questions: {{ team_email }}
```

**Template variables:**
- `{{ project_name }}`
- `{{ team_email }}`
- Tech stack detection (Python/Ruby/JS)

**Implementation:** Base template with tech-specific blocks.

#### 4. CHANGELOG.md - Initial Structure Only

**NOT actively templated** - Auto-generated by release-please.

Our role: Create initial structure, then release-please maintains it.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- Release notes generated by release-please will go here -->

## [{{ version }}] - {{ date }}

### Added
- Initial release
- [Features from SESSION01.md or project docs]
```

**Template variables:**
- `{{ version }}` - From pyproject.toml
- `{{ date }}` - Current date

**Implementation:** One-time initialization, then hands off to release-please.

### External Template Support Pattern

**Research finding:** Jinja2 ecosystem standard pattern uses **ChoiceLoader**.

```python
from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader

# User templates override bundled templates
loaders = []

# Priority 1: User-specified custom templates
if custom_dir:
    loaders.append(FileSystemLoader(custom_dir))

# Priority 2: User config directory
config_dir = Path.home() / ".config" / "repo-minder" / "templates"
if config_dir.exists():
    loaders.append(FileSystemLoader(str(config_dir)))

# Priority 3: Bundled package templates (fallback)
loaders.append(PackageLoader("repo_minder", "templates"))

env = Environment(loader=ChoiceLoader(loaders))
```

**CLI pattern:**
```bash
# Use custom templates
repo-minder --template-dir ~/.config/repo-minder/templates --file-type security
```

**Real-world examples:** Cookiecutter, Copier, Datasette, Ansible

---

## Epic Structure & Work Order

### Overview

4 Priority Epics organized by dependencies:

```
Epic 1: Modernize to 2025 Python Standards (Foundation)
    ↓
Epic 2: Documentation Infrastructure (Parallel with 3)
    ↓
Epic 3: Release & Publishing Automation (Requires 1)
    ↓
Epic 4: Community Health & Multi-File Support (Dog-food it!)
    ↓
Epic 5: Future Features (v1.1.0+)
```

### Epic 1: Modernize to 2025 Python Standards (P0)

**ID:** repo-minder-hxh
**Priority:** P0 (Foundation for all other work)
**Estimated effort:** 4-6 hours

**Why first:** Must establish modern tooling before adding features.

**Tasks:**
1. **repo-minder-hxh.1** - Update pyproject.toml: Remove black, add semantic-release config
2. **repo-minder-hxh.2** - Upgrade Python requirement to 3.12+
3. **repo-minder-hxh.3** - Create .pre-commit-config.yaml
4. **repo-minder-hxh.4** - Update CI workflow to match guide standards
5. **repo-minder-hxh.5** - Design: External template support (P1 - documentation only)

**Dependencies:** None (blocking others)

**Deliverables:**
- Updated pyproject.toml (no black, has semantic-release)
- Python 3.12+ requirement
- Working pre-commit hooks
- Modernized CI workflow
- External template design doc

### Epic 2: Documentation Infrastructure (P0)

**ID:** repo-minder-rpb
**Priority:** P0 (Parallel with Epic 3)
**Estimated effort:** 6-8 hours

**Why second:** Can work in parallel with Epic 3, no code changes.

**Tasks:**
1. **repo-minder-rpb.1** - Create docs/ directory structure
2. **repo-minder-rpb.2** - Create mkdocs.yml configuration
3. **repo-minder-rpb.3** - Create .github/workflows/docs.yml
4. **repo-minder-rpb.4** - Write documentation content (P1)

**Dependencies:** Epic 1 complete (modern tooling established)

**Deliverables:**
- docs/index.md (project overview)
- docs/getting-started.md (installation, quick start)
- docs/developer-guide/contributing.md (dev workflow)
- docs/developer-guide/release-process.md (semver, publishing)
- docs/developer-guide/custom-templates.md (external templates)
- mkdocs.yml (Material theme)
- GitHub Pages deployment

### Epic 3: Release & Publishing Automation (P0)

**ID:** repo-minder-3r0
**Priority:** P0 (Parallel with Epic 2)
**Estimated effort:** 4-6 hours

**Why third:** Can work in parallel with docs, critical infrastructure.

**Tasks:**
1. **repo-minder-3r0.1** - Create .github/workflows/release.yml
2. **repo-minder-3r0.2** - Configure PyPI trusted publisher
3. **repo-minder-3r0.3** - Document branch-based workflow (P1)
4. **repo-minder-3r0.4** - Create initial CHANGELOG.md (P1)

**Dependencies:** Epic 1 complete (semantic-release in pyproject.toml)

**Deliverables:**
- Working release.yml workflow
- PyPI trusted publisher configured
- Automated CHANGELOG.md generation
- First automated release (v1.1.0)

### Epic 4: Community Health & Multi-File Support (P0)

**ID:** repo-minder-bn7
**Priority:** P0 (Dog-fooding opportunity)
**Estimated effort:** 8-12 hours

**Why fourth:** Requires all infrastructure in place, validates the tool.

**Tasks:**
1. **repo-minder-bn7.1** - Create SECURITY.md template
2. **repo-minder-bn7.2** - Create CODE_OF_CONDUCT.md template
3. **repo-minder-bn7.3** - Add template variables to Settings class
4. **repo-minder-bn7.4** - Implement multi-file CLI support
5. **repo-minder-bn7.5** - Create CONTRIBUTING.md template (Python variant)
6. **repo-minder-bn7.6** - Dog-food: Use repo-minder to generate community files for itself
7. **repo-minder-bn7.7** - Update README.md with badges and links (P1)

**Dependencies:** Epic 1, 2, 3 complete

**Deliverables:**
- templates/SECURITY.md.j2
- templates/CODE_OF_CONDUCT.md
- templates/CONTRIBUTING/python.md.j2
- Extended Settings class (team_email, security_email, etc.)
- CLI: `repo-minder --file-type security,code-of-conduct,contributing`
- Community health files for this project (generated by the tool itself!)
- Updated README with badges

### Epic 5: Future Features (P2)

**ID:** repo-minder-vcn
**Priority:** P2 (Post v1.1.0)
**Estimated effort:** 20-40 hours

**Why last:** Nice-to-have features for future releases.

**Tasks:**
1. **repo-minder-vcn.1** - Full multi-file support (all tech stacks)
2. **repo-minder-vcn.2** - Template preview commands
3. **repo-minder-vcn.3** - Fork management features
4. **repo-minder-vcn.4** - Policy enforcement & compliance scoring

**Dependencies:** All epics complete, v1.1.0 released

**From ROADMAP.md:**
- v1.1.0: Standard Files Support (SECURITY, CODE_OF_CONDUCT, CONTRIBUTING)
- v1.2.0: Template Preview & Rendering
- v1.3.0: Fork Management
- v2.0.0+: Policy Enforcement & Compliance

---

## Implementation Details

### Phase 1: Epic 1 - Modernization (Days 1-2)

#### Task 1: Update pyproject.toml

**Remove:**
```toml
[project.optional-dependencies]
dev = [
    "black>=23.0.0",  # REMOVE - ruff handles formatting
    ...
]

[tool.black]  # REMOVE entire section
```

**Add:**
```toml
[build-system]
requires = ["setuptools>=68.0.0", "python-semantic-release>=9.0.0"]

[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
upload_to_vcs_release = true
upload_to_pypi = false  # Workflow handles this
build_command = "pip install build && python -m build"

[tool.semantic_release.commit_parser_options]
allowed_tags = ["feat", "fix", "docs", "chore", "refactor", "test"]
minor_tags = ["feat"]
patch_tags = ["fix"]
```

#### Task 2: Upgrade Python Requirement

```toml
[project]
requires-python = ">=3.12"
classifiers = [
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
```

**Update CI matrix:**
```yaml
strategy:
  matrix:
    python-version: ["3.12", "3.13"]  # Only modern versions
```

#### Task 3: Create .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/PyCQA/bandit
    rev: 1.9.2
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

#### Task 4: Update CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ruff:
    name: Lint and Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - name: Lint
        run: uv run --frozen --all-extras ruff check .
      - name: Format check
        run: uv run --frozen --all-extras ruff format --check .

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - name: Run Bandit
        run: uv run --frozen --all-extras bandit -r repo_minder.py -ll

  test:
    name: Test Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: uv run --frozen --all-extras pytest tests/ -v --cov=. --cov-report=xml
      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

### Phase 2: Epic 2 - Documentation (Days 2-3)

#### docs/ Structure

```
docs/
├── index.md                          # Project overview
├── getting-started.md                # Installation, quick start
├── user-guide/
│   ├── basic-usage.md
│   ├── template-detection.md
│   └── safety-features.md
└── developer-guide/
    ├── contributing.md               # Dev workflow
    ├── release-process.md            # Semver, publishing
    ├── custom-templates.md           # External templates
    └── architecture.md               # Design decisions
```

#### mkdocs.yml

```yaml
site_name: Repo Minder
site_description: Repository file standardization and compliance tool
site_author: MITRE SAF Team
site_url: https://mitre.github.io/repo-minder

repo_name: mitre/repo-minder
repo_url: https://github.com/mitre/repo-minder

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Dark mode
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Light mode

plugins:
  - search
  - autorefs

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
  - pymdownx.highlight
  - pymdownx.tabbed
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Developer Guide:
      - Contributing: developer-guide/contributing.md
      - Release Process: developer-guide/release-process.md
      - Custom Templates: developer-guide/custom-templates.md
```

### Phase 3: Epic 3 - Release Automation (Days 3-4)

#### .github/workflows/release.yml

```yaml
name: Release

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  release:
    name: Semantic Release
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    permissions:
      id-token: write    # PyPI trusted publishing
      contents: write    # Create releases/tags
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: astral-sh/setup-uv@v7
      - name: Install semantic-release
        run: uv pip install python-semantic-release
      - name: Semantic Release
        id: release
        uses: python-semantic-release/python-semantic-release@v9.17.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
      - name: Publish to PyPI
        if: steps.release.outputs.released == 'true'
        uses: pypa/gh-action-pypi-publish@release/v1
```

#### PyPI Trusted Publisher Setup

**Manual step:** https://pypi.org/manage/account/publishing/

- PyPI Project: `mitre-repo-minder`
- Owner: `mitre`
- Repository: `repo-minder`
- Workflow: `release.yml`
- Environment: (leave blank)

### Phase 4: Epic 4 - Multi-File Support (Days 4-6)

#### Extended Settings Class

```python
class Settings(BaseSettings):
    # ... existing fields ...

    # NEW: Contact Information
    team_email: str = Field(
        default="saf@mitre.org",
        description="General team contact email"
    )
    security_email: str = Field(
        default="saf-security@mitre.org",
        description="Security vulnerability reporting email"
    )

    # NEW: Project Information (auto-detect from pyproject.toml)
    project_name: Optional[str] = Field(
        default=None,
        description="Project name (defaults to pyproject.toml name)"
    )
    project_description: Optional[str] = Field(
        default=None,
        description="Project description (from pyproject.toml)"
    )

    # NEW: Optional Contract Info
    contract_number: Optional[str] = Field(
        default=None,
        description="Federal contract number (if applicable)"
    )
```

#### CLI Extension

```python
@app.command()
def init_files(
    file_types: Annotated[
        List[str],
        typer.Option(
            "--file-type",
            help="File types to create: security, code-of-conduct, contributing, changelog"
        )
    ] = ["security", "code-of-conduct", "contributing"],
    repo: Optional[str] = None,
    dry_run: bool = False,
):
    """Initialize community health files in repositories."""
    # Implementation
```

#### Templates to Create

**templates/CODE_OF_CONDUCT.md:**
```markdown
# Contributor Covenant Code of Conduct

[Standard Contributor Covenant v2.1 text]

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project team at {{ team_email }}.

[See full code of conduct]
```

**templates/SECURITY.md.j2:**
```markdown
# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities to {{ security_email }}.

Include:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

## Response Timeline

- Acknowledgment: 48 hours
- Initial assessment: 7 days
- Fix timeline: Based on severity

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| {{ current_major }}.x.x | :white_check_mark: |
| < {{ current_major }}.0.0 | :x:              |

## Contact

Security issues: {{ security_email }}
General questions: {{ team_email }}
```

**templates/CONTRIBUTING/python.md.j2:**
```markdown
# Contributing to {{ project_name }}

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/{{ organization }}/{{ project_name }}.git
cd {{ project_name }}
uv sync --all-extras
uv run pre-commit install
```

## Code Standards

```bash
# Linting
ruff check .
ruff format .

# Security
bandit -r {{ project_name }}.py

# Testing
pytest tests/
```

## Pull Request Process

1. Create feature branch
2. Make changes with tests
3. Run linting and tests
4. Push and create PR

## Commit Message Format

Use conventional commits:
- feat: New feature (minor version bump)
- fix: Bug fix (patch version bump)
- docs: Documentation
- test: Tests
- chore: Maintenance

## Contact

Questions: {{ team_email }}
Security: {{ security_email }}
```

---

## Success Criteria

### Epic 1: Modernize to 2025 Python Standards

- [ ] black removed from dependencies
- [ ] python-semantic-release in build-system.requires
- [ ] [tool.semantic_release] configuration present
- [ ] requires-python = ">=3.12"
- [ ] CI tests Python 3.12 and 3.13 only
- [ ] .pre-commit-config.yaml created
- [ ] pre-commit install runs successfully
- [ ] CI uses setup-uv@v7
- [ ] CI uses `ruff format --check` (not black)
- [ ] CI scans repo_minder.py (not standardize_licenses.py)
- [ ] All tests pass
- [ ] Pre-commit hooks pass

### Epic 2: Documentation Infrastructure

- [ ] docs/ directory created with all files
- [ ] mkdocs.yml configured with Material theme
- [ ] mkdocs build runs successfully
- [ ] .github/workflows/docs.yml created
- [ ] GitHub Pages enabled
- [ ] Documentation deployed to https://mitre.github.io/repo-minder
- [ ] All nav links work
- [ ] Mermaid diagrams render correctly

### Epic 3: Release & Publishing Automation

- [ ] .github/workflows/release.yml created
- [ ] Release workflow triggers after CI success
- [ ] PyPI trusted publisher configured
- [ ] Initial CHANGELOG.md created
- [ ] Conventional commits documented
- [ ] Branch-based workflow documented
- [ ] First automated release successful (v1.1.0)
- [ ] Package published to PyPI
- [ ] CHANGELOG.md auto-updated by release-please
- [ ] GitHub release created with notes

### Epic 4: Community Health & Multi-File Support

- [ ] templates/CODE_OF_CONDUCT.md created
- [ ] templates/SECURITY.md.j2 created
- [ ] templates/CONTRIBUTING/python.md.j2 created
- [ ] Settings class extended with new variables
- [ ] team_email variable working
- [ ] security_email variable working
- [ ] project_name auto-detection working
- [ ] CLI --file-type option implemented
- [ ] SECURITY.md generated for repo-minder
- [ ] CODE_OF_CONDUCT.md generated for repo-minder
- [ ] CONTRIBUTING.md generated for repo-minder
- [ ] README.md updated with badges
- [ ] All generated files render correctly on GitHub
- [ ] Tests added for multi-file support
- [ ] Documentation updated

---

## Appendix: Beads Task IDs

### Epic 1: Modernize to 2025 Python Standards
- repo-minder-hxh (Epic)
- repo-minder-hxh.1 (Update pyproject.toml)
- repo-minder-hxh.2 (Upgrade Python requirement)
- repo-minder-hxh.3 (Create pre-commit config)
- repo-minder-hxh.4 (Update CI workflow)
- repo-minder-hxh.5 (Design external template support)

### Epic 2: Documentation Infrastructure
- repo-minder-rpb (Epic)
- repo-minder-rpb.1 (Create docs/ structure)
- repo-minder-rpb.2 (Create mkdocs.yml)
- repo-minder-rpb.3 (Create docs.yml workflow)
- repo-minder-rpb.4 (Write documentation content)

### Epic 3: Release & Publishing Automation
- repo-minder-3r0 (Epic)
- repo-minder-3r0.1 (Create release.yml)
- repo-minder-3r0.2 (Configure PyPI trusted publisher)
- repo-minder-3r0.3 (Document branch-based workflow)
- repo-minder-3r0.4 (Create initial CHANGELOG.md)

### Epic 4: Community Health & Multi-File Support
- repo-minder-bn7 (Epic)
- repo-minder-bn7.1 (Create SECURITY.md template)
- repo-minder-bn7.2 (Create CODE_OF_CONDUCT.md template)
- repo-minder-bn7.3 (Add template variables to Settings)
- repo-minder-bn7.4 (Implement multi-file CLI support)
- repo-minder-bn7.5 (Create CONTRIBUTING.md template)
- repo-minder-bn7.6 (Dog-food: Generate files for repo-minder)
- repo-minder-bn7.7 (Update README.md with badges)

### Epic 5: Future Features
- repo-minder-vcn (Epic)
- repo-minder-vcn.1 (Dog-food multi-file support)

---

## Timeline Estimate

**Total estimated effort:** 22-32 hours

- Epic 1: 4-6 hours (Days 1-2)
- Epic 2: 6-8 hours (Days 2-3, parallel with Epic 3)
- Epic 3: 4-6 hours (Days 3-4, parallel with Epic 2)
- Epic 4: 8-12 hours (Days 4-6)

**Target completion:** 4-6 working days

---

## References

- PYTHON_PROJECT_SETUP_GUIDE.md (2025 Python standards)
- SESSION01.md (v1.0.0 development history)
- ROADMAP.md (v1.1.0+ future features)
- mitre/vulcan (community health files reference)
- mitre/train-k8s-container (complete reference implementation)
- Jinja2 ChoiceLoader documentation (external templates pattern)
