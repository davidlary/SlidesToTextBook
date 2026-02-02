
def fix_braces():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if "\\automarginnote" in line:
            # Simple check: Count { vs }
            opens = line.count("{")
            closes = line.count("}")
            diff = opens - closes
            if diff > 0:
                # Add missing braces
                line = line.rstrip() + "}" * diff + "\n"
                
        new_lines.append(line)
        
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("Braces fixed.")

if __name__ == "__main__":
    fix_braces()
