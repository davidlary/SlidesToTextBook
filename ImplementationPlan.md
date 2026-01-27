# SlidesToTextbook - Implementation Plan

**Version:** 1.0
**Date:** January 27, 2026
**Author:** Dr. David Lary
**Repository:** https://github.com/davidlary/SlidesToTextBook.git

---

## Executive Summary

This implementation plan details the creation of a robust, test-driven system to convert PDF lecture slides into professionally-formatted LaTeX textbooks. The system will be modular, reusable, and fully automated (except for topic analysis approval), producing textbooks that match the pedagogical excellence, accuracy, and aesthetic beauty of the Air Quality reference book.

### Goals
- **Excellence in Pedagogy**: Engaging, accessible writing style with historical context
- **Great Accuracy**: Precise mathematical notation, proper citations, validated content
- **Aesthetic Beauty**: High-quality figures, proper typography, consistent styling
- **90%+ Test Coverage**: Comprehensive unit, integration, and end-to-end tests
- **Full Automation**: Minimal human intervention after topic approval
- **Multi-Tool Compatibility**: Works seamlessly with Claude Code, Gemini Antigravity, GitHub CLI

---

## Book Projects

### Book 1: Machine Learning
- **Target Directory**: `/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/`
- **Source PDFs**: `/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-*.pdf` (14 lectures)
- **Implementation Code**: `/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/MachineLearning/`
- **Progress Tracking**: `MachineLearning/progress.json`

### Book 2: Computational Methods
- **Target Directory**: `/Users/davidlary/Dropbox/Apps/Overleaf/ComputationalMethodsBook/`
- **Source PDFs**: `/Users/davidlary/Dropbox/Lectures/2025/5315/Lecture*.pdf` (12+ lectures)
- **Implementation Code**: `/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/ComputationalPhysics/`
- **Progress Tracking**: `ComputationalPhysics/progress.json`

---

## Reference Materials

### Book Structure Reference
**Path**: `/Users/davidlary/Dropbox/Apps/Overleaf/AirQualityV3/`

**Key Components**:
- `main.tex` - Document class, packages, geometry, formatting, chapter inclusion
- `Chapter-*.tex` - Individual chapter files (separate includes)
- `bibliography.bib` - Complete citation database
- `Pictures/` - Chapter header images and book cover
  - `Cover-Clouds.pdf` - Book cover
  - `Head-*.pdf` - Chapter header images (one per chapter)
- `Figures/` - All scientific figures
  - `Portraits/` - Historical figure portraits (centralized, 900×1200px)
  - `Chapter-*/` - Chapter-specific figures
- `BookWritingStyle.md` - Writing style guidelines
- `abbrev.tex` - Abbreviations
- `journals.tex` - Journal abbreviations

### Writing Style Reference
**Path**: `/Users/davidlary/Dropbox/Apps/Overleaf/AirQualityV3/BookWritingStyle.md`

**Key Principles**:
- Accessible yet authoritative tone
- Context before technical details
- Historical figures, etymology, citations
- Margin notes with portraits, key terms, takeaways
- Concrete examples with dates, places, numbers
- Active voice, engaging narrative flow

### SICE Package (Scientific Image Creation)
**Path**: `/Users/davidlary/Dropbox/Environments/Code/Scientific_Image_Creation_and_Validation/`

**Capabilities**:
- AI-powered image generation (Google Gemini)
- Portrait generation (sepia pre-1900, color post-1900, 900×1200px)
- Scientific figure creation and validation
- Uses `GOOGLE_API_KEY` environment variable

---

## System Architecture

### Core Modules (Bite-Sized Chunks)

#### Module 1: PDFAnalyzer
**Purpose**: Extract topics, concepts, equations, figures from PDF slides
**Input**: PDF file path
**Output**: Structured JSON with topics, equations, figures, concepts
**Dependencies**: pdfplumber, PyPDF2, pytesseract (OCR), Claude/Gemini API
**Test Coverage Target**: 95%

#### Module 2: TopicResearcher
**Purpose**: Research historical context, key figures, citations for topics
**Input**: Topic list from PDFAnalyzer
**Output**: Historical figures, etymology, citations, dates
**Dependencies**: Claude/Gemini API, scholarly library, Wikipedia API
**Test Coverage Target**: 90%

#### Module 3: ContentAuthor
**Purpose**: Generate engaging textbook prose matching Air Quality style
**Input**: Topics, research, equations from previous modules
**Output**: LaTeX chapter sections with narrative flow
**Dependencies**: Claude/Gemini API, LaTeX validation
**Test Coverage Target**: 85%

#### Module 4: FigureRecreator
**Purpose**: Interface to SICE package for figure generation
**Input**: Figure description from PDFAnalyzer
**Output**: High-quality scientific figure (PDF/PNG/EPS)
**Dependencies**: SICE package, Google Gemini API
**Test Coverage Target**: 95%

#### Module 5: PortraitGenerator
**Purpose**: Create historical figure portraits
**Input**: Person name, birth/death dates
**Output**: Portrait (900×1200px, sepia pre-1900, color post-1900)
**Dependencies**: SICE package, Google Gemini API
**Test Coverage Target**: 95%

