
from PIL import Image
from pathlib import Path
import numpy as np

def check_whitespace(folder):
    p = Path(folder)
    for img_path in p.glob("*.jpg"):
        try:
            img = Image.open(img_path)
            img_np = np.array(img)
            # Check for white rows/cols
            # White is [255, 255, 255]
            # We'll allow a small tolerance
            is_white = np.all(img_np > 250, axis=2)
            
            rows_white = np.all(is_white, axis=1)
            cols_white = np.all(is_white, axis=0)
            
            top_border = np.argmax(~rows_white)
            bottom_border = len(rows_white) - np.argmax(~rows_white[::-1])
            left_border = np.argmax(~cols_white)
            right_border = len(cols_white) - np.argmax(~cols_white[::-1])
            
            height = img.height
            width = img.width
            
            # Calculate whitespace percentage
            whitespace_h = (top_border + (height - bottom_border)) / height
            whitespace_w = (left_border + (width - right_border)) / width
            
            print(f"Image: {img_path.name}")
            print(f"  Dimensions: {width}x{height}")
            print(f"  Whitespace Top: {top_border}px, Bottom: {height - bottom_border}px ({whitespace_h:.1%} vertical)")
            print(f"  Whitespace Left: {left_border}px, Right: {width - right_border}px ({whitespace_w:.1%} horizontal)")
        except Exception as e:
            print(f"Error checking {img_path.name}: {e}")

check_whitespace("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Portraits/Chapter-Introduction")
