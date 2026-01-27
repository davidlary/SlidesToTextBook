# Gemini Antigravity Quick Start Guide

**Purpose**: Step-by-step guide for Gemini Antigravity to implement the SlidesToTextBook system.

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Activate Environment (CRITICAL)

```bash
# Execute these commands in order:
cd /Users/davidlary/Dropbox/Environments/
source base-env/.venv/bin/activate
cd Code/SlidesToLatex
```

**Verify**:
```bash
# Should show: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
pwd

# Should show: davidlary
echo $GITHUB_USER

# Should show: 4 or more
env | grep -E '_API_KEY' | wc -l
```

### Step 2: Review Key Documents

**Read in this order**:
1. **ENVIRONMENT_SETUP.md** (this file) - Environment configuration ← START HERE
2. **README.md** - Project overview and quick start
3. **ImplementationPlan.md** - Complete implementation roadmap (25 chunks)
4. **verification.md** - Testing prompts for all three tools

### Step 3: Check Repository Status

```bash
# Check git status
git status

# Check remote
git remote -v

# View recent commits
git log --oneline -5

# Check current branch
git branch
```

---

## 📋 Implementation Roadmap

**Total**: 25 chunks, ~25-50 hours
**Current Status**: Ready to begin Chunk 1

### Phase 1: Foundation (Chunks 1-2)
- ✅ **Chunk 1**: Project Setup (1-2 hours)
- ✅ **Chunk 2**: ProgressTracker Module (1-2 hours)

### Phase 2: Core Modules (Chunks 3-12)
- **Chunk 3-4**: PDFAnalyzer (2-4 hours)
- **Chunk 5-6**: TopicResearcher (2-4 hours)
- **Chunk 7-8**: ContentAuthor (2-4 hours)
- **Chunk 9**: FigureRecreator (1-2 hours)
- **Chunk 10**: PortraitGenerator (1-2 hours)
- **Chunk 11**: MarginNoteGenerator (1-2 hours)
- **Chunk 12**: BibliographyManager (1-2 hours)

### Phase 3: Assembly & Validation (Chunks 13-15)
- **Chunk 13-14**: LaTeXBuilder (2-4 hours)
- **Chunk 15**: QualityValidator (1-2 hours)

### Phase 4: Interface & Testing (Chunks 16-21)
- **Chunk 16**: CLI Interface (1-2 hours)
- **Chunk 17**: Test Fixtures (1-2 hours)
- **Chunk 18-20**: Integration Tests (3-6 hours)
- **Chunk 21**: End-to-End Tests (2 hours)

### Phase 5: Packaging & CI/CD (Chunks 22-24)
- **Chunk 22**: Package Configuration (1-2 hours)
- **Chunk 23**: GitHub Actions Testing (1-2 hours)
- **Chunk 24**: SLSA3 Provenance (1-2 hours)

### Phase 6: Finalization (Chunk 25)
- **Chunk 25**: Final Documentation (2 hours)

---

## 🎯 Chunk 1: Project Setup (START HERE)

### Goal
Create directory structure and basic package files.

### Tasks
1. Create `src/slides_to_textbook/` directory structure
2. Create `tests/` directory structure
3. Create `docs/` directory
4. Create `setup.py`
5. Create `pyproject.toml`
6. Create `requirements.txt`
7. Create `requirements-dev.txt`
8. Create `environment.yml`
9. Create basic `__init__.py` files
10. Create `__version__.py`

### Commands

```bash
# Create directory structure
mkdir -p src/slides_to_textbook/modules
mkdir -p src/slides_to_textbook/templates
mkdir -p src/slides_to_textbook/utils
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e
mkdir -p tests/fixtures
mkdir -p docs

# Create __init__.py files
touch src/slides_to_textbook/__init__.py
touch src/slides_to_textbook/modules/__init__.py
touch src/slides_to_textbook/templates/__init__.py
touch src/slides_to_textbook/utils/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/e2e/__init__.py
```

### File Contents

**src/slides_to_textbook/__version__.py**:
```python
__version__ = "1.0.0"
```

**src/slides_to_textbook/__init__.py**:
```python
"""SlidesToTextbook - Convert PDF lecture slides to LaTeX textbooks."""

from .__version__ import __version__

__all__ = ["__version__"]
```

**setup.py**: See ImplementationPlan.md for complete content

**requirements.txt**: See ImplementationPlan.md for complete list

**requirements-dev.txt**:
```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0
```

**environment.yml**: See ImplementationPlan.md for complete content

### Verification

```bash
# Check directory structure
tree -L 3 src/
tree -L 2 tests/

# Try installing package (should work even with empty modules)
pip install -e .

# Verify installation
pip show slides-to-textbook

# Check version
python -c "from slides_to_textbook import __version__; print(__version__)"
```

