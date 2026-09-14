from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path('/Users/alina/Documents/сайт 1')
SRC = Path('/Users/alina/Desktop/Программы_реализации_конспект.pdf')
OUT = ROOT / 'output/pdf/Программы_реализации_конспект.pdf'
ORIGINAL_RENDER = ROOT / 'tmp/pdfs/contact/p-10.png'


def corrected_quote_page():
    # Start from the original rendered slide so its texture, spacing and labels stay intact.
    source = cv2.imread(str(ORIGINAL_RENDER))
    # Rebuild only the quote field from a heavily smoothed copy of the original
    # background. This removes every antialiased trace of the old wording while
    # retaining the slide's broad vignette and texture.
    clean = source.copy()
    y0, y1, x0, x1 = 165, 470, 55, 905
    top = source[y0 - 1, x0:x1].astype(np.float32)
    bottom = source[y1, x0:x1].astype(np.float32)
    rng = np.random.default_rng(7)
    for y in range(y0, y1):
        alpha = (y - y0) / max(1, y1 - y0 - 1)
        row = top * (1 - alpha) + bottom * alpha
        noise = rng.normal(0, 0.65, row.shape)
        clean[y, x0:x1] = np.clip(row + noise, 0, 255).astype(np.uint8)
    image = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Italic.ttf', 28)
    lines = [
        'Все правды сосуществуют одновременно. Поэтому',
        'вы не спорите с чёрными — они просто несозвучны',
        'с вашей истиной, а не доказательство того, что вы',
        'неправы.',
    ]
    for text, y in zip(lines, (224, 286, 348, 410)):
        box = draw.textbbox((0, 0), text, font=font)
        x = (image.width - (box[2] - box[0])) / 2
        draw.text((x, y), text, font=font, fill=(235, 235, 235))

    png = BytesIO()
    image.save(png, 'PNG')
    png.seek(0)
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(768, 480))
    c.drawImage(ImageReader(png), 0, 0, width=768, height=480)
    c.showPage()
    c.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


def numbered_overlay(number):
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(768, 480))
    c.setFillColorRGB(14 / 255, 16 / 255, 17 / 255)
    c.rect(680, 445, 75, 24, stroke=0, fill=1)
    c.setFillColorRGB(0.58, 0.60, 0.62)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawRightString(735, 455, f'{number:02d} / 13')
    c.showPage()
    c.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


reader = PdfReader(str(SRC))
replacement = corrected_quote_page()

# On the first run, remove the original question slides (4-5) from the middle
# and keep their copies at the end. On verification reruns, the deck is already
# in its final 13-page order.
order = [0, 1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] if len(reader.pages) == 15 else list(range(13))
writer = PdfWriter()
for index in order:
    quote_index = 9 if len(reader.pages) == 15 else 7
    page = replacement if index == quote_index else reader.pages[index]
    if len(writer.pages) + 1 >= 2:
        page.merge_page(numbered_overlay(len(writer.pages) + 1))
    writer.add_page(page)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('wb') as stream:
    writer.write(stream)
SRC.write_bytes(OUT.read_bytes())

# Keep the alternate filename synchronized so either Desktop file opens the same deck.
alternate = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')
alternate.write_bytes(OUT.read_bytes())
