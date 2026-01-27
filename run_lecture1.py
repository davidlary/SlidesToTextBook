
import os
import logging
import json
from pathlib import Path

# Import our modules
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer
from slides_to_textbook.modules.topic_researcher import TopicResearcher
from slides_to_textbook.modules.content_author import ContentAuthor
from slides_to_textbook.modules.image_generators import FigureRecreator, PortraitGenerator
from slides_to_textbook.modules.latex_builder import LaTeXBuilder
from slides_to_textbook.modules.latex_components import MarginNoteGenerator, BibliographyManager
from slides_to_textbook.modules.progress_tracker import ProgressTracker

# Configuration
LECTURE_PATH = Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf")
OUTPUT_DIR = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook")

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Pipeline")
    
    logger.info("Starting pipeline for Lecture 1...")
    
    # Debug Auth
    import os
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
    
    # Save intermediate for debugging
    with open("debug_analysis.json", "w") as f:
        json.dump(analysis_result, f, indent=2)

    # 2. Research Topic
    researcher = TopicResearcher()
    enriched_topic = researcher.research_topic(topic_structure)
    
    # 3. Content Generation
    author = ContentAuthor()
    # Mocking equations/figures if missing for robustness
    if "equations" not in enriched_topic: enriched_topic["equations"] = []
    if "concepts" not in enriched_topic: enriched_topic["concepts"] = []
    if "people" not in enriched_topic: enriched_topic["people"] = []
    
    chapter_content_body = author.generate_chapter_content(enriched_topic)
    
    # 4. Images & Portraits
    fig_creator = FigureRecreator(OUTPUT_DIR / "Figures")
    portrait_creator = PortraitGenerator(OUTPUT_DIR / "Figures" / "Portraits")
    
    # Simple logic regarding figures from analysis? 
    # For now, we assume ContentAuthor might reference them, but we haven't parsed exact figure calls yet.
    # We will generate portraits for identified people.
    
    latex_margin = MarginNoteGenerator()
    
    for person in enriched_topic.get("people", []):
         portrait_path = portrait_creator.generate_portrait(person)
         # In a real run, we'd insert this into the text.
         # For this test run, we assume the ContentAuthor *might* have added placeholders,
         # or we force a margin note at the start.
         if portrait_path:
             # Just demonstrating creation, inserting into content is complex without parsing the prose.
             pass

    # 5. Bibliography
    bib_manager = BibliographyManager()
    for citation in enriched_topic.get("research", {}).get("citations", []):
        bib_manager.add_entry(citation)
    
    # 6. Build LaTeX
    builder = LaTeXBuilder(OUTPUT_DIR)
    
    safe_title = enriched_topic.get("title", "Lecture1").replace(" ", "")
    chapter_data = {
        "title": enriched_topic.get("title", "Lecture 1"),
        "safe_title": safe_title,
        "content": chapter_content_body,
        "file_name": f"Chapter-{safe_title}.tex"
    }
    
    # Create main.tex and chapter
    # Note: build_book overwrites main.tex, so normally we'd accumulate chapters.
    # Here we just do one.
    builder.build_book("Machine Learning", [chapter_data])
    builder.build_chapter(chapter_data)
    builder.write_bibliography(bib_manager.generate_bibtex())
    
    logger.info(f"Pipeline complete. Output at {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
