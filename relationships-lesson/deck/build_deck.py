import subprocess, os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1600, 1000

STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #0A0A0A; }
  body {
    font-family: 'Inter', system-ui, sans-serif;
    color: #ffffff;
    width: 1600px; height: 1000px;
    position: relative; overflow: hidden;
  }
  .grain { position: absolute; inset: 0; opacity: 0.05; pointer-events: none; z-index: 5;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }

  .eyebrow { position: absolute; top: 56px; left: 72px; z-index: 3;
    font-family: 'Unbounded', sans-serif; font-size: 21px; letter-spacing: 0.14em;
    color: #A8B4BE; text-transform: uppercase; }
  .pagenum { position: absolute; top: 56px; right: 72px; z-index: 3;
    font-family: 'Unbounded', sans-serif; font-size: 21px; letter-spacing: 0.1em;
    color: rgba(168,180,190,0.6); }

  h1.title {
    font-family: 'Unbounded', sans-serif; font-weight: 500; font-size: 108px;
    letter-spacing: -0.01em; line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, #b8c4c8 50%, #dbe4e2 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .label {
    font-family: 'Unbounded', sans-serif; font-weight: 500; font-size: 52px;
    letter-spacing: -0.005em; color: #ffffff; margin-bottom: 32px; line-height: 1.2;
    display: flex; align-items: flex-start; gap: 20px;
  }
  .num {
    width: 60px; height: 60px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #A8B4BE 0%, #d0d8de 100%); color: #0e1318;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Unbounded', sans-serif; font-size: 26px; font-weight: 500;
    margin-top: 4px;
  }
  p { font-size: 33px; line-height: 1.7; font-weight: 300; color: rgba(255,255,255,0.97); margin-bottom: 38px; }
  p:last-child { margin-bottom: 0; }
  p b { color: #ffffff; font-weight: 600; }
  p.small { font-size: 26px; font-style: italic; color: rgba(255,255,255,0.82); }

  .bullets { list-style: none; margin: 4px 0 0; padding: 0; }
  .bullets li { position: relative; padding-left: 34px; font-size: 28px; line-height: 1.6;
    font-weight: 300; color: rgba(255,255,255,0.94); margin-bottom: 18px; }
  .bullets li::before { content: ''; position: absolute; left: 0; top: 12px; width: 10px; height: 10px;
    border-radius: 50%; background: linear-gradient(135deg, #A8B4BE, #d0d8de); }
  .bullets li b { color: #ffffff; font-weight: 600; }

  .takeaway { margin-top: 22px; padding: 16px 22px; border-left: 2px solid rgba(168,180,190,0.6);
    background: rgba(168,180,190,0.06); border-radius: 0 8px 8px 0; }
  .takeaway p { font-size: 24px; font-style: italic; color: rgba(255,255,255,0.95); margin: 0; }

  .split { position: absolute; inset: 0; display: flex; align-items: flex-start; padding: 150px 72px 70px; gap: 64px; }
  .split .text { flex: 1.25; min-width: 0; }
  .split .imgwrap { flex: 1; align-self: center; display: flex; align-items: center; justify-content: center; }
  .split .imgwrap img { width: 100%; max-height: 500px; object-fit: contain; border-radius: 14px; }

  .hero-full { position: absolute; inset: 0; }
  .hero-full img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; display: block; }
  .hero-full::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(10,10,10,0.05) 0%, rgba(10,10,10,0.45) 55%, #0A0A0A 100%); }
  .hero-bottom { position: absolute; left: 0; right: 0; bottom: 0; z-index: 2;
    display: flex; justify-content: space-between; align-items: flex-end; padding: 0 72px 64px; }
  .tag { font-family: 'Unbounded', sans-serif; font-size: 24px; letter-spacing: 0.12em;
    color: #A8B4BE; text-transform: uppercase; padding-bottom: 14px; white-space: nowrap; }

  .centered { position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; text-align: center; padding: 0 160px; }
  .centered p { font-size: 50px; line-height: 1.4; font-style: italic; font-weight: 300;
    color: rgba(255,255,255,0.92); }
  .rule { width: 64px; height: 2px; background: linear-gradient(90deg, #A8B4BE, #d0d8de); margin: 32px 0; }

  .agenda { position: absolute; inset: 0; display: flex; flex-direction: column;
    justify-content: center; padding: 0 100px; gap: 52px; }
  .agenda-item { display: flex; align-items: flex-start; gap: 30px; }
  .agenda-item .num { width: 64px; height: 64px; font-size: 28px; }
  .agenda-item .a-title { font-family: 'Unbounded', sans-serif; font-size: 43px; font-weight: 500;
    color: #ffffff; margin-bottom: 10px; }
  .agenda-item .a-desc { font-size: 27px; color: rgba(255,255,255,0.68); font-weight: 300; }

  .points-page { position: absolute; inset: 0; display: flex; flex-direction: column;
    justify-content: center; padding: 0 130px; }
  .points-page .label { margin-bottom: 46px; }
  .points-page .bullets li { font-size: 32px; line-height: 1.65; margin-bottom: 34px; padding-left: 40px; }
  .points-page .bullets li::before { width: 12px; height: 12px; top: 12px; }
  .points-page .takeaway { margin-top: 40px; padding: 22px 28px; }
  .points-page .takeaway p { font-size: 27px; }
  .points-page.tall { justify-content: flex-start; padding-top: 150px; }
  .points-page.tall .bullets li { margin-bottom: 20px; }
  .bullets.twocol { column-count: 2; column-gap: 56px; }
  .bullets.twocol li { font-size: 25px; line-height: 1.45; margin-bottom: 26px; padding-left: 30px;
    break-inside: avoid; }
  .bullets.twocol li::before { width: 9px; height: 9px; top: 9px; }
  .bullets.twocol.big li { font-size: 30px; line-height: 1.4; margin-bottom: 30px; padding-left: 34px; }
  .bullets.twocol.big li::before { width: 11px; height: 11px; top: 11px; }
  .bullets.twocol.big li b { color: #d0d8de; font-weight: 600; }
  .bullets.big:not(.twocol) li { font-size: 34px; line-height: 1.5; margin-bottom: 26px; padding-left: 40px; }
  .bullets.big:not(.twocol) li::before { width: 13px; height: 13px; top: 13px; }
</style>
"""

def wrap(body_inner, page_no=None, total=None):
    pg = f'<div class="pagenum">{page_no:02d} / {total:02d}</div>' if page_no else ""
    return f"""<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<link rel="stylesheet" href="../fonts/local-fonts.css">
{STYLE}</head><body>{body_inner}{pg}<div class="grain"></div></body></html>"""

def bullets(items, extra_class=""):
    cls = ("bullets " + extra_class).strip()
    return f"<ul class='{cls}'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def takeaway(text):
    return f'<div class="takeaway"><p>{text}</p></div>'

TOTAL = 12
slides = []

# 1 — title
slides.append(wrap(f"""
  <div class="hero-full"><img src="../img/03_solitaire.jpg"></div>
  <div class="hero-bottom">
    <h1 class="title" style="font-size:64px;">САМОЦЕННОСТЬ</h1>
  </div>
"""))

# 2 — Ценность — в вашей энергии
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Ценность — в вашей энергии</div>
    {bullets([
      "Уникальный способ пропускать через себя информацию, опыт, слова",
      "Вы — как бриллиант, второго такого не существует",
    ])}
    {takeaway("Ваша уникальная энергия — драгоценна уже сама по себе.")}
  </div>
""", 2, TOTAL))

# 3 — Больше контакта с собой — больше энергии (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Больше контакта с собой — больше энергии</div>
    <p style="font-size:28px; margin-bottom:30px;">Суть не в том, чтобы узнать «как правильно» и повторить за кем-то — вставать в 6, читать книгу в день, быть юристом, потому что это «круто».</p>
    {bullets([
      "Спросите себя: что мне нравится, как я хочу общаться, чем хочу заниматься?",
      "Чем больше вы в контакте с собой, тем более вы притягательны",
    ])}
    {takeaway("Внешний шум не покажет вам ваш бриллиант — только контакт с собой.")}
  </div>
""", 3, TOTAL))

# 4 — Удовольствие — маркер контакта с собой (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Удовольствие — маркер контакта с собой</div>
    {bullets([
      "Удовольствие — естественное состояние, когда вы в контакте со своими желаниями",
      "Страдание и дискомфорт — маркер того, что вы разъединились с собой и пошли за внешним",
      "«Все замуж — и я замуж», «все ведут блог — и я тоже» — не ваш путь, если это не откликается",
    ])}
  </div>
""", 4, TOTAL))

# 5 — Вы источник всего
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label">Вы источник всего</div>
      {bullets([
        "Вся ваша реальность создаётся из вас, как из источника",
        "Деньги, проекты, партнёры, работодатели — существуют благодаря вам",
        "Исчезнете вы — схлопнется весь этот мир целиком",
      ])}
      {takeaway("Ничего в этой реальности не может быть больше или выше вас.")}
    </div>
    <div class="imgwrap"><img src="../img/06_reality.jpg"></div>
  </div>
""", 5, TOTAL))

# 8 — Не измеряйте ценность опытами (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Не измеряйте ценность опытами</div>
    <p style="font-size:28px; margin-bottom:30px;">Это как стоять у холодильника и говорить себе: «Вот получу банан — тогда стану офигенной». Деньги, партнёр, признание — тоже просто банан.</p>
    {bullets([
      "Опыты — крупицы, которые происходят из вас, они меньше вас",
      "Суть не в доказательстве ценности, а в удовольствии от проживания опыта",
    ])}
    {takeaway("Проживая или не проживая опыт, ваша ценность не убавляется и не прибавляется.")}
  </div>
""", 6, TOTAL))

# 7 — Чужой объектив
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:44px;">Чужой объектив</div>
      {bullets([
        "Первое ощущение своей ценности формирует взгляд семейной системы",
        "Люди, которые не любят себя, видят в вас то же самое — через свою линзу",
        "Это никогда не было про вас — это всегда про них",
      ])}
      {takeaway("Отдайте им их очки. Вы изначально ценны — до и без их взгляда.")}
    </div>
    <div class="imgwrap"><img src="../img/05_lens.jpg"></div>
  </div>
""", 7, TOTAL))

# 10 — Задание 1: Ваша формула
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="points-page">
    <div class="label"><span class="num">1</span>Ваша формула</div>
    {bullets([
      "Честно закончите: «Чтобы получить любовь и признание, мне нужно ___»",
      "Заметьте, если там «быть удобной», «идеальной», «полезной»",
      "Перепишите на: «Мне нужно быть максимально в контакте с собой»",
    ])}
  </div>
""", 8, TOTAL))

# 11 — Задание 2: Найдите своего человека, которому вас отдали
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="points-page">
    <div class="label"><span class="num">2</span>Отдайте чужие очки</div>
    {bullets([
      "Вспомните, кто в семье смотрел на вас искажённо — обесценивал, сравнивал, критиковал",
      "Спросите себя: это правда было про меня, или про то, как этот человек видел себя?",
      "Мысленно верните эту линзу — она никогда вам не принадлежала",
    ])}
    {takeaway("Вы бриллиант независимо от того, в чьих глазах когда-то не блестели.")}
  </div>
""", 9, TOTAL))

# Final deck for the lesson “Отношения”. The inherited slide definitions above
# are intentionally replaced here while retaining the shared design system.
slides = []

# 1 — title
slides.append(wrap(f"""
  <div class="hero-full"><img src="../img/01_title.jpg" style="object-position:50% 30%;"></div>
  <div class="hero-bottom">
    <h1 class="title" style="font-size:82px;">ОТНОШЕНИЯ</h1>
  </div>
"""))

# 2 — relationships are a scenario
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Отношения — это сценарий</div>
    {bullets([
      "Отношения — такая же декорация реальности, как деньги или реализация",
      "Они рождаются из вас как из источника и обслуживают ваше внутреннее состояние",
      "Формат отношений отражает знания о себе, людях, партнёрстве и близости",
    ])}
    {takeaway("Вы можете создать любой формат отношений, который действительно хотите прожить.")}
  </div>
""", 2, TOTAL))

