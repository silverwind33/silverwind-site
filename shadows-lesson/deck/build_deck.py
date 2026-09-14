import os
import subprocess
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, TOTAL = 1600, 1000, 14

STYLE = r'''
<style>
@font-face{font-family:'Manrope';font-style:normal;font-weight:800;font-display:block;src:url('fonts/manrope-800.ttf') format('truetype')}
*{box-sizing:border-box;margin:0;padding:0}html,body{background:#0A0A0A}
body{font-family:'Inter',system-ui,sans-serif;color:#fff;width:1600px;height:1000px;position:relative;overflow:hidden}
.grain{position:absolute;inset:0;opacity:.045;pointer-events:none;z-index:10;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.eyebrow{position:absolute;top:55px;left:72px;z-index:4;font-family:'Unbounded';font-size:20px;letter-spacing:.14em;color:#B8C1C9;text-transform:uppercase}
.pagenum{position:absolute;top:55px;right:72px;z-index:4;font-family:'Unbounded';font-size:20px;letter-spacing:.1em;color:rgba(190,199,207,.62)}
.label{font-family:'Unbounded',sans-serif;font-size:40px;font-weight:700;line-height:1.25;color:#fff;margin-bottom:34px;letter-spacing:-.01em}
p{font-size:31px;line-height:1.55;font-weight:300;color:rgba(255,255,255,.96);margin-bottom:24px}
p b{font-weight:600;color:#fff}
.bullets{list-style:none;margin-top:4px}.bullets li{position:relative;padding-left:35px;font-size:30px;line-height:1.5;font-weight:300;color:rgba(255,255,255,.96);margin-bottom:20px}
.subq{display:flex;flex-direction:column;gap:8px;margin-top:14px}.subq span{font-size:26px;font-style:italic;color:rgba(255,255,255,.78);line-height:1.4}
.bullets li:before{content:'';position:absolute;left:0;top:14px;width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#A8B4BE,#E5E9EC)}
.bullets li b{font-weight:600;color:#fff}
.takeaway{margin-top:28px;padding:19px 25px;border-left:2px solid rgba(184,193,201,.72);background:rgba(184,193,201,.065);border-radius:0 8px 8px 0}
.takeaway p{font-size:29px;line-height:1.48;font-style:italic;margin:0;color:rgba(255,255,255,.96)}
.points{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:125px 120px 80px}
.points.compact .bullets li{font-size:28px;margin-bottom:15px;line-height:1.44}
.split{position:absolute;inset:0;display:flex;align-items:center;padding:135px 72px 70px;gap:62px}
.split .text{flex:1.16;min-width:0}.split .imgwrap{flex:.84;display:flex;align-items:center;justify-content:center}
.split .imgwrap img{width:100%;max-height:590px;object-fit:contain;display:block}
.hero{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding-bottom:110px}
.hero img{width:78%;height:62%;object-fit:contain;display:block;filter:brightness(.9)}
.hero:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.02),rgba(10,10,10,.18) 52%,#0A0A0A 100%)}
.hero-title{position:absolute;z-index:3;left:72px;right:72px;bottom:60px}
.hero-title h1{font-family:'Unbounded',sans-serif;font-size:78px;font-weight:700;line-height:1.08;color:#fff}
.hero-title p{font-family:'Unbounded';font-size:21px;letter-spacing:.13em;text-transform:uppercase;color:#B8C1C9;margin:0 0 18px}
.center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px 150px}
.center .label{font-size:56px}.center p{max-width:1190px;font-size:35px;line-height:1.5}.rule{width:68px;height:2px;background:linear-gradient(90deg,#A8B4BE,#E5E9EC);margin:32px 0}
.steps{display:flex;flex-direction:column;gap:24px}.step{display:flex;align-items:flex-start;gap:22px}.step p{margin:4px 0 0;font-size:29px;line-height:1.43}
.num{width:58px;height:58px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#A8B4BE,#E5E9EC);color:#111820;font-family:'Unbounded';font-size:25px;margin-top:2px}
.examples{display:grid;grid-template-columns:1fr 1fr;gap:24px 34px;margin-top:8px}.example{padding:22px 24px;border-left:2px solid rgba(184,193,201,.55);background:rgba(184,193,201,.05)}
.example h3{font-family:'Unbounded';font-size:24px;font-weight:500;color:#D8E0E5;margin-bottom:10px}.example p{font-size:26px;line-height:1.42;margin:0}
</style>'''

