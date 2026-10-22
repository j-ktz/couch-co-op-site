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
      fan="home/today.jpg", devices=[("max", "home/today.jpg", "Mackro Today screen on iPhone 17 Pro Max"), ("watch", "home/watch.jpg", "Mackro on Apple Watch with Log meal")],
      line="A macro tracker with a squirrel named Mack who keeps score and never judges.",
      points=["Log a meal by describing it or snapping a photo", "Calories and macros at a glance, with a nudge from Mack", "Trends over 7, 30 or 90 days, plus widgets"],
      screens=[("today.jpg", "Today screen with calories, macros and Mack"), ("describe.jpg", "Logging a meal by describing it"),
               ("trends.jpg", "Trends screen with calorie bars and macro averages"), ("training.jpg", "Training day targets")]),
 dict(slug="tanklog", name="TankLog", g="#2EE6B6", ink=NAVY, live=True,
      line="A free, offline journal for planted tank and shrimp keepers. Log water tests, watch the trends and know when your CO₂ drifts.",
      points=["pH, KH, GH, nitrate and more, graded against your own ranges", "Care schedules and dosing with reminders", "No login, no ads. Your data stays on your device"],
      screens=[("shot1.jpg", "CO₂ estimate and a pH trend chart"), ("shot2.jpg", "Water test and care schedule screens"), ("shot3.jpg", "TankLog tank overview")]),
 dict(slug="stashday", name="Stashday", g="#34C79A", ink=NAVY, live=False,
      fan="home/fund.jpg", devices=[("pad", "home/ipad-home.jpg", "Stashday on iPad: the payday number beside a bill"), ("reg", "home/fund.jpg", "A fund with its progress ring on iPhone")],
      line="Tells you exactly what to set aside each payday so the irregular bills stop being a surprise.",
      points=["One number per paycheck that covers every bill", "A ring for each fund, so you see what is on track", "Tick off what you paid and set aside"],
      screens=[("number.jpg", "Your number: the amount to set aside this payday"), ("fund.jpg", "A single fund with progress ring and due date"), ("checklist.jpg", "Payday checklist")]),
 # One app for two trades: the user picks Electrician or Plumber at setup. Plumber screens live in /tabbed/img/plumber/.
 dict(slug="tabbed", name="Tabbed", kicker="Electrician or plumber", g="#0A84FF", ink=WHITE, live=False,
      fan="home/plumber-answer.jpg", devices=[("pad", "home/ipad-answer.jpg", "An electrician answer on iPad with its NEC reference"), ("reg", "home/plumber-answer.jpg", "A plumber answer on iPhone with its UPC reference")],
      line="Exam prep for journeyman electricians and plumbers. Every answer cites the code section.",
      points=["Pick electrician or plumber at setup, each with its own questions and exams", "Practice questions with the explanation and the NEC, UPC or IPC reference", "Timed lookup drills, step-by-step calcs and practice exams in your exam's format"],
      screens=[("answer.jpg", "An electrician practice answer with explanation and code citation"), ("plumber/answer.jpg", "A plumber practice answer with explanation and code citation"),
               ("lookup.jpg", "A timed lookup drill with a countdown"), ("plumber/calc.jpg", "A plumbing calculation with every step shown")]),
 dict(slug="fantasyqueens", name="Fantasy Queens", g="#F8218A", ink=WHITE, live=False,
      fan="home/vote.jpg", devices=[("duo", "home/duo-home.jpg", "Fantasy Queens on the unfolded iPhone Duo"), ("reg", "home/vote.jpg", "The rules vote on iPhone")],
      line="Fantasy leagues for your Drag Race watch party. Pick your queens, vote on the rules, see who leads after every episode.",
      points=["Draft your queens with your watch-party group", "Vote on the rules before the premiere", "A leaderboard that updates after every episode"],
      screens=[("shot2.jpg", "Rules vote screen"), ("shot3.jpg", "Leaderboard after an episode"), ("shot4.jpg", "A house's queens")]),
 dict(slug="sitout", name="Sitout", g="#E2FB2C", ink=NAVY, live=False,
      fan="home/live.jpg", devices=[("max", "home/live.jpg", "A live round with scores on iPhone 17 Pro Max"), ("reg", "home/summary.jpg", "Night complete: the winner and standings")],
      line="Runs a pickleball round robin from one phone. Fair sit-outs, rotating partners, standings at the end of the night.",
      points=["Sit-outs shared evenly, every round", "Scores in two taps, late arrivals without lost scores", "Players never pay and never need the app"],
      screens=[("live.jpg", "A live round: who sits out, then each court with its teams and scores"), ("score.jpg", "Entering a score"), ("standings.jpg", "End-of-night standings ranked by win rate")]),
 dict(slug="statecount", name="Statecount", g="#4A8FD6", ink=NAVY, live=False,
      fan="home/home.jpg", devices=[("max", "home/home.jpg", "Days left for New York and Florida on iPhone 17 Pro Max (example data)"), ("reg", "home/calendar.jpg", "A calendar month colored by place (example data)")],
      line="For snowbirds, remote workers and second-home owners who need to know, and be able to show, how many days they spent where. Your location never leaves your phone.",
      points=["Any part of a day counts; travel days count for both places", "Every day shows where its record came from", "Day-by-day PDF and CSV report"],
      screens=[("home.jpg", "Days used and days left for New York and Florida (example data)"), ("calendar.jpg", "Calendar month colored by state (example data)")]),
 dict(slug="pocketarr", name="Pocketarr", g="#2DD4BF", ink=NAVY, live=False,
      line="For people who run their own media server. Your Sonarr, Radarr, Lidarr and Plex servers on your Lock Screen and Home Screen. No account. Pay once.",
      points=["Widgets for what's airing, the queue and server health", "Talks only to the servers you add", "One-time purchase, no subscription"],
      screens=[("dashboard.jpg", "Dashboard with server warnings and what's playing (demo data)"), ("calendar.jpg", "Calendar of upcoming episodes and movies (demo data)")]),
]
BY = {a["slug"]: a for a in APPS}
# The three fanned hero phones, each cycling through a few apps.
# An entry is an app slug (its "fan" screen, else its first screen), or (slug, screen, chip label, chip color).
COUCH = [["mackro", "stashday", "statecount"], ["mvn", "fantasyqueens", "sitout"], ["tabbed", "pocketarr"]]