#### Module 6: MarginNoteGenerator
**Purpose**: Create margin notes with portraits, key terms, takeaways
**Input**: Content, key terms, historical figures
**Output**: LaTeX margin note commands with formatting
**Dependencies**: PortraitGenerator
**Test Coverage Target**: 90%

#### Module 7: LaTeXBuilder
**Purpose**: Assemble complete LaTeX structure (main.tex, chapters, figures)
**Input**: All content from previous modules
**Output**: Complete book directory ready for XeLaTeX compilation
**Dependencies**: jinja2 (templates), pylatex
**Test Coverage Target**: 95%

#### Module 8: BibliographyManager
**Purpose**: Build and manage bibliography.bib from citations
**Input**: Citation list from TopicResearcher
**Output**: Properly formatted bibliography.bib
**Dependencies**: bibtexparser, scholarly library
**Test Coverage Target**: 95%

#### Module 9: ProgressTracker
**Purpose**: Log progress, enable recovery from interruptions
**Input**: Module events (start, complete, error)
**Output**: progress.json with state, timestamps, checkpoints
**Dependencies**: json, logging
**Test Coverage Target**: 100%

#### Module 10: QualityValidator
**Purpose**: Verify LaTeX compiles, figures exist, citations valid
**Input**: Book directory path
**Output**: Validation report with errors/warnings
**Dependencies**: subprocess (xelatex), bibtex, os.path
**Test Coverage Target**: 95%

---

## LaTeX Book Structure (Exact Replication of Air Quality Book)

### Directory Structure
```
MachineLearningBook/  (or ComputationalMethodsBook/)
├── main.tex
├── bibliography.bib
├── abbrev.tex
├── journals.tex
├── BookWritingStyle.md
├── Pictures/
│   ├── Cover-MachineLearning.pdf
│   ├── Head-Introduction.pdf
│   ├── Head-SupervisedLearning.pdf
│   ├── Head-UnsupervisedLearning.pdf
│   └── ... (one per chapter)
├── Figures/
│   ├── Portraits/
│   │   ├── ArthurSamuel.jpg
│   │   ├── GeoffreyHinton.jpg
│   │   └── ... (all historical figures)
│   ├── Chapter-Introduction/
│   ├── Chapter-SupervisedLearning/
│   └── ... (one per chapter)
└── Chapter-*.tex (one file per chapter)
    ├── Chapter-Introduction.tex
    ├── Chapter-SupervisedLearning.tex
    ├── Chapter-UnsupervisedLearning.tex
    └── ...
```

### main.tex Structure
- Document class: `\documentclass[letterpaper,11pt,twoside]{book}`
- Packages: amsmath, graphicx, natbib, mhchem, hyperref, tikz, etc.
- Geometry: Wide right margin for margin notes
- Colors: SectionColor (RGB 52,177,201)
- Fonts: Polyglossia for multi-language support
- Custom commands: `\automarginnote{}`, `\topimage{}`
- Chapter inclusion pattern:
  ```latex
  \newpage
  \topimage{Head-ChapterName.pdf}
  \chapter{Chapter Title}
  \input{Chapter-ChapterName.tex}
  ```

### Chapter File Structure
- Starts with `\section{Introduction}` or `\section{Context}`
- Uses `\subsection{}`, `\subsubsection{}`
- Figures: `\begin{figure}[t!]` with detailed captions
- Margin notes: `\automarginnote{\includegraphics{...}\it \small Person Name}`
- Citations: `\citep{key1, key2}`
- Equations: `\begin{equation}...\end{equation}` with labels
- Cross-references: `\ref{label}`, `\label{label}`

### Chapter Naming Convention
- **Named, not numbered**: `Chapter-SupervisedLearning.tex` NOT `Chapter-1.tex`
- **Rationale**: Allows reordering without renaming files
- **Pattern**: `Chapter-{TopicName}.tex` (CamelCase, no spaces)

---

## Workflow Pipeline

### Phase 1: Topic Analysis (Human-in-the-Loop)
**Goal**: Identify topics, get user approval before proceeding

1. **For each lecture PDF**:
   - Run PDFAnalyzer to extract topics, concepts, equations
   - Run TopicResearcher to identify historical context
   - Generate topic summary report
   - **STOP - Request user approval**
   - User reviews and approves/modifies topics
   - Update progress.json

2. **Progress Checkpoint**: Save approved topics to `approved_topics.json`

### Phase 2: Content Generation (Fully Automated)
**Goal**: Generate all book content

**For each approved topic/chapter**:

1. **Content Authoring**:
   - ContentAuthor generates textbook prose
   - MarginNoteGenerator creates margin notes
   - BibliographyManager builds citations
   - Progress: Update progress.json after each chapter

2. **Figure Creation**:
   - FigureRecreator generates all scientific figures
   - PortraitGenerator creates all historical figure portraits
   - Save to appropriate directories
   - Progress: Update progress.json after each figure

3. **LaTeX Assembly**:
   - LaTeXBuilder creates main.tex
   - LaTeXBuilder creates each Chapter-*.tex
   - LaTeXBuilder creates bibliography.bib
   - Copy abbrev.tex, journals.tex from template
   - Progress: Update progress.json

4. **Validation**:
   - QualityValidator runs XeLaTeX compilation test
   - QualityValidator checks all figures exist
   - QualityValidator verifies all citations resolve
   - Generate validation report
   - Progress: Update progress.json with validation results