# 3 — projection
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:44px;">Реальность отражает внутреннее</div>
      {bullets([
        "То, что происходит сейчас, — точное отражение внутренних представлений",
        "Если сфера отношений удивляет или ранит, часть знаний действует неосознанно",
        "Внешняя ситуация — уже следствие, тень того, что направлено изнутри",
      ])}
    </div>
    <div class="imgwrap"><img src="../img/02_broken.jpg"></div>
  </div>
""", 3, TOTAL))

# 4 — nothing is fixed
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Внутреннее не зафиксировано</div>
    {bullets([
      "Ваши знания об отношениях — не неизменная истина и не ваша сущность",
      "Это то, на что когда-то было направлено внимание — осознанно или нет",
      "Меняется отождествление — вслед за ним меняется отражение в физическом мире",
    ])}
    {takeaway("Вы — проектор и источник сценария, а не только персонаж внутри него.")}
  </div>
""", 4, TOTAL))

# 5 — choose a relationship area
slides.append(wrap(f"""
  <div class="eyebrow">Практика</div>
  <div class="points-page">
    <div class="label"><span class="num">1</span>Выберите область отношений</div>
    <p style="font-size:30px;margin-bottom:32px;">Возьмите одну группу людей, с которой хотите глубже разобраться прямо сейчас:</p>
    {bullets([
      "мужчины или романтические партнёры",
      "подруги, женщины или коллеги",
      "работодатели, клиенты или партнёры по работе",
      "родители, дети или другие близкие",
    ], "twocol big")}
    {takeaway("Пишите или надиктовывайте честно — этот материал остаётся только между вами и листом или диктофоном.")}
  </div>
""", 5, TOTAL))