e = lambda s: html.escape(s, quote=True)


def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


def _mix(a, b, t):
    return "#" + "".join(f"{round(int(a[i:i+2], 16) * (1 - t) + int(b[i:i+2], 16) * t):02X}" for i in (1, 3, 5))


def fill(g, ink):
    """The accent, darkened (white ink) or lightened (navy ink) just enough for 4.6:1 text contrast."""
    toward = NAVY if ink == WHITE else WHITE
    t = 0.0
    while contrast(_mix(g, toward, t), ink) < 4.6 and t < 1:
        t += .02
    return _mix(g, toward, t)


def img(slug, f, alt="", cls="", lazy=True):
    a = ' loading="lazy" decoding="async"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="/{slug}/img/{f}" alt="{e(alt)}" width="640" height="1390"{a}>'


def phone(screens, delay=0, label=None, lazy=True):
    """screens: list of (slug, file, alt). The first one shows without JavaScript."""
    imgs = "".join(img(s, f, alt, "on" if i == 0 else "", lazy) for i, (s, f, alt) in enumerate(screens))
    aria = f' role="img" aria-label="{e(label)}"' if label else ""
    return f'<div class="ph" data-delay="{delay}"{aria}><div class="scr">{imgs}</div></div>'


_PLAY = '<svg class="i-play" viewBox="0 0 14 16" aria-hidden="true"><path d="M1 1.5v13L13 8z" fill="currentColor"/></svg>'
_PAUSE = '<svg class="i-pause" viewBox="0 0 14 16" aria-hidden="true"><path d="M1 1h4v14H1zM9 1h4v14H9z" fill="currentColor"/></svg>'


def preview(slug, name, frame="ph", auto=True):
    """The app's App Store preview (/<slug>/img/preview.mp4 + .jpg poster) as a silent loop in a phone frame,
    with a Play/Pause button. auto plays it while on screen; otherwise it waits for a tap.
    The page needs /assets/preview.css and /assets/preview.js."""
    big = '<span class="pv-big" aria-hidden="true"><svg viewBox="0 0 14 16"><path d="M1 1.5v13L13 8z" fill="currentColor"/></svg></span>'
    return (f'<figure class="pvw" data-name="{e(name)}"{" data-auto" if auto else ""}>'
            f'<div class="{frame} pv idle"><div class="scr"><video src="/{slug}/img/preview.mp4" poster="/{slug}/img/preview.jpg" '
            f'muted loop playsinline controls preload="{"metadata" if auto else "none"}" width="592" height="1282" '
            f'aria-label="{e(name)} App Store preview, silent, with captions on screen"></video></div>{big}</div>'
            f'<button type="button" class="pv-btn" hidden>{_PLAY}{_PAUSE}<span>Play</span></button></figure>')


# Each app row can show a mix of devices instead of two iPhones: (kind, file, alt) where kind is
# max (iPhone Pro Max), reg (iPhone), pad (iPad, portrait), duo (iPhone Duo, unfolded) or watch (Apple Watch).
DEVICE_PX = {"max": (640, 1390), "reg": (640, 1390), "pad": (900, 1200), "duo": (760, 1106), "watch": (422, 514)}


def device(slug, kind, f, alt, speed):
    w, h = DEVICE_PX[kind]
    return (f'<div class="ph dv {kind}" role="img" aria-label="{e(alt)}" data-speed="{speed}"><div class="scr">'
            f'<img class="on" src="/{slug}/img/{f}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async"></div></div>')


def fan_phone(i, entries):
    items = [x if isinstance(x, tuple) else (x, BY[x].get("fan") or BY[x]["screens"][0][0], BY[x]["name"], BY[x]["g"]) for x in entries]
    slugs = [x[0] for x in items]
    screens = [(s, f, "") for s, f, _, _ in items]
    chips = "".join(f'<span class="chip{" on" if j == 0 else ""}" data-slug="{s}" style="--g:{g}"><img src="/{s}/img/icon.png" alt="" width="22" height="22">{e(n)}</span>' for j, (s, _, n, g) in enumerate(items))
    return (f'<a class="fp f{i}" href="#{slugs[0]}" tabindex="-1" data-speed="{(".03", "-.04", ".06")[i]}"><div class="rise">'
            f'<div class="chips">{chips}</div>{phone(screens, delay=i * 1100, lazy=False)}</div></a>')


def kick(a):
    return f'<span class="kick">{e(a["kicker"])}</span>' if a.get("kicker") else ""


