
from PIL import Image
from pathlib import Path

img_path = Path("/Users/davidlary/Dropbox/Environments/Code/SlidesToLatex/Examples/Project-Bastion-Mobile.jpeg")
try:
    with Image.open(img_path) as img:
        print(f"Example Image: {img_path.name}")
        print(f"Dimensions: {img.width}x{img.height}")
        print(f"Aspect Ratio: {img.width/img.height:.2f}")
except Exception as e:
    print(f"Error: {e}")