### Phase 3: Finalization (Fully Automated)
**Goal**: Package and commit

1. **Git Operations**:
   - Stage code, documentation, tests (NOT PDFs)
   - Commit with descriptive message
   - Push to GitHub remote

2. **Final Progress Update**:
   - Mark book as complete in progress.json
   - Generate final summary report

---

## Progress Tracking System

### progress.json Schema
```json
{
  "book_name": "MachineLearning",
  "version": "1.0",
  "started": "2026-01-27T10:00:00Z",
  "updated": "2026-01-27T12:30:00Z",
  "status": "in_progress",
  "current_phase": "content_generation",
  "current_chunk": "Module 3: ContentAuthor - Chapter 2",

  "phases": {
    "topic_analysis": {
      "status": "completed",
      "started": "2026-01-27T10:00:00Z",
      "completed": "2026-01-27T10:30:00Z",
      "lectures_processed": 14,
      "topics_identified": 12,
      "user_approved": true
    },
    "content_generation": {
      "status": "in_progress",
      "started": "2026-01-27T10:35:00Z",
      "chapters_completed": 1,
      "chapters_total": 12,
      "figures_created": 5,
      "figures_total": 48,
      "portraits_created": 3,
      "portraits_total": 15
    },
    "validation": {
      "status": "pending"
    },
    "finalization": {
      "status": "pending"
    }
  },

  "chapters": [
    {
      "name": "Introduction",
      "file": "Chapter-Introduction.tex",
      "status": "completed",
      "word_count": 3500,
      "figures": 6,
      "portraits": 2,
      "citations": 15,
      "started": "2026-01-27T10:35:00Z",
      "completed": "2026-01-27T11:00:00Z"
    },
    {
      "name": "SupervisedLearning",
      "file": "Chapter-SupervisedLearning.tex",
      "status": "in_progress",
      "word_count": 1200,
      "figures": 2,
      "portraits": 1,
      "citations": 8,
      "started": "2026-01-27T11:05:00Z"
    }
  ],

  "errors": [],
  "warnings": [],

  "recovery_checkpoint": {
    "module": "ContentAuthor",
    "chapter": "SupervisedLearning",
    "section": 2,
    "timestamp": "2026-01-27T12:30:00Z"
  }
}
```

### Progress Update Requirements
- **Every module completion**: Update progress.json
- **Every chapter completion**: Update chapters array
- **Every figure creation**: Increment figure counters
- **Every error**: Append to errors array
- **Every 5 minutes**: Save recovery checkpoint

---

## Testing Strategy (90%+ Coverage)

### Unit Tests (per module)

**Test Files Structure**:
```
tests/
├── unit/
│   ├── test_pdf_analyzer.py
│   ├── test_topic_researcher.py
│   ├── test_content_author.py
│   ├── test_figure_recreator.py
│   ├── test_portrait_generator.py
│   ├── test_margin_note_generator.py
│   ├── test_latex_builder.py
│   ├── test_bibliography_manager.py
│   ├── test_progress_tracker.py
│   └── test_quality_validator.py
├── integration/
│   ├── test_pipeline_phase1.py
│   ├── test_pipeline_phase2.py
│   └── test_pipeline_phase3.py
├── e2e/
│   ├── test_sample_lecture.py
│   └── test_full_book.py
├── fixtures/
│   ├── sample_lecture.pdf
│   ├── expected_topics.json
│   └── expected_chapter.tex
└── conftest.py
```

### Test Data Creation

**Sample Test PDF**: Create `tests/fixtures/sample_lecture.pdf` with:
- Title slide: "Introduction to Machine Learning"
- Content slides: 5 slides with equations, bullet points, figures
- Topics: supervised learning, training, testing
- Historical figure: Arthur Samuel
- Mathematical equations: Loss function, gradient descent

### Integration Tests

1. **Phase 1 Pipeline Test**:
   - Input: sample_lecture.pdf
   - Run: PDFAnalyzer → TopicResearcher
   - Verify: Topics extracted, historical context found

2. **Phase 2 Pipeline Test**:
   - Input: Approved topics
   - Run: ContentAuthor → FigureRecreator → LaTeXBuilder
   - Verify: Chapter.tex created, figures exist, compiles

3. **Phase 3 Pipeline Test**:
   - Input: Complete book directory
   - Run: QualityValidator → Git operations
   - Verify: No errors, committed to git

### End-to-End Tests

1. **Single Chapter Test**:
   - Input: sample_lecture.pdf
   - Run: Full pipeline (with mock user approval)
   - Verify: Chapter compiles with XeLaTeX, all figures present

2. **Full Book Test** (longer running):
   - Input: All lecture PDFs for one book
   - Run: Full pipeline (with mock user approval)
   - Verify: Complete book compiles, 100+ pages, bibliography correct

### Coverage Requirements

**Target: 90%+ overall**
- Core modules (1-8): 95%+ each
- ProgressTracker: 100%
- Integration tests: 85%+
- E2E tests: Coverage reporting disabled (manual verification)

### Running Tests
```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run E2E tests (slow)
pytest tests/e2e/ -v

# Run specific module tests
pytest tests/unit/test_pdf_analyzer.py -v
```

---

## Python Package Structure

