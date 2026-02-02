
import json
import re
import os

def restore_missing_portraits(tex_path, json_path):
    print(f"Restoring portraits for {tex_path}")
    
    # 1. Load People List
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    people = data.get('people', [])
    print(f"Target People: {len(people)}")
    
    # 2. Read TeX File
    with open(tex_path, 'r') as f:
        content = f.read()
        
    # 3. Check for existing portraits
    # Regex to find filenames in extracted margin notes
    existing_portraits = set(re.findall(r'Portraits/[^/]+/([^/]+\.(?:jpg|png))', content))
    print(f"Found {len(existing_portraits)} existing portraits: {existing_portraits}")
    
    # 4. Inject Missing
    # We need a robust Name -> Filename mapper.
    # Heuristic: Remove spaces, add .jpg
    
    new_content = content
    
    for person_name in people:
        # Construct Filename
        clean_name = person_name.replace(" ", "").replace(".", "")
        filename = f"{clean_name}.jpg"
        
        if filename in existing_portraits:
            print(f" - {person_name}: Exists ({filename})")
            continue
            
        # Not found. Search for name in text.
        # We want the FIRST mention.
        # We assume the name appears as "First Last" or "Last"
        
        # Search strategies:
        # 1. Full Name
        idx = new_content.find(person_name)
        
        # 2. Last Name Only (if fallback needed)
        # Split name "Ian Goodfellow" -> "Goodfellow"
        if idx == -1 and " " in person_name:
            last_name = person_name.split()[-1]
            # Be careful not to match generic words. "Turing" is safe. "Ng" might be risky? as in "ng"?
            # We'll trust the list is "Famous People".
            idx = new_content.find(last_name)
            if idx != -1:
                person_name = last_name # Update target strings for replacement
            else:
                 # 3. Lowercase Last Name (for citation keys like 'goodfellow2016deep')
                 idx = new_content.find(last_name.lower())
                 if idx != -1:
                     # We found the location, but we want to inject using the Proper Name for the caption/image
                     # We can't replace "goodfellow" with "Ian Goodfellow\automargin..." easily if it's inside a citation key?
                     # Replacing inside \citep{...} might break bibtex?
                     # \citep{goodfellow Ian Goodfellow\automargin... 2016} -> BROKEN
                     
                     # Strategy: If found in lowercase (likely citation), we should probably NOT inject INTO the citation.
                     # Instead, inject AFTER the current paragraph or sentence? Too complex.
                     # Alternative: Inject at the location, but be careful.
                     # If it is inside \citep{...}, we probably shouldn't touch it.
                     
                     # Improved Strategy:
                     # If we find "goodfellow", check if it is part of \citep.
                     # If so, maybe append the portrait to the closest \end{figure} or something?
                     # Or just blindly inject and risk it? 
                     # \citep{goodfellow\automarginnote{...}2016}
                     # Automarginnote inside \citep might be valid or might resolve to nothing?
                     # \citep is rigid.
                     
                     # Safer fallback: If only found in citation, skip injection?
                     # User WANTS the portrait.
                     # Let's search for "Goodfellow" (Capitalized) in References section? No, we edit Chapter-Introduction.tex.
                     
                     # What if we just force inject at the first blank line after validity?
                     pass
        
        if idx == -1:
            print(f" ! {person_name}: Not found in text (Cannot inject)")
            continue
            
        print(f" + {person_name}: Found at index {idx}. Injecting portrait.")
        
        # Injection Logic
        # We want to insert `\automarginnote{\includegraphics[width=1.0\linewidth]{Portraits/Chapter-Introduction/Filename.jpg}}`
        # right after the name.
        
        # Note: We must be careful not to break existing commands.
        # We insert AFTER the name.
        
        injection = f"\\automarginnote{{\\includegraphics[width=1.0\\linewidth]{{Portraits/Chapter-Introduction/{filename}}}}}"
        
        # We start searching from the beginning of new_content each time? 
        # No, that might duplicate if we run this script multiple times.
        # But we already checked `existing_portraits` at the start.
        
        # However, `new_content` is a string. We can replace the *first* occurrence.
        # Be careful: `person_name` might be inside another word? Unlikely for full names.
        
        # Valid injection: Replace "Name" with "Name\command..."
        # Use str.replace for safety with backslashes
        new_content = new_content.replace(person_name, f"{person_name}{injection}", 1)
        
    with open(tex_path, 'w') as f:
        f.write(new_content)
    print("Restoration complete.")

if __name__ == "__main__":
    restore_missing_portraits(
        "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex",
        "/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/detected_people.json"
    )
