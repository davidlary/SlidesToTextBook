
def remove_underfitting():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    skip = False
    for line in lines:
        if "\\label{fig:Underfitting}" in line:
            # We are inside the bad block.
            # We need to have seemingly commented out the previous lines?
            # Easier: Just rewriting the file skipping the block.
            pass
            
        # Context-aware removal
        # We look for \includegraphics...Fig-Underfitting
        if "Fig-Underfitting.png" in line:
            new_lines.append("% " + line) # Comment out
        elif "\\label{fig:Underfitting}" in line:
            new_lines.append("% " + line)
        elif "Underfitting" in line and "\\caption" in line:
            new_lines.append("% " + line)
        else:
            new_lines.append(line)
            
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("Commented out Cursed Figure.")

if __name__ == "__main__":
    remove_underfitting()
