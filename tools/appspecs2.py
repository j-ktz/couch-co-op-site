"""App specs, part two: Tabbed (electrician and plumber, one app), Fantasy Queens, Sitout."""
import re
import landing
from hub import fill

C = landing.C
NAVY, WHITE = "#0B1A4A", "#FFFFFF"


def faq(slug):
    return [(q, landing.esc(a)) for q, a in C[slug]["faq"]]


# ---------------------------------------------------------------- Tabbed (one app, two trades)
TABBED_CSS = r'''
.dplay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:64px;align-items:center}
.drill{background:#fff;border-radius:30px;padding:26px;box-shadow:0 0 0 1px var(--line),0 50px 90px -46px rgba(11,31,68,.55)}
.dTop{display:flex;justify-content:space-between;font-weight:700;color:var(--soft);font-size:.9rem}
.dTimer{font-variant-numeric:tabular-nums;color:var(--ink)}
.dBar{height:7px;border-radius:99px;background:var(--bg2);margin:12px 0 18px;overflow:hidden}
.dBar i{display:block;height:100%;background:var(--a2);transform-origin:left}
.dQ{font:700 1.18rem/1.45 var(--body);margin:0 0 16px}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.opt{display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:16px;border:2px solid var(--line);background:#fff;font:600 1rem var(--body);color:var(--ink);cursor:pointer;text-align:left;transition:border-color .2s,transform .2s cubic-bezier(.3,1.6,.4,1)}
.opt b{display:grid;place-items:center;width:30px;height:30px;border-radius:9px;background:var(--bg2);flex:none}
.opt:hover:not(:disabled){border-color:var(--a);transform:translateY(-2px)}
.opt:disabled{cursor:default}
.opt.ok{border-color:#1A8F52;background:#E3F7EC}.opt.ok b{background:#1A8F52;color:#fff}
.opt.no{border-color:#D63E2F;background:#FDE8E5}.opt.no b{background:#D63E2F;color:#fff}
.reveal{display:none;margin-top:16px;padding:16px 18px;border-radius:18px;background:var(--bg)}
.reveal.on{display:block;animation:rin .45s cubic-bezier(.2,.8,.2,1)}
@keyframes rin{from{opacity:0;transform:translateY(10px)}}
.reveal strong{display:block;margin-bottom:10px}
.reveal .chip{display:inline-block;font:800 .95rem var(--disp);padding:5px 12px;border-radius:9px;background:var(--a2);color:#0B1A4A}
.find{margin:10px 0 12px;color:var(--soft)}
.again{border:0;border-radius:99px;padding:10px 18px;background:var(--af);color:var(--ai);font:700 .92rem var(--body);cursor:pointer}
.dNote{font-size:.82rem;color:var(--soft);margin:14px 0 0}
.clock{display:inline-flex;align-items:center;gap:16px;margin-top:8px;padding:14px 20px 14px 14px;border-radius:22px;background:#fff;box-shadow:0 0 0 1px var(--line)}
.clock b{font:800 2.4rem/1 var(--disp);letter-spacing:-.04em;padding:10px 14px;border-radius:14px;background:var(--a2);color:#0B1A4A;font-variant-numeric:tabular-nums}
.calc{display:grid;gap:8px;margin-top:8px;max-width:30em}
.calc div{display:grid;grid-template-columns:90px minmax(0,1fr);gap:12px;align-items:baseline;padding:12px 16px;border-radius:16px;background:#fff;box-shadow:0 0 0 1px var(--line)}
.calc span{font-size:.82rem;font-weight:700;color:var(--soft)}
.calc b{font-variant-numeric:tabular-nums}
.calc div:nth-last-child(-n+2){background:color-mix(in srgb,var(--a) 14%,#fff)}
.g18{display:grid;grid-template-columns:repeat(6,44px);gap:8px;margin:8px 0 14px}
.g18 i{display:grid;place-items:center;height:44px;border-radius:12px;background:#fff;box-shadow:0 0 0 1px var(--line);font-style:normal;font-weight:700;font-size:.9rem}
.g18 i.ans{background:var(--af);color:var(--ai);box-shadow:none}
.g18 i.flag{box-shadow:inset 0 0 0 3px #FF8A1F}
.g18 i.cur{outline:2.5px solid var(--ink);outline-offset:2px}
@media(max-width:960px){.dplay{grid-template-columns:minmax(0,1fr);gap:36px}}
@media(max-width:560px){.opts{grid-template-columns:1fr}.g18{grid-template-columns:repeat(6,1fr)}}
'''


TABBED_CSS += r"""
.trades{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px}
.trade{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);padding:8px 18px 8px 8px;border-radius:99px;background:var(--card);box-shadow:0 0 0 1.5px color-mix(in srgb,var(--t) 60%,transparent),0 14px 28px -18px var(--t);font-weight:800;transition:transform .2s cubic-bezier(.3,1.6,.4,1)}
.trade i{display:grid;place-items:center;width:34px;height:34px;border-radius:11px;background:var(--t);color:#fff;flex:none}
.trade small{font-weight:600;color:var(--soft);font-size:.85rem}
.trade:hover{transform:translateY(-2px)}
.thead{max-width:44em}
.kicker{display:inline-flex;align-items:center;gap:8px;font:800 .78rem/1 var(--body);letter-spacing:.08em;text-transform:uppercase;padding:8px 13px 8px 9px;border-radius:99px;background:var(--af);color:var(--ai);margin:0 0 18px}
.kicker svg{width:16px;height:16px}
.trade-sec{background:var(--bg)}
.trade-sec+.trade-sec{border-top:0;padding-top:0}
.trade-sec .dplay{margin-top:40px}
.dplay .sth{font:800 clamp(1.6rem,3vw,2.3rem)/1.05 var(--disp);letter-spacing:-.035em;margin:0 0 14px}
@media(max-width:960px){.trades{justify-content:center}.thead{margin:0 auto;text-align:center}}
"""