# 6 — what are relationships
slides.append(wrap(f"""
  <div class="eyebrow">Практика</div>
  <div class="points-page tall">
    <div class="label"><span class="num">2</span>Что вы знаете об отношениях?</div>
    {bullets([
      "Что такое отношения именно с выбранной группой?",
      "Какими они бывают чаще всего?",
      "Как они обычно складываются?",
      "Что в них регулярно происходит?",
      "Что для них характерно?",
      "Какие истории вы обычно рассказываете об этой сфере?",
    ], "twocol big")}
    {takeaway("Не пишите «как правильно». Вспомните, что вы реально обсуждали с близкими в последний раз.")}
  </div>
""", 6, TOTAL))

# 7 — image of the group
slides.append(wrap(f"""
  <div class="eyebrow">Практика</div>
  <div class="points-page tall">
    <div class="label"><span class="num">3</span>Какой образ этой группы живёт в вас?</div>
    {bullets([
      "Кто эти люди в вашем внутреннем представлении?",
      "Какие они чаще всего?",
      "Как они обычно проявляются — и как не проявляются?",
      "Можно ли им доверять?",
      "Что вы ожидаете от них заранее?",
      "Совпадает ли написанное с тем, что показывает ваша реальность?",
    ], "twocol big")}
    {takeaway("Реальность — маркер честности. Если написанное ей противоречит, где-то вы даёте социально правильный ответ.")}
  </div>
""", 7, TOTAL))

