
import os
import sys
import json
import re
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))
from slides_to_textbook.utils.api_clients import AIClient

def extract_people(tex_path, output_json):
    print(f"Extracting people from {tex_path}...")
    
    with open(tex_path, 'r') as f:
        content = f.read()
        
    client = AIClient()
    
    # We want a strict JSON list of people mentioned who are famous/historical figures
    # capable of having a portrait.
    
    prompt = f"""
    Analyze the following Textbook Chapter content and extract a list of all famous scientists, researchers, or historical figures mentioned.
    
    CRITICAL:
    1. Look for names in the prose (e.g. "Arthur Samuel").
    2. Look for names in citations (e.g. from "\citep{{goodfellow2016deep}}" -> "Ian Goodfellow").
    3. Include all authors of major referenced works if they are mentioned or cited.
    
    Return ONLY a valid JSON object with a single key "people" containing the list of strings.
    Do not include fictional characters or generic terms.
    Use their standard full names.
    
    Content:
    {content[:15000]} 
    """
    
    # Use the same method as expander, or robust structured output
    # Since generate_text might verify json, let's try direct call
    try:
        response = client.generate_text(prompt, "You are a data extraction agent. Output raw JSON.")
        
        # Parse JSON
        # Response might have markdown blocks
        clean_json = response.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0]
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0]
            
        data = json.loads(clean_json)
        
        with open(output_json, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Extraction successful. Found {len(data.get('people', []))} people.")
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        # Make sure we don't crash the pipeline, write partial or empty?
        # If extraction fails, we should fall back to empty or error out.
        sys.exit(1)

if __name__ == "__main__":
    extract_people(
        "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex",
        "/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/detected_people.json"
    )