BOLT = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12z"/></svg>'
DROP = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6.5 6.6 6.5 11.2a6.5 6.5 0 0 1-13 0C5.5 9.6 12 3 12 3z"/></svg>'

# Electrician keeps Tabbed blue (the page's own accent). Plumber gets the copper from the plumber
# brand (PlumberPrep branch claude/copper-accent, AccentColor 0x9A5B26) on a warm tint.
EL_A, PL_A = "#0A84FF", "#9A5B26"
PL_VARS = f"--a:{PL_A};--af:{fill(PL_A, WHITE)};--ai:{WHITE};--a2:#FFC233;--a3:#3E7BFA;--bg:#F8F0E8;--bg2:#F0E1D2"


def _g18(word):
    out = ""
    for n in range(1, 19):
        cls = "ans" if n in (1, 2, 3, 5, 6, 7, 8, 9, 10) else ""
        if n in (4, 11):
            cls = (cls + " flag").strip()
        if n == 12:
            cls = "cur"
        out += f'<i class="{cls}">{n}</i>'
    return (f'<div class="g18" aria-hidden="true">{out}</div>'
            f'<p style="font-size:.95rem">{word} is answered. The orange edge is flagged. The outline is where you are.</p>')


def trade(t):
    """One trade's part of the Tabbed page: a heading, a lookup drill and four stories."""
    k = t["key"]
    style = f' style="{t["vars"]}"' if t.get("vars") else ""
    opts = "".join(f'<button class="opt" type="button" data-k="{x}"><b>{x.upper()}</b>{v}</button>' for x, v in zip("abcd", t["opts"]))
    intro = (f'<section class="sec trade-sec" id="{t["id"]}"{style}><div class="wrap">'
             f'<div class="thead"><span class="kicker">{t["icon"]}{t["label"]}</span><h2>{t["h"]}</h2><p class="sub" style="margin-bottom:0">{t["sub"]}</p></div>'
             '<div class="dplay">'
             '<div><h3 class="sth">Try a lookup.</h3><p class="sub" style="margin:0">A timed lookup drill, the way the app runs them. Pick an answer and see where it lives in the book.</p></div>'
             f'<div class="drill" data-ok="{t["ok"]}" data-good="{landing.esc(t["good"])}" data-bad="{landing.esc(t["bad"])}">'
             '<div class="dTop"><span>Lookup drill, question 3 of 10</span><span class="dTimer">0:00</span></div>'
             '<div class="dBar"><i></i></div>'
             f'<p class="dQ">{t["q"]}</p><div class="opts">{opts}</div>'
             f'<div class="reveal" aria-live="polite"><strong class="verdict"></strong><span class="chip">{t["sec"]}</span><p class="find"><b>Find it:</b> {t["find"]}</p><button class="again" type="button">Try another look</button></div>'
             f'<p class="dNote">A sample question. Tabbed\'s {t["bank"]} bank cites the section for every answer.</p>'
             '</div></div></div></section>')
    calc = '<div class="calc">' + "".join(f"<div><span>{a}</span><b>{b}</b></div>" for a, b in t["calc"]) + "</div>"
    img = lambda f: f'{t["img"]}{f}'
    stories = ("stories", dict(cls="trade-sec", style=t.get("vars"), items=[
       dict(id=f"{k}-answers", h="Answers you can check.", p=[t["answers_p"]],
            bullets=["<b>Your answer, marked.</b> Right or wrong, you see why.", "<b>Find it.</b> Exactly where to look in your book.", "<b>The code section.</b> Cited on every answer.", "<b>Report a problem.</b> Flag a question from the answer screen."],
            screens=[img("answer.jpg")], alt=f"{t['label']} practice question with the explanation, the code section it cites and a Find it hint"),
       dict(id=f"{k}-find", h="Find it in the book, fast.", html=f'<p>{t["find_p"]}</p><div class="clock"><b>0:41</b><span>That\'s how long you get. Beat it.</span></div>',
            screens=[img("lookup.jpg")], alt=f"A timed {t['bank']} lookup drill with a countdown"),
       dict(id=f"{k}-calcs", h="Calcs, one step at a time.", html=f'<p>{t["calc_p"]}</p>{calc}', screens=[img("calc.jpg")], alt=f"A {t['bank']} calculation with the full working shown"),
       dict(id=f"{k}-exam", h="Your exam, your format.", html=f'<p>{t["exam_p"]}</p>{_g18(t["answered"])}<p style="font-size:.95rem">A readiness estimate by topic shows your weak spots. It\'s an estimate from your practice, not a prediction of your result.</p>',
            screens=[img(f) for f in t["exam_screens"]], alt=f"Timed {t['bank']} practice exam with a question navigator"),
    ]))
    return [("raw", intro), stories]


