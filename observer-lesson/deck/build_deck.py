import os
import subprocess
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1600, 1000

STYLE = """
<style>
*{box-sizing:border-box;margin:0;padding:0}html,body{background:#0A0A0A}
body{font-family:'Inter',system-ui,sans-serif;color:#fff;width:1600px;height:1000px;position:relative;overflow:hidden}
.grain{position:absolute;inset:0;opacity:.045;pointer-events:none;z-index:10;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.eyebrow{position:absolute;top:55px;left:72px;z-index:4;font-family:'Unbounded';font-size:20px;letter-spacing:.14em;color:#B8C1C9;text-transform:uppercase}
.pagenum{position:absolute;top:55px;right:72px;z-index:4;font-family:'Unbounded';font-size:20px;letter-spacing:.1em;color:rgba(190,199,207,.62)}
.label{font-family:'Unbounded';font-size:50px;font-weight:500;line-height:1.18;color:#fff;margin-bottom:34px;letter-spacing:-.015em}
p{font-size:31px;line-height:1.55;font-weight:300;color:rgba(255,255,255,.96);margin-bottom:24px}
p b{font-weight:600;color:#fff}.small{font-size:27px;color:rgba(255,255,255,.82)}
.bullets{list-style:none;margin-top:4px}.bullets li{position:relative;padding-left:35px;font-size:31px;line-height:1.5;font-weight:300;color:rgba(255,255,255,.96);margin-bottom:22px}
.bullets li:before{content:'';position:absolute;left:0;top:14px;width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#A8B4BE,#E5E9EC)}
.bullets li b{font-weight:600;color:#fff}
.takeaway{margin-top:28px;padding:19px 25px;border-left:2px solid rgba(184,193,201,.72);background:rgba(184,193,201,.065);border-radius:0 8px 8px 0}
.takeaway p{font-size:30px;line-height:1.48;font-style:italic;margin:0;color:rgba(255,255,255,.96)}
.points{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:125px 120px 80px}
.points.compact .bullets li{font-size:29px;margin-bottom:16px;line-height:1.46}
.split{position:absolute;inset:0;display:flex;align-items:center;padding:135px 72px 70px;gap:62px}
.split .text{flex:1.18;min-width:0}.split .imgwrap{flex:.9;display:flex;align-items:center;justify-content:center}
.split .imgwrap img{width:100%;max-height:610px;object-fit:contain;display:block}
.hero{position:absolute;inset:0}.hero img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.86)}
.hero:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.1),rgba(10,10,10,.35) 48%,#0A0A0A 100%)}
.hero-title{position:absolute;z-index:3;left:72px;right:72px;bottom:60px}
.hero-title h1{font-family:'Unbounded';font-size:82px;font-weight:500;line-height:1.05;background:linear-gradient(135deg,#fff 0%,#AEB8C0 50%,#E7ECEF 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-title p{font-family:'Unbounded';font-size:21px;letter-spacing:.13em;text-transform:uppercase;color:#B8C1C9;margin:0 0 18px}
.center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px 150px}
.center .label{font-size:58px}.center p{max-width:1180px;font-size:34px;line-height:1.5}.rule{width:68px;height:2px;background:linear-gradient(90deg,#A8B4BE,#E5E9EC);margin:32px 0}
.numline{display:flex;align-items:flex-start;gap:20px}.num{width:58px;height:58px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#A8B4BE,#E5E9EC);color:#111820;font-family:'Unbounded';font-size:25px;margin-top:2px}
.steps{display:flex;flex-direction:column;gap:25px}.step{display:flex;align-items:flex-start;gap:22px}.step p{margin:4px 0 0;font-size:30px;line-height:1.45}
</style>
"""

