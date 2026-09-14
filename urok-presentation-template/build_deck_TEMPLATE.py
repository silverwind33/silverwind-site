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
  p { font-size: 33px; line-height: 1.45; font-weight: 300; color: rgba(255,255,255,0.97); margin-bottom: 18px; }
  p:last-child { margin-bottom: 0; }
  p b { color: #ffffff; font-weight: 600; }
  p.small { font-size: 26px; font-style: italic; color: rgba(255,255,255,0.82); }

  .bullets { list-style: none; margin: 4px 0 0; padding: 0; }
  .bullets li { position: relative; padding-left: 34px; font-size: 28px; line-height: 1.4;
    font-weight: 300; color: rgba(255,255,255,0.94); margin-bottom: 13px; }
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
  .points-page .bullets li { font-size: 32px; line-height: 1.5; margin-bottom: 30px; padding-left: 40px; }
  .points-page .bullets li::before { width: 12px; height: 12px; top: 12px; }
  .points-page .takeaway { margin-top: 40px; padding: 22px 28px; }
  .points-page .takeaway p { font-size: 27px; }
</style>
"""

def wrap(body_inner, page_no=None, total=None):
    pg = f'<div class="pagenum">{page_no:02d} / {total:02d}</div>' if page_no else ""
    return f"""<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<link rel="stylesheet" href="../fonts/local-fonts.css">
{STYLE}</head><body>{body_inner}{pg}<div class="grain"></div></body></html>"""

def bullets(items):
    return "<ul class='bullets'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def takeaway(text):
    return f'<div class="takeaway"><p>{text}</p></div>'

TOTAL = 12
slides = []

# 1 — title
slides.append(wrap(f"""
  <div class="hero-full"><img src="../img/01_hero_matrix.jpg"></div>
  <div class="hero-bottom">
    <h1 class="title" style="font-size:62px;">ПРИРОДА ФИЗИЧЕСКОЙ РЕАЛЬНОСТИ</h1>
  </div>
"""))

# 2 — Реальность — не источник
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text" style="flex:1;">
      <div class="label">Реальность — не источник</div>
      <p>Физическая реальность не объективна и не рождает саму себя. Это проекция, которую вы создаёте каждую секунду из своего состояния.</p>
      <p>Это как голограмма, декорации, которые идеально обслуживают ваше состояние сознания — и не существуют отдельно от вас.</p>
    </div>
  </div>
""", 2, TOTAL))

# 3 — Вы — не декорации (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Вы — не декорации</div>
    {bullets([
      "Физическая реальность — материализованная энергия, исходящая от вас",
      "Ничто не проявится в реальности, если у этого нет корня внутри вас",
      "У каждого — своя персональная симуляция",
    ])}
    {takeaway("Источник того, что вы наблюдаете, — не реальность, а вы.")}
  </div>
""", 3, TOTAL))

# 4 — Вы — проектор, не экран
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:44px;">Вы — проектор, не экран</div>
      <p>Представьте кинозал: на экране — фильм, рождённый из проектора. Вы отождествляете себя с фильмом и думаете, что источник — реальность. Но источник — проектор, а проектор это вы.</p>
      <p>Спецэффекты настолько убедительны, что вы вовлекаетесь, забываете о проекторе и создаёте один и тот же фильм снова и снова.</p>
    </div>
    <div class="imgwrap"><img src="../img/02_projector.jpg"></div>
  </div>
""", 4, TOTAL))

# 5 — Экран нельзя починить, стоя перед ним (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Экран нельзя починить, стоя перед ним</div>
    {bullets([
      "Менять реальность действием — то же самое, что бежать к экрану и кричать на героиню",
      "Следствие нельзя изменить следствием",
      "Нужно вернуться к проектору — внутрь себя",
    ])}
    {takeaway("Спросите себя честно: контроль и борьба хоть раз действительно меняли сценарий?")}
  </div>
""", 5, TOTAL))

# 6 — Ум — маленький ИИ (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Ум — маленький ИИ</div>
    <p style="font-size:30px; margin-bottom:32px;">Ум обучен на маленькой базе — вашем прошлом опыте. Если в базе не было опыта открытия бизнеса, ум будет пугать: это невозможно, это опасно.</p>
    {bullets([
      "Ум полезен для практических задач — таблиц, планов, расчётов",
      "Для новых сценариев он обычно бесполезен: выдаёт только страх из старых программ",
    ])}
    {takeaway("Зовите ум для Excel-таблицы, а не тогда, когда выбираете новый сценарий.")}
  </div>
""", 6, TOTAL))

# 7 — Всё уже существует одновременно
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:44px;">Всё уже существует одновременно</div>
      <p>Представьте миллион параллельных линий сценариев. Вы не создаёте их с нуля — вы резонируете и подключаетесь через состояние.</p>
      <p>У каждого — своя персональная симуляция, своя частота: люди в Монако не в курсе новостей, которые триггерят вас.</p>
    </div>
    <div class="imgwrap"><img src="../img/03_paths.jpg"></div>
  </div>
""", 7, TOTAL))

# 8 — Практика выбора сценария (points)
slides.append(wrap(f"""
  <div class="eyebrow">Конспект</div>
  <div class="points-page">
    <div class="label">Как выбрать сценарий</div>
    {bullets([
      "Чётко определите, чего хотите — не из нехватки «хоть бы что-нибудь», а из «мне доступно всё»",
      "Культивируйте нужное состояние картинкой, звуком, воображением — как кино перед сном",
      "Текущий и желаемый сценарий равноценны — это просто разные сериалы",
    ])}
    {takeaway("Внимание нужно вернуть с поверхности внутрь — именно там происходит сдвиг.")}
  </div>
""", 8, TOTAL))

# 9 — Задание intro
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="centered">
    <p>Две практики: сначала честно увидеть, что контроль не работал —<br>затем собрать внутри картинку того, что выбираете вместо него.</p>
    <div class="rule"></div>
  </div>
""", 9, TOTAL))

# 10 — Задание 1
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="split">
    <div class="text" style="flex:1;">
      <div class="label"><span class="num">1</span>Проверьте, что не работает</div>
      <p>Честно вспомните: когда вы пытались контролировать уже включённый сценарий силой или борьбой — это правда сработало?</p>
      {bullets([
        "Выпишите 2–3 ситуации, где контроль или борьба не дали результата",
        "Отметьте, что менялось только после смены состояния, а не действия",
      ])}
    </div>
  </div>
""", 10, TOTAL))

# 11 — Задание 2
slides.append(wrap(f"""
  <div class="eyebrow">Задание</div>
  <div class="split">
    <div class="text">
      <div class="label" style="font-size:46px;"><span class="num">2</span>Соберите картинку желаемого</div>
      <p>Опишите сценарий, который хотите проживать, — максимально ярко, как кадр из фильма.</p>
      {bullets([
        "Не из нехватки «хоть бы что-нибудь», а из «мне доступно всё»",
        "Выберите инструмент — фото, музыку, картинку",
        "Прокручивайте его перед сном, как киноленту",
      ])}
    </div>
  </div>
""", 11, TOTAL))

# 12 — closing
slides.append(wrap(f"""
  <div class="centered">
    <p>«Вы приходите не в готовый мир. Мир приходит из вас.»</p>
    <div class="rule"></div>
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
out_pdf = os.path.join(BASE, "Природа_реальности_презентация.pdf")
imgs[0].save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=imgs[1:])
print("saved", out_pdf, len(imgs), "pages")