ELECTRICIAN = dict(
 key="el", id="electrician", label="Electrician", icon=BOLT, bank="electrical", img="", answered="Blue",
 h="For electricians.", sub="The National Electrical Code, 2023 and 2026 editions. Set up for your state, and practice exams run in its format. Texas runs as two separately scored parts.",
 q="A 120/240 V service drop crosses a house driveway. What's the minimum clearance above the driveway?",
 opts=["18 ft", "15 ft", "12 ft", "10 ft"], ok="c", sec="230.24(B)(2)", find="index under Clearances, overhead service conductors.",
 good="Correct. Twelve feet over a driveway, in {t}.", bad="Not quite. It's 12 ft. 10 ft is the tempting pick, but that lower clearance doesn't apply over a driveway.",
 answers_p="Every explanation names the NEC section it came from, so you learn where the answer lives instead of memorizing a letter.",
 find_p="The exam is open book. Timed lookup drills train your own tabbed code book, so the index feels like muscle memory.",
 calc_p="The full working is shown on every problem. Answers come from tested code, never typed by hand.",
 calc=[("Given", "3-phase, 127 A, 300 ft run"), ("Formula", "VD = 1.732 × K × I × L ÷ CM"), ("Plug in", "1.732 × 12.9 × 127 × 300 ÷ 83,690"), ("Volts", "VD ≈ 10.2 V"), ("Percent", "10.2 ÷ 480 ≈ 2.1%")],
 exam_p="Timed full-length practice in your state's format. Flag what you're unsure about, review, then submit, just like test day.",
 exam_screens=["exam.jpg", "progress.jpg"],
)

PLUMBER = dict(
 key="pl", id="plumber", label="Plumber", icon=DROP, bank="plumbing", img="plumber/", answered="Copper", vars=PL_VARS,
 h="For plumbers.", sub="The Uniform Plumbing Code (2021) and the International Plumbing Code (2018), with fuel gas questions from the International Fuel Gas Code. Pick the exam you're taking, and practice runs in its format.",
 q="Under the 2018 IPC, what is the minimum diameter of a water service pipe?",
 opts=["1/2 inch", "3/4 inch", "1 inch", "1 1/4 inches"], ok="b", sec="IPC 603.1", find="Chapter 6, water service, size of water service pipe.",
 good="Correct. Three-quarters of an inch, in {t}.", bad="Not quite. It's 3/4 inch. The water service pipe is never smaller than that.",
 answers_p="Every explanation names the UPC or IPC section it came from, so you learn where the answer lives instead of memorizing a letter.",
 find_p="Most journeyman exams are open book. Timed lookup drills train your own tabbed code book, so the index feels like muscle memory.",
 calc_p="The full working is shown on every problem, from offsets to pressure and head to water heating. Answers come from tested code, never typed by hand.",
 calc=[("Given", "Two 22½° fittings, 27 in offset"), ("Formula", "run = offset × run multiplier"), ("Plug in", "27 × 2.414"), ("Run", "run ≈ 65.18 in"), ("Travel", "27 × 2.613 ≈ 70.55 in")],
 exam_p="Timed full-length practice in the format of the exam you pick: the ICC national exams, Kansas, Maryland, Montana, Nebraska, Washington and a UPC exam in the IAPMO format. Flag what you're unsure about, review, then submit, just like test day.",
 exam_screens=["exam.jpg"],
)

TABBED_JS = r"""
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
  [].forEach.call(document.querySelectorAll('.drill'),function(d){
    var q=function(c){return d.querySelector(c)},opts=q('.opts'),reveal=q('.reveal'),verdict=q('.verdict'),timer=q('.dTimer'),bar=q('.dBar i');
    var key=d.dataset.ok,t=0,done=false,iv;
    function run(){clearInterval(iv);t=0;timer.textContent='0:00';bar.style.transition='none';bar.style.transform='scaleX(1)';
      if(!reduce){void bar.offsetWidth;bar.style.transition='transform 41s linear';bar.style.transform='scaleX(0)';}
      iv=setInterval(function(){if(!done){t++;timer.textContent=fmt(t);if(t>=41)clearInterval(iv)}},1000);}
    function reset(){done=false;reveal.classList.remove('on');[].forEach.call(opts.children,function(b){b.disabled=false;b.classList.remove('ok','no')});run();}
    opts.addEventListener('click',function(e){
      var b=e.target.closest('.opt');if(!b||done)return;done=true;clearInterval(iv);
      var good=b.dataset.k===key,ok=opts.querySelector('[data-k="'+key+'"]');
      [].forEach.call(opts.children,function(x){x.disabled=true});
      ok.classList.add('ok');if(!good)b.classList.add('no');
      bar.style.transition='none';
      verdict.textContent=good?d.dataset.good.replace('{t}',fmt(t)):d.dataset.bad;
      reveal.classList.add('on');
    });
    q('.again').addEventListener('click',reset);
    // Each drill's clock starts when it scrolls into view.
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();run();}},{threshold:.4});io.observe(d);}else run();
  });
})();
"""


