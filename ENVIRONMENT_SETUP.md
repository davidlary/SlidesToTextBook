# Environment Setup Guide

**CRITICAL**: This document specifies the exact environment setup required for implementing the SlidesToTextBook system. All environment variables, API keys, and credentials are pre-configured in a base virtual environment.

---

## Environment Activation (REQUIRED)

### Step 1: Navigate to Environments Directory
```bash
cd /Users/davidlary/Dropbox/Environments/
```

### Step 2: Activate Base Virtual Environment
```bash
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate
```

**This activation script automatically sets ALL required environment variables including**:
- GitHub credentials (GITHUB_TOKEN, GITHUB_USER, GITHUB_EMAIL)
- ANTHROPIC_API_KEY (for Claude)
- GOOGLE_API_KEY (for Gemini)
- GROK API key
- CHATGPT API key
- Any other configured credentials

### Step 3: Verify Environment Variables
```bash
# Verify all required variables are set
echo "GitHub User: ${GITHUB_USER}"
echo "GitHub Email: ${GITHUB_EMAIL}"
echo "GitHub Token: ${GITHUB_TOKEN:0:10}..."  # First 10 chars only
echo "Anthropic API Key: ${ANTHROPIC_API_KEY:0:10}..."
echo "Google API Key: ${GOOGLE_API_KEY:0:10}..."
```

**Expected Output**: All variables should show values (not empty).

### Step 4: Navigate to Project Directory
```bash
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
```

---

## Complete Startup Sequence

**For every work session, execute these commands in order**:

```bash
# 1. Go to Environments directory
cd /Users/davidlary/Dropbox/Environments/

# 2. Activate base environment (sets all credentials)
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# 3. Go to project directory
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

# 4. Verify you're in the right place
pwd  # Should show: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

# 5. Check git status
git status

# 6. Verify environment variables (optional but recommended)
env | grep -E "GITHUB_|ANTHROPIC_|GOOGLE_|GROK|CHATGPT" | wc -l  # Should be > 5
```

---

## Environment Variables Reference

### Required Variables (Set by base-env activation)

| Variable | Purpose | Used By |
|----------|---------|---------|
| `GITHUB_TOKEN` | GitHub API authentication | Git operations, GitHub CLI |
| `GITHUB_USER` | GitHub username | Git commits, GitHub CLI |
| `GITHUB_EMAIL` | GitHub email | Git commits |
| `ANTHROPIC_API_KEY` | Claude API access | ContentAuthor, TopicResearcher |
| `GOOGLE_API_KEY` | Gemini API access | FigureRecreator, PortraitGenerator, SICE |
| `GROK_API_KEY` | Grok API access | Optional: Alternative AI provider |
| `CHATGPT_API_KEY` | ChatGPT API access | Optional: Alternative AI provider |

---

## Security Notes

### ✅ SAFE - Environment Variables
- All API keys stored in base-env virtual environment activation script
- Never hardcoded in any Python files
- Never committed to git repository
- Automatically available when base-env is activated

### ⚠️ DO NOT
- Never echo full API keys (use `${VAR:0:10}...` to show only first 10 chars)
- Never commit `.env` files
- Never put credentials in code comments
- Never push `.env` or credential files to GitHub

### 🔒 `.gitignore` Protection
The repository `.gitignore` file explicitly excludes:
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
```

---

## Verification Checklist

Before starting implementation, verify:

- [ ] Base environment activated: `echo $VIRTUAL_ENV` shows path
- [ ] GitHub credentials set: `echo $GITHUB_USER` shows username
- [ ] Anthropic API key set: `echo ${ANTHROPIC_API_KEY:0:10}` shows value
- [ ] Google API key set: `echo ${GOOGLE_API_KEY:0:10}` shows value
- [ ] In correct directory: `pwd` shows `.../SlidesToLatex`
- [ ] Git repository initialized: `git status` works
- [ ] Git remote configured: `git remote -v` shows GitHub URL

**If any check fails, STOP and fix before proceeding.**

---

## Troubleshooting

### Problem: Environment variables not set after activation

**Solution**:
```bash
# Deactivate if already in a venv
deactivate 2>/dev/null

# Go to base directory
cd /Users/davidlary/Dropbox/Environments/

# Re-activate
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# Verify
env | grep ANTHROPIC_API_KEY
```

### Problem: "command not found: source"

**Solution**: You might be using a different shell.
```bash
# For bash/zsh
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# For csh/tcsh
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate.csh

# For fish
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate.fish
```

### Problem: Git operations fail with authentication error

**Solution**: Verify GitHub credentials:
```bash
# Check token is set
echo ${GITHUB_TOKEN:0:10}

# Test GitHub CLI authentication
gh auth status

# If needed, re-login
gh auth login
```

### Problem: API calls fail with authentication error

**Solution**: Verify API keys are set:
```bash
# Check Anthropic
python -c "import os; print('Anthropic:', 'SET' if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET')"

# Check Google
python -c "import os; print('Google:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"
```

---

## For Gemini Antigravity Implementation

**Before starting ANY implementation work, execute**:

```bash
# Setup sequence
cd /Users/davidlary/Dropbox/Environments/
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex

# Verification
echo "Environment: $(basename $VIRTUAL_ENV)"
echo "Directory: $(pwd)"
echo "Git status: $(git status -s | wc -l) modified files"
echo "GitHub: $GITHUB_USER"
echo "APIs: $(env | grep -E '_API_KEY' | wc -l) keys configured"
```

**Expected output**:
```
Environment: .venv
Directory: /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
Git status: 0 modified files  (or appropriate number)
GitHub: davidlary
APIs: 4 keys configured  (or more)
```

---

## Python Virtual Environment vs Base Environment

### Base Environment (base-env)
- **Location**: `/Users/davidlary/Dropbox/Environments/base-env/.venv/`
- **Purpose**: Sets environment variables (API keys, credentials)
- **Always activate first**: This is REQUIRED for all work

### Project Virtual Environment (optional, created during Chunk 22)
- **Location**: Will be created in project directory during package setup
- **Purpose**: Project-specific Python packages
- **Note**: Base environment MUST still be activated first to get credentials

### Workflow
```bash
# 1. Activate base environment (for credentials)
source /Users/davidlary/Dropbox/Environments/base-env/.venv/bin/activate

# 2. Then optionally activate project venv (if created)
# source venv/bin/activate  # After Chunk 22

# OR use system Python with base-env credentials
python3 -m pip install -e .
```

---

## Quick Reference Card

**Copy this to start each session**:

```bash
cd /Users/davidlary/Dropbox/Environments/
source base-env/.venv/bin/activate
cd Code/SlidesToLatex
git status
```

---

**Last Updated**: January 27, 2026
**Version**: 1.0
**Critical**: This setup MUST be completed before any implementation work
