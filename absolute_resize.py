
def absolute_resize():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
    
    # Force replacement of ANY options for Fig-Underfitting
    import re
    
    # Regex: \includegraphics[ANYTHING]{...Fig-Underfitting.png}
    # We replace the whole tag
    pattern = r"\\includegraphics\[.*?\]\{Figures/Chapter-Introduction/Fig-Underfitting.png\}"
    replacement = r"\\includegraphics[width=6cm, keepaspectratio]{Figures/Chapter-Introduction/Fig-Underfitting.png}"
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(path, 'w') as f:
        f.write(new_content)
    print("Resized Underfitting to 6cm.")

if __name__ == "__main__":
    absolute_resize()