### Directory Layout
```
SlidesToLatex/
├── README.md
├── ImplementationPlan.md
├── verification.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── package.yml
│       └── slsa.yml
├── setup.py
├── setup.cfg
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── environment.yml (for Anaconda)
├── src/
│   └── slides_to_textbook/
│       ├── __init__.py
│       ├── __version__.py
│       ├── cli.py
│       ├── config.py
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── pdf_analyzer.py
│       │   ├── topic_researcher.py
│       │   ├── content_author.py
│       │   ├── figure_recreator.py
│       │   ├── portrait_generator.py
│       │   ├── margin_note_generator.py
│       │   ├── latex_builder.py
│       │   ├── bibliography_manager.py
│       │   ├── progress_tracker.py
│       │   └── quality_validator.py
│       ├── templates/
│       │   ├── main.tex.jinja2
│       │   ├── chapter.tex.jinja2
│       │   └── bibliography.bib.jinja2
│       └── utils/
│           ├── __init__.py
│           ├── api_clients.py
│           └── latex_utils.py
├── tests/
│   └── (as described above)
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   ├── modules.md
│   └── api.md
├── MachineLearning/
│   └── progress.json
└── ComputationalPhysics/
    └── progress.json
```

### Package Metadata (setup.py)
```python
from setuptools import setup, find_packages

setup(
    name="slides-to-textbook",
    version="1.0.0",
    author="Dr. David Lary",
    description="Convert PDF lecture slides to LaTeX textbooks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davidlary/SlidesToTextBook",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.9.0",
        "PyPDF2>=3.0.0",
        "pytesseract>=0.3.10",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        "scholarly>=1.7.0",
        "bibtexparser>=1.4.0",
        "jinja2>=3.1.0",
        "pylatex>=1.4.0",
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "sphinx>=7.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "slides2tex=slides_to_textbook.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
```

### Anaconda Environment (environment.yml)
```yaml
name: slides-to-textbook
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pip
  - pytest>=7.4.0
  - pytest-cov>=4.1.0
  - pillow>=10.0.0
  - requests>=2.31.0
  - jinja2>=3.1.0
  - click>=8.1.0
  - pip:
    - pdfplumber>=0.9.0
    - PyPDF2>=3.0.0
    - pytesseract>=0.3.10
    - anthropic>=0.7.0
    - google-generativeai>=0.3.0
    - scholarly>=1.7.0
    - bibtexparser>=1.4.0
    - pylatex>=1.4.0
```

---

## Security & Git Workflow

### Security Requirements

**Environment Variables** (MUST be set):
```bash
export GOOGLE_API_KEY='your-google-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'
export GITHUB_TOKEN='your-github-token'
export GITHUB_USER='davidlary'
export GITHUB_EMAIL='your-email@example.com'
```

**Never Commit**:
- API keys
- Credentials
- Large PDFs (source lectures)
- Generated book PDFs (output)
- Temporary files
- `.env` files

### .gitignore
```gitignore
# Security - API keys and credentials
*.key
.env
.env.*
credentials.json
*_api_key*
GOOGLE_API_KEY*
ANTHROPIC_API_KEY*
GITHUB_TOKEN*

# Large files - PDFs
*.pdf
!tests/fixtures/sample_lecture.pdf

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# LaTeX
*.aux
*.log
*.out
*.toc
*.synctex.gz
*.fls
*.fdb_latexmk

# Temporary
tmp/
temp/
*.tmp
*.bak
*.backup
```

### Git Workflow

**Initial Setup**:
```bash
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
git init
git remote add origin https://github.com/davidlary/SlidesToTextBook.git
git config user.name "${GITHUB_USER}"
git config user.email "${GITHUB_EMAIL}"
```

**Commit Pattern**:
```bash
# After each bite-sized chunk completion
git add <relevant-files>
git commit -m "<type>: <short description>

<detailed description>

Progress: <chunk name> completed
Coverage: <percentage>%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main
```

**Commit Types**:
- `feat:` - New module or feature
- `test:` - New tests
- `docs:` - Documentation
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `ci:` - CI/CD changes

---

## SLSA3 Provenance

### Goal
Generate SLSA Level 3 provenance for releases to ensure supply chain security.

### Implementation

**GitHub Actions Workflow** (`.github/workflows/slsa.yml`):
```yaml
name: SLSA3 Provenance

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      hashes: ${{ steps.hash.outputs.hashes }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Build package
        run: |
          python -m pip install build
          python -m build
      - name: Generate hashes
        id: hash
        run: |
          cd dist
          echo "hashes=$(sha256sum * | base64 -w0)" >> $GITHUB_OUTPUT
      - uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  provenance:
    needs: [build]
    permissions:
      actions: read
      id-token: write
      contents: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
    with:
      base64-subjects: "${{ needs.build.outputs.hashes }}"
      upload-assets: true

  release:
    needs: [build, provenance]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/*
```

### Verification
```bash
# Download release artifacts
gh release download v1.0.0

# Verify provenance
slsa-verifier verify-artifact \
  --provenance-path slides-to-textbook-1.0.0.tar.gz.intoto.jsonl \
  --source-uri github.com/davidlary/SlidesToTextBook \
  slides-to-textbook-1.0.0.tar.gz
```

---

## Multi-Tool Compatibility

### Design Principles