def section(a, flip):
    s = a["slug"]
    tag = '<span class="tag live">On the App Store</span>' if a["live"] else '<span class="tag">Coming soon</span>'
    pts = "".join(f"<li>{e(p)}</li>" for p in a["points"])
    sc = a["screens"]
    one = [(s, f, alt) for f, alt in sc[0::2]]
    two = [(s, f, alt) for f, alt in (sc[1::2] or sc[:1])]
    phones = phone(one, 0, f"{a['name']} screens").replace('class="ph"', 'class="ph" data-speed="-.045"', 1) + phone(two, 1600, f"More {a['name']} screens").replace('class="ph"', 'class="ph" data-speed=".06"', 1)
    if a.get("devices"):
        phones = "".join(device(s, k, f, alt, sp) for (k, f, alt), sp in zip(a["devices"], ("-.045", ".06")))
    return f'''
    <section class="app{" flip" if flip else ""}" id="{s}" data-tint="{_mix(a["g"], "#EEF1FB", .84)}" style="--g:{a["g"]};--gf:{fill(a["g"], a["ink"])};--gi:{a["ink"]}" aria-labelledby="{s}-h">
      <div class="info">
        <div class="head"><img src="/{s}/img/icon.png" alt="" width="72" height="72" loading="lazy"><div><h2 id="{s}-h">{e(a["name"])}</h2>{tag}{kick(a)}</div></div>
        <p class="line">{e(a["line"])}</p>
        <ul>{pts}</ul>
        <a class="go" href="/{s}/">See {e(a["name"])}</a>
      </div>
      <div class="shots">{phones}</div>
    </section>'''


