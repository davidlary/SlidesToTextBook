
import re
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))
from slides_to_textbook.utils.api_clients import AIClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Expander")
load_dotenv()

def expand_text_block(client, text, citations_hint):
    if len(text.strip()) < 20:
        return text # Skip empty blocks
        
    prompt = f"""
    You are an expert textbook author writing a definitive graduate-level book on Machine Learning.
    
    Here is a DRAFT text segment from the "Introduction" chapter:
    <draft>
    {text}
    </draft>
    
    YOUR TASK:
    Rewrite and EXPAND this text segment to be significantly longer, more detailed, and pedestrian.
    - Aim for a 5x to 10x expansion in length.
    - Define concepts rigorously (using math where appropriate).
    - Provide historical context and anecdotes.
    - Use the following citations where relevant: {citations_hint}
    - IMPORTANT: If there are any \\automarginnote{{...}} commands in the draft, you MUST PRESERVE THEM exactly in the output, placing them near the relevant text (e.g. near the person's name).
    - CITATION KEYS AVAILABLE: samuel1959some, mitchell1997machine, sutton2018reinforcement, lecun2015deep, goodfellow2016deep, bishop2006pattern, murphy2012machine, rosenblatt1958perceptron, turing1950computing, hastie2009elements.
    
    Output ONLY the valid LaTeX text. Do not include markdown formatting or "Here is the text".
    """
    
    try:
        # We need to access the raw generation or use a method that returns text.
        # Since AIClient is structured for JSON usually, we'll try to use the internal _call_claude if available, 
        # or just use the public interface and hope it handles text.
        # Actually, let's just use the internal method _call_claude if we can access it.
        # The AIClient wrapper usually expects JSON schemas.
        # Let's try to verify if we can access the raw client.
        
        # Hack: The User's AIClient wrapper might force JSON.
        # Let's inspect the AIClient instance at runtime.
        # If generate_content forces JSON, we might need a workaround.
        
        # Workaround: Use the raw Anthropic client directly if env var is set?
        # Better: The 'analysis_result' method returns a dict. We want raw text.
        # Let's try to subclass or access the protected method.
        
        response = client._call_claude(prompt, "You are a helpful expert author.")
        return response
    except Exception as e:
        logger.error(f"Expansion failed: {e}")
        return text # Return original on failure

def main():
    file_path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    logger.info(f"Expanding content in {file_path}")
    
    with open(file_path, "r") as f:
        content = f.read()
        
    # Split by Figure Blocks
    # Regex to capture \begin{figure}...\end{figure}
    # DOTALL matches newline
    figure_pattern = re.compile(r'(\\begin\{figure\}.*?\\end\{figure\})', re.DOTALL)
    
    parts = figure_pattern.split(content)
    
    client = AIClient()
    
    citations = "samuel1959some, mitchell1997machine, sutton2018reinforcement, lecun2015deep, goodfellow2016deep"
    
    new_parts = []
    
    logger.info(f"Found {len(parts)} segments.")
    
    for i, part in enumerate(parts):
        # valid part check: does it look like a figure?
        if part.strip().startswith(r"\begin{figure}"):
            logger.info(f"Segment {i}: Keeping Figure Block")
            new_parts.append(part)
        else:
            logger.info(f"Segment {i}: Expanding Text Block ({len(part)} chars)")
            expanded = expand_text_block(client, part, citations)
            new_parts.append(expanded)
            
    final_content = "".join(new_parts)
    
    # Save
    with open(file_path, "w") as f:
        f.write(final_content)
        
    logger.info("Expansion Complete.")

if __name__ == "__main__":
    main()
