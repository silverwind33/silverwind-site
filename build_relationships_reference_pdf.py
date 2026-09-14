from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import os, textwrap

OUT = "/Users/alina/Downloads/Конспект урока - Отношения - сценарий.pdf"
W, H = 768, 480
M = 58

pdfmetrics.registerFont(TTFont("Mont", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("MontBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("MontExtra", "/System/Library/Fonts/Supplemental/Arial Black.ttf"))
pdfmetrics.registerFont(TTFont("MontItalic", "/System/Library/Fonts/Supplemental/Arial Italic.ttf"))

BG = HexColor("#101112")
PANEL = HexColor("#181A1B")
WHITE = HexColor("#F4F4F2")
TEXT = HexColor("#D8D8D5")
MUTED = HexColor("#8D9298")
ACCENT = HexColor("#C7D0D8")
LINE = HexColor("#34383C")

c = canvas.Canvas(OUT, pagesize=(W,H))

def bg():
    c.setFillColor(BG); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(Color(1,1,1,alpha=.018)); c.circle(640,390,240,stroke=0,fill=1)

def label(page, total, kind="КОНСПЕКТ"):
    c.setFillColor(MUTED); c.setFont("MontBold", 10)
    c.drawString(M, H-38, kind)
    c.drawRightString(W-M, H-38, f"{page:02d} / {total:02d}")

def wrap(text, font, size, width):
    words = text.split()
    lines=[]; cur=""
    for w in words:
        test = w if not cur else cur+" "+w
        if pdfmetrics.stringWidth(test,font,size) <= width:
            cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def title(text, y=390, size=25):
    c.setFillColor(WHITE); c.setFont("MontExtra", size)
    lines=wrap(text,"MontExtra",size,W-2*M)
    for line in lines:
        c.drawString(M,y,line); y-=size*1.18
    return y

def body(text,y,size=14,width=None,font="Mont",leading=None,color=TEXT):
    width=width or W-2*M; leading=leading or size*1.55
    c.setFillColor(color); c.setFont(font,size)
    for line in wrap(text,font,size,width):
        c.drawString(M,y,line); y-=leading
    return y

def bullets(items,y,size=14,gap=12):
    for item in items:
        lines=wrap(item,"Mont",size,W-2*M-32)
        c.setFillColor(ACCENT); c.circle(M+5,y+4,2.5,stroke=0,fill=1)
        c.setFillColor(TEXT); c.setFont("Mont",size)
        for line in lines:
            c.drawString(M+26,y,line); y-=size*1.48
        y-=gap
    return y

def callout(text,y,h=None):
    lines=wrap(text,"MontItalic",13,W-2*M-34)
    h=h or 32+len(lines)*21
    c.setFillColor(PANEL); c.roundRect(M,y-h,W-2*M,h,6,stroke=0,fill=1)
    c.setStrokeColor(ACCENT); c.setLineWidth(1); c.line(M,y-h,M,y)
    c.setFillColor(WHITE); c.setFont("MontItalic",13)
    ty=y-25
    for line in lines:
        c.drawString(M+18,ty,line); ty-=21
    return y-h

def card(num, heading, text, y, h=82):
    c.setFillColor(PANEL); c.setStrokeColor(LINE); c.roundRect(M,y-h,W-2*M,h,7,stroke=1,fill=1)
    c.setFillColor(ACCENT); c.circle(M+25,y-25,12,stroke=0,fill=1)
    c.setFillColor(BG); c.setFont("MontBold",10); c.drawCentredString(M+25,y-29,str(num))
    c.setFillColor(WHITE); c.setFont("MontBold",13); c.drawString(M+48,y-24,heading)
    c.setFillColor(TEXT); c.setFont("Mont",11.5)
    ty=y-46
    for line in wrap(text,"Mont",11.5,W-2*M-70):
        c.drawString(M+48,ty,line); ty-=17
    return y-h-10

slides = []

def slide_cover(page,total):
    cover="/tmp/relationships_ref/page-01.jpg"
    if os.path.exists(cover): c.drawImage(cover,0,0,W,H,mask='auto')
    else:
        bg(); c.setFillColor(WHITE); c.setFont("MontExtra",35); c.drawCentredString(W/2,150,"ОТНОШЕНИЯ")
    c.showPage()

def slide(page,total,kind,heading,draw):
    bg(); label(page,total,kind); y=title(heading)
    draw(y); c.showPage()

TOTAL=16
slide_cover(1,TOTAL)

slide(2,TOTAL,"КОНСПЕКТ","Отношения - сценарий, рождённый из вас",lambda y: bullets([
    "Любые отношения во внешнем мире - такая же декорация, как реализация или деньги: они рождаются из вас как из источника.",
    "Они обслуживают ваше состояние и ваши знания о мире, людях, себе, любви и близости.",
],y-8,14))

slide(3,TOTAL,"КЛЮЧЕВАЯ МЫСЛЬ","Реальность - тень, а не источник",lambda y: callout(
    "Отношения в реальности похожи на фильм, который проектор высвечивает на стену. Фильм - уже следствие. Проектор - вы и то, куда направлено ваше внимание.",y-20))

slide(4,TOTAL,"НОВОЕ НАБЛЮДЕНИЕ","Сценарий не зафиксирован",lambda y: (
    body("То, что сейчас проявлено в отношениях, не является окончательной правдой о вас или о людях.",y-8,15),
    callout("Это форма знания, которую можно увидеть, перестать считать собой и заменить осознанно выбранным наблюдением.",y-105)
))

def practice1(y):
    y=card(1,"Отношения - это?","Выберите одну группу людей и выпишите всё, что вы знаете об отношениях с ней.",y-5)
    y=card(2,"Какие эти люди?","Как они обычно поступают? Чего от них можно ожидать? Что вы говорите о них близким?",y)
    card(3,"Кто вы рядом с ними?","Какая вы в этом контакте? Как вас воспринимают? Какое место вам обычно достаётся?",y)
slide(5,TOTAL,"ПРАКТИКА","Пять вопросов к своему сценарию",practice1)

def practice2(y):
    y=card(4,"Что вы знаете о долгих отношениях?","Они могут быть спокойными или обязательно требуют труда, боли, измен и преодоления?",y-5,86)
    card(5,"Как вы относитесь к себе?","Как вы с собой разговариваете? Кто в приоритете: вы или сначала все остальные?",y,86)
slide(6,TOTAL,"ПРАКТИКА","Разберите отношения - продолжение",practice2)

slide(7,TOTAL,"НАБЛЮДЕНИЕ","Отношение к себе - три среза",lambda y: bullets([
    "Как вы разговариваете с собой внутри: поддерживаете или наказываете.",
    "Как вы относитесь к другим: из любви, зависти, агрессии, долга или жертвы.",
    "Как другие относятся к вам: какое место дают, как выбирают и как с вами обращаются.",
],y-8,14,14))

slide(8,TOTAL,"ЧЕСТНОСТЬ","Смотрите не на правильный ответ, а на живой",lambda y: (
    body("Вспомните недавние разговоры о мужчинах, женщинах, клиентах или подругах. Именно спонтанные формулировки показывают знание, через которое вы смотрите.",y-8,14),
    callout("Вход в трансформацию происходит через честность: пока программа не замечена, менять нечего.",y-120)
))

slide(9,TOTAL,"РАЗОТОЖДЕСТВЛЕНИЕ","Программа - не вы",lambda y: bullets([
    "Спросите: кто мне это сказал? А ему кто сказал?",
    "Увидьте: деструктивное знание могло быть передано вам, но вы не выбирали его осознанно.",
    "Перестаньте считать унаследованную формочку собственной природой.",
],y-10,14,17))

slide(10,TOTAL,"ПЕРЕПРОШИВКА","Старый чемодан - новый чемодан",lambda y: (
    body("Старые деструктивные знания можно символически сложить в чемодан и отпустить. Новый чемодан заполняется тем, что вы выбираете видеть теперь.",y-5,14),
    callout("Новая программа сильна не потому, что она позитивная, а потому, что впервые выбрана вами осознанно.",y-125)
))

slide(11,TOTAL,"ПРОГРАММА 01","Условная ценность",lambda y: (
    bullets(["Я начну ценить себя, когда стану богатой, красивой, реализованной или любимой.","Внешний опыт становится условием права на любовь и уважение к себе."],y-8,14,13),
    callout("Новое наблюдение: моя ценность существует до денег, отношений, тела и результатов.",y-190)
))

slide(12,TOTAL,"ПРОГРАММА 02","Самонаказание",lambda y: (
    bullets(["Пока условие ценности не выполнено, человек оскорбляет себя, лишает заботы и считает недостойным хорошего отношения.","Самонаказание - следствие попытки заслужить собственную ценность."],y-8,14,13),
    callout("Результат не создаёт мою ценность. Опыт рождается из точки, из которой я уже существую и выбираю.",y-190)
))

slide(13,TOTAL,"ПРОГРАММА 03","Любовь равна жертве",lambda y: (
    bullets(["Нужно быть удобной, чтобы получить любовь.","Чужой комфорт и чужие потребности ставятся выше собственного присутствия."],y-8,14,16),
    callout("Мне не нужно уменьшать себя, чтобы быть источником любви. Другой человек не является условием моей ценности.",y-175)
))

slide(14,TOTAL,"НОВАЯ ИЕРАРХИЯ","Я существую раньше любого опыта",lambda y: (
    body("Деньги, отношения, тело, реализация и признание могут быть желаниями, но не могут стать мерой вашей ценности.",y-8,15),
    callout("Не я завишу от опыта как от источника своей ценности - опыт зависит от моего присутствия и внимания.",y-118)
))

slide(15,TOTAL,"ЗАДАНИЕ","Алгоритм переписывания",lambda y: bullets([
    "Выберите одну сферу и выгрузите все знания о ней.",
    "Найдите, кем вы считаете себя внутри этого сценария.",
    "Определите, откуда пришли деструктивные программы.",
    "Разотождествитесь с тем, что не выбирали осознанно.",
    "Сформулируйте новое наблюдение и начните относиться к себе из него.",
],y-10,12.5,9))

slide(16,TOTAL,"ЯДРО УРОКА","То, что вы выбираете теперь",lambda y: (
    callout("Отношения - проявленный сценарий моих внутренних знаний. Переданное мне убеждение - не обязательно моё. Я могу выбрать новую точку наблюдения.",y-15),
    body("Моя ценность не создаётся опытом. Я существую раньше любого результата.",y-180,16,font="MontBold",color=WHITE)
))

c.save()
print(OUT)
