# SlidesToTextbook

**Convert PDF lecture slides into professionally-formatted LaTeX textbooks**

[![Tests](https://github.com/davidlary/SlidesToTextBook/workflows/test/badge.svg)](https://github.com/davidlary/SlidesToTextBook/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This system automatically transforms PDF lecture slides into high-quality LaTeX textbooks that match the pedagogical excellence, accuracy, and aesthetic beauty of professional academic textbooks.

### Key Features

- 🎓 **Pedagogical Excellence**: Engaging, accessible writing style with historical context
- 🔬 **Scientific Accuracy**: Precise mathematical notation, proper citations
- 🎨 **Aesthetic Beauty**: High-quality figures, professional typography
- 🤖 **AI-Powered**: Uses Claude & Gemini for content generation
- 📊 **Comprehensive Testing**: 90%+ test coverage
- 🔒 **Secure**: Never commits API keys or credentials
- 🔄 **Recoverable**: Resume from interruptions
- 📦 **Multi-Platform**: Works with standard Python and Anaconda

---

## Current Projects

### Machine Learning Textbook
- **Source**: 14 lecture PDFs from PHYS 5336 (2026)
- **Target**: `/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/`
- **Status**: In development

### Computational Methods Textbook
- **Source**: 12+ lecture PDFs from PHYS 5315 (2025)
- **Target**: `/Users/davidlary/Dropbox/Apps/Overleaf/ComputationalMethodsBook/`
- **Status**: Planned

---

## Installation

### ⚠️ CRITICAL: Environment Setup FIRST

**Before any installation or usage, you MUST activate the base environment**:

```bash
# 1. Navigate to Environments directory
cd /Users/davidlary/Dropbox/Environments/

# 2. Activate base virtual environment (sets ALL credentials)
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# 3. Navigate to project directory
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

# 4. Verify credentials are set
echo "GitHub: $GITHUB_USER | APIs configured: $(env | grep -E '_API_KEY' | wc -l)"
```

**This activation automatically sets**:
- GitHub credentials (GITHUB_TOKEN, GITHUB_USER, GITHUB_EMAIL)
- ANTHROPIC_API_KEY (Claude)
- GOOGLE_API_KEY (Gemini)
- GROK_API_KEY
- CHATGPT_API_KEY

**See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for complete details.**

---

### Standard Python

```bash
# AFTER activating base-env (see above), then:

# Clone repository (if not already cloned)
git clone https://github.com/davidlary/SlidesToTextBook.git
cd SlidesToTextBook

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Anaconda

```bash
# AFTER activating base-env (see above), then:

# Create environment from environment.yml
conda env create -f environment.yml

# Activate conda environment
conda activate slides-to-textbook

# Install package
pip install -e .
```

---

## Quick Start

### Prerequisites

1. **Environment Activation** (REQUIRED - see above):
   ```bash
   cd /Users/davidlary/Dropbox/Environments/
   source base-env/.venv/bin/activate
   cd Code/SlidesToLatex
   ```

2. **System Requirements**:
   - Python 3.8+
   - XeLaTeX (for compilation)
   - tesseract-ocr (for OCR)

### Usage

```bash
# Analyze lecture PDFs
slides2tex analyze --input /path/to/lectures/*.pdf --output topics.json

# Review and approve topics (interactive)
slides2tex approve --topics topics.json --output approved_topics.json

# Generate complete textbook (automated)
slides2tex generate --topics approved_topics.json --output /path/to/book/

# Validate book
slides2tex validate --book /path/to/book/

# Full pipeline
slides2tex pipeline --input /path/to/lectures/*.pdf --output /path/to/book/

# Check progress
slides2tex progress --book MachineLearning

# Resume from interruption
slides2tex resume --book MachineLearning
```

---

## Architecture

### Core Modules

1. **PDFAnalyzer**: Extract topics, equations, figures from PDFs
2. **TopicResearcher**: Research historical context, citations
3. **ContentAuthor**: Generate engaging textbook prose
4. **FigureRecreator**: Create high-quality scientific figures
5. **PortraitGenerator**: Generate historical figure portraits
6. **MarginNoteGenerator**: Create margin notes with key terms
7. **LaTeXBuilder**: Assemble complete LaTeX structure
8. **BibliographyManager**: Build bibliography from citations
9. **ProgressTracker**: Enable recovery from interruptions
10. **QualityValidator**: Verify compilation and quality

### Workflow

```
PDFs → Topic Analysis (human approval) → Content Generation (automated) → Validation → Git Commit
```

---

## Testing

```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run E2E tests
pytest tests/e2e/ -v
```

**Coverage Target**: 90%+ overall

---

## Documentation

- **[ImplementationPlan.md](ImplementationPlan.md)**: Comprehensive implementation guide
- **[verification.md](verification.md)**: Multi-tool testing prompts
- **[docs/](docs/)**: Detailed API documentation

---

## Development

### Project Structure

```
SlidesToLatex/
├── src/slides_to_textbook/    # Main package
│   ├── modules/                # Core modules
│   ├── templates/              # LaTeX templates
│   └── utils/                  # Utilities
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test data
├── MachineLearning/            # ML book project
└── ComputationalPhysics/       # Comp methods book project
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## Security

**CRITICAL**: Never commit API keys or credentials.

- Use environment variables for all secrets
- Review `.gitignore` before committing
- Run `git status` to check staged files
- Use `git diff --staged` to review changes

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Authors

- **Dr. David Lary** - University of Texas at Dallas
- **Claude Sonnet 4.5** - AI Assistant

---

## Acknowledgments

- Reference book structure: **Air Quality V3** textbook
- SICE Package: Scientific Image Creation and Validation
- Claude API: Anthropic
- Gemini API: Google

---

## Status

🚧 **In Active Development** 🚧

See [ImplementationPlan.md](ImplementationPlan.md) for detailed roadmap.

---

**Last Updated**: January 27, 2026
**Version**: 1.0.0