1. **Self-Contained Documentation**: All documentation in markdown, no external dependencies
2. **Clear Module Interfaces**: Each module has well-defined inputs/outputs
3. **CLI Access**: Full functionality available via command-line interface
4. **JSON Communication**: Progress and state stored in JSON (parseable by all tools)
5. **GitHub Integration**: All three tools can access GitHub repo

### CLI Interface (cli.py)

```bash
# Phase 1: Analyze lectures
slides2tex analyze --input /path/to/lectures/*.pdf --output topics.json

# Phase 1: User approval (interactive)
slides2tex approve --topics topics.json --output approved_topics.json

# Phase 2: Generate book (fully automated)
slides2tex generate --topics approved_topics.json --output /path/to/book/

# Phase 3: Validate
slides2tex validate --book /path/to/book/ --output validation_report.json

# Full pipeline (with manual approval step)
slides2tex pipeline --input /path/to/lectures/*.pdf --output /path/to/book/

# Check progress
slides2tex progress --book MachineLearning

# Resume from interruption
slides2tex resume --book MachineLearning
```

### verification.md (Optimized Prompts)
See separate section below.

---

## Bite-Sized Implementation Chunks

### Chunk Size Guidelines
- **Time**: 1-2 hours per chunk
- **Scope**: One module or one test suite
- **Verification**: Must have passing tests before next chunk
- **Documentation**: Update README and docstrings

### Implementation Order (25 Chunks)

#### **Chunk 1**: Project Setup (1-2 hours)
- Create directory structure
- Initialize git repository
- Set up GitHub remote
- Create .gitignore
- Create README.md skeleton
- Create requirements.txt
- **Verification**: `git status` clean, remote connected
- **Progress**: Update progress.json

#### **Chunk 2**: ProgressTracker Module (1-2 hours)
- Implement ProgressTracker class
- JSON schema definition
- Read/write methods
- Update methods
- Recovery checkpoint methods
- **Tests**: test_progress_tracker.py (100% coverage)
- **Verification**: Tests pass, module importable
- **Progress**: Update progress.json

#### **Chunk 3**: PDFAnalyzer Module - Basic (1-2 hours)
- Implement PDFAnalyzer class skeleton
- PDF text extraction (pdfplumber)
- Topic identification (keyword extraction)
- **Tests**: test_pdf_analyzer.py (basic)
- **Verification**: Can extract text from sample PDF
- **Progress**: Update progress.json

#### **Chunk 4**: PDFAnalyzer Module - Advanced (1-2 hours)
- Equation extraction (LaTeX detection)
- Figure extraction (images)
- Concept extraction (NLP/AI)
- **Tests**: test_pdf_analyzer.py (complete, 95%+ coverage)
- **Verification**: All tests pass
- **Progress**: Update progress.json

#### **Chunk 5**: TopicResearcher Module - API Integration (1-2 hours)
- Implement TopicResearcher class
- Claude/Gemini API client setup
- Wikipedia API integration
- **Tests**: test_topic_researcher.py (mocked APIs)
- **Verification**: Can query APIs successfully
- **Progress**: Update progress.json

#### **Chunk 6**: TopicResearcher Module - Historical Context (1-2 hours)
- Historical figure identification
- Etymology research
- Citation generation
- **Tests**: test_topic_researcher.py (complete, 90%+ coverage)
- **Verification**: All tests pass
- **Progress**: Update progress.json

#### **Chunk 7**: ContentAuthor Module - Style Templates (1-2 hours)
- Implement ContentAuthor class
- Load Air Quality writing style guidelines
- Create prompt templates for AI
- Section generation logic
- **Tests**: test_content_author.py (basic)
- **Verification**: Can generate sample section
- **Progress**: Update progress.json

#### **Chunk 8**: ContentAuthor Module - Full Generation (1-2 hours)
- Chapter introduction generation
- Section/subsection generation
- Equation integration
- Citation integration
- **Tests**: test_content_author.py (complete, 85%+ coverage)
- **Verification**: Generated content matches style
- **Progress**: Update progress.json

#### **Chunk 9**: FigureRecreator Module (1-2 hours)
- Implement FigureRecreator class
- Interface to SICE package
- Figure prompt generation
- Figure validation
- **Tests**: test_figure_recreator.py (95%+ coverage)
- **Verification**: Can generate sample figure
- **Progress**: Update progress.json

#### **Chunk 10**: PortraitGenerator Module (1-2 hours)
- Implement PortraitGenerator class
- Interface to SICE portrait generation
- Sepia/color logic (pre-1900/post-1900)
- Size validation (900×1200px)
- **Tests**: test_portrait_generator.py (95%+ coverage)
- **Verification**: Can generate sample portrait
- **Progress**: Update progress.json

#### **Chunk 11**: MarginNoteGenerator Module (1-2 hours)
- Implement MarginNoteGenerator class
- Key term extraction
- Key takeaway generation
- Portrait integration
- LaTeX formatting
- **Tests**: test_margin_note_generator.py (90%+ coverage)
- **Verification**: Generates proper LaTeX
- **Progress**: Update progress.json

#### **Chunk 12**: BibliographyManager Module (1-2 hours)
- Implement BibliographyManager class
- BibTeX parsing/generation
- Citation deduplication
- Scholarly API integration
- **Tests**: test_bibliography_manager.py (95%+ coverage)
- **Verification**: Generates valid .bib file
- **Progress**: Update progress.json

