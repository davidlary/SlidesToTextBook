"""
Complete Integrated Pipeline for Lecture 1

This version includes full integration with standalone PortraitGenerator CLI.
"""

import os
import logging
import json
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables immediately
load_dotenv()

# Import our modules
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer
from slides_to_textbook.modules.topic_researcher import TopicResearcher
from slides_to_textbook.modules.content_author import ContentAuthor
from slides_to_textbook.modules.portrait_preprocessor import PortraitPreprocessor
from slides_to_textbook.modules.latex_builder import LaTeXBuilder
from slides_to_textbook.modules.latex_components import MarginNoteGenerator, BibliographyManager
from slides_to_textbook.modules.progress_tracker import ProgressTracker
from slides_to_textbook.modules.quality_validator import QualityValidator

# Configuration
LECTURE_PATH = Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf")
OUTPUT_DIR = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook")


def generate_portraits_for_people(people_list, output_dir, logger):
    """
    Generate portraits using standalone CLI with smart existence checking.

    Args:
        people_list: List of people names
        output_dir: Directory to save portraits
        logger: Logger instance

    Returns:
        Dict mapping person name to portrait path
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check which portraits already exist
    existing_portraits = {}
    missing_people = []

    for person in people_list:
        # Expected filename format: PersonName_Painting.png
        filename = f"{person.replace(' ', '')}_Painting.png"
        portrait_path = output_dir / filename

        if portrait_path.exists():
            logger.info(f"Portrait already exists: {filename}")
            existing_portraits[person] = portrait_path
        else:
            missing_people.append(person)

    # Generate only missing portraits
    if missing_people:
        logger.info(f"Generating {len(missing_people)} missing portraits...")

        # Use CLI batch generation
        cmd = ["portrait-generator", "batch"] + missing_people
        cmd += ["--output-dir", str(output_dir)]
        cmd += ["--styles", "Painting"]

        logger.info(f"Running: {' '.join(cmd)}")

        try:
            # Calculate timeout: ~2-3 min per portrait
            timeout_seconds = max(600, len(missing_people) * 180)  # 3 minutes per portrait, min 10 min
            logger.info(f"Timeout set to {timeout_seconds}s for {len(missing_people)} portraits")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=True
            )

            logger.info("Portrait generation completed successfully")
            logger.debug(f"CLI output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Portrait generation failed: {e}")
            logger.error(f"CLI stderr: {e.stderr}")
            # Don't raise - continue with partial portraits
            logger.warning("Continuing with partially generated portraits")

        except subprocess.TimeoutExpired as e:
            logger.error(f"Portrait generation timed out after {timeout_seconds}s")
            logger.warning("Continuing with partially generated portraits")
            # Don't raise - some portraits may have been generated

    # Build complete portrait map
    portrait_map = {}
    for person in people_list:
        filename = f"{person.replace(' ', '')}_Painting.png"
        portrait_path = output_dir / filename

        if portrait_path.exists():
            portrait_map[person] = portrait_path
        else:
            logger.warning(f"Portrait still missing after generation: {filename}")

    return portrait_map


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Pipeline")

    logger.info("Starting integrated pipeline for Lecture 1...")

    # Debug Auth
    keys = ["ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GITHUB_TOKEN"]
    for k in keys:
        val = os.getenv(k)
        status = "SET" if val else "MISSING"
        masked = f"{val[:5]}...{val[-5:]}" if val and len(val) > 10 else "N/A"
        logger.info(f"Key {k}: {status} ({masked})")

    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("GOOGLE_API_KEY not set! Required for portrait generation.")
        sys.exit(1)

    # 0. Setup
    tracker = ProgressTracker("MachineLearning", OUTPUT_DIR.parent)

    # 1. Analyze PDF
    analyzer = PDFAnalyzer()
    if not LECTURE_PATH.exists():
        logger.error(f"Lecture file not found: {LECTURE_PATH}")
        return

    analysis_result = analyzer.analyze_pdf(str(LECTURE_PATH))
    topic_structure = analysis_result["analysis"]

    # 2. Research Topic
    researcher = TopicResearcher()
    enriched_topic = researcher.research_topic(topic_structure)

    # BYPASS: Load hardcoded analysis if available
    hardcoded_path = Path(__file__).parent / "hardcoded_topic_analysis.json"
    if hardcoded_path.exists():
        logger.info("Loading hardcoded topic analysis (Bypass AI)")
        with open(hardcoded_path) as f:
            enriched_topic = json.load(f)

    # Force title
    logger.info("Overriding topic title to 'Introduction' (EARLY).")
    enriched_topic["title"] = "Introduction"

    # 3. Extract People Names Using Preprocessor
    logger.info("Extracting people names from PDF...")
    preprocessor = PortraitPreprocessor()

    try:
        # Extract people from the PDF (uses REAL AI)
        people_data = preprocessor.extract_from_pdf(LECTURE_PATH, use_ai=True)
        extracted_people = [p["name"] for p in people_data]

        # Merge with enriched topic people
        all_people = list(set(extracted_people + enriched_topic.get("people", [])))
        enriched_topic["people"] = all_people

        logger.info(f"Found {len(all_people)} unique people: {all_people}")

    except Exception as e:
        logger.error(f"Name extraction failed: {e}")
        logger.info("Falling back to enriched_topic people only")
        all_people = enriched_topic.get("people", [])

    # 4. Pre-process Assets & Citations
    # -----------------------------------------------------------

    # 4a. Bibliography Manager
    bib_manager = BibliographyManager()
    citation_map = {}  # Title -> Key

    for citation in enriched_topic.get("research", {}).get("citations", []):
        key = bib_manager.add_entry(citation)
        citation_map[citation.get('title')] = key

    # 4b. Asset Mapping
    assets_map = {
        "figures": {},
        "portraits": {}
    }

    # NOTE: Figure generation removed (not working)
    # Only portraits remain

    # 5. Generate Portraits Using Integrated CLI
    # -------------------------------------------
    portrait_dir = OUTPUT_DIR / "Portraits" / "Chapter-Introduction"
    logger.info(f"Portrait directory: {portrait_dir}")

    if all_people:
        try:
            portrait_paths = generate_portraits_for_people(
                people_list=all_people,
                output_dir=portrait_dir,
                logger=logger
            )

            # Update assets map with actual paths
            for person, path in portrait_paths.items():
                # Relative path from OUTPUT_DIR - just the filename within Portraits/Chapter-X/
                chapter_rel_path = path.relative_to(OUTPUT_DIR)
                assets_map["portraits"][person] = str(chapter_rel_path)

            logger.info(f"Generated/verified {len(portrait_paths)} portraits")

        except Exception as e:
            logger.error(f"Portrait generation failed: {e}")
            logger.warning("Continuing without portraits")

    else:
        logger.warning("No people found - skipping portrait generation")

    # 6. Content Generation
    # ---------------------
    author = ContentAuthor()
    if "equations" not in enriched_topic:
        enriched_topic["equations"] = []

    chapter_content_body = author.generate_chapter_content(
        enriched_topic,
        assets_map=assets_map,
        citation_map=citation_map
    )

    # 7. Build LaTeX
    # --------------
    builder = LaTeXBuilder(OUTPUT_DIR)

    safe_title = "Introduction"

    chapter_data = {
        "title": "Introduction",
        "safe_title": safe_title,
        "content": chapter_content_body,
        "file_name": f"Chapter-{safe_title}.tex"
    }

    builder.build_book("Machine Learning", [chapter_data])
    builder.build_chapter(chapter_data)
    builder.write_bibliography(bib_manager.generate_bibtex())

    # 8. Quality Validation
    validator = QualityValidator(OUTPUT_DIR)
    report = validator.validate()

    if report["status"] == "failed":
        logger.error("Quality Validation FAILED:")
        for err in report["errors"]:
            logger.error(f" - {err}")
        sys.exit(1)
    else:
        logger.info("Quality Validation PASSED.")
        for warn in report["warnings"]:
            logger.warning(f" - {warn}")

    logger.info(f"Pipeline complete. Output at {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
