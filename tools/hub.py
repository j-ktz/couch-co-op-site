#!/usr/bin/env python3
"""Builds the studio hub, index.html, for couchcoopstudios.com.

Run from the repo root:  python3 tools/hub.py
Edit APPS below and re-run. The whole file is rewritten, so don't hand-edit index.html.
App copy matches each app's own page and the original apps hub. No em dashes (house style).
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://couchcoopstudios.com"
SUPPORT = "support@couchcoopstudios.com"
NAVY, WHITE = "#0B1A4A", "#FFFFFF"

# ink = text color on the app's accent (white on dark accents, navy on light ones).
APPS = [
 dict(slug="mvn", name="Music Video Night", g="#9867FF", ink=WHITE, live=True,
      line="A party game. Everyone picks a music video, everyone votes blind, one person wins the Night.",
      points=["Names stay hidden until the votes are in", "Pick a theme, queue the videos, play them on the big screen", "Results reveal who chose the winner"],
      screens=[("screen-themes.webp", "Host a Night screen with themes to pick from"), ("screen-voting.webp", "Blind voting on the videos"),
               ("screen-playback.webp", "A video playing during the Night"), ("screen-results.webp", "Results revealing who chose the winner")]),
 dict(slug="mackro", name="Mackro", g="#F5B82A", ink=NAVY, live=True,
      line="A macro tracker with a squirrel named Mack who keeps score and never judges.",
      points=["Log a meal by describing it or snapping a photo", "Calories and macros at a glance, with a nudge from Mack", "Trends over 7, 30 or 90 days, plus widgets"],
      screens=[("today.jpg", "Today screen with calories, macros and Mack"), ("describe.jpg", "Logging a meal by describing it"),
               ("trends.jpg", "Trends screen with calorie bars and macro averages"), ("training.jpg", "Training day targets")]),
 dict(slug="tanklog", name="TankLog", g="#2EE6B6", ink=NAVY, live=True,
      line="A free, offline journal for planted tank and shrimp keepers. Log water tests, watch the trends and know when your CO₂ drifts.",
      points=["pH, KH, GH, nitrate and more, graded against your own ranges", "Care schedules and dosing with reminders", "No login, no ads. Your data stays on your device"],
      screens=[("shot1.jpg", "CO₂ estimate and a pH trend chart"), ("shot2.jpg", "Water test and care schedule screens"), ("shot3.jpg", "TankLog tank overview")]),
 dict(slug="stashday", name="Stashday", g="#34C79A", ink=NAVY, live=False,
      line="Tells you exactly what to set aside each payday so the irregular bills stop being a surprise.",
      points=["One number per paycheck that covers every bill", "A ring for each fund, so you see what is on track", "Tick off what you paid and set aside"],
      screens=[("number.jpg", "Your number: the amount to set aside this payday"), ("fund.jpg", "A single fund with progress ring and due date"), ("checklist.jpg", "Payday checklist")]),
 dict(slug="tabbed", name="Tabbed Electrician", g="#0A84FF", ink=WHITE, live=False,
      line="Exam prep for journeyman electricians. Every answer cites the code section.",
      points=["Practice questions with the explanation and the NEC reference", "Timed lookup drills for finding the right article fast", "Full timed practice exams with a question navigator"],
      screens=[("answer.jpg", "A practice answer with explanation and code citation"), ("lookup.jpg", "A timed lookup drill with a countdown"), ("exam.jpg", "A timed practice exam")]),
 dict(slug="tabbed-plumber", name="Tabbed Plumber", g="#1FA2C8", ink=NAVY, live=False,
      line="Exam prep for journeyman plumbers. Every answer cites the code section.",
      points=["Practice questions with the explanation and the UPC or IPC reference", "Step-by-step plumbing calcs, from offsets to pressure and head", "Timed practice exams in the format of the exam you pick"],
      screens=[("answer.jpg", "A practice answer with explanation and code citation"), ("calc.jpg", "A plumbing calculation with every step shown"), ("exam.jpg", "A timed practice exam")]),
 dict(slug="fantasyqueens", name="Fantasy Queens", g="#F8218A", ink=WHITE, live=False,
      line="Fantasy leagues for your Drag Race watch party. Pick your queens, vote on the rules, see who leads after every episode.",
      points=["Draft your queens with your watch-party group", "Vote on the rules before the premiere", "A leaderboard that updates after every episode"],
      screens=[("shot2.jpg", "Rules vote screen"), ("shot3.jpg", "Leaderboard after an episode"), ("shot4.jpg", "A house's queens")]),
 dict(slug="sitout", name="Sitout", g="#E2FB2C", ink=NAVY, live=False,
      line="Runs a pickleball round robin from one phone. Fair sit-outs, rotating partners, standings at the end of the night.",
      points=["Sit-outs shared evenly, every round", "Scores in two taps, late arrivals without lost scores", "Players never pay and never need the app"],
      screens=[("live.jpg", "A live round: who sits out, then each court with its teams and scores"), ("score.jpg", "Entering a score"), ("standings.jpg", "End-of-night standings ranked by win rate")]),
 dict(slug="statecount", name="Statecount", g="#4A8FD6", ink=NAVY, live=False,
      line="For snowbirds, remote workers and second-home owners who need to know, and be able to show, how many days they spent where. Your location never leaves your phone.",
      points=["Any part of a day counts; travel days count for both places", "Every day shows where its record came from", "Day-by-day PDF and CSV report"],
      screens=[("home.jpg", "Days used and days left for New York and Florida (example data)"), ("calendar.jpg", "Calendar month colored by state (example data)")]),
]
BY = {a["slug"]: a for a in APPS}
# The three phones on the hero couch, each cycling through a few apps.
COUCH = [["mackro", "stashday", "statecount"], ["mvn", "fantasyqueens", "sitout"], ["tabbed", "tanklog", "tabbed-plumber"]]

e = lambda s: html.escape(s, quote=True)


def img(slug, f, alt="", cls="", lazy=True):
    a = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="/{slug}/img/{f}" alt="{e(alt)}" width="640" height="1390"{a}>'


def phone(screens, slug=None, delay=0, label=None):
    """screens: list of (slug, file, alt). The first one shows without JavaScript."""
    imgs = "".join(img(s, f, alt, "on" if i == 0 else "") for i, (s, f, alt) in enumerate(screens))
    aria = f' role="img" aria-label="{e(label)}"' if label else ""
    return f'<div class="ph" data-delay="{delay}"{aria}><div class="scr">{imgs}</div></div>'


def couch_phone(i, slugs):
    screens = [(s, BY[s]["screens"][0][0], "") for s in slugs]
    chips = "".join(f'<span class="chip{" on" if j == 0 else ""}" style="--g:{BY[s]["g"]}"><img src="/{s}/img/icon.png" alt="" width="22" height="22">{e(BY[s]["name"])}</span>' for j, s in enumerate(slugs))
    return f'<div class="seat s{i}"><div class="chips" aria-hidden="true">{chips}</div>{phone(screens, delay=i * 1100)}</div>'


def section(a, flip):
    s = a["slug"]
    tag = '<span class="tag live">On the App Store</span>' if a["live"] else '<span class="tag">Coming soon</span>'
    pts = "".join(f"<li>{e(p)}</li>" for p in a["points"])
    sc = a["screens"]
    one = [(s, f, alt) for f, alt in sc[0::2]]
    two = [(s, f, alt) for f, alt in (sc[1::2] or sc[:1])]
    phones = phone(one, delay=0, label=f"{a['name']} screens") + phone(two, delay=1600, label=f"More {a['name']} screens")
    return f'''
    <section class="app{" flip" if flip else ""}" id="{s}" style="--g:{a["g"]};--gi:{a["ink"]}" aria-labelledby="{s}-h">
      <div class="info">
        <div class="head"><img src="/{s}/img/icon.png" alt="" width="72" height="72" loading="lazy"><div><h2 id="{s}-h">{e(a["name"])}</h2>{tag}</div></div>
        <p class="line">{e(a["line"])}</p>
        <ul>{pts}</ul>
        <a class="go" href="/{s}/">See {e(a["name"])}</a>
      </div>
      <div class="shots">{phones}</div>
    </section>'''


COUCH_BACK = '''<svg class="cb" viewBox="0 0 1000 640" aria-hidden="true"><ellipse cx="500" cy="618" rx="440" ry="20" fill="#0B1A4A" opacity=".10"/><path d="M128 470V262C128 160 214 118 330 136C420 150 458 178 500 178C542 178 580 150 670 136C786 118 872 160 872 262V470Z" fill="#1857E1"/></svg>'''
COUCH_FRONT = '''<svg class="cf" viewBox="0 0 1000 640" aria-hidden="true"><g fill="#0F3BB0"><rect x="104" y="580" width="46" height="40" rx="10"/><rect x="850" y="580" width="46" height="40" rx="10"/></g><g fill="#1857E1" stroke="#EEF1FB" stroke-width="9"><rect x="158" y="452" width="346" height="134" rx="44"/><rect x="496" y="452" width="346" height="134" rx="44"/><path d="M58 360C58 300 96 276 132 276C176 276 206 304 206 360V586H86C70 586 58 574 58 558Z"/><path d="M942 360C942 300 904 276 868 276C824 276 794 304 794 360V586H914C930 586 942 574 942 558Z"/></g></svg>'''

CSS = r'''
@font-face{font-family:"Manrope";font-style:normal;font-weight:200 800;font-display:swap;src:url(/fonts/manrope-latin-wght-normal.woff2) format("woff2-variations"),url(/fonts/manrope-latin-wght-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/dm-sans-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/dm-sans-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/dm-sans-latin-700-normal.woff2) format("woff2")}
:root{--paper:#EEF1FB;--ink:#0B1A4A;--soft:#4A5680;--cobalt:#1857E1;--deep:#0F3BB0;--mist:#DCE4FB;--line:rgba(11,26,74,.12);
  --body:"DM Sans",system-ui,-apple-system,sans-serif;--disp:"Manrope",system-ui,-apple-system,sans-serif;color-scheme:light}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 var(--body);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:inherit}
img{max-width:100%}
:focus-visible{outline:3px solid var(--cobalt);outline-offset:3px;border-radius:10px}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:12px;z-index:9;background:#fff;padding:8px 14px;border-radius:10px}

/* top */
.bar{display:flex;justify-content:flex-end;gap:6px;padding:22px 0 0}
.bar a{text-decoration:none;font-weight:700;font-size:.95rem;padding:9px 16px;border-radius:99px;color:var(--soft)}
.bar a:hover{color:var(--ink);background:var(--mist)}
.hero{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:center;padding:8px 0 40px}
.logo{display:block;width:min(340px,78%);height:auto;margin:0 0 30px -6px}
h1{font:800 clamp(2.6rem,5.4vw,4.6rem)/.98 var(--disp);letter-spacing:-.045em;margin:0 0 20px;text-wrap:balance}
.lede{font-size:1.2rem;color:var(--soft);max-width:28em;margin:0 0 28px}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;text-decoration:none;font-weight:700;padding:14px 24px;border-radius:99px;background:var(--cobalt);color:#fff;box-shadow:0 12px 24px -12px rgba(24,87,225,.8);transition:transform .2s,background .2s}
.btn:hover{background:var(--deep);transform:translateY(-1px)}
.btn.alt{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 2px var(--line)}
.btn.alt:hover{background:var(--mist)}

/* the couch */
.couch{position:relative;aspect-ratio:1000/640;width:100%;margin-top:120px}
.couch svg{position:absolute;inset:0;width:100%;height:100%}
.cf{z-index:3;pointer-events:none}
.seat{position:absolute;bottom:31%;width:18.5%;z-index:2;animation:sit 6s ease-in-out infinite}
.seat.s0{left:21.5%;transform-origin:bottom center;rotate:-5deg;animation-delay:-2s}
.seat.s1{left:40.75%;bottom:33%;animation-delay:-4s}
.seat.s2{left:60%;rotate:5deg}
@keyframes sit{0%,100%{translate:0 0}50%{translate:0 -8px}}
.chips{position:absolute;left:50%;top:-14px;translate:-50% -100%;height:34px;width:190px;z-index:4}
.chip{position:absolute;left:50%;top:0;translate:-50% 0;display:flex;align-items:center;gap:7px;white-space:nowrap;padding:5px 13px 5px 6px;border-radius:99px;background:#fff;font:700 .8rem var(--body);box-shadow:0 0 0 1.5px color-mix(in srgb,var(--g) 70%,transparent),0 10px 22px -12px var(--g);opacity:0;transition:opacity .6s}
.chip.on{opacity:1}
.s1 .chips{top:-52px}
.chip img{width:22px;height:22px;border-radius:6px}

/* iPhone */
.ph{position:relative;padding:3.6%;border-radius:17% / 7.8%;background:linear-gradient(150deg,#3a4152,#11141c 42%,#2a2f3b);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.22),0 0 0 1px rgba(11,26,74,.35),0 34px 60px -26px rgba(11,26,74,.65)}
.ph:before{content:"";position:absolute;right:-1.4%;top:20%;width:1.6%;height:11%;border-radius:0 3px 3px 0;background:#2a2f3b}
.ph:after{content:"";position:absolute;top:5.2%;left:50%;width:30%;height:3.4%;translate:-50% 0;border-radius:99px;background:#000;z-index:2}
.scr{position:relative;aspect-ratio:640/1390;border-radius:13.5% / 6.2%;overflow:hidden;background:#000;isolation:isolate}
.scr img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .8s ease}
.scr img.on{opacity:1}

/* picker */
.pick{display:flex;flex-wrap:wrap;justify-content:center;gap:4px;padding:18px 0 56px;border-bottom:1px solid var(--line)}
.pick a{display:flex;flex-direction:column;align-items:center;gap:8px;width:104px;padding:12px 6px;border-radius:22px;text-decoration:none;font-weight:700;font-size:.82rem;line-height:1.2;text-align:center;color:var(--soft);transition:transform .3s cubic-bezier(.3,1.5,.4,1),background .25s,color .2s}
.pick img{width:68px;height:68px;border-radius:16px;box-shadow:0 10px 22px -12px rgba(11,26,74,.6);transition:transform .35s cubic-bezier(.3,1.6,.4,1)}
.pick a:hover,.pick a:focus-visible{transform:translateY(-4px);background:#fff;color:var(--ink)}
.pick a:hover img{transform:rotate(-5deg) scale(1.06)}

/* app rows */
.app:last-child{border-bottom:0}
.app{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:center;padding:84px 0;border-bottom:1px solid var(--line);scroll-margin-top:16px}
.app.flip .info{order:2}
.head{display:flex;align-items:center;gap:18px}
.head img{width:72px;height:72px;border-radius:17px;box-shadow:0 14px 30px -14px var(--g)}
h2{font:800 clamp(1.9rem,3.6vw,2.7rem)/1.02 var(--disp);letter-spacing:-.04em;margin:0 0 8px}
.tag{display:inline-block;font-size:.76rem;font-weight:700;padding:4px 11px;border-radius:99px;background:var(--mist);color:var(--soft)}
.tag.live{background:var(--g);color:var(--gi)}
.line{font-size:1.22rem;line-height:1.45;margin:24px 0 18px;max-width:28em}
.info ul{list-style:none;margin:0 0 28px;padding:0;display:grid;gap:10px;max-width:30em}
.info li{position:relative;padding-left:28px;color:var(--soft)}
.info li:before{content:"";position:absolute;left:0;top:.42em;width:14px;height:14px;border-radius:5px;background:var(--g);box-shadow:inset 0 0 0 1px rgba(11,26,74,.18)}
.go{display:inline-block;font-weight:700;text-decoration:none;color:var(--gi);background:var(--g);padding:13px 24px;border-radius:99px;box-shadow:0 12px 24px -14px var(--g),inset 0 0 0 1px rgba(11,26,74,.12);transition:transform .2s,filter .2s}
.go:hover{transform:translateY(-1px);filter:saturate(1.15) brightness(1.04)}
.shots{position:relative;display:flex;justify-content:center;align-items:flex-start;gap:22px}
.shots:before{content:"";position:absolute;inset:10% 4% 6%;border-radius:50%;background:var(--g);filter:blur(70px);opacity:.32;z-index:0}
.shots .ph{position:relative;z-index:1;flex:0 1 250px}
.shots .ph+.ph{margin-top:56px}
.app .shots .ph{transition:transform 1s cubic-bezier(.2,.8,.2,1),opacity .8s}
.js .app:not(.in) .shots .ph{transform:translateY(40px) rotate(3deg);opacity:0}
.js .app:not(.in) .shots .ph+.ph{transform:translateY(70px) rotate(-3deg)}
.app.in .shots .ph+.ph{transition-delay:.12s}

/* house rules: three cushions */
.studio{background:var(--cobalt);color:#fff;padding:110px 0;margin-top:0;position:relative;overflow:hidden}
.studio:before{content:"";position:absolute;right:-12%;top:-30%;width:60%;aspect-ratio:1;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.16),transparent);pointer-events:none}
.studio h2{font-size:clamp(2.4rem,5.4vw,4.4rem);line-height:.98;letter-spacing:-.045em;max-width:12em;margin:0 0 48px;text-wrap:balance}
.cols{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:64px;align-items:start}
.say p{font-size:1.22rem;line-height:1.55;margin:0 0 18px;max-width:32em;color:rgba(255,255,255,.9)}
.facts{margin:0;display:grid;gap:0}
.facts div{display:grid;grid-template-columns:110px minmax(0,1fr);align-items:baseline;gap:18px;padding:18px 0;border-top:1px solid rgba(255,255,255,.22)}
.facts div:last-child{border-bottom:1px solid rgba(255,255,255,.22)}
.facts dt{font:800 3.4rem/1 var(--disp);letter-spacing:-.05em}
.facts dd{margin:0;font-size:1.05rem;color:rgba(255,255,255,.85)}
.rules{padding:96px 0 40px;text-align:center}
.rules h2{margin-bottom:12px}
.rules>p{color:var(--soft);font-size:1.15rem;max-width:32em;margin:0 auto 40px}
.cush{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;max-width:980px;margin:0 auto;padding:12px;border-radius:44px;background:var(--cobalt)}
.cush div{background:var(--mist);border-radius:34px;padding:34px 28px 30px;text-align:left}
.cush h3{font:800 1.35rem/1.15 var(--disp);letter-spacing:-.03em;margin:0 0 8px}
.cush p{margin:0;color:var(--soft)}
.help{text-align:left;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;max-width:980px;margin:56px auto 0;padding:34px 36px;border-radius:30px;background:#fff;box-shadow:0 0 0 1px var(--line)}
.help h3{font:800 1.5rem/1.1 var(--disp);letter-spacing:-.03em;margin:0 0 6px}
.help p{margin:0;color:var(--soft)}
footer{padding:64px 0 56px;color:var(--soft);font-size:.92rem;text-align:center}
footer p{margin:6px 0}
footer nav{display:flex;justify-content:center;flex-wrap:wrap;gap:4px 18px;margin-bottom:14px}
footer nav a{font-weight:700;text-decoration:none;color:var(--ink)}
footer nav a:hover{color:var(--cobalt)}
.fine{font-size:.8rem;opacity:.8;max-width:46em;margin:14px auto 0}

@media(max-width:960px){
  .hero{grid-template-columns:minmax(0,1fr);gap:20px}
  .logo{width:min(300px,70%)}
  .couch{max-width:640px;margin:30px auto 0}
  .chips{display:none}
  .app{grid-template-columns:minmax(0,1fr);gap:40px;padding:64px 0}
  .app.flip .info{order:0}
  .cush{grid-template-columns:minmax(0,1fr);border-radius:36px}
  .help{grid-template-columns:minmax(0,1fr)}
  .cols{grid-template-columns:minmax(0,1fr);gap:36px}
  .studio{padding:80px 0}
}
@media(max-width:560px){
  .wrap{padding:0 16px}
  .bar{justify-content:center}
  .pick a{width:84px;font-size:.76rem}.pick img{width:58px;height:58px}
  .shots{gap:14px}.shots .ph+.ph{margin-top:36px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .seat{animation:none}
  .js .app:not(.in) .shots .ph,.js .app:not(.in) .shots .ph+.ph{transform:none;opacity:1}
  .scr img,.chip,.pick a,.pick img{transition:none}
}
'''

JS = r'''
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rows = document.querySelectorAll('.app');
  if (!('IntersectionObserver' in window)) { rows.forEach(function(r){ r.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, {threshold:.18});
  rows.forEach(function(r){ io.observe(r); });
  if (reduce) return;
  // Cycle each phone's screens, only while it is on screen.
  var phones = [].slice.call(document.querySelectorAll('.ph')).filter(function(p){ return p.querySelectorAll('.scr img').length > 1; });
  var seen = new Set();
  var vis = new IntersectionObserver(function(es){ es.forEach(function(en){ en.isIntersecting ? seen.add(en.target) : seen.delete(en.target); }); }, {threshold:.25});
  phones.forEach(function(p){ vis.observe(p); });
  function step(p){
    if (!seen.has(p) || document.hidden) return;
    var imgs = p.querySelectorAll('.scr img'), i = [].findIndex.call(imgs, function(x){ return x.classList.contains('on'); });
    var n = (i + 1) % imgs.length;
    imgs[i].classList.remove('on'); imgs[n].classList.add('on');
    var chips = p.parentNode.querySelectorAll('.chip');
    if (chips.length) { chips[i].classList.remove('on'); chips[n].classList.add('on'); }
  }
  phones.forEach(function(p){
    setTimeout(function(){ step(p); setInterval(function(){ step(p); }, 3600); }, 2400 + (+p.dataset.delay || 0));
  });
})();
'''


def build():
    couch = "".join(couch_phone(i, s) for i, s in enumerate(COUCH))
    picker = "".join(f'<a href="#{a["slug"]}"><img src="/{a["slug"]}/img/icon.png" alt="" width="68" height="68">{e(a["name"])}</a>' for a in APPS)
    rows = "".join(section(a, i % 2 == 1) for i, a in enumerate(APPS))
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Couch Co-Op Studios", "url": f"{SITE}/",
         "description": "Small, useful iPhone apps with fair prices, clear privacy and real support.",
         "publisher": {"@type": "Organization", "name": "Couch Co-Op Studios", "url": "https://couchcoopstudios.com/"}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "iPhone apps from Couch Co-Op Studios",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a["name"], "url": f"{SITE}/{a['slug']}/"} for i, a in enumerate(APPS)]},
    ]
    ldtags = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    desc = "Couch Co-Op Studios makes small iPhone apps that each do one job well. No ads, fair prices, and only the data the app needs."
    og = f"{SITE}/assets/brand/couch-co-op-studios-primary.png"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#EEF1FB">
<title>Couch Co-Op Studios: small apps, made together</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/">
<link rel="icon" type="image/png" href="/assets/brand/couch-co-op-studios-mark-600.png">
<link rel="preload" as="image" href="/assets/brand/couch-co-op-studios-mark-600.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Couch Co-Op Studios">
<meta property="og:title" content="Couch Co-Op Studios: small apps, made together"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{og}">
{ldtags}
<style>{CSS}</style>
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#apps">Skip to the apps</a>
<main>
<div class="wrap">
  <nav class="bar" aria-label="Site"><a href="#apps">Our apps</a><a href="#studio">Studio</a><a href="#rules">House rules</a><a href="mailto:{SUPPORT}">Contact</a></nav>
  <header class="hero">
    <div>
      <img class="logo" src="/assets/brand/couch-co-op-studios-mark-600.png" alt="Couch Co-Op Studios" width="607" height="380">
      <h1>Small apps, made together.</h1>
      <p class="lede">We're an independent iPhone studio. Our team designs, builds and supports small apps for game night, everyday life and the oddly specific problem you wish somebody would just solve.</p>
      <div class="cta"><a class="btn" href="#apps">See our apps</a><a class="btn alt" href="mailto:hello@couchcoopstudios.com">Say hello</a></div>
    </div>
    <div class="couch" aria-hidden="true">{COUCH_BACK}{couch}{COUCH_FRONT}</div>
  </header>
  <nav class="pick" id="apps" aria-label="Jump to an app">{picker}</nav>
  <div class="rows">{rows}
  </div>
</div>
<section class="studio" id="studio" aria-labelledby="studio-h">
  <div class="wrap">
    <h2 id="studio-h">A small studio with a big couch.</h2>
    <div class="cols">
      <div class="say">
        <p>Couch Co-Op Studios started the way most good ideas do: a couple of people on a couch, wishing an app worked a little better. So we made it ourselves.</p>
        <p>Our team does everything in-house. We design every screen, write every line, and answer every support email. If an app has our name on it, we use it too.</p>
      </div>
      <dl class="facts">
        <div><dt>9</dt><dd>iPhone apps, out now or on the way</dd></div>
        <div><dt>0</dt><dd>ads in any of them</dd></div>
        <div><dt>1</dt><dd>inbox, read by the people who built the app</dd></div>
      </dl>
    </div>
  </div>
</section>
<div class="wrap">
  <div class="tail">
    <section class="rules" id="rules" aria-labelledby="rules-h">
      <h2 id="rules-h">House rules</h2>
      <p>Every app looks different. Our house rules don't change.</p>
      <div class="cush">
        <div><h3>No ads</h3><p>The app solves its problem. It doesn't rent your attention to anybody else.</p></div>
        <div><h3>Plain privacy</h3><p>Each app's privacy page says what it uses, what leaves your phone and why.</p></div>
        <div><h3>Fair prices</h3><p>Free to download. Any upgrade shows its price before you buy, with no surprise subscriptions.</p></div>
      </div>
      <div class="help">
        <div><h3>Need a hand?</h3><p>Our team reads every message. Tell us the app, your device and what happened.</p></div>
        <a class="btn" href="mailto:{SUPPORT}">Email {SUPPORT}</a>
      </div>
    </section>
  </div>
  <footer>
    <nav aria-label="Apps">{"".join(f'<a href="/{a["slug"]}/">{e(a["name"])}</a>' for a in APPS)}</nav>
    <p>&copy; 2026 Couch Co-Op Studios.</p>
    <p class="fine">Apple, the Apple logo and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc.</p>
  </footer>
</div>
</main>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build())
    print("wrote index.html")
