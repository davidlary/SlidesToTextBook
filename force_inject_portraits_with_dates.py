
import re

PEOPLE_METADATA = [
    {"name": "Arthur Samuel", "file": "ArthurSamuel.jpg", "dates": "(1901–1990)"},
    {"name": "Tom Mitchell", "file": "TomMitchell.jpg", "dates": "(born 1951)"},
    {"name": "Yann LeCun", "file": "YannLeCun.jpg", "dates": "(born 1960)"},
    {"name": "Frank Rosenblatt", "file": "FrankRosenblatt.jpg", "dates": "(1928–1971)"},
    {"name": "Alan Turing", "file": "AlanTuring.jpg", "dates": "(1912–1954)"},
    {"name": "Geoffrey Hinton", "file": "GeoffreyHinton.jpg", "dates": "(born 1947)"},
    {"name": "Donald Hebb", "file": "DonaldHebb.jpg", "dates": "(1904–1985)"},
    {"name": "Yoshua Bengio", "file": "YoshuaBengio.jpg", "dates": "(born 1964)"},
    {"name": "Ian Goodfellow", "file": "IanGoodfellow.jpg", "dates": "(born 1985)"}
]


def force_inject():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()

    # 1. Clean existing automarginnotes
    # Simple regex to remove them? OR just manual clean lines.
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        if "\\automarginnote" in line and "Portraits/" in line and "\\includegraphics" in line:
            continue
        clean_lines.append(line)
    content = "\n".join(clean_lines)

    # 2. Iterate through people
    for person in PEOPLE_METADATA:
        name = person["name"]
        filename = person["file"]
        dates = person["dates"]
        
        latex_code = (
            f"\\automarginnote{{\\includegraphics[width=\\linewidth]{{Portraits/Chapter-Introduction/{filename}}}"
            f" \\\\ \\centering \\footnotesize {name} {dates}}}"
        )
        
        # SEARCH STRATEGY:
        # We walk through the content. We track if we are inside \begin{figure}...\end{figure}.
        # If we find the name in a safe zone, we inject.
        
        # We can simulate a parser
        new_content_chars = []
        i = 0
        in_figure = False
        injected = False
        
        # We need to rebuild the string or use a regex replacement function that checks context.
        # Regex is easier: re.sub(pattern, replacements_func)
        # But tracking state in regex is hard.
        
        # Let's tokenize by \begin{figure} ... \end{figure}
        # Split by regex `(\\begin\{figure\}.*?\\end\{figure\})`, keeping delimiters (using capturing group)
        # Note: DOTALL needed.
        
        tokens = re.split(r'(\\begin\{figure\}.*?\\end\{figure\})', content, flags=re.DOTALL)
        
        # Now tokens is a list: [Text, FigureBlock, Text, FigureBlock, Text]
        # We only inject in Text blocks.
        
        for idx, token in enumerate(tokens):
            if injected:
                break # Done for this person
            
            if "\\begin{figure}" in token:
                continue # Skip figures
                
            # If safe text, look for name
            if name in token:
                # Replace FIRST occurrence only
                # "Arthur Samuel" -> "Arthur Samuel\latex_code"
                
                # Careful: make sure it's not part of a command like \citet{...} if possible, but usually those are lowercase keys.
                # However, if it's "Arthur Samuel" (Capitalized), it's likely text.
                
                # We need to update existing token in the list
                # Use string replace, count=1
                # But we need to make sure we don't accidentally match `\citep{ArthurSamuel...}` if that existed.
                # Assuming standard text:
                
                new_token = token.replace(name, f"{name}{latex_code}", 1)
                tokens[idx] = new_token
                injected = True
                print(f"Injected {name} into text block {idx}.")
        
        if not injected:
            # Fallback: Just append to the very beginning of the chapter?
            # Or print warning.
            # If "Arthur Samuel" is ONLY in a figure, we can't inject in text.
            # Maybe inject AFTER the first figure that mentions him?
            # Or just inject at the very first line of the file (after section headers)?
            print(f"WARNING: Could not safe-inject {name} (maybe only in figures?)")
        
        # Reassemble for next person
        content = "".join(tokens)

    # 3. Resize Underfitting Figure
    content = content.replace("Figures/Chapter-Introduction/Fig-Underfitting.png}", "Figures/Chapter-Introduction/Fig-Underfitting.png}")
    content = content.replace("width=1.0\\linewidth]{Figures/Chapter-Introduction/Fig-Underfitting.png}", "width=0.5\\linewidth]{Figures/Chapter-Introduction/Fig-Underfitting.png}")
    content = content.replace("width=0.8\\linewidth]{Figures/Chapter-Introduction/Fig-Underfitting.png}", "width=0.5\\linewidth]{Figures/Chapter-Introduction/Fig-Underfitting.png}")

    with open(path, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    force_inject()
