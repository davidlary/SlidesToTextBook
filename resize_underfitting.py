
def resize_underfitting():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
        
    # Drastic resize
    # Regex replace any includegraphics for Fig-Underfitting
    import re
    
    # We look for \includegraphics[...]{...Fig-Underfitting.png}
    # and replace the options [...]
    
    pattern = r"\\includegraphics\[.*?\]\{Figures/Chapter-Introduction/Fig-Underfitting.png\}"
    replacement = r"\\includegraphics[width=0.8\\linewidth, height=0.3\\textheight, keepaspectratio]{Figures/Chapter-Introduction/Fig-Underfitting.png}"
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print("Warning: regex did not match. Trying manual replace.")
        # Try simple string replace of known variants
        variants = [
            "width=1.0\\linewidth",
            "width=0.8\\linewidth",
            "width=0.5\\linewidth",
            "width=0.4\\linewidth"
        ]
        for v in variants:
             new_content = new_content.replace(
                 f"\\includegraphics[{v}]{{Figures/Chapter-Introduction/Fig-Underfitting.png}}",
                 r"\includegraphics[width=0.8\linewidth, height=0.3\textheight, keepaspectratio]{Figures/Chapter-Introduction/Fig-Underfitting.png}"
             )
    
    with open(path, 'w') as f:
        f.write(new_content)
    print("Resized Underfitting.")

if __name__ == "__main__":
    resize_underfitting()
