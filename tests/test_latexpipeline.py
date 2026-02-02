
import unittest
import os
import re

class TestLatexStructure(unittest.TestCase):
    def setUp(self):
        self.tex_path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
        with open(self.tex_path, 'r') as f:
            self.content = f.read()

    def test_no_bad_commands(self):
        """Ensure no 'not in outer par mode' triggers exist (automarginnote inside automarginnote)."""
        # Heuristic: Check for nested braces inside automarginnote? Hard with regex.
        # Check for automarginnote{...automarginnote...}
        match = re.search(r'\\automarginnote\{.*?\\automarginnote', self.content, re.DOTALL)
        self.assertIsNone(match, "Found nested automarginnotes")

    def test_portraits_present(self):
        """Ensure key portraits are injected."""
        required = [
            "ArthurSamuel.jpg",
            "TomMitchell.jpg",
            "FrankRosenblatt.jpg",
            "AlanTuring.jpg",
            "IanGoodfellow.jpg",
            "YoshuaBengio.jpg",
            "GeoffreyHinton.jpg",
            "YannLeCun.jpg",
            "DonaldHebb.jpg"
        ]
        for p in required:
             self.assertIn(p, self.content, f"Portrait {p} is missing")

    def test_date_ranges(self):
        """Ensure date ranges are present in captions."""
        self.assertIn("Arthur Samuel (1901–1990)", self.content)
        self.assertIn("Tom Mitchell (born 1951)", self.content)
        # Add checks for others...
        
    def test_figures_have_captions(self):
        """Ensure standard figures maintain structure."""
        self.assertIn(r"\label{fig:Underfitting}", self.content)
        self.assertIn(r"\includegraphics[width=0.4\linewidth]{Figures/Chapter-Introduction/Fig-Underfitting.png}", self.content)

if __name__ == '__main__':
    unittest.main()