### Git Commit

```bash
git add src/ tests/ docs/ setup.py pyproject.toml requirements*.txt environment.yml
git commit -m "feat: Create project structure and package configuration (Chunk 1)

Setup complete package structure:
- src/slides_to_textbook/ with modules/, templates/, utils/
- tests/ with unit/, integration/, e2e/, fixtures/
- docs/ directory
- setup.py with complete metadata
- requirements.txt and requirements-dev.txt
- environment.yml for Anaconda support
- All __init__.py files created

Package now installable with: pip install -e .

Progress: Chunk 1 of 25 complete

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main
```

---

## 📚 Key Reference Documents

### File Locations
```
/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/
├── ENVIRONMENT_SETUP.md          ← Environment configuration (READ FIRST)
├── GEMINI_QUICK_START.md         ← This file
├── README.md                      ← Project overview
├── ImplementationPlan.md          ← Complete 25-chunk roadmap
├── verification.md                ← Testing prompts
├── .env.example                   ← Environment variables reference
└── progress.json files            ← Progress tracking
```

### Reference Book Structure
```
/Users/davidlary/Dropbox/Apps/Overleaf/AirQualityV3/
├── main.tex                       ← LaTeX structure to replicate
├── Chapter-*.tex                  ← Chapter file examples
├── BookWritingStyle.md            ← Writing style guidelines
├── bibliography.bib               ← Bibliography format
├── Figures/                       ← Figure organization
│   ├── Portraits/                 ← Historical figure portraits
│   └── Chapter-*/                 ← Chapter-specific figures
└── Pictures/                      ← Cover and chapter headers
```

### Lecture PDFs
```
# Machine Learning (14 lectures)
/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-*.pdf

# Computational Methods (12+ lectures)
/Users/davidlary/Dropbox/Lectures/2025/5315/Lecture*.pdf
```

### SICE Package (for figure generation)
```
/Users/davidlary/Dropbox/Environments/Code/Scientific_Image_Creation_and_Validation/
```

---

## 🔧 Common Commands

### Development Workflow
```bash
# Start session
cd /Users/davidlary/Dropbox/Environments/
source base-env/.venv/bin/activate
cd Code/SlidesToLatex

# Check status
git status
cat MachineLearning/progress.json | jq '.current_chunk'

# Run tests
pytest tests/unit/test_<module>.py -v --cov=src

# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/

# Build docs
cd docs && make html

# Commit work
git add <files>
git commit -m "<type>: <description>"
git push origin main
```

### Testing Commands
```bash
# Run all tests
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific module tests
pytest tests/unit/test_pdf_analyzer.py -v

# Run integration tests
pytest tests/integration/ -v

# Run E2E tests
pytest tests/e2e/ -v -s
```

### Package Commands
```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Build distribution
python -m build

# Check package
twine check dist/*
```

---

## 🚨 Critical Reminders

1. **Always activate base-env first** - ALL credentials come from there
2. **Never commit API keys** - They're in .gitignore
3. **Test before committing** - Run pytest for modified modules
4. **Update progress.json** - After each chunk completion
5. **Follow bite-sized chunks** - Don't skip ahead or combine chunks
6. **90%+ test coverage** - Write tests as you go
7. **Match Air Quality book style** - Study BookWritingStyle.md
8. **Git commit after each chunk** - Use standardized commit messages

---

## 🆘 Getting Help

### If Stuck
1. Read relevant section in ImplementationPlan.md
2. Check ENVIRONMENT_SETUP.md for environment issues
3. Review verification.md for testing prompts
4. Check Air Quality book for examples

### Common Issues

**Issue**: Import errors when running tests
**Solution**: Make sure you ran `pip install -e .`

**Issue**: API calls fail
**Solution**: Verify base-env is activated: `echo $ANTHROPIC_API_KEY`

**Issue**: Git operations fail
**Solution**: Check GitHub credentials: `echo $GITHUB_TOKEN`

**Issue**: Tests fail due to missing fixtures
**Solution**: Create test fixtures first (Chunk 17)

---

## ✅ Ready to Begin?

**Pre-flight checklist**:
- [ ] Base environment activated
- [ ] In correct directory (`pwd` shows SlidesToLatex)
- [ ] Environment variables verified (4+ API keys set)
- [ ] Git repository status checked
- [ ] ImplementationPlan.md reviewed
- [ ] Ready to start Chunk 1

**If all checked, begin with Chunk 1: Project Setup**

---

**Last Updated**: January 27, 2026
**Version**: 1.0
**Status**: Ready for implementation