def _plan(name, price, per, items, hl=False, style=""):
    st = f' style="{style}"' if style else ""
    return (f'<div class="plan{" hl" if hl else ""}"{st}><h3>{name}</h3><div class="price">{price}</div><div class="per">{per}</div><ul>'
            + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>")


TABBED_PRICING = ('<section class="sec" id="pricing"><div class="wrap center"><h2>Free to start. Pay once.</h2>'
 '<p class="sub">The free tier is the same for both trades. When you are ready, buy the Exam Pass for your trade, once.</p><div class="plans" style="max-width:1040px">'
 + _plan("Free", "$0", "Electrician or plumber", ["10 questions a day with explanations", "The drills", "A 25-question diagnostic", "A 10-question sample exam"])
 + _plan("Electrician Exam Pass", "$29.99", "One time, per NEC edition (2023 or 2026)", ["Unlocks everything for that edition", "Full practice exams", "No subscription"], hl=True)
 + _plan("Plumber Exam Pass", "$29.99", "One time, covers both the UPC and the IPC", ["Unlocks everything for both codes", "Full practice exams", "No subscription"], hl=True, style=PL_VARS)
 + '</div><p class="fine" style="margin:26px auto 0">Coming soon to the App Store. Exam Passes are one-time in-app purchases through Apple. Prices in US dollars.</p></div></section>')


def _head():
    c = C["tabbed"]
    url, img = f"{landing.SITE}/tabbed/", f"{landing.SITE}/tabbed/og-image.png"
    E = landing.esc
    meta = [f'<meta name="description" content="{E(c["desc"])}">', f'<link rel="canonical" href="{url}">',
            f'<meta property="og:title" content="{E(c["og_title"])}">', f'<meta property="og:description" content="{E(c["desc"])}">',
            f'<meta property="og:image" content="{img}">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
            '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Tabbed">', f'<meta property="og:url" content="{url}">',
            '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{E(c["og_title"])}">',
            f'<meta name="twitter:description" content="{E(c["desc"])}">']
    ld = re.findall(r'<script type="application/ld\+json">.*?</script>', landing.jsonld("tabbed", c), re.S)
    return dict(title=E(c["title"]), meta=meta, ld=ld, js=[])


TRADES = ('<div class="trades" aria-label="Pick your trade">'
          f'<a class="trade" href="#electrician" style="--t:{EL_A}"><i>{BOLT}</i><span>Electrician <small>NEC 2023 and 2026</small></span></a>'
          f'<a class="trade" href="#plumber" style="--t:{PL_A}"><i>{DROP}</i><span>Plumber <small>UPC and IPC</small></span></a></div>')

TABBED = dict(
 name="Tabbed", navname="Tabbed", live=False, head=_head(),
 bg="#EEF3FF", a=EL_A, ink=WHITE, a2="#FFC233", a3="#FF6B4A", band="#0B1F44",
 nav=[("Electrician", "#electrician"), ("Plumber", "#plumber"), ("Pricing", "#pricing"), ("FAQ", "#faq")],
 status="Coming soon",
 h1=["Exam prep for journeyman", "electricians and plumbers."],
 hero_extra=TRADES,
 lede="Every answer cites the code section. Pick your trade at setup, then drill the lookups, work the calcs and sit the timed exam. All offline.",
 note="iPhone. Free to start. Pay once for your trade's Exam Pass, no subscription.", cta2=("See pricing", "#pricing"),
 screens=["answer.jpg", "plumber/answer.jpg", "lookup.jpg", "plumber/calc.jpg", "exam.jpg", "plumber/exam.jpg"],
 trust=["Every answer cites the code section", "A separate blind check on every answer", "Works offline", "Pay once, no subscription"],
 css=TABBED_CSS, js=TABBED_JS,
 blocks=trade(ELECTRICIAN) + trade(PLUMBER) + [
  ("raw", TABBED_PRICING),
  ("who", dict(items=C["tabbed"]["who"])),
  ("band", dict(h="Pay once. Study anywhere.", bg="#0B1F44", sub="No account and nothing to renew. Questions, drills and exams all work offline, on the job site or in the truck.", nos=["No account", "No ads", "No subscription", "No data collected"])),
  ("faq", dict(items=faq("tabbed"), after='<p class="fine" style="margin:26px auto 0">Guide: <a href="guide/find-answers-fast-open-book-electrical-exam.html">How to find answers fast in an open-book electrical exam</a></p>')),
  ("more", C["tabbed"]["more"]),
 ],
 finale=("Know where it lives.", "Coming soon to the App Store. Electrician or plumber, free to start, pay once for your Exam Pass."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html"), ("Open-book guide", "guide/find-answers-fast-open-book-electrical-exam.html")],
 legal=["Tabbed is an independent study aid. It is not affiliated with, endorsed by, or sponsored by NFPA, IAPMO, the International Code Council (ICC), IBEW, NECA, PSI, Prometric, Pearson VUE, TDLR, or any state licensing board, and not reviewed or approved by them. "
        "NEC® and National Electrical Code® are registered trademarks of the National Fire Protection Association, Quincy, MA. Uniform Plumbing Code is a trademark of IAPMO, and International Plumbing Code and International Fuel Gas Code are trademarks of the International Code Council, used here only to describe the codes covered. "
        "No code text or tables are reproduced. Passing your exam depends on your own preparation; no study tool can guarantee a result."],
)

# ---------------------------------------------------------------- Fantasy Queens
FQ_CSS = r'''
.lbplay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:center}
.lb{position:relative;background:linear-gradient(160deg,#341043,#1C0A26);border-radius:30px;padding:24px;box-shadow:0 0 0 1px rgba(255,255,255,.14),0 50px 90px -40px rgba(248,33,138,.6)}
.lb .lbh{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;font-weight:700}
.lb .lbh small{color:var(--soft);font-weight:500}
.lb ol{list-style:none;margin:0;padding:0;position:relative}
.lb li{display:grid;grid-template-columns:28px 40px minmax(0,1fr) auto;align-items:center;gap:12px;padding:10px 12px;border-radius:16px;margin-bottom:8px;background:rgba(255,255,255,.06);transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.lb li:first-child{background:linear-gradient(90deg,rgba(255,201,77,.28),rgba(255,201,77,.06));box-shadow:inset 0 0 0 1px rgba(255,201,77,.5)}
.lb .rk{font:800 1rem var(--disp);color:var(--soft);text-align:center}
.lb li:first-child .rk{color:#FFC94D}
.lb .av{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-weight:800;color:#170A1F}
.lb .pt{font:800 1.1rem var(--disp);font-variant-numeric:tabular-nums}
.lb .up{font-size:.75rem;font-weight:700;color:#7CF0B2;margin-left:6px;opacity:0;transition:opacity .4s}
.lb .up.on{opacity:1}
.lb .ep{margin-top:10px}
.lb .eg{font-size:.82rem;color:var(--soft);margin:12px 0 0}
@media(max-width:960px){.lbplay{grid-template-columns:minmax(0,1fr);gap:36px}}
'''
FQ_PLAY = '''<section class="sec demo" id="board"><div class="wrap"><div class="lbplay">
<div><h2>Watch the leaderboard.</h2><p class="sub">Scores post after each episode. See who's leading and who moved up. Tap through a few episodes of an example house.</p></div>
<div class="lb" id="lb" aria-label="Example leaderboard">
  <div class="lbh"><span>The Werk Room</span><small id="lbEp">After episode 1</small></div>
  <ol id="lbList"></ol>
  <button class="btn ep" type="button" id="lbNext">Next episode</button>
  <p class="eg">An example house with made-up names and scores.</p>
</div></div></div></section>'''
FQ_JS = r'''
(function(){var list=document.getElementById('lbList');if(!list)return;
var P=[{n:'Jordan',c:'#FF6FB5',s:14},{n:'Priya',c:'#FFC94D',s:12},{n:'Marcus',c:'#A98BFF',s:11},{n:'Dev',c:'#58E1FF',s:9},{n:'Sam',c:'#7CF0B2',s:7}];
var ep=1,red=matchMedia('(prefers-reduced-motion: reduce)').matches,rows={};
P.forEach(function(p){var li=document.createElement('li');li.innerHTML='<span class="rk"></span><span class="av" style="background:'+p.c+'">'+p.n[0]+'</span><b>'+p.n+'<span class="up"></span></b><span class="pt"></span>';rows[p.n]=li;list.appendChild(li)});
function draw(gain){var before={};P.forEach(function(p){before[p.n]=rows[p.n].getBoundingClientRect().top});
P.sort(function(a,b){return b.s-a.s||a.n.localeCompare(b.n)});
P.forEach(function(p,i){var li=rows[p.n];list.appendChild(li);li.querySelector('.rk').textContent=i+1;li.querySelector('.pt').textContent=p.s;
var up=li.querySelector('.up');up.textContent=gain&&gain[p.n]?'+'+gain[p.n]:'';up.classList.toggle('on',!!(gain&&gain[p.n]))});
if(red||!gain)return;P.forEach(function(p){var li=rows[p.n],d=before[p.n]-li.getBoundingClientRect().top;if(!d)return;li.style.transition='none';li.style.transform='translateY('+d+'px)';void li.offsetWidth;li.style.transition='';li.style.transform=''})}
draw();
document.getElementById('lbNext').addEventListener('click',function(){var g={};P.forEach(function(p){var x=[0,2,3,5,6,8][Math.floor(Math.random()*6)];p.s+=x;if(x)g[p.n]=x});ep++;document.getElementById('lbEp').textContent='After episode '+ep;draw(g)});
})();
'''

FANTASYQUEENS = dict(
 name="Fantasy Queens", live=False, dark=True,
 bg="#170A1F", bg2="#211029", a="#F8218A", ink=WHITE, a2="#FFC94D", a3="#A855F7", band="#3A0C33",
 nav=[("How it works", "#how"), ("FAQ", "#faq")],
 status="Coming soon",
 h1=["Your watch party,", "scored."],
 lede="Start a private house for your group. Pick your queens, vote on the rules before the season, and see who's leading after every episode.",
 note="Free to play. Private houses for your group.", cta2=("How it works", "#how"),
 screens=["shot2.jpg", "shot3.jpg", "shot4.jpg"],
 trust=[t for _, t in C["fantasyqueens"]["trust"]],
 css=FQ_CSS, js=FQ_JS,
 blocks=[
  ("feats", dict(h="Play your way", sub="Four ways to play. Your house picks.", items=[
   ("crown", "Weekly Call", "One queen for the top, one safe, one for the bottom."),
   ("list", "Survival Bracket", "Rank the whole cast before the season, first out to winner."),
   ("users", "Team", "Pick a team each week, and keep it as long as your house decides."),
   ("target", "Boot Pick", "Call who goes home, with a backup for a double elimination.")])),
  ("raw", FQ_PLAY),
  ("stories", dict(items=[
   dict(h="Picks that stay honest.", p=["Picks for each episode open when the last one ends, so nobody picks days ahead with spoilers in hand. Pick together while you watch, or pick late for a small penalty. The app records when each pick was saved, and everyone's picks show once the episode starts."], screens=["shot4.jpg"], alt="Making a Weekly Call"),
   dict(h="Your house, your rules.", p=["Before the season starts, members vote on the rules: team size, the pick window, what a late pick costs and more. The majority wins, the result goes into a rule book everyone can read, and the rules lock when the season starts."], screens=["shot2.jpg"], alt="The rules vote screen"),
  ])),
  ("steps", dict(id="how", alt=True, h="How it works", items=[(a, landing.esc(b)) for a, b in C["fantasyqueens"]["steps"]])),
  ("feats", dict(h="What's inside", items=[(i, a, landing.esc(b)) for i, a, b in C["fantasyqueens"]["feats"]])),
  ("faq", dict(items=faq("fantasyqueens"))),
  ("more", C["fantasyqueens"]["more"]),
 ],
 finale=("Start your house.", "Coming soon to the App Store. Free to play."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html"), ("Terms", "terms.html"), ("Queen photos", "photos.html")],
 legal=["Fantasy Queens is an unofficial fan app. It isn't affiliated with, endorsed by or sponsored by any television network, production company or performer."],
)

# ---------------------------------------------------------------- Sitout
SITOUT_CSS = r'''
:root{--court:#1A5BB5;--volt:#E2FB2C;--navy:#111A33;--display:var(--disp)}
.court{position:relative;z-index:1;background:var(--navy);color:#EEF2FA;padding:100px 0}
.court h2{color:#fff}.court .sub{color:#C3CDE3}
.board-card{margin-top:34px;background:var(--court);border-radius:28px;padding:22px;box-shadow:inset 0 0 0 3px rgba(255,255,255,.9),0 40px 80px -40px rgba(0,0,0,.7)}
.controls{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center}
.stepper{display:inline-flex;align-items:center;gap:4px;background:rgba(9,22,56,.38);border-radius:99px;padding:5px 5px 5px 16px}
.stepper .lbl{font-weight:700;color:#E8EFFB;margin-right:6px;min-width:4.2em}
.stepper button{width:44px;height:44px;border:0;border-radius:50%;background:#fff;color:var(--navy);font:800 1.5rem/1 var(--display);cursor:pointer;display:grid;place-items:center;padding:0 0 3px}
.stepper button:hover{background:var(--volt)}
.stepper button:disabled{opacity:.35;cursor:not-allowed;background:#fff}
.stepper output{min-width:2.1em;text-align:center;font:800 1.55rem var(--display);font-variant-numeric:tabular-nums;color:#fff}
.readout{margin:16px 0 0;font:700 1.08rem var(--body);color:#fff}
.board{--n:9;display:grid;grid-template-columns:2.4rem repeat(var(--n),minmax(0,1fr));column-gap:2px;row-gap:5px;align-items:center;justify-items:center;margin-top:16px;padding:14px 10px 12px;border-radius:14px;background:rgba(9,22,56,.32);font-variant-numeric:tabular-nums}
.board .corner,.board .rh{justify-self:start;color:#D3E0F7;font:700 .74rem var(--body)}
.board .ph{color:#D3E0F7;font:700 .72rem var(--body);white-space:nowrap}
.board.compact .ph{font-size:.64rem}
.board .c{display:block;width:min(78%,22px);aspect-ratio:1;border-radius:50%;background:rgba(255,255,255,.34);transform:scale(.36);animation:pop .32s cubic-bezier(.3,1.6,.5,1) both;animation-delay:calc(var(--d) * 45ms)}
.board .c.sit{transform:none;background:radial-gradient(circle at 34% 30%,#F8FFC4 0,var(--volt) 52%,#C5DB12 100%);box-shadow:0 0 0 1.5px rgba(17,26,51,.35),0 0 12px rgba(226,251,44,.5)}
.board .rh.tot{margin-top:6px}
.board .tv{margin-top:6px;color:#fff;font:800 .82rem var(--display)}
.board.still .c{animation:none}
@keyframes pop{from{opacity:0;transform:scale(.1)}}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;margin:14px 2px 0;color:#E8EFFB;font-size:.92rem}
.legend span{display:inline-flex;align-items:center;gap:8px}
.legend i{display:inline-block;width:14px;height:14px;border-radius:50%}
.legend .k-sit{background:var(--volt);box-shadow:0 0 0 1.5px rgba(17,26,51,.35)}
.legend .k-play{width:6px;height:6px;margin:0 4px;background:rgba(255,255,255,.6)}
.check{margin:12px 2px 0;color:#fff;font-weight:700}
.rule-note{margin:22px 0 0;color:#C3CDE3;font-size:.95rem;max-width:46em}
.court a{color:var(--volt)}
.court :focus-visible{outline-color:var(--volt)}
.fmts{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.fmts>div{border-radius:28px;padding:30px;background:var(--card);box-shadow:0 0 0 1px var(--line)}
.fmts>div:first-child{background:#F4FFC2}
.fmts small{font-weight:700;color:var(--soft)}
.fmts p{margin:0;color:var(--soft)}
@media (max-width:640px){
  .board-card{padding:14px;border-radius:20px}
  .board{grid-template-columns:2rem repeat(var(--n),minmax(0,1fr));padding:12px 6px 10px}
  .board.compact{column-gap:1px}
  .board.compact .pp{display:none}
  .board.compact .corner{font-size:0}
  .board.compact .corner:after{content:"Rd";font-size:.7rem}
  .board.compact .tv{font-size:.6rem}
  .board.compact .tv.w,.board.compact .ph.w{font-size:.52rem;letter-spacing:-.06em}
  .stepper .lbl{min-width:3.9em}
}
@media (prefers-reduced-motion:reduce){.board .c{animation:none}}
'''
SITOUT_BOARD = '''<section class="court" id="try" aria-labelledby="try-h"><div class="wrap">
  <h2 id="try-h">Who sits out next?</h2>
  <p class="sub">Pick a player count and a number of courts. This board uses the same rule Sitout uses to choose who sits out, round by round.</p>
  <div class="board-card">
    <div class="controls">
      <div class="stepper" data-key="players" role="group" aria-labelledby="players-l"><span class="lbl" id="players-l">Players</span><button type="button" class="dec" aria-label="One fewer player">&minus;</button><output id="players-v">9</output><button type="button" class="inc" aria-label="One more player">+</button></div>
      <div class="stepper" data-key="courts" role="group" aria-labelledby="courts-l"><span class="lbl" id="courts-l">Courts</span><button type="button" class="dec" aria-label="One fewer court">&minus;</button><output id="courts-v">2</output><button type="button" class="inc" aria-label="One more court">+</button></div>
    </div>
    <p class="readout" id="readout" aria-live="polite">9 players on 2 courts: 8 play and 1 sits out each round.</p>
    <div class="board" id="board" aria-hidden="true"></div>
    <div class="legend" aria-hidden="true"><span><i class="k-sit"></i>Sits out</span><span><i class="k-play"></i>Plays</span><span>Rows are rounds 1 to 12, columns are players P1, P2 and so on. The last row counts each player's sit-outs.</span></div>
    <h3 class="sr">Who sits out, round by round</h3>
    <ol class="sr" id="board-text"></ol>
    <p class="check" id="check"></p>
    <noscript><p class="check">The board needs JavaScript. The guide <a href="/sitout/how-to/how-many-players-for-a-round-robin.html">How many players for a round robin</a> has the same numbers as tables.</p></noscript>
  </div>
  <p class="rule-note">The rule: whoever has sat out the fewest times sits next. On a tie, whoever sat longest ago sits, then roster order. So sit-outs never differ by more than one between any two players, and nobody is benched while someone with fewer sit-outs keeps playing. This board shows sit-outs only; the app also rotates partners and opponents every round.</p>
</div></section>'''
SITOUT_FORMATS = '''<section class="sec alt" id="formats"><div class="wrap"><h2>Two ways to play.</h2><p class="sub">Pick a format before the first round.</p><div class="fmts">
<div><small>Rotating partners</small><h3>A new partner every round, your own score.</h3><p>Everyone keeps an individual record: your team's result counts for you, whoever you played with. Add the mixed-doubles rule for a mixer.</p></div>
<div><small>Fixed partners</small><h3>Bring a partner, play every team.</h3><p>Teams stay together all night and standings are per team. Every team plays every other team once before any rematch when you have enough courts.</p></div>
</div><p class="fine">Standings rank by win rate, then point difference per game, then total points. Ranking by win rate means the player who drew one extra sit-out isn't punished for playing one fewer game.</p></div></section>'''

SITOUT = dict(
 name="Sitout", live=False, soon="Coming soon on the App Store",
 bg="#EEF3FF", bg2="#E2EAFB", a="#E2FB2C", ink=NAVY, a2="#2F6BFF", a3="#FF7A59", band="#111A33",
 nav=[("Try it", "#try"), ("Guides", "/sitout/how-to/")],
 status="Pickleball round robins",
 h1=["Fair rotations.", "Even sit-outs."],
 lede="One organizer's phone runs league night or open play: who's on which court, who partners whom, who sits out, the scores and the standings. Players never pay, and they never need the app or an account.",
 note="For iPhone and iPad. Any single night is free.", cta2=("Try the sit-out rule", "#try"),
 screens=["live.jpg", "score.jpg", "standings.jpg", "season.jpg"],
 trust=["Players never pay", "No accounts", "No server", "Any single night is free"],
 css=SITOUT_CSS, scripts=["/sitout/demo.js"], ld_marker=True,
 blocks=[
  ("raw", SITOUT_BOARD),
  ("steps", dict(id="how", h="From the first serve to the final standings, on one phone.", items=[
   ("Add players and courts", "Type in names. That's all a player needs to be. Pick a format and the number of courts, and turn on the mixed-doubles rule if you want it.", "live.jpg"),
   ("Play the rounds", "Sitout shows each court, who partners whom and who sits out. Enter scores fast between games. Latecomers join and early leavers go mid-night without losing a score, and a wrong tap can be undone.", "score.jpg"),
   ("Share the standings", "End the night with standings for everyone. Share cards for the next round and the final standings are free, and players can see them without the app.", "standings.jpg")])),
  ("feats", dict(alt=True, h="The little things that keep a night moving.", items=[
   ("timer", "Round timer", "Set 8 to 20 minutes a round. The countdown is big enough to hold up to a court, shows on the Lock Screen, and buzzes when time's up."),
   ("pin", "Your court names", "Call the courts what your venue calls them, like “7, 8, 9” or “Pink”. The round, the score pad and every share card use your names."),
   ("chart", "Balance by level", "Give players a level (a DUPR rating or your club's 3.0 to 5.0) and Sitout spreads stronger players across teams so games stay close. Fair sit-outs and fresh partners still come first."),
   ("repeat", "Hand off the night", "Leaving early? AirDrop the night to a co-organizer. Their phone picks up on the same round, with every score.")])),
  ("feats", dict(h="Fairness you can check, not just trust.", sub="Every rotation follows rules you can read right here. They're the same rules the app runs.", items=[
   ("users", "Sit-outs", "Sit-outs never differ by more than one between any two players. Nobody is benched while someone with fewer sit-outs keeps playing. Ties go to whoever sat longest ago, so sit-outs spread through the night instead of piling up at the end."),
   ("repeat", "Partners", 'Sitout spreads partners so repeats are as rare as the math allows, then spreads opponents. With 8 players on 2 courts, everyone partners everyone else exactly once in 7 rounds. <a href="/sitout/how-to/how-does-a-pickleball-round-robin-work.html#example">See the rotation</a>.'),
   ("calendar", "Late arrivals, early exits", "Someone who walks in at round 5 starts level with the group's fewest sit-outs, so they aren't benched to catch up. Someone who leaves early keeps every score already entered. Only the rounds still to come change."),
   ("heart", "Mixed doubles", "Turn on the mixed-doubles rule and Sitout keeps teams one man and one woman whenever the players on court allow it. Fair sit-outs come first, so nobody sits out of turn just to make a team mixed.")])),
  ("stories", dict(h="A look inside.", items=[
   dict(h="A round, at a glance.", p=["Courts, partners and who sits out, on one screen you can hold up to the group."], screens=["live.jpg"], alt="A live round: who sits out, then each court with its two teams and scores"),
   dict(h='A season that adds up.<span class="tag">Pro</span>', p=["Run the same group week after week and Sitout keeps standings across the season."], screens=["season.jpg"], alt="A group's season standings across four nights"),
  ])),
  ("raw", SITOUT_FORMATS),
  ("plans", dict(h="Any single night is free, at any size.", sub="Players never pay. Sitout Pro is for the organizer who runs the same group week after week.", items=[
   ("Free", "$0", "Every night you run", ["Any number of players and courts", "Both formats, with the mixed-doubles rule", "Fair sit-outs and rotating partners", "Fast scores, undo and end-of-night standings", "Share cards for the next round and the standings", "Round timer, court names and balance by level"], False),
   ("Sitout Pro", "$29.99/year", "or $69.99 once for lifetime. For the organizer only.", ["Saved seasons, with standings across weeks", "Group history", "DUPR CSV export"], True)],
   fine="The yearly plan renews automatically until you cancel it in your Apple Account settings. Prices in US dollars. DUPR is a trademark of its owner. Sitout is not affiliated with or endorsed by DUPR.")),
  ("band", dict(h="Everything stays on the organizer's phone.", bg="#111A33", sub="Players, scores and standings are stored on the organizer's iPhone and leave it only when the organizer shares a card or a CSV file.",
   html='<p style="margin-top:18px"><a href="privacy.html">Read the privacy policy</a></p>', nos=["No accounts", "No server", "No analytics", "No ads"])),
  ("faq", dict(h="Frequently asked questions", items=[
   ("Do players need the app?", "No. Only the organizer installs Sitout. Players never pay and never need an account. They see the rounds and standings on the organizer's phone, or on the share cards the organizer sends."),
   ("How does Sitout choose who sits out?", "Whoever has sat out the fewest times sits next. On a tie, whoever sat longest ago sits, then roster order. Sit-outs never differ by more than one between any two players, and nobody is benched while someone with fewer sit-outs keeps playing."),
   ("Can people arrive late or leave early?", "Yes. Add a latecomer or mark someone as gone at any point in the night. Scores already entered stay put, and only the rounds still to come change. A latecomer starts level with the group's fewest sit-outs, so they aren't benched to catch up."),
   ("Does Sitout keep mixed doubles mixed?", "With the mixed-doubles rule on, it keeps teams one man and one woman whenever the players on court allow it. Fair sit-outs come first, so on a night with many more men than women (or the other way around), some teams will be two men or two women rather than benching someone out of turn."),
   ("How are standings ranked?", "By win rate, then point difference per game, then total points. Win rate keeps things fair when sit-outs leave some players with one game fewer than others."),
   ("What's free and what's in Sitout Pro?", "Any single night is free, at any size, in either format, with standings and share cards. Sitout Pro adds saved seasons with standings across weeks, group history and DUPR CSV export, for $29.99 a year or $69.99 once for lifetime."),
   ("Does Sitout need an account or the internet?", "It needs no account. Sitout has no server: players, scores and standings are stored on the organizer's iPhone and leave it only when the organizer shares a card or a CSV file."),
   ("Does it work with an odd number of players?", 'Yes. Any number works. Four players fit on each court and everyone else sits out that round, chosen by the fair rule above. The guide on <a href="/sitout/how-to/how-many-players-for-a-round-robin.html">how many players you need</a> has a table for 4 to 32 players on 1 to 8 courts.')])),
  ("guides", dict(h="Running a round robin? Start here.", sub="Every schedule in these guides was generated by Sitout's own rotation engine.", items=[
   ("/sitout/how-to/pickleball-rotation-9-players.html", "Pickleball rotation for 9 players", "Who sits out each round on 2 courts and on 1, plus 5 to 16 players."),
   ("/sitout/how-to/how-does-a-pickleball-round-robin-work.html", "How does a pickleball round robin work?", "Rotating vs fixed partners, sit-outs, scoring and a full 8-player example."),
   ("/sitout/how-to/how-many-players-for-a-round-robin.html", "How many players for a round robin?", "Who plays and who sits for 4 to 32 players on 1 to 8 courts."),
   ("/sitout/how-to/", "All guides", "Mixed doubles, scoring and standings, open play and more.")])),
  ("more", ["mvn", "fantasyqueens", "stashday"]),
 ],
 finale=("Run a fair night.", "Coming soon on the App Store. Any single night is free."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html"), ("Guides", "/sitout/how-to/")],
 legal=["DUPR is a trademark of its owner. Sitout is not affiliated with or endorsed by DUPR."],
)