def wrap(content, page=None):
    pn = f'<div class="pagenum">{page:02d} / {TOTAL:02d}</div>' if page else ''
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/local-fonts.css">{STYLE}</head><body>{content}{pn}<div class="grain"></div></body></html>'

def bullets(items):
    return '<ul class="bullets">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

def takeaway(text):
    return f'<div class="takeaway"><p>{text}</p></div>'

slides=[]
slides.append(wrap('''<div class="hero"><img src="img/title_puzzle_matched.png"></div><div class="hero-title"><p>Конспект урока</p><h1>ТЕНИ</h1></div>'''))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="center"><div class="label">Тень — часть вас,<br>которую вы отвергли</div><div class="rule"></div><p>Она не исчезла. Она продолжает существовать внутри, но остаётся непризнанной и действует из-под тени.</p></div>''',2))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="points"><div class="label">Маска забирает энергию</div>''' + bullets([
"Чем больше вы живёте в согласии со своими истинными <b>«хочу»</b>, тем больше у вас энергии",
"Чем больше частей себя вы принимаете, тем меньше ресурса уходит на поддержание образа",
"Чтобы никто не увидел вытесненную грань, приходится постоянно контролировать себя и носить маску",
]) + takeaway("Принятие возвращает энергию, которая раньше уходила на сокрытие части себя.") + '</div>',3))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="split"><div class="text"><div class="label">В тени часто спрятан нужный ресурс</div><p>Именно отвергнутого качества может не хватать версии вас, которая уже проживает желаемый опыт.</p><p>Когда грань принята, вы легче перетекаете в нужную идентичность — без внутреннего саботажа и искажений.</p>''' + takeaway("Разные опыты требуют разных версий вас.") + '''</div><div class="imgwrap"><img src="img/diamond_matched.png"></div></div>''',4))

slides.append(wrap('''<div class="eyebrow">Примеры из урока</div><div class="points"><div class="label">Как вытесненная часть блокирует опыт</div><div class="examples"><div class="example"><h3>Реализация</h3><p>Без внутренней «плохой девочки» трудно говорить «нет», выдерживать недовольство и сохранять границы.</p></div><div class="example"><h3>Отношения</h3><p>Отвергая часть, которая легко принимает заботу, сложно позволить мужчине давать без чувства долга.</p></div><div class="example"><h3>Публичность</h3><p>Если нельзя быть «глупой» и ошибаться, масштабирование голоса будет вызывать стыд и саботаж.</p></div><div class="example"><h3>Ресурс</h3><p>Отвергая жёсткость и мужскую часть, сложнее действовать, брать ответственность и проявлять ресурсы.</p></div></div></div>''',5))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="points"><div class="label">Принять — не значит стать этой частью</div>''' + bullets([
"В вас одновременно существуют противоположные качества",
"Признать внутреннюю «содержанку» не значит полностью стать содержанкой",
"Признать «глупышку» — разрешить себе иногда не знать и ошибаться",
"Экологичная агрессия — это энергия наружу: заявить о желании, защитить границу, сказать «нет»",
]) + takeaway("Вы возвращаете себе доступ к качеству и сами выбираете, как его использовать.") + '</div>',6))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="split"><div class="text"><div class="label">Реакции на людей показывают ваши тени</div><p>Человек нейтрален. Но сильное раздражение, осуждение или стыд разворачиваются внутри вашего восприятия.</p><p>То, что особенно задевает в другом, часто является качеством, которое вы запретили себе.</p>''' + takeaway("Не исследуйте человека — исследуйте свою реакцию на него.") + '''</div><div class="imgwrap"><img src="img/projection_matched.png"></div></div>''',7))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="points compact"><div class="label">Как расшифровать триггер</div>''' + bullets([
"Раздражают женщины, которые легко получают? Возможно, вы запрещаете себе принимать без усилия",
"Бесит человек, который требует лучшего? Возможно, вы не разрешаете себе хотеть много",
"Злит чужое «нет»? Возможно, вы сами не позволяете себе отказывать",
"Страшно выглядеть неидеально? Возможно, любовь связана с обязанностью всегда быть «при параде»",
"Задевает чужая яркость? Возможно, вы блокируете право заявлять о себе",
]) + '</div>',8))

