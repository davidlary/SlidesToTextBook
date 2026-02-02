
def destroy_block():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # We want to remove lines 150 to 156 (inclusive 0-indexed or 1-indexed?)
    # View showed:
    # 151: \centering
    # 152: % \includegraphics
    # ...
    # 155: \end{figure}
    
    # We will filter out this block based on content markers
    new_lines = []
    in_cursed_block = False
    
    for i, line in enumerate(lines):
        # Start of block identifier:
        # We need to find the \begin{figure} that matches this end.
        # It was around line 150.
        
        # Heuristic: If we see the commented out Underfitting, we delete surrounding lines?
        # Better: Read the file, identify indices of the block [start, end], delete slice.
        pass

    # New strategy:
    # 1. Read file.
    # 2. Find index of "% \includegraphics...Fig-Underfitting"
    # 3. Search backwards for \begin{figure}
    # 4. Search forwards for \end{figure}
    # 5. Remove that range.
    
    idx_target = -1
    for i, line in enumerate(lines):
        if "Fig-Underfitting.png" in line and "%" in line:
            idx_target = i
            break
            
    if idx_target == -1:
        print("Could not find cursed line.")
        return

    start = idx_target
    while start > 0:
        if "\\begin{figure}" in lines[start]:
            break
        start -= 1
        
    end = idx_target
    while end < len(lines):
        if "\\end{figure}" in lines[end]:
            break
        end += 1
        
    print(f"Deleting lines {start} to {end}")
    
    # Slice out
    final_lines = lines[:start] + lines[end+1:]
    
    with open(path, 'w') as f:
        f.writelines(final_lines)
    print("Destroyed.")

if __name__ == "__main__":
    destroy_block()
