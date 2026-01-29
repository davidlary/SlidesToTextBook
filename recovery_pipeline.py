import logging
import os
from pathlib import Path
from slides_to_textbook.modules.topic_researcher import TopicResearcher
from slides_to_textbook.modules.pdf_analyzer import PDFAnalyzer
from slides_to_textbook.modules.image_generators import PortraitGenerator, FigureRecreator

# Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RecoveryPipeline")

OUTPUT_DIR = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Figures")
PORTRAIT_DIR = OUTPUT_DIR / "Portraits"
LECTURE_PATH = Path("/Users/davidlary/Dropbox/Lectures/2026/5336/Lecture-1.pdf")

def safe_filename(name):
    return f"{name.replace(' ', '')}.jpg"

def main():
    logger.info("Starting Recovery Pipeline...")
    
    # 1. Get Data
    analyzer = PDFAnalyzer()
    analysis = analyzer.analyze_pdf(str(LECTURE_PATH))
    
    researcher = TopicResearcher()
    enriched = researcher.research_topic(analysis["analysis"])
    
    people = enriched.get("people", [])
    concepts = enriched.get("concepts", [])
    
    # Force add George Boole if extraction missed him (User Requirement)
    if "George Boole" not in people:
        logger.info("Injecting missing George Boole...")
        people.append("George Boole")
        
    people.sort() # sort for clean logs
    
    # 2. Finish Portraits
    pg = PortraitGenerator(PORTRAIT_DIR)
    
    logger.info(f"Checking {len(people)} people...")
    for person in people:
        fname = safe_filename(person)
        if (PORTRAIT_DIR / fname).exists():
            logger.info(f"[SKIP] {person} exists.")
            continue
            
        logger.info(f"[GENERATE] {person}")
        try:
            pg.generate_portrait(person)
        except Exception as e:
            logger.error(f"Failed to generate {person}: {e}")

    # 3. Finish Figures
    fg = FigureRecreator(OUTPUT_DIR)
    logger.info(f"Checking {len(concepts)} concepts...")
    
    for concept in concepts:
        fname = f"Fig-{concept.replace(' ', '')}.png"
        if (OUTPUT_DIR / fname).exists():
             logger.info(f"[SKIP] {concept} exists.")
             continue
             
        logger.info(f"[GENERATE] {concept}")
        desc = f"A complex, labeled scientific visualization illustrating the concept of '{concept}'. Include typical metrics, decision boundaries, or structural diagrams as appropriate for a university textbook."
        try:
            fg.recreate_figure(desc, fname)
        except Exception as e:
             logger.error(f"Failed to generate {concept}: {e}")
             
    logger.info("Recovery Complete.")

if __name__ == "__main__":
    main()