CSS = r'''
@font-face{font-family:"Manrope";font-style:normal;font-weight:200 800;font-display:swap;src:url(/fonts/manrope-latin-wght-normal.woff2) format("woff2-variations"),url(/fonts/manrope-latin-wght-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/dm-sans-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/dm-sans-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"DM Sans";font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/dm-sans-latin-700-normal.woff2) format("woff2")}
:root{--paper:#EEF1FB;--ink:#0B1A4A;--soft:#3D4A75;--cobalt:#1857E1;--deep:#0F3BB0;--mist:#DCE4FB;--coral:#FF7A59;--mint:#3DDBB0;--sun:#FFC83D;--lav:#A98BFF;--pink:#FF6FB5;--line:rgba(11,26,74,.12);
  --body:"DM Sans",system-ui,-apple-system,sans-serif;--disp:"Manrope",system-ui,-apple-system,sans-serif;color-scheme:light}
*{box-sizing:border-box}
html{overflow-x:clip;scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--tint,var(--paper));transition:background-color .9s ease;color:var(--ink);font:17px/1.55 var(--body);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:inherit}
img{max-width:100%;height:auto}
:focus-visible{outline:3px solid var(--cobalt);outline-offset:3px;border-radius:10px}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:12px;z-index:30;background:#fff;padding:8px 14px;border-radius:10px}

/* top bar: one centered pill that stays put */
.top{position:sticky;top:12px;z-index:20;display:flex;justify-content:center;padding:16px 16px 0;pointer-events:none}
.bar{pointer-events:auto;display:inline-flex;align-items:center;gap:2px;padding:5px;border-radius:99px;background:rgba(255,255,255,.82);-webkit-backdrop-filter:blur(16px) saturate(1.5);backdrop-filter:blur(16px) saturate(1.5);box-shadow:0 0 0 1px var(--line),0 14px 34px -20px rgba(11,26,74,.55)}
.bar a{white-space:nowrap;text-decoration:none;font-weight:700;font-size:.93rem;padding:9px 17px;border-radius:99px;color:var(--ink);transition:background .2s}
.bar a:hover{background:var(--mist)}
.bar a.c{background:var(--cobalt);color:#fff}
.bar a.c:hover{background:var(--deep)}

.hero{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:center;padding:36px 0 40px}
.logo{display:block;width:min(340px,78%);height:auto;margin:0 0 30px}
h1{font:800 clamp(2.6rem,5.4vw,4.6rem)/.98 var(--disp);letter-spacing:-.045em;margin:0 0 20px;text-wrap:balance}
.lede{font-size:1.2rem;color:var(--soft);max-width:28em;margin:0 0 28px}
.cta{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;text-decoration:none;font-weight:700;padding:14px 24px;border-radius:99px;background:var(--cobalt);color:#fff;box-shadow:0 12px 24px -12px rgba(24,87,225,.8);transition:transform .2s,background .2s}
.btn:hover{background:var(--deep);transform:translateY(-1px)}
.btn.alt{background:#fff;color:var(--ink);box-shadow:inset 0 0 0 2px rgba(11,26,74,.22)}
.btn.alt:hover{background:var(--mist)}

/* three phones, fanned at different depths */
.fan{position:relative;height:640px;margin-top:20px;transform:perspective(1400px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.fan:before{content:"";position:absolute;left:12%;right:12%;bottom:4%;height:16%;border-radius:50%;background:radial-gradient(closest-side,rgba(11,26,74,.22),transparent);filter:blur(6px)}
.fp{position:absolute;display:block;text-decoration:none;will-change:translate}
.fp.f0{left:4%;top:92px;width:30%;rotate:-9deg;z-index:1}
.fp.f1{left:33%;top:24px;width:34%;z-index:3}
.fp.f2{right:3%;top:104px;width:30%;rotate:8deg;z-index:2}
.fp .ph{animation:bob 7s ease-in-out infinite}
.fp.f0 .ph{animation-delay:-2.5s}.fp.f2 .ph{animation-delay:-5s}
.rise{animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both}
.f0 .rise{animation-delay:.15s}.f1 .rise{animation-delay:.3s}.f2 .rise{animation-delay:.45s}
@keyframes rise{0%{transform:translateY(80px) scale(.94);opacity:0}100%{transform:none;opacity:1}}
@keyframes bob{0%,100%{translate:0 0}50%{translate:0 -10px}}
.fp:hover .ph{animation-play-state:paused}
.chips{position:absolute;left:50%;top:-14px;translate:-50% -100%;height:34px;width:0;z-index:5}
.f1 .chips{top:-18px}
.chip{position:absolute;left:50%;top:0;translate:-50% 0;width:max-content;display:flex;align-items:center;gap:7px;white-space:nowrap;padding:5px 13px 5px 6px;border-radius:99px;background:#fff;color:var(--ink);font:700 .8rem var(--body);box-shadow:0 0 0 1.5px color-mix(in srgb,var(--g) 70%,transparent),0 10px 22px -12px var(--g);opacity:0;transition:opacity .6s}
.chip.on{opacity:1}
.chip img{width:22px;height:22px;border-radius:6px}

/* the sky: colored shapes at different depths behind the hero */
main{position:relative}
.sky{position:absolute;left:0;right:0;top:-120px;height:1100px;overflow:hidden;pointer-events:none;z-index:0}
.sky:before{content:"";position:absolute;inset:0;background:radial-gradient(30% 32% at 12% 72%,rgba(255,122,89,.20),transparent 70%),radial-gradient(28% 30% at 88% 18%,rgba(61,219,176,.22),transparent 70%),radial-gradient(34% 36% at 62% 70%,rgba(169,139,255,.22),transparent 70%),radial-gradient(22% 24% at 40% 8%,rgba(255,200,61,.20),transparent 70%)}
.sh{position:absolute;will-change:transform}
.sh svg{display:block;width:100%;height:100%;animation:float 9s ease-in-out infinite}
.sh:nth-child(2n) svg{animation-duration:11s;animation-direction:reverse}
.sh:nth-child(3n) svg{animation-duration:13s}
@keyframes float{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-14px) rotate(8deg)}}
.hero,.pick,.rows{position:relative;z-index:1}
.shots{transform:perspective(1100px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.shots .ph{will-change:translate}

/* iPhone */
.ph{position:relative;padding:3.6%;border-radius:17% / 7.8%;background:linear-gradient(150deg,#3a4152,#11141c 42%,#2a2f3b);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.22),0 0 0 1px rgba(11,26,74,.35),0 34px 60px -26px rgba(11,26,74,.65)}
.ph:before{content:"";position:absolute;right:-1.4%;top:20%;width:1.6%;height:11%;border-radius:0 3px 3px 0;background:#2a2f3b}
.ph:after{content:"";position:absolute;top:5.2%;left:50%;width:30%;height:3.4%;translate:-50% 0;border-radius:99px;background:#000;z-index:2}
.scr{position:relative;aspect-ratio:640/1390;border-radius:13.5% / 6.2%;overflow:hidden;background:#000;isolation:isolate}
.scr img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .8s ease}
.scr img.on{opacity:1}
/* other devices (the .ph base above is an iPhone) */
.shots .ph.dv{min-width:0}
.shots .ph.max{flex-basis:268px}
.shots .ph.reg{flex-basis:226px}
.ph.pad{padding:2.4%;border-radius:6.4% / 4.8%}
.ph.pad:before{right:16%;top:-.9%;width:10%;height:.9%;border-radius:3px 3px 0 0}
.ph.pad:after{display:none}
.ph.pad .scr{aspect-ratio:3/4;border-radius:4.2% / 3.2%}
.shots .ph.pad{flex-basis:380px}
.ph.duo{padding:2.2%;border-radius:8.4% / 5.8%}
.ph.duo:after{top:2.2%;bottom:2.2%;height:auto;width:2px;translate:-1px 0;border-radius:0;background:linear-gradient(transparent,rgba(255,255,255,.22) 6%,rgba(0,0,0,.22) 50%,rgba(255,255,255,.22) 94%,transparent)}
.ph.duo .scr{aspect-ratio:1398/2034;border-radius:6.2% / 4.3%}
.shots .ph.duo{flex-basis:350px}
.ph.watch{padding:6%;border-radius:32% / 26%}
.ph.watch:before{right:-5.5%;top:22%;width:6%;height:19%;border-radius:0 7px 7px 0;background:linear-gradient(90deg,#2a2f3b,#5a6170)}
.ph.watch:after{top:-24%;bottom:-24%;left:17%;right:17%;width:auto;height:auto;translate:none;border-radius:22px;background:linear-gradient(#3a4152,#2a2f3b 50%,#3a4152);z-index:-1}
.ph.watch .scr{aspect-ratio:422/514;border-radius:26% / 21%}
.shots .ph.watch{flex-basis:190px;align-self:center;margin-right:8px}
.shots .ph.watch+.ph,.shots .ph+.ph.watch{margin-top:0}

/* picker */
.pick{display:flex;flex-wrap:wrap;justify-content:center;gap:4px;padding:30px 0 56px;border-bottom:1px solid var(--line)}
.pick a{display:flex;flex-direction:column;align-items:center;gap:8px;width:104px;padding:12px 6px;border-radius:22px;text-decoration:none;font-weight:700;font-size:.82rem;line-height:1.2;text-align:center;color:var(--ink);transition:transform .3s cubic-bezier(.3,1.5,.4,1),background .25s}
.pick img{width:68px;height:68px;border-radius:16px;box-shadow:0 10px 22px -12px rgba(11,26,74,.6);transition:transform .35s cubic-bezier(.3,1.6,.4,1)}
.pick a:hover,.pick a:focus-visible{transform:translateY(-4px);background:#fff}
.pick a:hover img{transform:rotate(-5deg) scale(1.06)}

/* app rows */
.app{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:center;padding:84px 0;border-bottom:1px solid var(--line)}
.app:last-child{border-bottom:0}
.app.flip .info{order:2}
.head{display:flex;align-items:center;gap:18px}
.head img{width:72px;height:72px;border-radius:17px;box-shadow:0 14px 30px -14px var(--g)}
h2{font:800 clamp(1.9rem,3.6vw,2.7rem)/1.02 var(--disp);letter-spacing:-.04em;margin:0 0 8px}
.tag{display:inline-block;font-size:.78rem;font-weight:700;padding:4px 11px;border-radius:99px;background:var(--mist);color:var(--ink)}
.tag.live{background:var(--gf);color:var(--gi)}
.kick{display:inline-block;margin-left:8px;font-size:.85rem;font-weight:700;color:var(--soft)}
.line{font-size:1.22rem;line-height:1.45;margin:24px 0 18px;max-width:28em}
.info ul{list-style:none;margin:0 0 28px;padding:0;display:grid;gap:10px;max-width:30em}
.info li{position:relative;padding-left:28px;color:var(--soft)}
.info li:before{content:"";position:absolute;left:0;top:.42em;width:14px;height:14px;border-radius:5px;background:var(--g);box-shadow:inset 0 0 0 1px rgba(11,26,74,.2)}
.go{display:inline-block;font-weight:700;text-decoration:none;color:var(--gi);background:var(--gf);padding:13px 24px;border-radius:99px;box-shadow:0 12px 24px -14px var(--g),inset 0 0 0 1px rgba(11,26,74,.12);transition:transform .2s,filter .2s}
.go:hover{transform:translateY(-1px);filter:saturate(1.1)}
.shots{position:relative;display:flex;justify-content:center;align-items:flex-start;gap:22px}
.shots:before{content:"";position:absolute;inset:10% 4% 6%;border-radius:50%;background:var(--g);filter:blur(70px);opacity:.32;z-index:0}
.shots .ph{position:relative;z-index:1;flex:0 1 250px}
.shots .ph+.ph{margin-top:56px}
.app .shots .ph{transition:transform 1s cubic-bezier(.2,.8,.2,1),opacity .8s}
.js .app:not(.in) .shots .ph{transform:translateY(40px) rotate(3deg);opacity:0}
.js .app:not(.in) .shots .ph+.ph{transform:translateY(70px) rotate(-3deg)}
.app.in .shots .ph+.ph{transition-delay:.12s}

/* studio band */
.studio{background:var(--cobalt);color:#fff;padding:110px 0;position:relative;overflow:hidden;isolation:isolate}
.studio .wrap{position:relative;z-index:1}
.blob{position:absolute;border-radius:50%;filter:blur(60px);opacity:.55;z-index:0;will-change:translate}
.blob.b1{width:420px;height:420px;background:var(--coral);left:-120px;bottom:-160px}
.blob.b2{width:360px;height:360px;background:var(--mint);right:8%;top:-160px;opacity:.4}
.blob.b3{width:300px;height:300px;background:var(--lav);right:-80px;bottom:-120px;opacity:.6}
.studio:before{content:"";position:absolute;right:-12%;top:-30%;width:60%;aspect-ratio:1;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.14),transparent);pointer-events:none}
.studio h2{font-size:clamp(2.4rem,5.4vw,4.4rem);line-height:.98;letter-spacing:-.045em;max-width:12em;margin:0 0 48px;text-wrap:balance}
.say{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px}
.say p{font-size:1.18rem;line-height:1.6;margin:0;color:#fff}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:56px}
.fact{display:flex;flex-direction:column;border-radius:30px;padding:26px;background:rgba(255,255,255,.1);box-shadow:inset 0 0 0 1px rgba(255,255,255,.24);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.fact .fv{height:150px;display:grid;place-items:center;margin-bottom:14px;border-radius:22px;background:rgba(11,26,74,.22)}
.fnum{font:800 4.2rem/1 var(--disp);letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.fact:nth-child(1) .fnum{color:#FFD45E}.fact:nth-child(2) .fnum{color:#8FF0D2}.fact:nth-child(3) .fnum{color:#FFC6E2}
.fact p{margin:6px 0 0;font-size:1.06rem;color:#fff}
.fact small{display:block;margin-top:auto;padding-top:14px;font-size:.9rem;color:#fff}
.fact small a{color:#fff;font-weight:700}
.igrid{display:grid;grid-template-columns:repeat(3,40px);gap:10px}
.igrid i{position:relative;display:block}
.igrid img{display:block;width:40px;height:40px;border-radius:10px;box-shadow:0 8px 16px -8px rgba(0,0,0,.55);transform:scale(.3);opacity:0;transition:transform .55s cubic-bezier(.3,1.6,.4,1),opacity .4s;transition-delay:calc(var(--i) * 70ms)}
.igrid i.soon:after{content:"";position:absolute;right:-3px;top:-3px;width:11px;height:11px;border-radius:50%;background:#FFD45E;box-shadow:0 0 0 2px #1857E1;opacity:0;transition:opacity .3s .8s}
.in .igrid img{transform:none;opacity:1}.in .igrid i.soon img{opacity:.62;filter:saturate(.6)}.in .igrid i.soon:after{opacity:1}
.noad svg,.inbox svg{width:150px;height:auto;overflow:visible}
.noad .slash{stroke-dasharray:170;stroke-dashoffset:170;transition:stroke-dashoffset .7s cubic-bezier(.6,0,.2,1) .35s}
.noad .badge{transform-origin:80px 55px;transition:transform .5s cubic-bezier(.3,1.6,.4,1) .9s}
.in .noad .slash{stroke-dashoffset:0}.in .noad .badge{transform:rotate(-4deg) scale(.96)}
.inbox .env{animation:hover 5s ease-in-out infinite}
.inbox .tick{transform-origin:126px 26px;transform:scale(0);transition:transform .5s cubic-bezier(.3,1.6,.4,1) .5s}
.in .inbox .tick{transform:none}
@keyframes hover{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}

/* house rules: three cushions */
.rules{padding:96px 0 40px;text-align:center}
.rules h2{margin-bottom:12px}
.rules>p{color:var(--soft);font-size:1.15rem;max-width:32em;margin:0 auto 40px}
.cush{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;max-width:980px;margin:0 auto;padding:12px;border-radius:44px;background:var(--deep)}
.cush div{background:#2C62DB;border-radius:34px;padding:34px 28px 30px;text-align:left;color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -10px 22px -14px rgba(8,30,110,.55);transition:transform .35s cubic-bezier(.3,1.5,.4,1)}
.cush div:hover{transform:translateY(-6px) scale(1.01)}
.cush h3{font:800 1.35rem/1.15 var(--disp);letter-spacing:-.03em;margin:0 0 8px}
.cush p{margin:0;color:#EAF0FF}
.cush a{color:#fff}
.help+.help{margin-top:16px}
.help{text-align:left;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;max-width:980px;margin:56px auto 0;padding:34px 36px;border-radius:30px;background:#fff;box-shadow:0 0 0 1px var(--line)}
.help h3{font:800 1.5rem/1.1 var(--disp);letter-spacing:-.03em;margin:0 0 6px}
.help p{margin:0;color:var(--soft)}
footer{padding:64px 0 56px;color:var(--soft);font-size:.92rem;text-align:center}
footer p{margin:6px 0}
footer nav{display:flex;justify-content:center;flex-wrap:wrap;gap:4px 18px;margin-bottom:14px}
footer nav a{font-weight:700;text-decoration:none;color:var(--ink)}
footer nav a:hover{color:var(--cobalt)}
.fine{font-size:.8rem;max-width:46em;margin:14px auto 0}

@media(max-width:960px){
  .hero{grid-template-columns:minmax(0,1fr);gap:8px;text-align:center;padding-top:28px}
  .hero .logo{margin:0 auto 26px;width:min(300px,76%)}
  .lede{margin-left:auto;margin-right:auto}
  .cta{justify-content:center}
  .fan{width:100%;max-width:560px;height:560px;margin:56px auto 0}
  .app{grid-template-columns:minmax(0,1fr);gap:40px;padding:64px 0}
  .app.flip .info{order:0}
  .cush{grid-template-columns:minmax(0,1fr);border-radius:36px}
  .help{grid-template-columns:minmax(0,1fr)}
  .say{grid-template-columns:minmax(0,1fr);gap:16px}
  .facts{grid-template-columns:minmax(0,1fr);margin-top:40px}
  .studio{padding:80px 0}
}
@media(max-width:560px){
  .wrap{padding:0 16px}
  .top{top:8px;padding:10px 10px 0}
  .bar a{font-size:.86rem;padding:8px 12px}
  h1{font-size:2.5rem}
  .lede{font-size:1.08rem}
  .chip{font-size:.7rem;padding:4px 10px 4px 5px;gap:5px}.chip img{width:18px;height:18px}
  .chips{top:-8px}.f1 .chips{top:-10px}
  .f0 .chip{translate:-30% 0}.f2 .chip{translate:-74% 0}
  .fan{height:min(110vw,470px);margin-top:48px}
  .pick a{width:84px;font-size:.76rem}.pick img{width:58px;height:58px}
  .shots{gap:14px}.shots .ph+.ph{margin-top:36px}
  .sh{display:none}
  .sky{height:900px}
  .fnum{font-size:3.4rem}.fact .fv{height:130px}
  .help{padding:28px 24px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rise,.fp .ph,.sh svg,.inbox .env{animation:none}
  .igrid img,.noad .slash,.noad .badge,.inbox .tick{transition:none}
  .fan{transform:none}
  .shots{transform:none}
  .js .app:not(.in) .shots .ph,.js .app:not(.in) .shots .ph+.ph{transform:none;opacity:1}
  .scr img,.chip,.pick a,.pick img{transition:none}
}
'''

