from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader, PdfWriter

ROOT = Path('/Users/alina/Documents/сайт 1')
SOURCE = Path('/Users/alina/Desktop/Программы_реализации_конспект.pdf')
REPLACEMENT = ROOT / 'tmp/pdfs/questions_pages.pdf'
OUTPUT_DIR = ROOT / 'output/pdf'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT = OUTPUT_DIR / 'Программы_реализации_конспект_с_вопросами.pdf'

pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

questions = [
    'Чем я занималась бы, если бы мне не нужно было никому доказывать, что моя работа серьёзная и достойная?',
    'Что мне действительно нравится делать и за что я хотела бы получать деньги?',
    'Какой результат я хочу создавать для других людей?',
    'Сколько часов в день и сколько дней в неделю я хочу работать?',
    'В какое время суток мне комфортнее работать и какой ритм мне подходит?',
    'Где я хочу работать: дома, в офисе, собственной студии, путешествиях или разных местах?',
    'Какой формат мне подходит: онлайн, офлайн или их сочетание?',
    'С кем я хочу работать: одна, в небольшой команде, с большим коллективом, с клиентами лично или с широкой аудиторией?',
    'Хочу ли я сама принимать все решения или мне комфортнее работать внутри готовой системы?',
    'Какие задачи я хочу выполнять сама, а какие — делегировать?',
    'Что точно должно быть в моей идеальной работе и реализации себя?',
]

W, H = 768, 480

def draw_page(c, page_num, title, items, start_number):
    c.setFillColor(HexColor('#0f1112'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Subtle panels preserve the restrained visual language of the source.
    c.setFillColor(HexColor('#121516'))
    c.rect(0, 0, W, 92, fill=1, stroke=0)
    c.setFillColor(HexColor('#9aa0a3'))
    c.setFont('ArialBold', 9.5)
    c.drawString(56, 442, 'ПРАКТИКА')
    c.drawRightString(712, 442, f'{page_num:02d} / 13')

    c.setFillColor(HexColor('#ffffff'))
    c.setFont('ArialBold', 25)
    c.drawString(56, 398, title)

    y = 348
    body_size = 14
    leading = 18
    gap = 13
    number_x = 57
    text_x = 88
    max_width = 620

    for offset, question in enumerate(items):
        number = start_number + offset
        lines = simpleSplit(question, 'Arial', body_size, max_width)
        c.setFillColor(HexColor('#aeb4b7'))
        c.setFont('ArialBold', 12)
        c.drawRightString(76, y + 1, f'{number}.')
        c.setFillColor(HexColor('#f4f4f4'))
        c.setFont('Arial', body_size)
        for line in lines:
            c.drawString(text_x, y, line)
            y -= leading
        y -= gap

    c.showPage()

c = canvas.Canvas(str(REPLACEMENT), pagesize=(W, H))
draw_page(c, 4, 'Определите, чего вы вообще хотите', questions[:6], 1)
draw_page(c, 5, 'Соберите образ идеальной реализации', questions[6:], 7)
c.save()

source = PdfReader(str(SOURCE))
replacement = PdfReader(str(REPLACEMENT))
writer = PdfWriter()
for index, page in enumerate(source.pages):
    if index == 3:
        writer.add_page(replacement.pages[0])
    elif index == 4:
        writer.add_page(replacement.pages[1])
    else:
        writer.add_page(page)

with OUTPUT.open('wb') as stream:
    writer.write(stream)

print(OUTPUT)