def wrap(content, page=None, total=13):
    pn = f'<div class="pagenum">{page:02d} / {total:02d}</div>' if page else ''
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><link rel="stylesheet" href="../fonts/local-fonts.css">{STYLE}</head><body>{content}{pn}<div class="grain"></div></body></html>'''

def bullets(items):
    return '<ul class="bullets">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

def takeaway(text):
    return f'<div class="takeaway"><p>{text}</p></div>'

slides=[]
slides.append(wrap('''
<div class="hero"><img src="../assets/title_observer.jpg"></div>
<div class="hero-title"><p>Конспект урока</p><h1>НАБЛЮДАТЕЛЬ</h1></div>
'''))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="center">
<div class="label">Реальность создаётся<br>в момент наблюдения</div><div class="rule"></div>
<p>Вы выбираете из множества возможных событий и сценариев тот вариант, который соответствует вашему внутреннему наблюдению.</p>
</div>''',2))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="points">
<div class="label">Наблюдение = восприятие = внимание</div>
''' + bullets([
"Направить внимание — значит начать наблюдать и воспринимать определённым образом",
"Выбор и перевыбор идентичности — это смена наблюдения за собой",
"То, на что направлено внимание, становится выбранной версией вашей реальности",
]) + takeaway("Наблюдатель не просто смотрит на готовый мир — он выбирает, какая его версия проявится.") + '</div>',3))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="split"><div class="text">
<div class="label">До наблюдения существует всё</div>
<p>До восприятия событие, человек или объект находится в нейтрале: возможны разные исходы и разные грани.</p>
<p>Проявляется именно та сторона, которую вы выделяете своим вниманием.</p>
''' + takeaway("Ваше наблюдение определяет исход.") + '''</div>
<div class="imgwrap"><img src="../assets/reality.jpg"></div></div>''',4))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="points">
<div class="label">Внутренний наблюдатель выбирает проявление</div>
''' + bullets([
"Как вы воспринимаете <b>деньги</b> — так они проявляются в вашей материи",
"Как вы воспринимаете <b>реализацию и возможности</b> — такие варианты замечаете",
"Как вы воспринимаете <b>отношения и людей</b> — такие их грани высвечиваются",
"Как вы воспринимаете <b>себя</b> — такую идентичность отражает реальность",
]) + '</div>',5))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="split"><div class="text">
<div class="label">Ваша симуляция персональна</div>
<p>События, люди и процессы уже отразили ваше собственное наблюдение. Они проявились персонально для вас именно так, как вы их воспринимали.</p>
<p>Проекция не доказывает, что «мир такой». Она показывает, <b>как вы сейчас наблюдаете мир</b>.</p>
</div><div class="imgwrap"><img src="../assets/mirror.jpg"></div></div>''',6))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="points compact">
<div class="label">Ловушка объективной реальности</div>
''' + bullets([
"«Экономика упала, поэтому возможностей нет»",
"«Нормальных мужчин не осталось»",
"«Все люди ведут себя именно так»",
"«Мир снова доказал, что я была права»",
]) + takeaway("Когда вы считаете проекцию объективной, она укрепляет старое наблюдение и снова создаёт такую же проекцию.") + '</div>',7))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="points">
<div class="label">Реальность никогда вам не лжёт</div>
<p>Она показывает не абсолютную истину о мире, а вашу текущую выбранную правду — формочку сознания, в которой находится внимание.</p>
''' + bullets([
"Нет возможностей — вы наблюдаете их отсутствие",
"Повторяется один тип отношений — внимание закреплено на этой версии отношений",
"Мир постоянно подтверждает одно знание — наблюдатель продолжает выбирать его",
]) + takeaway("Смотря на исход, можно увидеть своё текущее наблюдение.") + '</div>',8))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="points">
<div class="label">Очки реальности</div>
<p>Фильтр восприятия работает как цветные очки: из множества людей, событий и возможностей вы замечаете только то, что совпадает с выбранным цветом.</p>
''' + bullets([
"Очки дефицита не позволяют увидеть доступные возможности",
"Очки недоверия выделяют людей, которые подтверждают недоверие",
"Новый фильтр не создаёт варианты из ничего — он делает заметным то, что уже существовало",
]) + '</div>',9))

slides.append(wrap('''
<div class="eyebrow">Конспект</div><div class="split"><div class="text">
<div class="label">Люди имеют множество граней</div>
<p>Вы никогда не знаете человека как одну окончательную форму. В нём одновременно существует множество вариантов проявления.</p>
<p>Ваше внимание подсвечивает ту грань, которую человек затем отражает в вашей персональной реальности.</p>
''' + takeaway("Поэтому один и тот же человек может вести себя с разными людьми совершенно по-разному.") + '''</div>
<div class="imgwrap"><img src="../assets/timeline.jpg"></div></div>''',10))

slides.append(wrap('''
<div class="eyebrow">Практика</div><div class="points">
<div class="label">Как изменить наблюдение</div><div class="steps">
<div class="step"><span class="num">1</span><p><b>Честно посмотрите на реальность.</b> Что она отражает в каждой сфере?</p></div>
<div class="step"><span class="num">2</span><p><b>Признайте персональность.</b> Это не объективный мир, а продолжение текущего восприятия.</p></div>
<div class="step"><span class="num">3</span><p><b>Считайте отражение.</b> Во что вы верите / как наблюдаете деньги, людей, себя и возможности, судя по идеальному отражению этого в реальности?</p></div>
</div></div>''',11))

slides.append(wrap('''
<div class="eyebrow">Практика</div><div class="points">
<div class="label">Закрепите новое наблюдение</div><div class="steps">
<div class="step"><span class="num">4</span><p><b>Поменяйте наблюдение.</b> Зная, что все правды сосуществуют, в новом дне продолжайте держать фокус, «вскармливая» новое наблюдение.</p></div>
<div class="step"><span class="num">5</span><p><b>Найдите подтверждения.</b> Найдите 3–5 примеров в физическом мире, которые подтвердят вам ваше новое выбранное наблюдение.</p></div>
</div></div>''',12))

slides.append(wrap('''
<div class="eyebrow">Задание</div><div class="points compact">
<div class="label">Проверьте своего наблюдателя</div>
''' + bullets([
"Что моя реальность показывает о том, как я наблюдаю <b>деньги и возможности</b>?",
"Как я наблюдаю <b>реализацию, отношения, людей и себя</b>?",
"Какую старую правду я продолжаю подтверждать внешними доказательствами?",
"Какой другой вариант уже существует, но раньше не попадал в моё внимание?",
"Что я выбираю наблюдать с этого момента? Какие подтверждения начну замечать?",
]) + takeaway("Честно отслеживайте внимание. Реальность персональна и неизбежно перестраивается под выбранное наблюдение.") + '</div>',13))

pngs=[]
for i,html in enumerate(slides,1):
    hp=os.path.join(BASE,f'slide{i}.html'); pp=os.path.join(BASE,f'slide{i}.png')
    with open(hp,'w',encoding='utf-8') as f:f.write(html)
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox','--hide-scrollbars',f'--window-size={W},{H}',f'--screenshot={pp}','--virtual-time-budget=3000',f'file://{hp}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    pngs.append(pp)

images=[Image.open(p).convert('RGB') for p in pngs]
out=os.path.join(BASE,'Наблюдатель_конспект.pdf')
images[0].save(out,'PDF',resolution=150.0,save_all=True,append_images=images[1:])
print(out)
