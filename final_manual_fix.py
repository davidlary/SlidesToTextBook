
def manual_fix():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # Data for injection
    samuel_code = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/ArthurSamuel.jpg} \\ \centering \footnotesize Arthur Samuel (1901–1990)}"
    mitchell_code = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/TomMitchell.jpg} \\ \centering \footnotesize Tom Mitchell (born 1951)}"
    
    new_lines = []
    for i, line in enumerate(lines):
        # 1. Inject Samuel and Mitchell at Line 7 (approx)
        if "Arthur Samuel, Tom Mitchell" in line and "SamuelsInjected" not in line:
            # We append the codes to the line definition
            # To avoid "Not in outer par mode", we should make sure we aren't inside a command?
            # Text is fine.
            # We append to the string match
            line = line.replace("Arthur Samuel", "Arthur Samuel" + samuel_code)
            line = line.replace("Tom Mitchell", "Tom Mitchell" + mitchell_code)
            # Mark as done to prevent double injection in this run if loop is complex
            
        # 2. Fix Float Queue (Insert \clearpage after some figures)
        # Figure 2 (Classification) ends around line 35
        if "Fig-Classification.png" in line and "\\end{figure}" in lines[i+3]: 
             # Heuristic: Find the end of this figure block
             pass 
        
        # Easier: Just replace specific \end{figure} lines with \end{figure}\clearpage
        if "\\label{fig:Classification}" in line:
            # The next line should be \end{figure}
            # We'll just append clearpage to THIS line's output effectively? No.
            pass

        # 3. Resize Underfitting
        if "Fig-Underfitting.png" in line:
             line = line.replace("width=1.0\\linewidth", "width=0.5\\linewidth")
             line = line.replace("width=0.8\\linewidth", "width=0.5\\linewidth")

        new_lines.append(line)
        
    # Post-process for \end{figure} \clearpage
    final_lines = []
    for line in new_lines:
        final_lines.append(line)
        if "\\label{fig:Classification}" in line:
             # Look ahead? No.
             # Just add clearpage after the NEXT line (which is end figure)
             # This is hard in single pass.
             pass
             
    # String based replacement for clearpage
    content = "".join(new_lines)
    content = content.replace("\\label{fig:Classification}\n\\end{figure}", "\\label{fig:Classification}\n\\end{figure}\n\\clearpage")
    content = content.replace("\\label{fig:UnsupervisedLearning}\n\\end{figure}", "\\label{fig:UnsupervisedLearning}\n\\end{figure}\n\\clearpage")

    # 4. Remove nested automarginnotes or bad placements causing "Not in outer par mode"
    # The error logs showed errors around line 103, 108.
    # Lines 100-110 in the view seem to have `\automarginnote{Figure 4...}`
    # If I injected a portrait inside that, it breaks.
    # Regex to clean `\automarginnote{...\automarginnote{...}...}`?
    # Or just look for known bad strings.
    
    with open(path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    manual_fix()
