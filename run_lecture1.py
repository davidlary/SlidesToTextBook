
import os
import logging
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables immediately
load_dotenv()

# Import our modules
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer
from slides_to_textbook.modules.topic_researcher import TopicResearcher
from slides_to_textbook.modules.content_author import ContentAuthor
# NOTE: FigureRecreator deleted - figure generation not working
# NOTE: PortraitGenerator moved to standalone CLI package at https://github.com/davidlary/PortraitGenerator
from slides_to_textbook.modules.latex_builder import LaTeXBuilder
from slides_to_textbook.modules.latex_components import MarginNoteGenerator, BibliographyManager
from slides_to_textbook.modules.progress_tracker import ProgressTracker
from slides_to_textbook.modules.quality_validator import QualityValidator

# Configuration
LECTURE_PATH = Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf")
OUTPUT_DIR = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Pipeline")
    
    logger.info("Starting pipeline for Lecture 1 (Excellence Mode)...")
    
    # Debug Auth
    keys = ["ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GITHUB_TOKEN"]
    for k in keys:
        val = os.getenv(k)
        status = "SET" if val else "MISSING"
        masked = f"{val[:5]}..." if val else "N/A"
        logger.info(f"Key {k}: {status} ({masked})")

    # 0. Setup
    tracker = ProgressTracker("MachineLearning", OUTPUT_DIR.parent) # Just to log
    
    # 1. Analyze PDF
    analyzer = PDFAnalyzer()
    if not LECTURE_PATH.exists():
        logger.error(f"Lecture file not found: {LECTURE_PATH}")
        return
        
    analysis_result = analyzer.analyze_pdf(str(LECTURE_PATH))
    topic_structure = analysis_result["analysis"]
    
    # 2. Research Topic (Strict Verification)
    researcher = TopicResearcher()
    enriched_topic = researcher.research_topic(topic_structure)

    # BYPASS: Load hardcoded analysis if available (Fixes Text Gen AI Failures)
    hardcoded_path = Path(__file__).parent / "hardcoded_topic_analysis.json"
    if hardcoded_path.exists():
        logger.info("loading hardcoded topic analysis (Bypass AI)")
        with open(hardcoded_path) as f:
            enriched_topic = json.load(f)
    
    # FORCE OVERRIDE HERE (Early Binding) to prevent any downstream drift
    logger.info("Overriding topic title to 'Introduction' per user request (EARLY).")
    enriched_topic["title"] = "Introduction"
    
    # 3. Pre-process Assets & Citations (The Fix for Integration)
    # -----------------------------------------------------------
    
    # 3a. Bibliography Manager (Initialize EARLY to get keys)
    bib_manager = BibliographyManager()
    citation_map = {} # Title -> Key
    
    for citation in enriched_topic.get("research", {}).get("citations", []):
         key = bib_manager.add_entry(citation)
         citation_map[citation.get('title')] = key
         
    # 3b. Asset Mapping (Deterministic Filenames)
    assets_map = {
        "figures": {},
        "portraits": {}
    }
    
    # Map Concepts to Figures
    for concept in enriched_topic.get("concepts", []):
        safe_concept = concept.replace(" ", "")
        assets_map["figures"][concept] = f"Chapter-Introduction/Fig-{safe_concept}.png"
        
    # Map People to Portraits (using new filename format: PersonName_Painting.png)
    for person in enriched_topic.get("people", []):
        port_filename = f"{person.replace(' ', '')}_Painting.png"
        assets_map["portraits"][person] = f"Chapter-Introduction/{port_filename}"

    # 4. Content Generation (With Asset Awareness)
    # --------------------------------------------
    author = ContentAuthor()
    # Mocking equations/figures if missing for robustness
    if "equations" not in enriched_topic: enriched_topic["equations"] = []
    
    # PASS THE MAPS!
    chapter_content_body = author.generate_chapter_content(enriched_topic, assets_map=assets_map, citation_map=citation_map)
    
    # 5. Portraits (Using Standalone CLI Package)
    # --------------------------------------------
    # NOTE: Figure generation DELETED - not working
    # NOTE: Portraits now use standalone PortraitGenerator CLI from:
    #       https://github.com/davidlary/PortraitGenerator

    logger.info(f"Enriched Topic People count: {len(enriched_topic.get('people', []))}")

    # TODO: Generate Portraits using standalone CLI
    # The new workflow should be:
    # 1. Create a portrait preprocessor that extracts names from PDFs
    # 2. Save names to a JSON file
    # 3. Call PortraitGenerator CLI in batch mode:
    #    portrait-generator batch --input people.json --output-dir /path/to/Portraits/Chapter-Introduction/
    # 4. CLI generates files with naming: PersonName_Painting.png
    # 5. Only generate Photorealistic paintings (no other styles)

    portrait_dir = OUTPUT_DIR / "Portraits" / "Chapter-Introduction"
    portrait_dir.mkdir(parents=True, exist_ok=True)

    # For now, log the people that need portraits
    for person in enriched_topic.get("people", []):
        expected_filename = f"{person.replace(' ', '')}_Painting.png"
        expected_path = portrait_dir / expected_filename
        if expected_path.exists():
            logger.info(f"Portrait already exists: {expected_filename}")
        else:
            logger.warning(f"Portrait missing (needs generation): {expected_filename}")
            logger.info(f"  Person: {person}")
            logger.info(f"  Expected: {expected_path}")

    # 6. Build LaTeX
    # --------------
    # 6. Build LaTeX
    # --------------
    builder = LaTeXBuilder(OUTPUT_DIR)
    
    safe_title = "Introduction" # Enforced
    
    chapter_data = {
        "title": "Introduction",
        "safe_title": safe_title,
        "content": chapter_content_body,
        "file_name": f"Chapter-{safe_title}.tex"
    }
    
    builder.build_book("Machine Learning", [chapter_data])
    builder.build_chapter(chapter_data)
    builder.write_bibliography(bib_manager.generate_bibtex())
    
    # 7. Quality Validation (Gatekeeper)
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
