import logging
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class QualityValidator:
    """
    Validates the quality of the generated book content.
    Enforces "Zero Tolerance" for placeholders and low-quality assets.
    """
    def __init__(self, book_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.book_dir = book_dir
        self.figures_dir = book_dir / "Figures"

    def validate(self) -> Dict[str, Any]:
        """Run all validation checks."""
        self.logger.info(f"Starting Quality Validation for: {self.book_dir}")
        report = {
            "status": "passed",
            "errors": [],
            "warnings": []
        }

        # 1. Check for Placeholder Text
        self._check_text_content(report)

        # 2. Check Figure Quality (Resolution/Size)
        self._check_image_quality(report)

        # 3. Check LaTeX Compilation (Dry run or syntax check)
        self._check_latex_structure(report)

        if report["errors"]:
            report["status"] = "failed"
        
        self.logger.info(f"Validation Complete. Status: {report['status']}")
        return report

    def _check_text_content(self, report: Dict[str, Any]):
        """Scan .tex files for forbidden strings."""
        forbidden = ["Lorem Ipsum", "PLACEHOLDER", "TBD", "Unknown"]
        
        for tex_file in self.book_dir.glob("*.tex"):
            try:
                content = tex_file.read_text()
                for term in forbidden:
                    if term in content:
                        normalized_term = term.lower()
                        # Allow "Unknown" if it's not a standalone placeholder (context dependent), 
                        # but for now be strict.
                        report["errors"].append(f"Found forbidden term '{term}' in {tex_file.name}")
            except Exception as e:
                report["errors"].append(f"Could not read {tex_file.name}: {e}")

    def _check_image_quality(self, report: Dict[str, Any]):
        """Check images for size and existence."""
        # Check Portraits
        portraits_dir = self.book_dir / "Portraits"
        
        if not portraits_dir.exists():
             report["errors"].append(f"Portraits directory missing: {portraits_dir}")
        else:
             images = list(portraits_dir.glob("*.[pj][pn][g]"))
             if not images:
                 report["errors"].append(f"No portraits generated in {portraits_dir}")
             else:
                 for img_path in images:
                     self._validate_single_image(img_path, report, min_size_kb=50)

        # Check Chapter Figures
        found_chapter_figures = False
        for chapter_dir in self.figures_dir.glob("Chapter-*"):
            if chapter_dir.is_dir():
                images = list(chapter_dir.glob("*.[pj][pn][g]"))
                if images:
                    found_chapter_figures = True
                    for img_path in images:
                        self._validate_single_image(img_path, report, min_size_kb=50)
        
        # Also check root for concept figures
        root_figures = list(self.figures_dir.glob("*.png"))
        if root_figures:
             found_chapter_figures = True
             for img_path in root_figures:
                 self._validate_single_image(img_path, report, min_size_kb=50)

        if not found_chapter_figures:
            report["errors"].append("No scientific figures generated.")

    def _validate_single_image(self, img_path: Path, report: Dict[str, Any], min_size_kb: int):
        if img_path.stat().st_size < min_size_kb * 1024:
             report["errors"].append(f"Image {img_path.name} is too small ({img_path.stat().st_size} bytes). Likely a placeholder.")
        
        # Could add resolution check with PIL, but size is a good proxy for "solid color block"

    def _check_latex_structure(self, report: Dict[str, Any]):
        """Check if main.tex exists and bibliography is non-empty."""
        main_tex = self.book_dir / "main.tex"
        if not main_tex.exists():
            report["errors"].append("main.tex missing")
            
        bib_file = self.book_dir / "bibliography.bib"
        if not bib_file.exists():
            report["errors"].append("bibliography.bib missing")
        elif bib_file.stat().st_size < 100:
             report["errors"].append("bibliography.bib is suspiciously empty")
