# Handoff Prompt: SlidesToTextBook (Jan 29)

**Current Objective**: Finalize the conversion of "Lecture-1.pdf" into a high-end, university-standard latex textbook.

**Status**: Phase 7 Completed. The system is fully functional and generating high-quality assets.

### 1. Key Achievements (Phase 7 Polish)

- **Adaptive Portraits**:
  - **Single/Pair**: Generated as **Vertical (3:4)** (768x1024). *Code*: `image_generators.py` (line 165+).
  - **Group (>2)**: Generated as **Horizontal (4:3)** (1024x768). *Code*: `image_generators.py` (line 187+).
  - **Result**: No more distortion/squished faces for groups like "Newell, Simon, and Shaw".
- **Cinematic Aesthetics**:
  - **Upgrade**: All figures prompt for "Cinematic 3D Scientific Render" and "Unreal Engine 5".
  - **Result**: Figures are >1MB detailed renders, not simple charts.
- **LaTeX Compilation**:
  - **Fix**: Patched `content_author.py` and `run_lecture1.py` to use correct `Portraits/` and `Figures/` paths.
  - **Result**: `main.pdf` compiles successfully (9.3 MB, 20 pages).

### 2. Immediate Next Steps (Phase 8)

1. **Generate Walkthrough**: Use `generate_walkthrough.py` (or create it) to create a visual evidence document showing the PDF pages with the new Art.
2. **User Notification**: Inform the user that the PDF is ready for final review.
3. **Integration**: If approved, apply the same logic to Lectures 2-N.

### 3. Environment & Configuration

- **Script**: `python run_lecture1.py` (Runs the full pipeline).
- **Virtual Env**: `/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/.venv` (Verified).
- **API Keys**:
  - `ANTHROPIC_API_KEY`: Set via env/keychain.
  - `GOOGLE_API_KEY`: Set via env/keychain (`AIzaSyDL...`).
  - `GITHUB_TOKEN`: Set via env/keychain.

### 4. Important File Paths

- **Output PDF**: `/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/main.pdf`
- **Portraits**: `/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Portraits/Chapter-Introduction/`
- **Figures**: `/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Figures/Chapter-Introduction/`
- **Code**: `/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/`

### 5. Verification Commands

To verify the system is working on the new machine:

```bash
cd /Users/davidlary/Dropbox/Environments/Code/SlidesToLatex
source .venv/bin/activate
# Run the pipeline (check strict flag)
python run_lecture1.py
# Check PDF
open /Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/main.pdf
```