#### **Chunk 13**: LaTeXBuilder Module - Templates (1-2 hours)
- Implement LaTeXBuilder class
- Create Jinja2 templates (main.tex)
- Create Jinja2 templates (chapter.tex)
- Template rendering logic
- **Tests**: test_latex_builder.py (basic)
- **Verification**: Templates render correctly
- **Progress**: Update progress.json

#### **Chunk 14**: LaTeXBuilder Module - Assembly (1-2 hours)
- Directory structure creation
- File copying (abbrev.tex, journals.tex)
- Figure organization
- Complete book assembly
- **Tests**: test_latex_builder.py (complete, 95%+ coverage)
- **Verification**: Generates complete book directory
- **Progress**: Update progress.json

#### **Chunk 15**: QualityValidator Module (1-2 hours)
- Implement QualityValidator class
- XeLaTeX compilation test
- Figure existence check
- Citation resolution check
- Validation report generation
- **Tests**: test_quality_validator.py (95%+ coverage)
- **Verification**: Can validate sample book
- **Progress**: Update progress.json

#### **Chunk 16**: CLI Interface (1-2 hours)
- Implement cli.py with Click
- Commands: analyze, approve, generate, validate, pipeline, progress, resume
- Argument parsing
- Help text
- **Tests**: test_cli.py (basic)
- **Verification**: All commands work
- **Progress**: Update progress.json

#### **Chunk 17**: Test Fixtures (1-2 hours)
- Create sample_lecture.pdf (test PDF)
- Create expected_topics.json
- Create expected_chapter.tex
- Document fixture creation process
- **Verification**: Fixtures loadable by tests
- **Progress**: Update progress.json

#### **Chunk 18**: Integration Tests - Phase 1 (1-2 hours)
- Implement test_pipeline_phase1.py
- Test: PDFAnalyzer → TopicResearcher
- Mock user approval
- **Verification**: Tests pass
- **Progress**: Update progress.json

#### **Chunk 19**: Integration Tests - Phase 2 (1-2 hours)
- Implement test_pipeline_phase2.py
- Test: ContentAuthor → FigureRecreator → LaTeXBuilder
- **Verification**: Tests pass, generates chapter
- **Progress**: Update progress.json

#### **Chunk 20**: Integration Tests - Phase 3 (1-2 hours)
- Implement test_pipeline_phase3.py
- Test: QualityValidator → Git operations
- **Verification**: Tests pass
- **Progress**: Update progress.json

#### **Chunk 21**: End-to-End Tests (2 hours)
- Implement test_sample_lecture.py
- Full pipeline test with sample_lecture.pdf
- Verify compiled output
- **Verification**: Chapter compiles successfully
- **Progress**: Update progress.json

#### **Chunk 22**: Package Configuration (1-2 hours)
- Create setup.py
- Create setup.cfg
- Create pyproject.toml
- Create environment.yml (Anaconda)
- Test package installation
- **Verification**: `pip install -e .` works
- **Progress**: Update progress.json

#### **Chunk 23**: GitHub Actions - Testing (1-2 hours)
- Create .github/workflows/test.yml
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Coverage reporting
- **Verification**: Workflow runs successfully
- **Progress**: Update progress.json

#### **Chunk 24**: GitHub Actions - SLSA3 (1-2 hours)
- Create .github/workflows/slsa.yml
- Configure SLSA generic generator
- Test with pre-release
- **Verification**: Provenance generated
- **Progress**: Update progress.json

#### **Chunk 25**: Documentation (2 hours)
- Complete README.md
- Create docs/ directory with detailed guides
- Update ImplementationPlan.md (this file)
- Create verification.md with tool-specific prompts
- **Verification**: Documentation complete
- **Progress**: Mark project as complete

---

## verification.md - Multi-Tool Testing Prompts

### For Claude Code

**Prompt 1: Module Testing**
```
Please test Module X (PDFAnalyzer, TopicResearcher, etc.) from the SlidesToTextBook repository at /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex.

Steps:
1. Read the module file: src/slides_to_textbook/modules/{module_name}.py
2. Read the test file: tests/unit/test_{module_name}.py
3. Run the tests: pytest tests/unit/test_{module_name}.py -v --cov=src/slides_to_textbook/modules/{module_name}
4. Report coverage percentage and any failing tests
5. If coverage < 90%, suggest additional tests
```

**Prompt 2: Integration Testing**
```
Please run the integration tests for Phase X (1, 2, or 3) from the SlidesToTextBook repository.

Steps:
1. Read tests/integration/test_pipeline_phaseX.py
2. Run: pytest tests/integration/test_pipeline_phaseX.py -v
3. Report results and any failures
4. Check progress.json for updated state
```

**Prompt 3: End-to-End Testing**
```
Please run the end-to-end test for a sample lecture from the SlidesToTextBook repository.

Steps:
1. Verify sample PDF exists: tests/fixtures/sample_lecture.pdf
2. Run: pytest tests/e2e/test_sample_lecture.py -v
3. Check that output chapter compiles with XeLaTeX
4. Report success/failure and any issues
```

