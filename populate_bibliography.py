
import os

BIB_CONTENT = """
@article{samuel1959some,
  title={Some studies in machine learning using the game of checkers},
  author={Samuel, Arthur L},
  journal={IBM Journal of research and development},
  volume={3},
  number={3},
  pages={210--229},
  year={1959},
  publisher={IBM}
}

@book{mitchell1997machine,
  title={Machine Learning},
  author={Mitchell, Tom M},
  year={1997},
  publisher={McGraw-Hill}
}

@book{sutton2018reinforcement,
  title={Reinforcement learning: An introduction},
  author={Sutton, Richard S and Barto, Andrew G},
  year={2018},
  publisher={MIT press}
}

@article{lecun2015deep,
  title={Deep learning},
  author={LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey},
  journal={nature},
  volume={521},
  number={7553},
  pages={436--444},
  year={2015},
  publisher={Nature Publishing Group}
}

@book{goodfellow2016deep,
  title={Deep Learning},
  author={Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  year={2016},
  publisher={MIT press}
}

@book{bishop2006pattern,
  title={Pattern Recognition and Machine Learning},
  author={Bishop, Christopher M},
  year={2006},
  publisher={Springer}
}

@book{murphy2012machine,
  title={Machine learning: a probabilistic perspective},
  author={Murphy, Kevin P},
  year={2012},
  publisher={MIT press}
}

@article{rosenblatt1958perceptron,
  title={The perceptron: a probabilistic model for information storage and organization in the brain},
  author={Rosenblatt, Frank},
  journal={Psychological review},
  volume={65},
  number={6},
  pages={386},
  year={1958},
  publisher={American Psychological Association}
}

@article{turing1950computing,
  title={Computing machinery and intelligence},
  author={Turing, Alan M},
  journal={Mind},
  volume={59},
  number={236},
  pages={433--460},
  year={1950},
  publisher={Oxford University Press}
}

@book{hastie2009elements,
  title={The elements of statistical learning: data mining, inference, and prediction},
  author={Hastie, Trevor and Tibshirani, Robert and Friedman, Jerome},
  year={2009},
  publisher={Springer Science \& Business Media}
}
"""

def main():
    path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/bibliography.bib"
    print(f"Populating bibliography at {path}")
    with open(path, "w") as f:
        f.write(BIB_CONTENT)
    print("Done.")

if __name__ == "__main__":
    main()
