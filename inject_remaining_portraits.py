
def inject_others():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
        
    people = [
        {"name": "Geoffrey Hinton", "file": "GeoffreyHinton.jpg", "dates": "(born 1947)"},
        {"name": "Yann LeCun", "file": "YannLeCun.jpg", "dates": "(born 1960)"},
        {"name": "Yoshua Bengio", "file": "YoshuaBengio.jpg", "dates": "(born 1964)"},
        {"name": "Donald Hebb", "file": "DonaldHebb.jpg", "dates": "(1904–1985)"}
    ]
    
    for p in people:
        name = p["name"]
        if name in content and p["file"] not in content:
            code = (
                f"\\automarginnote{{\\includegraphics[width=\\linewidth]{{Portraits/Chapter-Introduction/{p['file']}}}"
                f" \\\\ \\centering \\footnotesize {name} {p['dates']}}}"
            )
            # Replace first occurrence
            content = content.replace(name, name + code, 1)
            print(f"Injected {name}")
            
    with open(path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    inject_others()
