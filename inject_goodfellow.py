
def inject_goodfellow():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
        
    name = "Ian Goodfellow"
    # Find context: "goodfellow2016deep" or "Goodfellow"
    # If "Ian Goodfellow" provided in text?
    # Text usually says "...deep learning (LeCun... Goodfellow...)"
    # or citation.
    
    # We will look for "Goodfellow" text or citation.
    target = "goodfellow2016deep"
    if target in content and "IanGoodfellow.jpg" not in content:
        code = (
            f"\\automarginnote{{\\includegraphics[width=\\linewidth]{{Portraits/Chapter-Introduction/IanGoodfellow.jpg}}"
            f" \\\\ \\centering \\footnotesize Ian Goodfellow (born 1985)}}"
        )
        # We replace the citation with citation + code?
        # Or just append after citation?
        content = content.replace(target + "}", target + "}" + code, 1) # Close brace of cite
        print("Injected Goodfellow")
    
    # Also valid: "Goodfellow" in text?
    
    with open(path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    inject_goodfellow()
