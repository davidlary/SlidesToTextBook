
import sys
import os
from pathlib import Path

# Setup Path
sys.path.append(os.path.join(os.getcwd(), "src"))
from slides_to_textbook.modules.image_generators import FigureRecreator

def generate_figures():
    output_dir = Path("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Figures/Chapter-Introduction")
    recreator = FigureRecreator(output_dir)
    
    figures = {
        "Fig-Bias-VarianceTradeoff.png": "A diagram illustrating the Bias-Variance Tradeoff in machine learning. Show the relationship between Model Complexity (x-axis) and Error (y-axis). Include curves for Bias (decreasing), Variance (increasing), and Total Error (U-shaped). Mark the Optimal Complexity.",
        "Fig-DeepLearning.png": "A conceptual diagram of Deep Learning vs Machine Learning vs AI. Euler diagram style. AI > Machine Learning > Deep Learning. Or a network architecure showing input, many hidden layers, and output.",
        "Fig-NeuralNetworks.png": "A schematic of a Neural Network. Nodes connected by edges. Input layer, multiple Hidden layers, Output layer. Show weights and activation functions conceptually."
    }
    
    for filename, desc in figures.items():
        if not (output_dir / filename).exists():
            print(f"Generating {filename}...")
            recreator.recreate_figure(desc, filename)
        else:
            print(f"{filename} exists.")

if __name__ == "__main__":
    generate_figures()