# 8 — who are you inside these relationships
slides.append(wrap(f"""
  <div class="eyebrow">Практика</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:42px;"><span class="num">4</span>Кто вы внутри этих отношений?</div>
      {bullets([
        "Какая вы в контакте с этими людьми?",
        "Какой подругой, партнёром, коллегой или дочерью вы себя знаете?",
        "Как, по вашему ощущению, они воспринимают вас?",
        "Какой вы становитесь рядом с ними — свободной, напряжённой, желанной, незаметной?",
      ])}
    </div>
    <div class="imgwrap"><img src="../img/03_mirror.jpg"></div>
  </div>
""", 8, TOTAL))

# 9 — long-term relationships
slides.append(wrap(f"""
  <div class="eyebrow">Практика</div>
  <div class="points-page">
    <div class="label">Что вы знаете о серьёзных отношениях?</div>
    {bullets([
      "Могут ли отношения длиться долго и оставаться близкими?",
      "Обязательно ли любовь превращается в труд и преодоление?",
      "Возможен ли долгий союз без измен и тяжёлых конфликтов?",
      "Что, по вашему знанию, неизбежно происходит с парой со временем?",
    ])}
    {takeaway("Зафиксируйте не идеальный ответ, а те правила, по которым ваша реальность уже собирает отношения.")}
  </div>
""", 9, TOTAL))

