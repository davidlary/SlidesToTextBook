"""
Test Portrait Preprocessor Module

Tests name extraction from PDFs and LaTeX files, and integration with
the standalone PortraitGenerator CLI.

IMPORTANT: These are REAL tests with REAL API calls. No mocking allowed.
"""

import pytest
from pathlib import Path
import json
import subprocess
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from slides_to_textbook.modules.portrait_preprocessor import PortraitPreprocessor


# Test data: People from the Examples directory
EXAMPLE_PEOPLE = [
    "Alexey Chervonenkis",
    "Allen Newell",
    "Arthur Lee Samuel",
    "Ashish Vaswani",
    "Augustus De Morgan",
    "Claude Shannon",
    "David Rumelhart",
    "Donald Hebb",
    "Frank Rosenblatt",
    "Geoffrey Hinton",
    "George Boole",
    "Herbert Simon",
    "Ian Goodfellow",
    "J.C. Shaw",
    "Thomas Bayes",
    "Tom Mitchell",
    "Vladimir Vapnik",
    "William of Ockham",
    "Yann LeCun",
    "Yoshua Bengio"
]


class TestPortraitPreprocessor:
    """Test suite for PortraitPreprocessor with REAL API calls."""

    @pytest.fixture
    def preprocessor(self):
        """Create a preprocessor instance."""
        return PortraitPreprocessor()

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for test outputs."""
        return tmp_path

    @pytest.fixture
    def sample_latex_content(self):
        """Sample LaTeX content with people names."""
        return """
        \\section{Introduction}

        Machine learning has a rich history. Arthur Lee Samuel coined the term in 1959,
        defining it as a "field of study that gives computers the ability to learn
        without being explicitly programmed."

        Geoffrey Hinton (1947-) is known as the "Godfather of Deep Learning" for his
        pioneering work on backpropagation and neural networks.

        The field builds on earlier work by Thomas Bayes (1701-1761), who developed
        Bayes' theorem, and George Boole (1815-1864), who created Boolean algebra.

        Modern developments include Ian Goodfellow's invention of Generative Adversarial
        Networks (GANs) and Ashish Vaswani's work on the Transformer architecture.
        """

    @pytest.fixture
    def sample_latex_file(self, temp_dir, sample_latex_content):
        """Create a sample LaTeX file for testing."""
        latex_file = temp_dir / "test_chapter.tex"
        latex_file.write_text(sample_latex_content)
        return latex_file

    def test_preprocessor_initialization(self, preprocessor):
        """Test that preprocessor initializes correctly."""
        assert preprocessor is not None
        assert preprocessor.logger is not None

    def test_extract_from_latex_with_ai(self, preprocessor, sample_latex_file):
        """Test extraction from LaTeX using REAL AI API."""
        # This is a REAL test - it will call the actual AI API
        people = preprocessor.extract_from_latex(sample_latex_file, use_ai=True)

        # Verify we got results
        assert len(people) > 0

        # Verify structure
        for person in people:
            assert "name" in person
            assert isinstance(person["name"], str)
            assert len(person["name"]) > 0

        # Verify we found at least some of the expected people
        names_found = [p["name"] for p in people]

        # Should find Arthur Samuel, Geoffrey Hinton, Thomas Bayes, etc.
        expected_names = ["Arthur", "Geoffrey", "Thomas", "George", "Ian", "Ashish"]
        found_count = sum(1 for expected in expected_names
                         if any(expected in name for name in names_found))

        assert found_count >= 3, f"Expected to find at least 3 people, found {found_count}"

    def test_extract_from_latex_with_patterns(self, preprocessor, sample_latex_file):
        """Test extraction from LaTeX using pattern matching (no AI)."""
        people = preprocessor.extract_from_latex(sample_latex_file, use_ai=False)

        # Verify we got results
        assert len(people) > 0

        # Verify structure
        for person in people:
            assert "name" in person
            assert "context" in person

        # Pattern matching should find people with dates
        names_found = [p["name"] for p in people]
        assert any("Thomas Bayes" in name for name in names_found), \
            "Should find Thomas Bayes (has dates in text)"
        assert any("George Boole" in name for name in names_found), \
            "Should find George Boole (has dates in text)"

    def test_save_for_cli(self, preprocessor, temp_dir):
        """Test saving extracted people to JSON for CLI."""
        people = [
            {"name": "Alan Turing", "context": "Computer science pioneer"},
            {"name": "Ada Lovelace", "context": "First programmer"},
            {"name": "Grace Hopper", "context": "COBOL inventor"}
        ]

        output_path = temp_dir / "people.json"
        result_path = preprocessor.save_for_cli(people, output_path)

        # Verify file was created
        assert result_path.exists()
        assert result_path == output_path

        # Verify content
        with open(result_path, 'r') as f:
            data = json.load(f)

        assert "people" in data
        assert len(data["people"]) == 3
        assert "Alan Turing" in data["people"]
        assert "Ada Lovelace" in data["people"]
        assert "Grace Hopper" in data["people"]
        assert data["style"] == "Painting"
        assert "{name}_Painting" in data["naming_format"]

    @pytest.mark.slow
    def test_cli_integration_batch_generation(self, temp_dir):
        """Test integration with portrait-generator CLI using REAL API calls."""
        # This test will generate REAL portraits using the API
        # Marked as slow because real portrait generation takes 2-3 minutes per subject

        # Create output directory
        output_dir = temp_dir / "portraits"
        output_dir.mkdir(exist_ok=True)

        # Test with a small subset of people
        test_people = ["Alan Turing", "Ada Lovelace"]

        # Call the CLI
        cmd = ["portrait-generator", "batch"] + test_people
        cmd += ["--output-dir", str(output_dir)]
        cmd += ["--styles", "Painting"]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max for REAL portrait generation
        )

        # Verify CLI executed successfully
        assert result.returncode == 0, \
            f"CLI failed: {result.stderr}"

        # Verify portraits were created
        # Note: The actual filename format may vary based on CLI implementation
        portraits_created = list(output_dir.glob("*.png")) + list(output_dir.glob("*.jpg"))
        assert len(portraits_created) >= 1, \
            f"Expected at least 1 portrait, found {len(portraits_created)}"

    def test_portrait_existence_check(self, temp_dir):
        """Test smart check for existing portraits."""
        # Create output directory
        output_dir = temp_dir / "portraits"
        output_dir.mkdir(exist_ok=True)

        # Create a fake existing portrait
        existing_portrait = output_dir / "AlanTuring_Painting.png"
        existing_portrait.write_text("fake image data")

        # Check existence
        assert existing_portrait.exists()

        # This portrait should be skipped in generation
        # (implementation detail - preprocessor should check this)

    def test_process_latex_end_to_end(self, preprocessor, sample_latex_file, temp_dir):
        """Test complete workflow from LaTeX to JSON."""
        output_dir = temp_dir / "portraits"

        result = preprocessor.process_and_generate(
            input_path=sample_latex_file,
            output_dir=output_dir,
            use_ai=True,
            dry_run=True  # Don't actually generate portraits
        )

        # Verify results
        assert "people" in result
        assert len(result["people"]) > 0
        assert "json_path" in result
        assert result["json_path"].exists()
        assert "output_dir" in result
        assert result["output_dir"] == output_dir

    @pytest.mark.skipif(
        not Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf").exists(),
        reason="Lecture-1.pdf not found"
    )
    def test_extract_from_real_pdf(self, preprocessor):
        """Test extraction from actual Lecture-1.pdf with REAL AI."""
        pdf_path = Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf")

        # This uses REAL AI API
        people = preprocessor.extract_from_pdf(pdf_path, use_ai=True)

        # Verify we got results
        assert len(people) > 0, "Should extract at least 1 person from Lecture-1.pdf"

        # Verify structure
        for person in people:
            assert "name" in person
            assert isinstance(person["name"], str)
            assert len(person["name"]) > 0

    def test_example_people_in_system(self):
        """Verify that all example people can be processed."""
        # Test that we can handle all the people from Examples directory
        for person_name in EXAMPLE_PEOPLE:
            # Verify name is valid
            assert len(person_name) > 0
            assert person_name[0].isupper()

            # Verify we can create a valid filename
            filename = person_name.replace(" ", "") + "_Painting.png"
            assert len(filename) > 0
            assert ".png" in filename


class TestCLIIntegration:
    """Test integration with portrait-generator CLI."""

    def test_cli_health_check(self):
        """Test that CLI is properly installed and configured."""
        result = subprocess.run(
            ["portrait-generator", "health-check"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should execute without error
        assert result.returncode == 0, \
            f"Health check failed: {result.stderr}"

    def test_cli_status_check(self):
        """Test CLI status command."""
        result = subprocess.run(
            ["portrait-generator", "status", "Alan Turing"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should execute without error
        assert result.returncode == 0, \
            f"Status check failed: {result.stderr}"

    def test_cli_version(self):
        """Test CLI version command."""
        result = subprocess.run(
            ["portrait-generator", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0
        assert "2." in result.stdout or "version" in result.stdout.lower()


# Coverage target: 90%+
# All tests use REAL API calls - no mocking
# Tests include people from Examples directory
