from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path('/Users/alina/Documents/сайт 1')
SRC = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')
OUT = ROOT / 'output/pdf/Программы_реализации_конспект_с_вопросами.pdf'
DESKTOP = SRC

scale = 3
w, h = 768 * scale, 480 * scale
img = Image.new('RGB', (w, h), (14, 16, 17))
draw = ImageDraw.Draw(img)

italic_path = '/System/Library/Fonts/Supplemental/Arial Italic.ttf'
regular_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
italic = ImageFont.truetype(italic_path, 18 * scale)
small = ImageFont.truetype(regular_path, 7 * scale)

lines = [
    'Все правды сосуществуют одновременно. Поэтому',
    'вы не спорите с чёрными — они просто несозвучны',
    'с вашей истиной, а не доказательство того, что вы',
    'неправы.',
]

ys = [109, 139, 169, 199]
for text, y in zip(lines, ys):
    box = draw.textbbox((0, 0), text, font=italic)
    tw = box[2] - box[0]
    draw.text(((w - tw) / 2, y * scale), text, font=italic, fill=(238, 238, 238))

page_no = '10 / 13'
box = draw.textbbox((0, 0), page_no, font=small)
draw.text((735 * scale - (box[2] - box[0]), 20 * scale), page_no, font=small, fill=(145, 148, 151))
draw.line((369 * scale, 246 * scale, 399 * scale, 246 * scale), fill=(95, 101, 105), width=1 * scale)

png = BytesIO()
img.save(png, format='PNG')
png.seek(0)

page_pdf = BytesIO()
c = canvas.Canvas(page_pdf, pagesize=(768, 480))
c.drawImage(ImageReader(png), 0, 0, width=768, height=480)
c.showPage()
c.save()
page_pdf.seek(0)

reader = PdfReader(str(SRC))
replacement = PdfReader(page_pdf).pages[0]
writer = PdfWriter()
for idx, page in enumerate(reader.pages):
    writer.add_page(replacement if idx == 9 else page)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('wb') as f:
    writer.write(f)
DESKTOP.write_bytes(OUT.read_bytes())
