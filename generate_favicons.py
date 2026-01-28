"""Generate PNG and ICO favicons from favicon.svg

Usage:
  python3 -m venv .venv && . .venv/bin/activate
  pip install cairosvg pillow
  python generate_favicons.py

This will create: favicon-32.png, favicon-16.png, favicon.ico
"""
from pathlib import Path
import sys

try:
    import cairosvg
    from PIL import Image
except Exception as e:
    print("Missing dependencies. Run: pip install cairosvg pillow")
    raise

HERE = Path(__file__).parent
SVG = HERE / 'favicon.svg'
if not SVG.exists():
    print('favicon.svg not found in', HERE)
    sys.exit(1)

with SVG.open('rb') as f:
    svg_bytes = f.read()

sizes = [32, 16]
out_files = []
for s in sizes:
    out = HERE / f'favicon-{s}.png'
    cairosvg.svg2png(bytestring=svg_bytes, write_to=str(out), output_width=s, output_height=s)
    print('Wrote', out)
    out_files.append(out)

# Create ICO containing 32x32 and 16x16
# Pillow can build an .ico by saving one image with sizes argument
img32 = Image.open(out_files[0]).convert('RGBA')
img16 = Image.open(out_files[1]).convert('RGBA')
ico_out = HERE / 'favicon.ico'
# Save ICO from the largest image and include sizes tuple
img32.save(ico_out, format='ICO', sizes=[(32,32),(16,16)])
print('Wrote', ico_out)
print('Done')