JS = r'''
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rows = document.querySelectorAll('.app');
  if (!('IntersectionObserver' in window)) { document.querySelectorAll('.app,.fact').forEach(function(r){ r.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, {threshold:.18});
  rows.forEach(function(r){ io.observe(r); });
  // The page takes on a soft tint of whichever app you're looking at.
  var root = document.documentElement;
  var tio = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) root.style.setProperty('--tint', en.target.dataset.tint || ''); }); }, {rootMargin:'-45% 0px -45% 0px'});
  rows.forEach(function(r){ tio.observe(r); });
  var hero = document.querySelector('.hero'), rules = document.querySelector('.rules');
  var pio = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) root.style.removeProperty('--tint'); }); }, {rootMargin:'-45% 0px -45% 0px'});
  [hero, rules].forEach(function(x){ if (x) pio.observe(x); });

  // Count the studio numbers up when they come into view.
  var cio = new IntersectionObserver(function(es){ es.forEach(function(en){
    if (!en.isIntersecting) return; cio.unobserve(en.target);
    if (reduce) return;
    var dt = en.target, to = +dt.dataset.count, t0 = performance.now();
    (function tick(t){ var k = Math.min(1, (t - t0) / 900); dt.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); })(t0);
  }); }, {threshold:.6});
  document.querySelectorAll('[data-count]').forEach(function(d){ cio.observe(d); });
  var fio = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); fio.unobserve(en.target); } }); }, {threshold:.35});
  document.querySelectorAll('.fact').forEach(function(f){ reduce ? f.classList.add('in') : fio.observe(f); });

  if (reduce) return;

  // Parallax: things with data-speed drift against the scroll; hero shapes also lean toward the pointer.
  var par = [].slice.call(document.querySelectorAll('[data-speed]'));
  var px = 0, py = 0, tx = 0, ty = 0, ticking = false;
  function frame(){
    ticking = false;
    var vh = innerHeight;
    tx += (px - tx) * .08; ty += (py - ty) * .08;
    par.forEach(function(el){
      var r = el.getBoundingClientRect();
      if (r.bottom < -400 || r.top > vh + 400) return;
      var y = ((r.top + r.height / 2) - vh / 2) * -(+el.dataset.speed);
      var d = +el.dataset.depth || 0;
      el.style.translate = (tx * d).toFixed(1) + 'px ' + (y + ty * d).toFixed(1) + 'px';
    });
    if (Math.abs(px - tx) > .002 || Math.abs(py - ty) > .002) request();
  }
  function request(){ if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', request, {passive:true}); addEventListener('resize', request);
  if (matchMedia('(pointer: fine)').matches) {
    addEventListener('pointermove', function(ev){ px = ev.clientX / innerWidth - .5; py = ev.clientY / innerHeight - .5; request(); }, {passive:true});
    // Tilt each pair of phones toward the pointer.
    document.querySelectorAll('.shots,.fan').forEach(function(s){
      s.addEventListener('pointermove', function(ev){ var r = s.getBoundingClientRect(); s.style.setProperty('--ry', (((ev.clientX - r.left) / r.width - .5) * 14).toFixed(2) + 'deg'); s.style.setProperty('--rx', (-((ev.clientY - r.top) / r.height - .5) * 10).toFixed(2) + 'deg'); });
      s.addEventListener('pointerleave', function(){ s.style.setProperty('--ry', '0deg'); s.style.setProperty('--rx', '0deg'); });
    });
  }
  request();

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
    var fp = p.closest('.fp');
    if (fp) {
      var chips = fp.querySelectorAll('.chip');
      chips[i].classList.remove('on'); chips[n].classList.add('on');
      fp.setAttribute('href', '#' + chips[n].dataset.slug);
    }
  }
  phones.forEach(function(p){
    setTimeout(function(){ step(p); setInterval(function(){ step(p); }, 3800); }, 2600 + (+p.dataset.delay || 0));
  });
})();
'''