slides.append(wrap('''<div class="eyebrow">Практика</div><div class="points"><div class="label">Легализуйте вытесненную часть</div><div class="steps"><div class="step"><span class="num">1</span><p><b>Заметьте реакцию.</b> Что именно вас раздражает, пугает или заставляет осуждать?</p></div><div class="step"><span class="num">2</span><p><b>Назовите качество.</b> Какую грань человек сейчас проявляет?</p></div><div class="step"><span class="num">3</span><p><b>Верните её себе.</b> «Да, я тоже могу быть такой. Это тоже часть меня».</p></div><div class="step"><span class="num">4</span><p><b>Найдите ресурс.</b> Как это качество может служить вам экологично?</p></div></div></div>''',9))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="points"><div class="label">Прошлое не определяет настоящий момент, а создаётся из него</div>''' + bullets([
"Спросите: когда я впервые решила, что быть такой небезопасно или невыгодно?",
"Возможно, вы стали удобной, чтобы соответствовать семейной системе",
"Возможно, женственность, яркость или отказ когда-то были названы «плохими»",
"Смотрите на прошлое ради разотождествления, а не ради обвинения родителей или себя",
]) + takeaway("Главное можно сделать сейчас: осознать запрет и перевыбрать отношение к своей грани.") + '</div>',10))

slides.append(wrap('''<div class="eyebrow">Конспект</div><div class="split"><div class="text"><div class="label">Контакт с собой возвращает энергию</div><p>Следуйте не за модой, «надо» и чужими ответами, а за внутренним ощущением.</p><p>Ваше телесное «да» или «нет» помогает отличить своё от навязанного и плотнее соединяет вас с собой.</p>''' + takeaway("Ваша внутренняя правда важнее внешних правд.") + '''</div><div class="imgwrap"><img src="img/contact_matched.png"></div></div>''',11))

slides.append(wrap('''<div class="eyebrow">Задание</div><div class="points"><div class="label">Найдите свои тени</div>''' + bullets([
"В течение дня записывайте людей и ситуации, которые вызвали сильную реакцию",
"Что именно сделал человек? Какое качество вы ему приписали?",
"Где вы запрещаете себе быть такой же — получать, отказывать, требовать, ошибаться, проявляться?",
]) + '</div>',12))

slides.append(wrap('''<div class="eyebrow">Задание</div><div class="points"><div class="label">Верните себе эту грань</div>''' + bullets([
"Скажите: «Да, я тоже могу быть такой. Это часть меня»",
"Вспомните, когда и при каких обстоятельствах вы подавили эту грань в себе — осознайте, что это было не потому, что с гранью что-то не так, а потому что на вас смотрел человек, в призме восприятия которого эта грань тоже вытеснена.<div class='subq'><span>После чего / после какого события я решила, что такой быть нельзя?</span><span>Что тогда произошло?</span><span>В контакте с кем?</span></div>",
"Запишите, какой ресурс возвращает вам принятие этой грани",
]) + '</div>',13))

slides.append(wrap('''<div class="eyebrow">Задание</div><div class="points compact"><div class="label">Вечерняя практика</div>''' + bullets([
"Что сегодня мне действительно понравилось?",
"Что не понравилось — даже в мелочах: кружка, одежда, маршрут, разговор?",
"С кем мне было легко и наполненно? После кого стало меньше энергии?",
"Где я сказала «да», хотя тело отвечало «нет»?",
"Что я хочу повторить завтра, а что — перевыбрать?",
]) + takeaway("Главная правда — всегда у вас. Доверяйте себе, тем самым уплотняя контакт с собой.") + '</div>',14))

pngs=[]
for i,html in enumerate(slides,1):
    hp=os.path.join(BASE,f'slide{i}.html')
    pp=os.path.join(BASE,f'slide{i}.png')
    with open(hp,'w',encoding='utf-8') as f:
        f.write(html)
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox','--hide-scrollbars',f'--window-size={W},{H}',f'--screenshot={pp}','--virtual-time-budget=3000',f'file://{hp}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    pngs.append(pp)

images=[Image.open(p).convert('RGB') for p in pngs]
out=os.path.join(BASE,'Тени_конспект.pdf')
images[0].save(out,'PDF',resolution=150.0,save_all=True,append_images=images[1:])
print(out)
