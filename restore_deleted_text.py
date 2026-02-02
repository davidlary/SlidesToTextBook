
def restore_text():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # We will replace lines 6-10 (which are empty/newlines) with the restored text.
    # checking context: Line 5 ends with "...dating back to the 1950s."
    # Line 12 starts with "In the 1980s..."
    
    # Restored Block 1
    # Note: We include the portrait injection DIRECTLY here.
    samuel_pic = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/ArthurSamuel.jpg} \\ \centering \footnotesize Arthur Samuel (1901–1990)}"
    mitchell_pic = r"\automarginnote{\includegraphics[width=\linewidth]{Portraits/Chapter-Introduction/TomMitchell.jpg} \\ \centering \footnotesize Tom Mitchell (born 1951)}"
    
    block1 = (
        "The origins of machine learning can be traced to the pioneering work of researchers such as Arthur Samuel" + samuel_pic + ", Tom Mitchell, and others who laid the foundations for this field. "
        "In 1959, Arthur Samuel, a computer scientist at IBM, developed one of the first self-learning programs, a checkers-playing program that could improve its performance through experience \\citep{samuel1959some}. "
        "This groundbreaking work demonstrated the potential of machines to learn and adapt, paving the way for the development of more sophisticated machine learning algorithms.\n\n"
    )
    
    block2 = (
        "In the following decades, the field of machine learning continued to evolve, with researchers such as Tom Mitchell" + mitchell_pic + ", Geoffrey Hinton, Yann LeCun, and Yoshua Bengio making significant contributions to the field. "
        "Tom Mitchell, a renowned computer scientist, provided a formal definition of machine learning, stating that \"a computer program is said to learn from experience $E$ with respect to some class of tasks $T$ and performance measure $P$, if its performance at tasks in $T$, as measured by $P$, improves with experience $E$\" \\citep{mitchell1997machine}. "
        "This definition has become a cornerstone of the field, guiding the development of various machine learning algorithms and techniques.\n\n"
    )
    
    # We assume lines 6,7,8,9,10,11 are the empty ones.
    # Let's verify by checking content strictly?
    # Or just replace the range 6:12 with [block1, block2]
    # Line indices are 0-based.
    # File view showed:
    # 5: ... 1950s.
    # 6: 
    # 7: 
    # 8: 
    # 9: 
    # 10: 
    # 11: 
    # 12: In the 1980s...
    
    # So we replace slice [6:12]
    
    # Ensure lines[5] is the "1950s." line.
    if "dating back to the 1950s." in lines[4]: # Line 5 is index 4
         start_idx = 5
    elif "dating back to the 1950s." in lines[5]: # Maybe index 5?
         start_idx = 6
    else:
         print("Warning: Could not align lines strictly. Searching...")
         for i, l in enumerate(lines):
             if "dating back to the 1950s." in l:
                 start_idx = i + 1
                 break
                 
    end_idx = start_idx
    for i in range(start_idx, len(lines)):
        if "In the 1980s" in lines[i]:
            end_idx = i
            break
            
    # Replace slice
    lines[start_idx:end_idx] = [block1, block2]
    
    with open(path, 'w') as f:
        f.writelines(lines)
    print("Replanted text blocks.")

if __name__ == "__main__":
    restore_text()
