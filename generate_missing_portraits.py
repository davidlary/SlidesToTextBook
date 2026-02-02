
import json
import os
import sys
from pathlib import Path

# Setup Path
sys.path.append(os.path.join(os.getcwd(), "src"))
from slides_to_textbook.modules.image_generators import PortraitGenerator

def generate_missing():
    print("Checking for missing portraits...")
    
    json_path = "/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/detected_people.json"
    output_dir = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Portraits/Chapter-Introduction")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    people = data.get('people', [])
    generator = PortraitGenerator(output_dir)
    
    for person in people:
        safe_name = person.replace(" ", "")
        filename = f"{safe_name}.jpg"
        target_path = output_dir / filename
        
        if not target_path.exists():
            print(f"Generating missing portrait for {person}...")
            try:
                # Call generator
                # Note: We don't have birth years handy easily unless we use the LLM, 
                # but PortraitGenerator might handle it or we pass empty.
                generator.generate_portrait(person)
            except Exception as e:
                print(f"Failed to generate {person}: {e}")
        else:
            print(f"Portrait exists for {person}")

if __name__ == "__main__":
    generate_missing()
