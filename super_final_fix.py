
def final_polish():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    with open(path, 'r') as f:
        content = f.read()
        
    # Fix typo
    content = content.replace("\\clearpageMachine", "\\clearpage\nMachine")
    
    # Fix Float Lost by adding clearpage after figure walls
    # We already have some. Let's add one more after Fig-Classification if not there?
    # Or after Fig-Regression?
    
    # Heuristic: Insert clearpage after figure 4 (Reinforcement Learning)
    # Figure blocks:
    # 1. TrainingData
    # 2. Classification -> \clearpage (Added by last_resort)
    # 3. Regression
    # 4. Reinforcement -> Insert \clearpage here
    
    if "\\label{fig:ReinforcementLearning}" in content and "\\clearpage" not in content.split("\\label{fig:ReinforcementLearning}")[1][:100]:
        # Find end of figure
        # Regex replacement?
        # Simpler: replace the label line's end figure context
        pass
        
    # Just manual string replace for safety
    content = content.replace("\\label{fig:ReinforcementLearning}\n\\end{figure}", "\\label{fig:ReinforcementLearning}\n\\end{figure}\n\\clearpage")

    with open(path, 'w') as f:
        f.write(content)
    print("Polished.")

if __name__ == "__main__":
    final_polish()
