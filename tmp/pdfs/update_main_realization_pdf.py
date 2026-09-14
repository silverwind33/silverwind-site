from pathlib import Path

source = Path('/Users/alina/Desktop/Программы_реализации_конспект_с_вопросами.pdf')
target = Path('/Users/alina/Desktop/Программы_реализации_конспект.pdf')

target.write_bytes(source.read_bytes())
