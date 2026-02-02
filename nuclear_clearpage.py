
def nuclear_clearpage():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
        
    # Replace \end{figure} with \end{figure}\clearpage
    # Check if clearpage is already there to avoid duplicates
    # We can do a regex sub
    import re
    # Pattern: \end{figure} NOT followed by \clearpage
    # But re doesn't support lookahead well in replace sometimes?
    # Simple strategy: Replace ALL \end{figure} with \end{figure}\clearpage
    # Then replace \clearpage\clearpage with \clearpage
    
    content = content.replace("\\end{figure}", "\\end{figure}\n\\clearpage")
    content = content.replace("\\clearpage\n\\clearpage", "\\clearpage")
    content = content.replace("\\clearpage\\clearpage", "\\clearpage")
    
    with open(path, 'w') as f:
        f.write(content)
    print("Nuclear clearpages applied.")

if __name__ == "__main__":
    nuclear_clearpage()
