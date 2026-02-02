
def last_resort():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    figure_count = 0
    
    # Injection content
    samuel_block = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/ArthurSamuel.jpg} \\ \centering \footnotesize Arthur Samuel (1901–1990)}"
    mitchell_block = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/TomMitchell.jpg} \\ \centering \footnotesize Tom Mitchell (born 1951)}"
    
    injected_samuel = False
    
    for i, line in enumerate(lines):
        # 1. Inject Samuel/Mitchell at Line 7
        if "Arthur Samuel, Tom Mitchell" in line and not injected_samuel:
            line = line.replace("Arthur Samuel, Tom Mitchell", f"Arthur Samuel{samuel_block}, Tom Mitchell{mitchell_block}")
            injected_samuel = True
            
        # 2. Clearpage every 2 figures
        if "\\end{figure}" in line:
            figure_count += 1
            if figure_count % 2 == 0:
                line = line.replace("\\end{figure}", "\\end{figure}\n\\clearpage")
                
        # 3. Resize Underfitting
        if "Fig-Underfitting.png" in line:
             line = line.replace("width=1.0\\linewidth", "width=0.4\\linewidth")
             line = line.replace("width=0.8\\linewidth", "width=0.4\\linewidth")
             line = line.replace("width=0.5\\linewidth", "width=0.4\\linewidth")
             
        # 4. Remove potentially problematic automarginnotes
        # "Figure 4 shows..."
        if "\\automarginnote{Figure" in line:
            # Comment it out or remove
            line = "% " + line
            
        new_lines.append(line)
        
    with open(path, 'w') as f:
        f.writelines(new_lines)
        
    print("Last resort fix applied.")

if __name__ == "__main__":
    last_resort()