**Prompt 4: Package Testing (Multiple Python Versions)**
```
Please test the SlidesToTextBook package installation across multiple Python versions.

Steps:
1. Test Python 3.8: Create venv, install package, run tests
2. Test Python 3.9: Create venv, install package, run tests
3. Test Python 3.10: Create venv, install package, run tests
4. Test Python 3.11: Create venv, install package, run tests
5. Report any version-specific issues
```

**Prompt 5: Anaconda Package Testing**
```
Please test the SlidesToTextBook package with Anaconda package management.

Steps:
1. Create conda environment from environment.yml
2. Activate environment
3. Install package in development mode
4. Run full test suite
5. Deactivate and remove environment
6. Report results
```

**Prompt 6: SLSA3 Provenance Verification**
```
Please verify SLSA3 provenance for the SlidesToTextBook release.

Steps:
1. Check GitHub Actions workflow: .github/workflows/slsa.yml
2. Verify workflow ran successfully for latest release
3. Download provenance file from release
4. If slsa-verifier installed, verify provenance
5. Report verification status
```

---

### For Gemini Antigravity

**Prompt 1: Module Code Review**
```
Review Module X from the SlidesToTextBook repository (https://github.com/davidlary/SlidesToTextBook).

Focus on:
1. Code quality and readability
2. Adherence to Python best practices
3. Security considerations (API key handling)
4. Potential bugs or edge cases
5. Documentation completeness

Provide specific suggestions for improvements.
```

**Prompt 2: Test Coverage Analysis**
```
Analyze test coverage for the SlidesToTextBook repository.

Focus on:
1. Current coverage percentage per module
2. Untested code paths
3. Missing edge case tests
4. Test quality and assertions
5. Integration test coverage

Suggest additional tests to reach 90%+ coverage.
```

**Prompt 3: Documentation Review**
```
Review documentation for the SlidesToTextBook repository.

Check:
1. README.md completeness
2. ImplementationPlan.md accuracy
3. verification.md prompt quality
4. Docstring completeness
5. API documentation (docs/)

Provide specific improvements.
```

**Prompt 4: Writing Style Validation**
```
Validate that generated textbook content matches the Air Quality book writing style.

Compare:
1. Generated chapter sample with BookWritingStyle.md guidelines
2. Tone and voice consistency
3. Historical context integration
4. Margin note formatting
5. Citation style

Provide detailed feedback.
```

**Prompt 5: Figure Quality Assessment**
```
Assess quality of generated scientific figures.

Evaluate:
1. Resolution and clarity
2. Typography and labels
3. Color scheme appropriateness
4. Caption completeness
5. Consistency with Air Quality book style

Suggest improvements.
```

**Prompt 6: End-to-End Pipeline Test**
```
Test the complete pipeline from PDF to LaTeX textbook.

Execute:
1. Run full pipeline on sample lecture
2. Verify all modules execute successfully
3. Check generated LaTeX compiles
4. Validate output quality (content, figures, citations)
5. Measure total execution time

Report comprehensive results.
```

---

### For GitHub CLI

**Command 1: Repository Status**
```bash
# Check repository status
gh repo view davidlary/SlidesToTextBook

# View recent commits
gh repo view davidlary/SlidesToTextBook --json commits --jq '.commits[0:5]'

# Check open issues
gh issue list --repo davidlary/SlidesToTextBook

# Check PR status
gh pr list --repo davidlary/SlidesToTextBook
```

**Command 2: Test Workflow Status**
```bash
# View workflow runs
gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml

# View latest test run
gh run view --repo davidlary/SlidesToTextBook $(gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml --limit 1 --json databaseId --jq '.[0].databaseId')

# Download test artifacts
gh run download --repo davidlary/SlidesToTextBook <run-id>
```

**Command 3: Release and SLSA Provenance**
```bash
# List releases
gh release list --repo davidlary/SlidesToTextBook

# View release details
gh release view v1.0.0 --repo davidlary/SlidesToTextBook

# Download release with provenance
gh release download v1.0.0 --repo davidlary/SlidesToTextBook --pattern '*.tar.gz*'

# Check SLSA workflow
gh run list --repo davidlary/SlidesToTextBook --workflow=slsa.yml
```

**Command 4: Package Installation Test**
```bash
# Install from GitHub
pip install git+https://github.com/davidlary/SlidesToTextBook.git

# Verify installation
pip show slides-to-textbook

# Run CLI
slides2tex --help
```

**Command 5: Issue Creation for Test Failures**
```bash
# Create issue for failing test
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Test Failure: Module X" \
  --body "Test test_X failed with error: <error message>" \
  --label "bug,testing"
```

**Command 6: Performance Benchmarking**
```bash
# Time full pipeline execution
time slides2tex pipeline \
  --input tests/fixtures/sample_lecture.pdf \
  --output /tmp/test_book

# Report benchmark
gh issue comment <issue-number> --repo davidlary/SlidesToTextBook \
  --body "Pipeline execution time: X seconds"
```

---

## Environment Setup (CRITICAL - READ FIRST)

### ⚠️ MANDATORY: Base Environment Activation

**Before ANY work on this project, you MUST activate the base environment**:

```bash
# 1. Navigate to Environments directory
cd /Users/davidlary/Dropbox/Environments/

# 2. Activate base virtual environment
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# 3. Navigate to project directory
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
```

