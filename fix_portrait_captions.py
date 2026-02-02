#!/usr/bin/env python3
r"""
Fix Portrait Captions in Chapter-Introduction.tex

This script removes duplicate caption text from portrait margin notes.
Portraits already have captions embedded in the image, so additional
LaTeX captions create duplication.

BEFORE:
\automarginnote{\includegraphics[width=\linewidth]{Portraits/...} \\ \centering \footnotesize Person Name (dates)}

AFTER:
\automarginnote{\includegraphics[width=\linewidth]{Portraits/...}}
"""

import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fix_portrait_captions(tex_path: Path, backup: bool = True) -> int:
    """
    Remove caption text from portrait margin notes in a LaTeX file.

    Args:
        tex_path: Path to the .tex file to fix
        backup: If True, create a .bak backup first

    Returns:
        Number of captions fixed
    """
    logger.info(f"Fixing portrait captions in: {tex_path}")

    # Read original content
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create backup if requested
    if backup:
        backup_path = tex_path.with_suffix('.tex.bak')
        backup_path.write_text(content)
        logger.info(f"Created backup: {backup_path}")

    # Pattern to match portrait margin notes with captions
    # Matches: \automarginnote{\includegraphics[...]{path} \\ ... person info}
    # Captures: the graphics command and any text after \\
    pattern = r'(\\automarginnote\{\\includegraphics\[[^\]]+\]\{Portraits/[^}]+\})\s*\\\\\s*[^}]+(})'

    # Count matches
    matches = re.findall(pattern, content)
    logger.info(f"Found {len(matches)} portrait captions to fix")

    if len(matches) == 0:
        logger.info("No captions found - file may already be fixed")
        return 0

    # Replace: keep only the \automarginnote{\includegraphics{...}}
    # Remove the \\ \centering \footnotesize Person Name (dates) part
    fixed_content = re.sub(pattern, r'\1\2', content)

    # Write fixed content
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    logger.info(f"Fixed {len(matches)} portrait captions")
    return len(matches)


def main():
    """Fix captions in Chapter-Introduction.tex"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Remove duplicate captions from portrait margin notes"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"),
        help="Path to LaTeX file (default: Chapter-Introduction.tex)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup file"
    )

    args = parser.parse_args()

    if not args.input.exists():
        logger.error(f"File not found: {args.input}")
        return 1

    count = fix_portrait_captions(args.input, backup=not args.no_backup)

    print(f"\n✓ Fixed {count} portrait captions in {args.input}")
    if count > 0:
        print(f"✓ Backup saved to {args.input.with_suffix('.tex.bak')}")
    print("\nPortraits now display correctly without duplicate captions.")

    return 0


if __name__ == "__main__":
    exit(main())
