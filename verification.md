# SlidesToTextbook - Verification & Testing Guide

**Purpose**: Optimized prompts for testing with Claude Code, Gemini Antigravity, and GitHub CLI

**Version**: 1.0
**Date**: January 27, 2026

---

## Table of Contents

1. [Claude Code Prompts](#claude-code-prompts)
2. [Gemini Antigravity Prompts](#gemini-antigravity-prompts)
3. [GitHub CLI Commands](#github-cli-commands)
4. [Cross-Tool Workflows](#cross-tool-workflows)

---

## Claude Code Prompts

### Prompt 1: Module Unit Testing

```
Test the [MODULE_NAME] module from the SlidesToTextBook repository.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Read the module: src/slides_to_textbook/modules/[module_name].py
2. Read the tests: tests/unit/test_[module_name].py
3. Run tests: pytest tests/unit/test_[module_name].py -v --cov=src/slides_to_textbook/modules/[module_name] --cov-report=term
4. Report:
   - Coverage percentage
   - Passing/failing tests
   - Any warnings or issues
5. If coverage < 90%, suggest specific additional tests

Replace [MODULE_NAME] with: PDFAnalyzer, TopicResearcher, ContentAuthor, FigureRecreator, PortraitGenerator, MarginNoteGenerator, LaTeXBuilder, BibliographyManager, ProgressTracker, or QualityValidator
```

### Prompt 2: Integration Testing

```
Run integration tests for Phase [X] of the SlidesToTextBook pipeline.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Read: tests/integration/test_pipeline_phase[X].py
2. Verify test fixtures exist
3. Run: pytest tests/integration/test_pipeline_phase[X].py -v --tb=short
4. Check progress.json for state updates
5. Report:
   - Test results (pass/fail for each test case)
   - Execution time
   - Progress tracking verification
   - Any integration issues

Replace [X] with: 1 (Topic Analysis), 2 (Content Generation), or 3 (Validation)
```

### Prompt 3: End-to-End Pipeline Test

```
Execute the complete end-to-end pipeline test for SlidesToTextBook.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Verify sample PDF: tests/fixtures/sample_lecture.pdf exists
2. Run: pytest tests/e2e/test_sample_lecture.py -v -s
3. Verify output:
   - Check generated chapter LaTeX
   - Verify figures created
   - Test XeLaTeX compilation
   - Validate bibliography
4. Measure:
   - Total execution time
   - Memory usage (if possible)
5. Report:
   - Complete success/failure
   - Quality metrics (word count, figure count, citation count)
   - Any warnings or issues
   - Suggestions for improvements
```

### Prompt 4: Multi-Version Python Testing

```
Test SlidesToTextBook package installation and tests across Python versions.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

For each Python version (3.8, 3.9, 3.10, 3.11):
1. Check if version available: python3.X --version
2. Create virtual environment: python3.X -m venv test_env_3X
3. Activate: source test_env_3X/bin/activate
4. Install package: pip install -e .
5. Run tests: pytest tests/unit/ -v
6. Check coverage: pytest --cov=src
7. Deactivate and clean up

Report:
- Success/failure per version
- Version-specific issues
- Compatibility matrix
- Recommended minimum version
```

### Prompt 5: Anaconda Environment Testing

```
Test SlidesToTextBook with Anaconda package management.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Check Anaconda installed: conda --version
2. Create environment: conda env create -f environment.yml
3. Activate: conda activate slides-to-textbook
4. Verify packages: conda list
5. Install in dev mode: pip install -e .
6. Run full test suite: pytest tests/ -v --cov=src --cov-report=term
7. Test CLI: slides2tex --help
8. Deactivate: conda deactivate
9. Remove environment: conda env remove -n slides-to-textbook

Report:
- Environment creation success
- Package installation success
- Test results
- CLI functionality
- Any Anaconda-specific issues
```

### Prompt 6: Code Quality & Security Audit

```
Perform code quality and security audit for SlidesToTextBook.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Run Black formatter check: black --check src/
2. Run Flake8 linter: flake8 src/
3. Run MyPy type checker: mypy src/
4. Security audit:
   - Search for hardcoded secrets: grep -r "api_key\|password\|token" src/ --exclude-dir=__pycache__
   - Check .gitignore coverage
   - Verify environment variable usage
5. Code complexity analysis:
   - Identify functions > 50 lines
   - Check cyclomatic complexity

Report:
- Formatting issues
- Linting warnings/errors
- Type hints coverage
- Security vulnerabilities (CRITICAL if found)
- Code complexity hotspots
- Recommendations for improvements
```

### Prompt 7: LaTeX Compilation Validation

```
Validate LaTeX compilation for generated textbook.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
Book Directory: [BOOK_PATH]

Steps:
1. Verify book structure:
   - main.tex exists
   - All Chapter-*.tex files exist
   - bibliography.bib exists
   - Figures/ directory structure correct
   - Pictures/ directory has header images
2. Test compilation:
   - Run: xelatex -interaction=nonstopmode main.tex
   - Run: bibtex main
   - Run: xelatex -interaction=nonstopmode main.tex (2nd pass)
   - Run: xelatex -interaction=nonstopmode main.tex (3rd pass)
3. Check output:
   - main.pdf created
   - File size reasonable (> 1MB)
   - No undefined references
   - All figures embedded
4. Validate quality:
   - Page count
   - Chapter count
   - Figure count
   - Citation count

Report:
- Compilation success/failure
- Error messages (if any)
- Output statistics
- Quality assessment
- Missing elements (if any)

Replace [BOOK_PATH] with actual book directory path.
```

### Prompt 8: Progress Tracking & Recovery Test

```
Test progress tracking and recovery mechanisms for SlidesToTextBook.

Repository: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

Steps:
1. Start pipeline on test data
2. Verify progress.json updates:
   - After each module execution
   - After each chapter completion
   - After figure creation
3. Simulate interruption:
   - Stop pipeline mid-execution (Ctrl+C)
4. Verify recovery checkpoint saved
5. Resume pipeline: slides2tex resume --book [TEST_BOOK]
6. Verify:
   - No duplicate work
   - Progress continues from checkpoint
   - Final output identical to uninterrupted run

Report:
- Progress tracking accuracy
- Recovery checkpoint frequency
- Resume functionality success
- Data integrity after recovery
- Suggestions for improvement
```

---

## Gemini Antigravity Prompts

### Prompt 1: Comprehensive Code Review

```
Conduct a comprehensive code review of the SlidesToTextBook repository.

Repository: https://github.com/davidlary/SlidesToTextBook

Focus Areas:
1. **Architecture & Design**:
   - Module separation and cohesion
   - Interface design
   - Error handling patterns
   - Logging strategy

2. **Code Quality**:
   - Readability and maintainability
   - Naming conventions
   - Documentation completeness
   - DRY principle adherence

3. **Best Practices**:
   - Python idioms usage
   - Type hints coverage
   - Exception handling
   - Resource management (file handles, API connections)

4. **Security**:
   - API key handling (must use environment variables)
   - Input validation
   - Path traversal prevention
   - Dependency vulnerabilities

5. **Performance**:
   - Algorithmic complexity
   - Memory usage
   - API call efficiency
   - Caching opportunities

Provide:
- Detailed findings per module
- Priority ranking (Critical, High, Medium, Low)
- Specific code examples with issues
- Concrete refactoring suggestions
- Estimated effort for fixes
```

### Prompt 2: Test Coverage Deep Dive

```
Analyze test coverage for SlidesToTextBook in detail.

Repository: https://github.com/davidlary/SlidesToTextBook

Analysis Required:
1. **Coverage Statistics**:
   - Overall coverage percentage
   - Per-module coverage breakdown
   - Line coverage vs branch coverage
   - Uncovered code identification

2. **Test Quality Assessment**:
   - Assertion adequacy
   - Edge case coverage
   - Error path testing
   - Mock usage appropriateness

3. **Missing Tests**:
   - Critical paths without tests
   - Error handling gaps
   - Integration points not tested
   - Performance test needs

4. **Test Organization**:
   - Test file structure
   - Fixture reusability
   - Test naming clarity
   - Test independence

5. **Improvement Plan**:
   - Priority tests to add (for 90%+ coverage)
   - Suggested test refactoring
   - Test data generation needs
   - CI/CD integration recommendations

Deliverable:
- Detailed coverage report
- Test gap analysis
- Prioritized test addition roadmap (to reach 90%+)
- Example test code for critical gaps
```

### Prompt 3: Writing Style Validation

```
Validate generated textbook content against Air Quality book writing style.

Repository: https://github.com/davidlary/SlidesToTextBook
Reference: /Users/davidlary/Dropbox/Apps/Overleaf/AirQualityV3/BookWritingStyle.md

Compare generated sample chapter with style guidelines:

1. **Tone & Voice**:
   - Accessible yet authoritative ✓/✗
   - Conversational transitions ✓/✗
   - Active engagement ✓/✗

2. **Structure**:
   - Context before technical details ✓/✗
   - Proper section hierarchy ✓/✗
   - Paragraph flow (4-8 sentences) ✓/✗

3. **Historical Context**:
   - Etymology explanations ✓/✗
   - Historical figures introduced ✓/✗
   - Cultural origins noted ✓/✗

4. **Technical Integration**:
   - Equations introduced naturally ✓/✗
   - Units provided (metric + imperial) ✓/✗
   - Chemical notation correct ✓/✗

5. **Examples & Details**:
   - Specific dates, places, numbers ✓/✗
   - Quantitative details ✓/✗
   - Diverse geographic examples ✓/✗

6. **Margin Notes**:
   - Key terms highlighted ✓/✗
   - Portraits properly formatted ✓/✗
   - Takeaways in italics ✓/✗

7. **Citations**:
   - Smooth integration ✓/✗
   - Not citation-heavy ✓/✗
   - Proper citation style ✓/✗

Provide:
- Section-by-section style adherence scores
- Specific examples of style violations
- Rewritten samples demonstrating correct style
- Prompts for ContentAuthor improvement
```

### Prompt 4: Figure Quality Assessment

```
Assess quality of generated scientific figures for SlidesToTextBook.

Repository: https://github.com/davidlary/SlidesToTextBook
Sample Figures: [FIGURE_DIRECTORY]

Evaluation Criteria:

1. **Visual Quality**:
   - Resolution (should be high, 300+ DPI)
   - Clarity and sharpness
   - Color scheme appropriateness
   - Contrast and readability

2. **Typography**:
   - Label font size (readable)
   - Font consistency
   - Special characters (Greek, subscripts) correct
   - Axis labels clear

3. **Content Accuracy**:
   - Data representation correct
   - Units labeled
   - Scale appropriate
   - Legend clear (if applicable)

4. **Style Consistency**:
   - Matches Air Quality book aesthetic
   - Color palette appropriate
   - Figure sizing consistent
   - Caption format correct

5. **LaTeX Integration**:
   - File format appropriate (PDF/EPS/PNG)
   - Proper embedding
   - Cross-references work
   - Width specifications correct

6. **Portrait Specific** (if applicable):
   - Resolution: 900×1200px ✓/✗
   - Sepia pre-1900, color post-1900 ✓/✗
   - Aspect ratio: 3:4 ✓/✗
   - Vignette effect appropriate ✓/✗

Provide:
- Per-figure quality scores
- Specific issues identified
- Comparison with reference figures
- SICE package prompt improvements
- Regeneration recommendations
```

### Prompt 5: Documentation Completeness Review

```
Review documentation completeness for SlidesToTextBook.

Repository: https://github.com/davidlary/SlidesToTextBook

Check:

1. **README.md**:
   - Clear overview ✓/✗
   - Installation instructions complete ✓/✗
   - Quick start examples ✓/✗
   - Links work ✓/✗
   - Badges accurate ✓/✗

2. **ImplementationPlan.md**:
   - All sections complete ✓/✗
   - Chunk definitions clear ✓/✗
   - Progress tracking specified ✓/✗
   - Timeline realistic ✓/✗

3. **verification.md** (this file):
   - Prompts clear and executable ✓/✗
   - All tools covered ✓/✗
   - Examples provided ✓/✗

4. **API Documentation**:
   - All modules documented ✓/✗
   - Function signatures complete ✓/✗
   - Parameter descriptions clear ✓/✗
   - Return types specified ✓/✗
   - Examples provided ✓/✗

5. **Docstrings**:
   - Coverage percentage
   - Format consistency (Google/NumPy style)
   - Parameter descriptions
   - Exception documentation
   - Example usage

6. **User Guides** (docs/):
   - Installation guide ✓/✗
   - Usage tutorial ✓/✗
   - Configuration guide ✓/✗
   - Troubleshooting ✓/✗

Provide:
- Documentation completeness score (%)
- Missing sections list
- Unclear sections to improve
- Suggested additions
- Example improvements
```

### Prompt 6: Performance & Scalability Analysis

```
Analyze performance and scalability of SlidesToTextBook.

Repository: https://github.com/davidlary/SlidesToTextBook

Analysis:

1. **Current Performance**:
   - Time per lecture PDF
   - Time per chapter generation
   - Time per figure creation
   - Total pipeline time (full book)

2. **Bottlenecks**:
   - Identify slowest modules
   - API call latency
   - File I/O operations
   - PDF processing time

3. **Scalability Testing**:
   - Test with 1, 5, 10, 20 lecture PDFs
   - Memory usage scaling
   - Concurrent processing limits
   - API rate limit handling

4. **Optimization Opportunities**:
   - Parallelization potential
   - Caching strategies
   - Batch API calls
   - Async operations

5. **Resource Usage**:
   - CPU utilization
   - Memory consumption
   - Disk I/O patterns
   - Network bandwidth

6. **Load Testing**:
   - Maximum concurrent pipelines
   - Error rate under load
   - Recovery after failures
   - Resource cleanup

Provide:
- Performance benchmark report
- Bottleneck analysis with data
- Optimization recommendations (prioritized)
- Scalability limits
- Infrastructure recommendations (if needed)
```

### Prompt 7: AI Content Quality Evaluation

```
Evaluate AI-generated content quality for SlidesToTextBook.

Repository: https://github.com/davidlary/SlidesToTextBook

Evaluation Focus:

1. **Accuracy**:
   - Mathematical equations correct ✓/✗
   - Technical terms used properly ✓/✗
   - Historical facts verified ✓/✗
   - Citations appropriate ✓/✗

2. **Coherence**:
   - Logical flow between sections
   - Topic transitions smooth
   - Concepts build properly
   - No contradictions

3. **Completeness**:
   - All topics from PDF covered
   - Key concepts explained
   - Examples provided
   - Equations derived/explained

4. **Pedagogical Quality**:
   - Suitable for target audience (graduate students)
   - Difficult concepts explained clearly
   - Build from simple to complex
   - Practical applications included

5. **Consistency**:
   - Terminology consistent throughout
   - Notation consistent
   - Style consistent (matches Air Quality book)
   - Voice consistent

6. **AI-Specific Issues**:
   - Hallucinations (false information)
   - Repetition or redundancy
   - Vague or generic content
   - "AI-sounding" language

Compare:
- Sample chapter from SlidesToTextBook
- Corresponding chapter from Air Quality book
- Original lecture PDF content

Provide:
- Quality scores per dimension
- Specific examples of issues
- Comparison with reference book
- Prompt engineering improvements
- Model selection recommendations (Claude vs Gemini)
```

---

## GitHub CLI Commands

### Command 1: Repository Status & Health

```bash
# View repository overview
gh repo view davidlary/SlidesToTextBook

# Check repository settings
gh repo view davidlary/SlidesToTextBook --json name,description,isPrivate,defaultBranchRef,diskUsage,forkCount,stargazerCount,updatedAt

# View recent commits (last 10)
gh api repos/davidlary/SlidesToTextBook/commits | jq '.[0:10] | .[] | {sha: .sha[0:7], author: .commit.author.name, message: .commit.message, date: .commit.author.date}'

# Check open issues
gh issue list --repo davidlary/SlidesToTextBook --state open

# Check closed issues
gh issue list --repo davidlary/SlidesToTextBook --state closed --limit 10

# Check pull requests
gh pr list --repo davidlary/SlidesToTextBook --state all

# View contributors
gh api repos/davidlary/SlidesToTextBook/contributors | jq '.[] | {login: .login, contributions: .contributions}'

# Check repository traffic (requires push access)
gh api repos/davidlary/SlidesToTextBook/traffic/views | jq '.'
```

### Command 2: Workflow & CI/CD Status

```bash
# List all workflows
gh workflow list --repo davidlary/SlidesToTextBook

# View workflow runs (test workflow)
gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml --limit 10

# View latest test run details
gh run view --repo davidlary/SlidesToTextBook $(gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml --limit 1 --json databaseId --jq '.[0].databaseId')

# Check test run status for all Python versions
gh run view --repo davidlary/SlidesToTextBook $(gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml --limit 1 --json databaseId --jq '.[0].databaseId') --json jobs --jq '.jobs[] | {name: .name, conclusion: .conclusion, duration: .completedAt}'

# Download test artifacts
gh run download --repo davidlary/SlidesToTextBook <run-id> -D /tmp/test-artifacts

# View workflow file
gh workflow view test.yml --repo davidlary/SlidesToTextBook

# Trigger workflow manually (if configured)
gh workflow run test.yml --repo davidlary/SlidesToTextBook

# Watch workflow run in real-time
gh run watch --repo davidlary/SlidesToTextBook <run-id>
```

### Command 3: Release & SLSA Provenance

```bash
# List all releases
gh release list --repo davidlary/SlidesToTextBook

# View specific release
gh release view v1.0.0 --repo davidlary/SlidesToTextBook

# Download release assets
gh release download v1.0.0 --repo davidlary/SlidesToTextBook -D /tmp/release

# Download specific pattern (provenance)
gh release download v1.0.0 --repo davidlary/SlidesToTextBook --pattern '*.intoto.jsonl' -D /tmp/provenance

# Create new release
gh release create v1.0.0 --repo davidlary/SlidesToTextBook --title "v1.0.0 - Initial Release" --notes "First stable release" dist/*

# View SLSA workflow runs
gh run list --repo davidlary/SlidesToTextBook --workflow=slsa.yml --limit 5

# Check SLSA workflow status
gh run view --repo davidlary/SlidesToTextBook $(gh run list --repo davidlary/SlidesToTextBook --workflow=slsa.yml --limit 1 --json databaseId --jq '.[0].databaseId')

# Verify provenance (requires slsa-verifier installed)
# Download first
gh release download v1.0.0 --repo davidlary/SlidesToTextBook
# Then verify
slsa-verifier verify-artifact \
  --provenance-path slides-to-textbook-1.0.0.tar.gz.intoto.jsonl \
  --source-uri github.com/davidlary/SlidesToTextBook \
  slides-to-textbook-1.0.0.tar.gz
```

### Command 4: Package Testing & Installation

```bash
# Install package from GitHub main branch
pip install git+https://github.com/davidlary/SlidesToTextBook.git

# Install specific release
pip install git+https://github.com/davidlary/SlidesToTextBook.git@v1.0.0

# Install in editable mode from local clone
git clone https://github.com/davidlary/SlidesToTextBook.git
cd SlidesToTextBook
pip install -e .

# Verify installation
pip show slides-to-textbook

# Test CLI availability
slides2tex --version
slides2tex --help

# Run installed package tests
python -m pytest --pyargs slides_to_textbook

# Uninstall
pip uninstall slides-to-textbook -y
```

### Command 5: Issue Management & Bug Reporting

```bash
# Create issue for bug
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Bug: Module X fails on edge case Y" \
  --body "**Description**: Detailed description of bug
**Steps to Reproduce**:
1. Step 1
2. Step 2
**Expected**: Expected behavior
**Actual**: Actual behavior
**Error**: \`\`\`
Error message
\`\`\`
**Environment**:
- Python: 3.10
- OS: macOS
- Version: 1.0.0" \
  --label "bug,priority:high"

# Create issue for feature request
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Feature: Add support for X" \
  --body "**Feature Description**: ...
**Use Case**: ...
**Proposed Solution**: ..." \
  --label "enhancement"

# Create issue for test failure
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Test Failure: test_module_x" \
  --body "**Test**: test_module_x
**Error**: \`\`\`
Error trace
\`\`\`
**Run**: https://github.com/davidlary/SlidesToTextBook/actions/runs/XXXXX" \
  --label "bug,testing"

# View issue details
gh issue view <issue-number> --repo davidlary/SlidesToTextBook

# Comment on issue
gh issue comment <issue-number> --repo davidlary/SlidesToTextBook --body "Additional information..."

# Close issue
gh issue close <issue-number> --repo davidlary/SlidesToTextBook --comment "Fixed in commit XXX"

# Search issues
gh issue list --repo davidlary/SlidesToTextBook --search "bug in:title"
```

### Command 6: Pull Request Workflow

```bash
# Create pull request
gh pr create --repo davidlary/SlidesToTextBook \
  --title "feat: Add module X" \
  --body "## Changes
- Added module X
- Added tests for module X
- Updated documentation

## Testing
- All tests pass
- Coverage: 95%

## Checklist
- [x] Tests added
- [x] Documentation updated
- [x] Code formatted (black)
- [x] Linting passed (flake8)" \
  --base main \
  --head feature/module-x

# View PR details
gh pr view <pr-number> --repo davidlary/SlidesToTextBook

# Check PR status
gh pr status --repo davidlary/SlidesToTextBook

# Check PR checks (CI/CD)
gh pr checks <pr-number> --repo davidlary/SlidesToTextBook

# Review PR
gh pr review <pr-number> --repo davidlary/SlidesToTextBook --approve --body "LGTM!"

# Merge PR
gh pr merge <pr-number> --repo davidlary/SlidesToTextBook --squash --delete-branch

# Close PR without merging
gh pr close <pr-number> --repo davidlary/SlidesToTextBook --comment "Not needed anymore"
```

### Command 7: Performance Benchmarking

```bash
# Time full pipeline execution
time slides2tex pipeline \
  --input tests/fixtures/sample_lecture.pdf \
  --output /tmp/test_book 2>&1 | tee /tmp/pipeline_benchmark.log

# Extract timing information
grep "Module.*completed" /tmp/pipeline_benchmark.log | awk '{print $1, $2, $3}'

# Create benchmark issue
BENCHMARK_RESULT=$(cat /tmp/pipeline_benchmark.log)
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Benchmark: Pipeline Performance" \
  --body "**Date**: $(date)
**Command**: \`slides2tex pipeline --input tests/fixtures/sample_lecture.pdf --output /tmp/test_book\`
**Results**:
\`\`\`
$BENCHMARK_RESULT
\`\`\`" \
  --label "performance,benchmark"

# Compare benchmark across versions
gh issue list --repo davidlary/SlidesToTextBook --label "benchmark" --state all --json number,title,createdAt,body | jq '.'
```

### Command 8: Dependency & Security Audit

```bash
# Clone repository
gh repo clone davidlary/SlidesToTextBook /tmp/slides-audit
cd /tmp/slides-audit

# Check for security vulnerabilities (requires pip-audit)
pip-audit -r requirements.txt

# Check outdated dependencies
pip list --outdated

# Generate dependency tree
pip install pipdeptree
pipdeptree

# Check for known vulnerabilities (requires safety)
pip install safety
safety check -r requirements.txt

# Report security issues
gh issue create --repo davidlary/SlidesToTextBook \
  --title "Security: Vulnerability in dependency X" \
  --body "**Package**: X
**Version**: Y
**Vulnerability**: CVE-XXXX-XXXX
**Severity**: High
**Fix**: Update to version Z" \
  --label "security,priority:critical"

# Cleanup
cd -
rm -rf /tmp/slides-audit
```

---

## Cross-Tool Workflows

### Workflow 1: Complete Testing Cycle

**Objective**: Test all aspects of the system across all three tools

1. **Claude Code**: Run unit tests for all modules
   ```
   [Use Claude Code Prompt 1 for each module]
   ```

2. **Claude Code**: Run integration tests
   ```
   [Use Claude Code Prompt 2 for phases 1, 2, 3]
   ```

3. **Gemini Antigravity**: Code review and test coverage analysis
   ```
   [Use Gemini Prompt 1 and Prompt 2]
   ```

4. **GitHub CLI**: Check CI/CD status
   ```bash
   gh run list --repo davidlary/SlidesToTextBook --workflow=test.yml --limit 1
   ```

5. **Claude Code**: E2E test
   ```
   [Use Claude Code Prompt 3]
   ```

6. **Gemini Antigravity**: Content quality evaluation
   ```
   [Use Gemini Prompt 7]
   ```

7. **GitHub CLI**: Create summary issue
   ```bash
   gh issue create --repo davidlary/SlidesToTextBook \
     --title "Testing Cycle Complete" \
     --body "All tests passed. Ready for release." \
     --label "testing,release"
   ```

### Workflow 2: Pre-Release Checklist

**Objective**: Verify everything before creating a release

1. **Claude Code**: Multi-version Python testing
   ```
   [Use Claude Code Prompt 4]
   ```

2. **Claude Code**: Anaconda environment testing
   ```
   [Use Claude Code Prompt 5]
   ```

3. **Claude Code**: Code quality & security audit
   ```
   [Use Claude Code Prompt 6]
   ```

4. **Gemini Antigravity**: Documentation review
   ```
   [Use Gemini Prompt 5]
   ```

5. **Gemini Antigravity**: Performance analysis
   ```
   [Use Gemini Prompt 6]
   ```

6. **GitHub CLI**: Run all workflows
   ```bash
   gh workflow run test.yml --repo davidlary/SlidesToTextBook
   gh run watch --repo davidlary/SlidesToTextBook
   ```

7. **GitHub CLI**: Create release
   ```bash
   gh release create v1.0.0 --repo davidlary/SlidesToTextBook \
     --title "v1.0.0 - Initial Release" \
     --notes-file RELEASE_NOTES.md \
     dist/*
   ```

8. **GitHub CLI**: Verify SLSA provenance
   ```bash
   [Use GitHub CLI Command 3]
   ```

### Workflow 3: Bug Investigation & Fix

**Objective**: Investigate, fix, and verify a bug

1. **User reports bug via GitHub**:
   ```bash
   gh issue view <issue-number> --repo davidlary/SlidesToTextBook
   ```

2. **Claude Code**: Reproduce bug
   ```
   Reproduce the bug reported in issue #<issue-number> for SlidesToTextBook.

   Steps:
   1. Read issue: gh issue view <issue-number>
   2. Understand reproduction steps
   3. Attempt to reproduce locally
   4. Confirm bug exists
   5. Report findings
   ```

3. **Gemini Antigravity**: Root cause analysis
   ```
   Analyze root cause of bug reported in issue #<issue-number> for SlidesToTextBook.

   Focus on:
   - Module involved
   - Input conditions causing bug
   - Expected vs actual behavior
   - Potential code locations
   - Suggested fix approach
   ```

4. **Claude Code**: Implement fix with tests
   ```
   Fix the bug reported in issue #<issue-number> for SlidesToTextBook.

   Steps:
   1. Implement fix in appropriate module
   2. Add regression test
   3. Run unit tests for module
   4. Run integration tests
   5. Verify fix works
   ```

5. **Claude Code**: Verify fix
   ```
   [Use Claude Code Prompt 1 for the fixed module]
   ```

6. **GitHub CLI**: Create PR
   ```bash
   gh pr create --repo davidlary/SlidesToTextBook \
     --title "fix: Bug in module X (closes #<issue-number>)" \
     --body "Fixes #<issue-number>

     ## Changes
     - Fixed bug in module X
     - Added regression test

     ## Testing
     - All tests pass
     - Bug no longer reproducible"
   ```

7. **GitHub CLI**: Merge and close issue
   ```bash
   gh pr merge <pr-number> --repo davidlary/SlidesToTextBook --squash
   gh issue close <issue-number> --repo davidlary/SlidesToTextBook
   ```

### Workflow 4: Feature Development

**Objective**: Develop a new feature from planning to deployment

1. **Gemini Antigravity**: Design review
   ```
   Review the design for new feature: [FEATURE_NAME] for SlidesToTextBook.

   Consider:
   - Architecture fit
   - Module design
   - Interface design
   - Error handling
   - Testing strategy
   - Documentation needs
   ```

2. **Claude Code**: Implement feature
   ```
   Implement [FEATURE_NAME] for SlidesToTextBook following the design.

   Steps:
   1. Create module file
   2. Implement core functionality
   3. Add error handling
   4. Add logging
   5. Add docstrings
   ```

3. **Claude Code**: Write tests
   ```
   Write comprehensive tests for [FEATURE_NAME] in SlidesToTextBook.

   Include:
   - Unit tests (95%+ coverage)
   - Integration tests
   - Edge case tests
   - Error handling tests
   ```

4. **Claude Code**: Run tests
   ```
   [Use Claude Code Prompt 1 for the new module]
   ```

5. **Gemini Antigravity**: Code review
   ```
   [Use Gemini Prompt 1 focusing on the new feature]
   ```

6. **Claude Code**: Update documentation
   ```
   Update documentation for new feature [FEATURE_NAME] in SlidesToTextBook.

   Update:
   - README.md (add feature to list)
   - API documentation (module docs)
   - Usage examples
   - ImplementationPlan.md (if architectural)
   ```

7. **GitHub CLI**: Create PR
   ```bash
   gh pr create --repo davidlary/SlidesToTextBook \
     --title "feat: Add [FEATURE_NAME]" \
     --body "## Feature Description
     [Description]

     ## Changes
     - Added module X
     - Added tests (95% coverage)
     - Updated documentation

     ## Testing
     - All tests pass
     - Feature works as expected"
   ```

8. **GitHub CLI**: Merge
   ```bash
   gh pr merge <pr-number> --repo davidlary/SlidesToTextBook --squash
   ```

---

## Quick Reference

### Claude Code - Best For
- ✅ Running tests (unit, integration, E2E)
- ✅ Package installation testing
- ✅ LaTeX compilation validation
- ✅ Code execution and debugging
- ✅ Progress tracking verification
- ✅ Multi-version Python testing

### Gemini Antigravity - Best For
- ✅ Comprehensive code review
- ✅ Architecture and design analysis
- ✅ Test coverage deep dive
- ✅ Content quality evaluation (AI-generated text)
- ✅ Figure quality assessment
- ✅ Performance and scalability analysis
- ✅ Documentation review

### GitHub CLI - Best For
- ✅ Repository status and health checks
- ✅ Workflow and CI/CD monitoring
- ✅ Release management
- ✅ SLSA provenance verification
- ✅ Issue and PR management
- ✅ Dependency and security audits
- ✅ Benchmarking and performance tracking

---

## Environment Setup

**Required Environment Variables**:
```bash
export GOOGLE_API_KEY='your-google-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'
export GITHUB_TOKEN='your-github-token'
export GITHUB_USER='davidlary'
export GITHUB_EMAIL='your-email@example.com'
```

**Verify Setup**:
```bash
# Check environment variables
echo $GOOGLE_API_KEY | cut -c1-10  # Should show first 10 chars
echo $ANTHROPIC_API_KEY | cut -c1-10
echo $GITHUB_TOKEN | cut -c1-10

# Check GitHub CLI authentication
gh auth status

# Check repository access
gh repo view davidlary/SlidesToTextBook
```

---

## Troubleshooting

### Common Issues

**Issue**: Tests fail due to missing API keys
**Solution**: Ensure all environment variables are set:
```bash
source ~/.bashrc  # or ~/.zshrc
# Re-export variables if needed
```

**Issue**: LaTeX compilation fails
**Solution**: Verify XeLaTeX installed:
```bash
xelatex --version
```

**Issue**: GitHub CLI commands fail
**Solution**: Re-authenticate:
```bash
gh auth login
```

**Issue**: Package import fails
**Solution**: Reinstall in editable mode:
```bash
pip install -e .
```

---

**Last Updated**: January 27, 2026
**Version**: 1.0
