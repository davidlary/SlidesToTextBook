import re
import json

tex_path = '/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex'
with open(tex_path, 'r') as f:
    content = f.read()

# Pattern to find figure environments
# We look for \begin{figure} ... \end{figure}
# This is a bit complex with regex, but we can do a simple approximation
# We'll traverse the file line by line

figures = []
current_figure = {}
in_figure = False

lines = content.split('\n')
for i, line in enumerate(lines):
    if '\\begin{figure}' in line or '\\begin{wrapfigure}' in line:
        in_figure = True
        current_figure = {'captions': [], 'images': []}
    
    if in_figure:
        # Extract images
        img_match = re.search(r'\\includegraphics.*?\{Figures/Chapter-Introduction/(.*?)\}', line)
        if img_match:
            current_figure['images'].append(img_match.group(1))
            
        # Extract caption
        if '\\caption' in line:
            # simple one-line caption extraction
            cap_match = re.search(r'\\caption\{(.*?)\}', line)
            if cap_match:
                current_figure['captions'].append(cap_match.group(1))
            else:
                # Multi-line caption handling (basic)
                # Just take the rest of the line and maybe next few? 
                # For now let's assume one line or close enough
                pass
                
    if ('\\end{figure}' in line or '\\end{wrapfigure}' in line) and in_figure:
        in_figure = False
        if current_figure['images']:
            figures.append(current_figure)

# Also look for automarginnotes (Portraits)
portraits = []
# Pattern: \automarginnote{... \includegraphics...{.../(.*?)}}
# This requires a bit more robust parsing as it might be inline
notes = re.findall(r'\\automarginnote\{(.*?)\}', content, re.DOTALL)
for note in notes:
    img_match = re.search(r'\\includegraphics.*?\{Figures/Chapter-Introduction/(.*?)\}', note)
    if img_match:
        # Extract name from italic text if present
        name_match = re.search(r'\\it \\small (\\\\)? (.*?) \}', note) # Adjusted based on observed patterns
        if not name_match:
             name_match = re.search(r'\\it \\small (.*?) \}', note)
        
        name = name_match.group(2) if name_match and len(name_match.groups()) > 1 else (name_match.group(1) if name_match else "Unknown")
        name = name.strip().replace('\\\\', '').strip()
        
        portraits.append({
            'filename': img_match.group(1),
            'person': name
        })

print(json.dumps({'figures': figures, 'portraits': portraits}, indent=2))
