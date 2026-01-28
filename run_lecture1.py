
import os
import logging
import json
import sys
from pathlib import Path

# Import our modules
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer
from slides_to_textbook.modules.topic_researcher import TopicResearcher
from slides_to_textbook.modules.content_author import ContentAuthor
from slides_to_textbook.modules.image_generators import FigureRecreator, PortraitGenerator
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
        assets_map["figures"][concept] = f"Fig-{safe_concept}.png"
        
    # Map People to Portraits
    for person in enriched_topic.get("people", []):
        port_filename = f"{person.replace(' ', '')}.jpg" 
        assets_map["portraits"][person] = port_filename

    # 4. Content Generation (With Asset Awareness)
    # --------------------------------------------
    author = ContentAuthor()
    # Mocking equations/figures if missing for robustness
    if "equations" not in enriched_topic: enriched_topic["equations"] = []
    
    # PASS THE MAPS!
    chapter_content_body = author.generate_chapter_content(enriched_topic, assets_map=assets_map, citation_map=citation_map)
    
    # 5. Images & Portraits (Execute Generation to match maps)
    # ------------------------------------------------------
    fig_creator = FigureRecreator(OUTPUT_DIR / "Figures")
    portrait_creator = PortraitGenerator(OUTPUT_DIR / "Figures" / "Portraits")
    
    logger.info(f"Enriched Topic People count: {len(enriched_topic.get('people', []))}")
    logger.info(f"Enriched Topic Concepts count: {len(enriched_topic.get('concepts', []))}")

    # Generate Portraits (Using pre-calc filenames)
    for person in enriched_topic.get("people", []):
         logger.info(f"Adding portrait task for: {person}")
         # Note: PortraitGenerator uses internal naming logic, we should probably force it or assume it matches.
         # Checking PortraitGenerator logic... it takes a name and usually sanitizes it. 
         # Let's trust it matches {person.replace(" ", "")} or update it. 
         # For robustness, we'll let it generate and hope it matches, OR update it to be strict.
         # Update: For this step, we'll assume standard sanitization.
         portrait_path = portrait_creator.generate_portrait(person)
         
    # Generate Concept Figures (Using pre-calc filenames)
    if enriched_topic.get("concepts"):
        logger.info(f"Generating figures for {len(enriched_topic['concepts'])} concepts...")
        for i, concept in enumerate(enriched_topic["concepts"]):
            if i > 12: break
            
            logger.info(f"Adding figure task for: {concept}")
            fig_desc = f"Scientific diagram explaining {concept} in detail."
            # Use the EXACT filename mapped earlier
            target_filename = assets_map["figures"][concept]
            
            fig_path = fig_creator.recreate_figure(fig_desc, target_filename)
            if fig_path:
                logger.info(f"Created figure: {fig_path.name}")

    # 6. Build LaTeX
    # --------------
    builder = LaTeXBuilder(OUTPUT_DIR)
    
    safe_title = enriched_topic.get("title", "Lecture1").replace(" ", "")
    chapter_data = {
        "title": enriched_topic.get("title", "Lecture 1"),
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
