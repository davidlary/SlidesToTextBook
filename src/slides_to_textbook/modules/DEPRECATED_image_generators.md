# DEPRECATED: image_generators.py

**Date Deprecated:** February 2, 2026

## Status

This module (`image_generators.py`) has been **DEPRECATED** and should not be used.

## Reason for Deprecation

### FigureRecreator Class
- **Status:** DELETED
- **Reason:** Figure generation was not working properly
- **Replacement:** None - figure generation has been removed from the pipeline

### PortraitGenerator Class
- **Status:** REPLACED
- **Reason:** Moved to standalone CLI package for better maintainability and batch processing
- **Replacement:** Use the standalone PortraitGenerator CLI package from:
  - Repository: https://github.com/davidlary/PortraitGenerator
  - Installation: `pip install portrait-generator` (or clone and install from repo)
  - Usage: `portrait-generator batch --input people.json --output-dir /path/to/portraits/`

## Migration Guide

### For Portraits

**Old Code (DEPRECATED):**
```python
from slides_to_textbook.modules.image_generators import PortraitGenerator

portrait_gen = PortraitGenerator(output_dir)
portrait_path = portrait_gen.generate_portrait(person_name)
```

**New Code:**
```python
import subprocess
import json

# 1. Create input JSON with people names
people_data = [{"name": "Arthur Samuel"}, {"name": "Geoffrey Hinton"}]
with open("people.json", "w") as f:
    json.dump(people_data, f)

# 2. Call standalone CLI in batch mode
subprocess.run([
    "portrait-generator", "batch",
    "--input", "people.json",
    "--output-dir", "/path/to/Portraits/Chapter-Introduction/",
    "--style", "Photorealistic",  # Only use Photorealistic paintings
    "--naming", "{name}_Painting"  # Output format: PersonName_Painting.png
])
```

### For Figures

Figure generation has been completely removed from the pipeline. If figures are needed in the future, they should be created manually or through a different system.

## Files to Update

If you see imports of `image_generators`, update them:

- ❌ `from slides_to_textbook.modules.image_generators import FigureRecreator, PortraitGenerator`
- ✅ Use CLI subprocess calls for portraits (see above)
- ✅ Remove all figure generation code

## Affected Files

The following files have been updated to remove these dependencies:
- `run_lecture1.py` - Updated to use CLI approach
- Any other scripts importing from `image_generators` should be updated

## Backup

The original `image_generators.py` file has been renamed to `image_generators.py.deprecated` for reference, but should not be imported or used.