SKY = (
 ('left:46%;top:650px;width:74px;height:74px', '.35', '', '<svg viewBox="0 0 74 74"><circle cx="37" cy="37" r="30" fill="none" stroke="#FF7A59" stroke-width="10"/></svg>'),
 ('left:41%;top:170px;width:96px;height:96px', '-.18', 'm-hide', '<svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="#FF7A59"/></svg>'),
 ('right:3%;top:190px;width:150px;height:58px', '.3', '', '<svg viewBox="0 0 150 58"><rect width="150" height="58" rx="29" fill="#3DDBB0" transform="rotate(-18 75 29)"/></svg>'),
 ('right:31%;top:120px;width:22px;height:22px', '.55', 'm-hide', '<svg viewBox="0 0 22 22"><circle cx="11" cy="11" r="11" fill="#FFC83D"/></svg>'),
 ('left:50%;top:760px;width:70px;height:70px', '.45', 'm-hide', '<svg viewBox="0 0 70 70"><path d="M35 0C38 22 48 32 70 35C48 38 38 48 35 70C32 48 22 38 0 35C22 32 32 22 35 0Z" fill="#FFC83D"/></svg>'),
 ('right:5%;top:840px;width:170px;height:50px', '.22', '', '<svg viewBox="0 0 170 50"><path d="M6 30C26 4 42 4 58 26S92 48 108 24S144 2 164 22" fill="none" stroke="#A98BFF" stroke-width="11" stroke-linecap="round"/></svg>'),
 ('left:46%;top:430px;width:30px;height:30px', '.65', 'm-hide', '<svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="15" fill="#FF6FB5"/></svg>'),
 ('right:44%;top:880px;width:58px;height:58px', '.4', 'm-hide', '<svg viewBox="0 0 58 58"><rect x="6" y="6" width="46" height="46" rx="12" fill="#A98BFF" transform="rotate(16 29 29)"/></svg>'),
)


