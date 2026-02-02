
def emergency_fix():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # We need to insert \end{figure}\clearpage at line 101 (index 101 or so)
    # View showed:
    # 100: \label{fig:Clustering}
    # 101: \n
    # 102: Over the past...
    
    # We look for \label{fig:Clustering}
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if "\\label{fig:Clustering}" in line:
            # Check if next line is end figure (it isn't)
            new_lines.append("\\end{figure}\n\\clearpage\n")
            
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("Emergency structure fix applied.")

if __name__ == "__main__":
    emergency_fix()
