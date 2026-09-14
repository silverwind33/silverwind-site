from io import BytesIO
from pathlib import Path
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path('/Users/alina/Documents/сайт 1')
PDF = Path('/Users/alina/Desktop/Программы_реализации_конспект.pdf')
OUT = ROOT / 'output/pdf/Программы_реализации_конспект.pdf'

S = 3
W, H = 768 * S, 480 * S
REG = '/Library/Fonts/Montserrat-Medium.otf'
SEMIBOLD = '/Library/Fonts/Montserrat-SemiBold.otf'
BOLD = '/Library/Fonts/Montserrat-Bold.otf'
ITALIC = '/Library/Fonts/Montserrat-MediumItalic.otf'


def background(seed=11):
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W * 0.48, H * 0.45
    radial = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    base = 17.5 - np.clip(radial * 5.0, 0, 3.5)
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 0.55, (H, W))
    values = np.clip(base + noise, 12, 20).astype(np.uint8)
    return Image.fromarray(np.dstack([values, values + 1, values + 1]), 'RGB')


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def top_chrome(draw, page_no, label='КОНСПЕКТ'):
    draw.text((32 * S, 25 * S), label, font=font(SEMIBOLD, 6.6), fill=(135, 139, 142))
    no = f'{page_no:02d} / 13'
    f = font(SEMIBOLD, 6.6)
    box = draw.textbbox((0, 0), no, font=f)
    draw.text((735 * S - (box[2] - box[0]), 25 * S), no, font=f, fill=(135, 139, 142))


def to_pdf_page(image):
    png = BytesIO(); image.save(png, 'PNG'); png.seek(0)
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(768, 480))
    c.drawImage(ImageReader(png), 0, 0, width=768, height=480)
    c.showPage(); c.save(); stream.seek(0)
    return PdfReader(stream).pages[0]


def quote_slide():
    im = background(8)
    d = ImageDraw.Draw(im)
    top_chrome(d, 8)
    f = font(ITALIC, 15.5)
    lines = [
        'Все правды сосуществуют одновременно. Поэтому',
        'вы не спорите с чёрными — они просто несозвучны',
        'с вашей истиной, а не доказательство того, что вы',
        'неправы.',
    ]
    for line, y in zip(lines, (151, 184, 217, 250)):
        box = d.textbbox((0, 0), line, font=f)
        d.text(((W - (box[2] - box[0])) / 2, y * S), line, font=f, fill=(231, 232, 232))
    d.line((369 * S, 292 * S, 399 * S, 292 * S), fill=(101, 106, 109), width=1 * S)
    return to_pdf_page(im)


def assignment_slide(page_no, title, questions):
    im = background(page_no)
    d = ImageDraw.Draw(im)
    top_chrome(d, page_no, 'ПРАКТИКА')
    d.text((36 * S, 72 * S), title, font=font(BOLD, 20), fill=(245, 245, 245))

    num_font = font(SEMIBOLD, 9.2)
    body_font = font(REG, 9.2)
    y = 132 * S
    max_width = 610 * S
    line_gap = 15.2 * S
    item_gap = 11 * S
    for number, question in questions:
        d.text((45 * S, y), f'{number}.', font=num_font, fill=(176, 180, 183))
        words = question.split()
        lines, current = [], ''
        for word in words:
            trial = f'{current} {word}'.strip()
            if d.textlength(trial, font=body_font) <= max_width:
                current = trial
            else:
                lines.append(current); current = word
        if current:
            lines.append(current)
        for i, line in enumerate(lines):
            d.text((72 * S, y + i * line_gap), line, font=body_font, fill=(225, 227, 228))
        y += len(lines) * line_gap + item_gap
    return to_pdf_page(im)


q1 = [
    (1, 'Чем я занималась бы, если бы мне не нужно было никому доказывать, что моя работа серьёзная и достойная?'),
    (2, 'Что мне действительно нравится делать и за что я хотела бы получать деньги?'),
    (3, 'Какой результат я хочу создавать для других людей?'),
    (4, 'Сколько часов в день и сколько дней в неделю я хочу работать?'),
    (5, 'В какое время суток мне комфортнее работать и какой ритм мне подходит?'),
    (6, 'Где я хочу работать: дома, в офисе, собственной студии, в путешествиях или разных местах?'),
]
q2 = [
    (7, 'Какой формат мне подходит: онлайн, офлайн или их сочетание?'),
    (8, 'С кем я хочу работать: одна, в небольшой команде, с большим коллективом, с клиентами лично или с широкой аудиторией?'),
    (9, 'Хочу ли я сама принимать все решения или мне комфортнее работать внутри готовой системы?'),
    (10, 'Какие задачи я хочу выполнять сама, а какие — делегировать?'),
    (11, 'Что точно должно быть в моей идеальной работе и реализации себя?'),
]

reader = PdfReader(str(PDF))
replacements = {
    7: quote_slide(),
    11: assignment_slide(12, 'Определите, чего вы вообще хотите', q1),
    12: assignment_slide(13, 'Соберите образ идеальной реализации', q2),
}
writer = PdfWriter()
for i, page in enumerate(reader.pages):
    writer.add_page(replacements.get(i, page))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('wb') as stream:
    writer.write(stream)
PDF.write_bytes(OUT.read_bytes())
Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf').write_bytes(OUT.read_bytes())