def build():
    sky = "".join(f'<div class="sh {c}" data-speed="{sp}" data-depth="{float(sp) * 40:.0f}" style="{st}">{svg}</div>' for st, sp, c, svg in SKY)
    fan = "".join(fan_phone(i, s) for i, s in enumerate(COUCH))
    live = sum(1 for a in APPS if a["live"])
    grid = "".join(f'<i class="{"" if a["live"] else "soon"}" style="--i:{k}"><img src="/{a["slug"]}/img/icon.png" alt="" width="40" height="40" loading="lazy"></i>' for k, a in enumerate(APPS))
    facts = f'''<div class="facts">
      <div class="fact"><div class="fv" aria-hidden="true"><div class="igrid">{grid}</div></div><div class="fnum" data-count="{len(APPS)}">{len(APPS)}</div><p>iPhone apps, out now or on the way</p><small>{live} on the App Store, {len(APPS) - live} on the way (the ones with a dot).</small></div>
      <div class="fact"><div class="fv noad" aria-hidden="true"><svg viewBox="0 0 160 110"><g class="badge"><rect x="12" y="18" width="136" height="74" rx="18" fill="rgba(255,255,255,.14)" stroke="#fff" stroke-width="4"/><text x="80" y="70" text-anchor="middle" font-family="Manrope, sans-serif" font-weight="800" font-size="44" fill="#fff">AD</text></g><path class="slash" d="M22 100 138 10" stroke="#8FF0D2" stroke-width="11" stroke-linecap="round" fill="none"/></svg></div><div class="fnum">0</div><p>ads in any of them</p><small>No ad networks, no trackers selling your attention.</small></div>
      <div class="fact"><div class="fv inbox" aria-hidden="true"><svg viewBox="0 0 160 110"><g class="env"><rect x="16" y="24" width="120" height="78" rx="14" fill="#fff"/><path d="M20 32 76 72l56-40" fill="none" stroke="#1857E1" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g><g class="tick"><circle cx="126" cy="26" r="20" fill="#FFC6E2"/><path d="m116 26 7 7 13-14" fill="none" stroke="#1857E1" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g></svg></div><div class="fnum" data-count="1">1</div><p>inbox, read by the people who built the app</p><small><a href="mailto:{SUPPORT}">{SUPPORT}</a></small></div>
    </div>'''
    picker = "".join(f'<a href="#{a["slug"]}"><img src="/{a["slug"]}/img/icon.png" alt="" width="68" height="68">{e(a["name"])}</a>' for a in APPS)
    rows = "".join(section(a, i % 2 == 1) for i, a in enumerate(APPS))
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Couch Co-Op Studios", "url": f"{SITE}/",
         "description": "Small, useful iPhone apps with fair prices, clear privacy and real support.",
         "publisher": {"@type": "Organization", "name": "Couch Co-Op Studios", "url": f"{SITE}/"}},
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
<header class="top"><nav class="bar" aria-label="Site"><a href="#apps">Apps</a><a href="#studio">Studio</a><a href="#rules">House rules</a><a class="c" href="mailto:hello@couchcoopstudios.com">Contact</a></nav></header>
<main>
<div class="sky" aria-hidden="true">{sky}</div>
<div class="wrap">
  <section class="hero" aria-labelledby="hero-h">
    <div>
      <img class="logo" src="/assets/brand/couch-co-op-studios-mark-600.png" alt="Couch Co-Op Studios" width="607" height="380">
      <h1 id="hero-h">Small apps, made together.</h1>
      <p class="lede">We're an independent iPhone studio. Our team designs, builds and supports small apps for game night, everyday life and the oddly specific problem you wish somebody would just solve.</p>
      <div class="cta"><a class="btn" href="#apps">See our apps</a><a class="btn alt" href="mailto:hello@couchcoopstudios.com">Say hello</a></div>
    </div>
    <div class="fan" aria-hidden="true">{fan}</div>
  </section>
  <nav class="pick" id="apps" aria-label="Jump to an app">{picker}</nav>
  <div class="rows">{rows}
  </div>