# 10 — three mirrors
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:43px;">Три зеркала отношения к себе</div>
      {bullets([
        "Как вы разговариваете с собой и поддерживаете себя",
        "Из какого состояния вы относитесь к другим: любовь, щедрость, зависть, агрессия",
        "Как близкие, партнёры и окружающие относятся к вам",
      ])}
      {takeaway("Себя можно убедить словами. Реальность показывает фактическое отношение к себе без самообмана.")}
    </div>
    <div class="imgwrap"><img src="../img/04_lens.jpg"></div>
  </div>
""", 10, TOTAL))

# 11 — honesty
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="points-page">
    <div class="label"><span class="num">5</span>Наблюдайте себя несколько дней</div>
    {bullets([
      "Как вы обращаетесь к себе после ошибок?",
      "Ставите ли себя в приоритет — или отдаёте себе только остатки?",
      "Что вы делаете сначала: для себя или всегда для других?",
      "Какое отношение к вам возвращают люди?",
    ])}
    {takeaway("Вход в трансформацию происходит через честность: увидеть паттерн — значит получить возможность его изменить.")}
  </div>
""", 11, TOTAL))

# 12 — choose a new form
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:43px;"><span class="num">6</span>Перевыберите форму</div>
      {bullets([
        "Осознайте: выписанные знания — сырьё сценария, но это не вы",
        "Опишите версию себя, которая желанна и ценна в отношениях",
        "Как она себя чувствует, ощущает и ведёт?",
        "Как к ней относятся партнёры, друзья, коллеги и близкие?",
        "Отождествитесь с тем, что теперь хотите познать",
      ])}
      {takeaway("Меняется то, с чем вы себя отождествляете, — меняется и ответ реальности.")}
    </div>
    <div class="imgwrap"><img src="../img/05_reality.jpg"></div>
  </div>
""", 12, TOTAL))

png_paths = []
for i, html in enumerate(slides, start=1):
    hpath = os.path.join(BASE, f"slide{i}.html")
    ppath = os.path.join(BASE, f"slide{i}.png")
    with open(hpath, "w") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                     f"--window-size={W},{H}", f"--screenshot={ppath}",
                     "--virtual-time-budget=3000", f"file://{hpath}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png_paths.append(ppath)
    print("rendered", ppath)

imgs = [Image.open(p).convert("RGB") for p in png_paths]
out_pdf = os.path.join(BASE, "Отношения_презентация.pdf")
imgs[0].save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=imgs[1:])
print("saved", out_pdf, len(imgs), "pages")
