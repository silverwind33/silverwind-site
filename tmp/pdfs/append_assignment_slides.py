from pathlib import Path

from pypdf import PdfReader, PdfWriter


src = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')
out = Path('/Users/alina/Documents/сайт 1/output/pdf/Программы_реализации_конспект_с_вопросами.pdf')

reader = PdfReader(str(src))
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Slides 04 and 05 contain the complete 11-question assignment.
writer.add_page(reader.pages[3])
writer.add_page(reader.pages[4])

out.parent.mkdir(parents=True, exist_ok=True)
with out.open('wb') as stream:
    writer.write(stream)

src.write_bytes(out.read_bytes())
