
from PIL import Image
from pathlib import Path
import statistics

ref_dir = Path("/Users/davidlary/Dropbox/Apps/Overleaf/AirQualityV3/Figures/Portraits")
files = list(ref_dir.glob("*.jpg"))[:10]  # Check first 10

ratios = []
widths = []
heights = []

print(f"Analyzing {len(files)} reference images...")
for f in files:
    try:
        with Image.open(f) as img:
            w, h = img.size
            ratio = w / h
            ratios.append(ratio)
            widths.append(w)
            heights.append(h)
            print(f"{f.name}: {w}x{h} (Ratio: {ratio:.2f})")
    except Exception as e:
        print(f"Skipping {f.name}: {e}")

if ratios:
    avg_ratio = statistics.mean(ratios)
    avg_w = statistics.mean(widths)
    avg_h = statistics.mean(heights)
    print(f"\nAverage Dimensions: {avg_w:.0f}x{avg_h:.0f}")
    print(f"Average Aspect Ratio: {avg_ratio:.2f}")
