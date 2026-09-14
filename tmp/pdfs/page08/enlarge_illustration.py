from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter

ROOT = Path('/Users/alina/Documents/сайт 1')
SOURCE_PDF = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')
SOURCE_PAGE = ROOT / 'tmp/pdfs/page08/images/img-000.png'
EDITED_PAGE = ROOT / 'tmp/pdfs/page08/page08_enlarged.png'
PAGE_PDF = ROOT / 'tmp/pdfs/page08/page08_enlarged.pdf'
OUTPUT = ROOT / 'output/pdf/Программы_реализации_конспект_с_вопросами.pdf'
DESKTOP = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')

page = Image.open(SOURCE_PAGE).convert('RGB')
arr = np.array(page)

# The illustration occupies a clean text-free area on the right.
x1, y1, x2, y2 = 1080, 330, 1415, 755
crop = arr[y1:y2, x1:x2].copy()

# Extract only the luminous blue figure and its shards from the dark backdrop.
gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
blue = crop[:, :, 2].astype(np.int16) - crop[:, :, 0].astype(np.int16)
mask = np.where((gray > 34) & ((blue > 0) | (gray > 72)), 255, 0).astype(np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
mask = cv2.GaussianBlur(mask, (0, 0), 1.2)

# Remove the old, smaller illustration and reconstruct its dark background.
full_mask = np.zeros(arr.shape[:2], dtype=np.uint8)
full_mask[y1:y2, x1:x2] = np.maximum(full_mask[y1:y2, x1:x2], mask)
clean = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), full_mask, 5, cv2.INPAINT_TELEA)
clean = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)
base = Image.fromarray(clean).convert('RGBA')

subject = Image.fromarray(crop).convert('RGBA')
subject.putalpha(Image.fromarray(mask).filter(ImageFilter.GaussianBlur(0.5)))
scale = 1.55
subject = subject.resize((round(subject.width * scale), round(subject.height * scale)), Image.Resampling.LANCZOS)

# Keep the larger figure balanced in the right column and away from the text.
base.alpha_composite(subject, (1005, 220))
base.convert('RGB').save(EDITED_PAGE, quality=96)

c = canvas.Canvas(str(PAGE_PDF), pagesize=(768, 480))
c.drawImage(ImageReader(str(EDITED_PAGE)), 0, 0, width=768, height=480)
c.showPage()
c.save()

reader = PdfReader(str(SOURCE_PDF))
replacement = PdfReader(str(PAGE_PDF))
writer = PdfWriter()
for i, p in enumerate(reader.pages):
    writer.add_page(replacement.pages[0] if i == 7 else p)
with OUTPUT.open('wb') as f:
    writer.write(f)

# Keep the user's working copy on the Desktop at the same stable filename.
DESKTOP.write_bytes(OUTPUT.read_bytes())
print(OUTPUT)