**Why?** The base-env activation script automatically sets ALL required environment variables:
- `GITHUB_TOKEN`, `GITHUB_USER`, `GITHUB_EMAIL` - for git operations
- `ANTHROPIC_API_KEY` - for Claude API
- `GOOGLE_API_KEY` - for Gemini API and SICE package
- `GROK_API_KEY` - optional AI provider
- `CHATGPT_API_KEY` - optional AI provider

**Verification**:
```bash
# Check environment is activated
echo $VIRTUAL_ENV  # Should show base-env path

# Check credentials are set
echo "GitHub: $GITHUB_USER"
echo "Anthropic: ${ANTHROPIC_API_KEY:0:10}..."
echo "Google: ${GOOGLE_API_KEY:0:10}..."
```

**See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for complete setup guide.**

---

## Dependencies

### Core Dependencies
- **Python**: 3.8+ (test on 3.8, 3.9, 3.10, 3.11)
- **LaTeX**: XeLaTeX (for compilation)
- **System**: tesseract-ocr (for OCR)
- **Environment**: base-env activation (for credentials)

### Python Packages
```
# PDF Processing
pdfplumber>=0.9.0
PyPDF2>=3.0.0
pytesseract>=0.3.10

# AI APIs
anthropic>=0.7.0
google-generativeai>=0.3.0

# Research
scholarly>=1.7.0
wikipedia>=1.4.0

# Bibliography
bibtexparser>=1.4.0

# LaTeX
pylatex>=1.4.0
jinja2>=3.1.0

# Images
pillow>=10.0.0

# General
requests>=2.31.0
click>=8.1.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Code Quality
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0

# Documentation
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0
```

---

## Success Criteria

### Module-Level Success
- ✅ All unit tests pass with 90%+ coverage
- ✅ Module documented with clear docstrings
- ✅ Module integrated into CLI
- ✅ Progress tracked in progress.json

### Integration-Level Success
- ✅ All integration tests pass
- ✅ Pipelines execute end-to-end
- ✅ No data loss between modules
- ✅ Error handling robust

### System-Level Success
- ✅ Complete textbook generated from PDFs
- ✅ Book compiles with XeLaTeX (no errors)
- ✅ Figures high quality and properly referenced
- ✅ Citations resolve correctly
- ✅ Writing style matches Air Quality book
- ✅ Package installs on Python 3.8-3.11
- ✅ Package installs with Anaconda
- ✅ SLSA3 provenance generated for releases
- ✅ 90%+ overall test coverage
- ✅ Documentation complete and accurate
- ✅ All tests pass in CI/CD (GitHub Actions)
- ✅ Compatible with Claude Code, Gemini, GitHub CLI

---

## Timeline Estimates

### Per-Module Development
- **Each bite-sized chunk**: 1-2 hours
- **25 chunks total**: 25-50 hours
- **Parallelization potential**: Some chunks can be done concurrently

### Per-Book Generation (After Implementation)
- **Phase 1 (Topic Analysis)**: 30 min - 1 hour (includes human review)
- **Phase 2 (Content Generation)**: 2-4 hours (automated, 12-14 chapters)
- **Phase 3 (Validation & Finalization)**: 30 min - 1 hour
- **Total per book**: 3-6 hours

---

## Recovery Procedures

### If Interrupted During Implementation

1. **Check progress.json**:
   ```bash
   cat MachineLearning/progress.json | jq '.recovery_checkpoint'
   ```

2. **Resume from last checkpoint**:
   ```bash
   slides2tex resume --book MachineLearning
   ```

3. **Manual recovery** (if needed):
   - Read progress.json to identify last completed chunk
   - Review ImplementationPlan.md for chunk requirements
   - Continue from next chunk in sequence

### If Interrupted During Book Generation

1. **Check progress.json**:
   ```bash
   slides2tex progress --book MachineLearning
   ```

2. **Resume pipeline**:
   ```bash
   slides2tex resume --book MachineLearning
   ```

3. **System automatically**:
   - Skips completed chapters
   - Resumes from last checkpoint
   - Validates completed work before continuing

---

## Next Steps

### Immediate Actions (Once Approved)

1. **Activate Base Environment** (REQUIRED FIRST):
   ```bash
   cd /Users/davidlary/Dropbox/Environments/
   source base-env/.venv/bin/activate
   cd Code/SlidesToLatex
   ```

2. **Verify Environment Variables Set**:
   ```bash
   echo "GitHub User: $GITHUB_USER"
   echo "GitHub Token: ${GITHUB_TOKEN:0:10}..."
   echo "Anthropic Key: ${ANTHROPIC_API_KEY:0:10}..."
   echo "Google Key: ${GOOGLE_API_KEY:0:10}..."
   ```

3. **Verify Git Repository** (already initialized):
   ```bash
   git status
   git remote -v  # Should show GitHub remote
   ```

4. **Begin Chunk 1: Project Setup**:
   - Follow implementation order above

---

## Questions for Clarification

**Before starting implementation, please confirm**:

1. ✅ Implementation plan approved?
2. ✅ All environment variables set?
3. ✅ Ready to initialize git repository?
4. ✅ Proceed with Chunk 1?

---

**Version History**:
- v1.0 (2026-01-27): Initial comprehensive implementation plan

**Last Updated**: January 27, 2026
**Status**: Awaiting approval to begin implementation