</div>
<section class="studio" id="studio" aria-labelledby="studio-h">
  <div class="blob b1" data-speed=".12" aria-hidden="true"></div><div class="blob b2" data-speed="-.1" aria-hidden="true"></div><div class="blob b3" data-speed=".08" aria-hidden="true"></div>
  <div class="wrap">
    <h2 id="studio-h">A small studio with a big couch.</h2>
    <div class="say">
      <p>Couch Co-Op Studios started the way most good ideas do: a couple of people on a couch, wishing an app worked a little better. So we made it ourselves.</p>
      <p>Our team does everything in-house. We design every screen, write every line, and answer every support email. If an app has our name on it, we use it too.</p>
    </div>
    {facts}
  </div>
</section>
<div class="wrap">
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
    <div class="help">
      <div><h3>Try our apps before they launch</h3><p>Use a test version for real and tell us what to fix. Free and invite-only for now, through Apple's TestFlight.</p></div>
      <a class="btn alt" href="/testers/">Become a tester</a>
    </div>
  </section>
</div>
</main>
<footer>
  <div class="wrap">
    <nav aria-label="Apps">{"".join(f'<a href="/{a["slug"]}/">{e(a["name"])}</a>' for a in APPS)}</nav>
    <p>&copy; 2026 Couch Co-Op Studios. <a href="/testers/">Become a tester</a></p>
    <p class="fine">Apple, the Apple logo and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc.</p>
  </div>
</footer>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build())
    print("wrote index.html")
