"""
Portrait Preprocessor Module

Extracts names of historical figures and scientists from PDF lecture slides
or LaTeX chapters to prepare input for the standalone PortraitGenerator CLI.

This module creates the bridge between PDF analysis and portrait generation.
"""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import pdfplumber
import re


class PortraitPreprocessor:
    """
    Extracts people names from PDFs or LaTeX files and prepares them
    for batch portrait generation using the standalone PortraitGenerator CLI.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_from_pdf(self, pdf_path: Path, use_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Extract names of historical figures from a PDF.

        Args:
            pdf_path: Path to the PDF lecture file
            use_ai: If True, use AI to identify names. If False, use regex patterns.

        Returns:
            List of dicts with person info: [{"name": "Arthur Samuel", "context": "..."}]
        """
        self.logger.info(f"Extracting people from PDF: {pdf_path}")

        # 1. Extract text from PDF
        text_content = self._extract_pdf_text(pdf_path)

        # 2. Extract names (AI or pattern-based)
        if use_ai:
            people = self._extract_with_ai(text_content)
        else:
            people = self._extract_with_patterns(text_content)

        self.logger.info(f"Found {len(people)} people in PDF")
        return people

    def extract_from_latex(self, latex_path: Path, use_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Extract names from an existing LaTeX chapter file.

        Args:
            latex_path: Path to the .tex file
            use_ai: If True, use AI to identify names. If False, use regex patterns.

        Returns:
            List of dicts with person info
        """
        self.logger.info(f"Extracting people from LaTeX: {latex_path}")

        with open(latex_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract names
        if use_ai:
            people = self._extract_with_ai(content)
        else:
            people = self._extract_with_patterns(content)

        self.logger.info(f"Found {len(people)} people in LaTeX")
        return people

    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract all text from PDF."""
        pages_text = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages_text.append(text)

        return "\n\n".join(pages_text)

    def _extract_with_ai(self, content: str) -> List[Dict[str, Any]]:
        """
        Use AI to identify historical figures and scientists mentioned in content.

        Args:
            content: Text content to analyze

        Returns:
            List of people with context
        """
        from slides_to_textbook.utils.api_clients import AIClient

        client = AIClient()

        prompt = f"""
        Analyze the following content and extract a list of all famous scientists,
        researchers, or historical figures mentioned.

        CRITICAL RULES:
        1. Look for names in the prose (e.g. "Arthur Samuel developed...").
        2. Look for names in citations if visible.
        3. Only include people who are historical/scientific figures capable of
           having a portrait painted (real people, not fictional characters).
        4. Use their standard full names (e.g., "Geoffrey Hinton" not "Hinton").
        5. Do NOT include generic terms like "researchers" or organization names.

        Return ONLY valid JSON with this exact structure:
        {{
            "people": [
                {{"name": "Full Name", "context": "brief context from text"}},
                {{"name": "Another Person", "context": "brief context"}}
            ]
        }}

        Content (first 15000 chars):
        {content[:15000]}
        """

        system_prompt = "You are a data extraction agent. Output only valid JSON."

        try:
            response = client.generate_text(prompt, system_prompt)

            # Parse JSON (handle markdown code blocks)
            clean_json = response.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0]
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0]

            data = json.loads(clean_json)
            people = data.get("people", [])

            # Validate format
            validated_people = []
            for person in people:
                if isinstance(person, dict) and "name" in person:
                    validated_people.append({
                        "name": person["name"],
                        "context": person.get("context", "")
                    })
                elif isinstance(person, str):
                    # Handle case where AI returns just names
                    validated_people.append({"name": person, "context": ""})

            return validated_people

        except Exception as e:
            self.logger.error(f"AI extraction failed: {e}")
            # Fallback to pattern-based extraction
            self.logger.info("Falling back to pattern-based extraction")
            return self._extract_with_patterns(content)

    def _extract_with_patterns(self, content: str) -> List[Dict[str, Any]]:
        """
        Use regex patterns to extract names (fallback method).

        Looks for patterns like:
        - Capitalized Names followed by dates (Arthur Samuel (1901-1990))
        - Names in citations

        Args:
            content: Text to analyze

        Returns:
            List of people
        """
        people = []
        seen_names = set()

        # Common false positives to filter out
        false_positives = {
            'Machine Learning', 'Deep Learning', 'Neural Networks',
            'Artificial Intelligence', 'Computer Science', 'Data Science',
            'Supervised Learning', 'Unsupervised Learning', 'Reinforcement Learning',
            'Natural Language', 'Pattern Recognition', 'Computer Vision',
            'Decision Trees', 'Random Forests', 'Support Vector',
            'K Nearest', 'Logistic Regression', 'Linear Regression',
            'Cross Validation', 'Feature Engineering', 'Model Selection',
            'Training Data', 'Test Data', 'Validation Set',
            'Fit Metrics', 'Performance Metrics', 'Loss Function',
            'Excellent Manual', 'Mechanical Automata', 'Component Analysis',
            'Dimensionality Reduction', 'Principal Component', 'Feature Extraction'
        }

        # Pattern 1: Name with dates (birth-death)
        # Matches: "Arthur Samuel (1901–1990)" or "Geoffrey Hinton (1947-)"
        date_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*\((\d{4})[–\-]'
        for match in re.finditer(date_pattern, content):
            name = match.group(1)
            if name not in seen_names and name not in false_positives and len(name.split()) >= 2:
                people.append({
                    "name": name,
                    "context": f"Born {match.group(2)}"
                })
                seen_names.add(name)

        # Pattern 2: Names followed by biographical context
        # Matches: "Arthur Samuel developed" or "Hinton's work on"
        bio_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+)(?:\'s|,| developed| discovered| invented| proposed| created| introduced)'
        for match in re.finditer(bio_pattern, content):
            name = match.group(1)
            if name not in seen_names and name not in false_positives and len(name.split()) >= 2:
                # Extract context (next 50 chars)
                start_pos = match.end()
                context = content[start_pos:start_pos + 50].split('.')[0]
                people.append({
                    "name": name,
                    "context": context.strip()
                })
                seen_names.add(name)

        self.logger.info(f"Pattern-based extraction found {len(people)} people")
        return people

    def save_for_cli(
        self,
        people: List[Dict[str, Any]],
        output_path: Path,
        style: str = "Painting",
        naming_format: str = "{name}_Painting"
    ) -> Path:
        """
        Save extracted people to JSON format suitable for PortraitGenerator CLI.

        Args:
            people: List of people dicts from extract_* methods
            output_path: Where to save the JSON file
            style: Portrait style (default: "Photorealistic")
            naming_format: Output filename pattern (default: "{name}_Painting")

        Returns:
            Path to the created JSON file
        """
        # Format for CLI: simple list of names or detailed format
        cli_input = {
            "people": [p["name"] for p in people],
            "style": style,
            "naming_format": naming_format,
            "metadata": {
                "source": "PortraitPreprocessor",
                "count": len(people)
            }
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cli_input, f, indent=2)

        self.logger.info(f"Saved {len(people)} people to {output_path}")
        return output_path

    def process_and_generate(
        self,
        input_path: Path,
        output_dir: Path,
        use_ai: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Complete workflow: Extract names and optionally generate portraits.

        Args:
            input_path: Path to PDF or .tex file
            output_dir: Directory for portrait output
            use_ai: Whether to use AI for extraction
            dry_run: If True, only extract names without generating portraits

        Returns:
            Dict with results: {"people": [...], "output_dir": Path, "generated": bool}
        """
        # Determine input type
        if input_path.suffix.lower() == '.pdf':
            people = self.extract_from_pdf(input_path, use_ai=use_ai)
        elif input_path.suffix.lower() == '.tex':
            people = self.extract_from_latex(input_path, use_ai=use_ai)
        else:
            raise ValueError(f"Unsupported file type: {input_path.suffix}")

        # Save JSON for CLI
        json_path = output_dir / "people_for_portraits.json"
        self.save_for_cli(people, json_path)

        result = {
            "people": people,
            "json_path": json_path,
            "output_dir": output_dir,
            "generated": False
        }

        if not dry_run:
            # TODO: Call standalone PortraitGenerator CLI here
            self.logger.warning(
                "Portrait generation via CLI not yet implemented. "
                f"Run manually: portrait-generator batch --input {json_path} "
                f"--output-dir {output_dir}"
            )

        return result


def main():  # pragma: no cover
    """CLI entrypoint for portrait preprocessing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract people names for portrait generation"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input PDF or LaTeX file"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./portraits"),
        help="Output directory for portraits"
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Output JSON path (default: output-dir/people_for_portraits.json)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Use pattern matching instead of AI"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only extract names, don't generate portraits"
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    preprocessor = PortraitPreprocessor()

    result = preprocessor.process_and_generate(
        input_path=args.input,
        output_dir=args.output_dir,
        use_ai=not args.no_ai,
        dry_run=args.dry_run
    )

    print(f"\n✓ Extracted {len(result['people'])} people")
    print(f"✓ Saved JSON: {result['json_path']}")
    print(f"\nNext steps:")
    print(f"  1. Review {result['json_path']}")
    print(f"  2. Run: portrait-generator batch --input {result['json_path']} "
          f"--output-dir {result['output_dir']}")


if __name__ == "__main__":
    main()
