
import re

def final_fix():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        # Fix spurious citations after figure
        # Pattern: \end{figure} \citep{...}
        if "\\end{figure}" in line and "\\citep" in line:
            line = re.sub(r'\\citep\{[^}]+\}', '', line)
            
        # Fix trailing braces from stripped italics
        # Heuristic: If line ends with ".}" and contains "machine learning" or similar
        # Specific known error: "machine learning.}"
        if line.strip().endswith(".}"):
            line = line.replace(".}", ".")
            
        # Resize huge figure
        if "Fig-Underfitting.png" in line:
             line = line.replace("width=1.0\\linewidth", "width=0.8\\linewidth")
             
        new_lines.append(line)
        
    # Check for \clearpage
    content = "".join(new_lines)
    if "\\clearpage" not in content:
        content += "\n\\clearpage\n"
        
    with open(path, 'w') as f:
        f.write(content)
        
    print("Final fix applied.")

if __name__ == "__main__":
    final_fix()
