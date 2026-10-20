#!/usr/bin/env python3
"""Builds the "Become a tester" page, testers/index.html, for couchcoopstudios.com.

Run from the repo root:  python3 tools/testers.py
Edit TESTERS below and re-run. The whole file is rewritten, so don't hand-edit testers/index.html.
Testing is invite-only for now (no public TestFlight links while App Review is strict), so every "link" is None
and each card asks people to email for an invite. To show a public link later, paste it into that app's "link" and re-run. Uses the hub's styles and app colors (tools/hub.py).
No em dashes (house style). No personal names.
"""
import json, pathlib, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import hub  # noqa: E402
from hub import BY, SITE, SUPPORT, e, fill, kick, phone  # noqa: E402

HELLO = "hello@couchcoopstudios.com"
TESTFLIGHT_APP = "https://apps.apple.com/app/testflight/id899247664"

TESTERS = [
 dict(slug="sitout", link=None,
      what="Runs a pickleball round robin from one phone: fair sit-outs, rotating partners, two-tap scoring and standings at the end of the night.",
      who="Whoever organizes open play, a ladder or a weekly round robin. Players never need the app; only the organizer holds the phone.",
      ask=["Did the sit-outs feel fair to your group?", "Was scoring quick enough between games?", "What happened when someone arrived late or left early?"]),
 dict(slug="stashday", link=None,
      what="Turns the bills you pay once in a while (insurance, gifts, car registration, annual subscriptions) into one amount to set aside each payday.",
      who="Anyone who budgets by paycheck and keeps getting surprised by the bills that don't come every month.",
      ask=["Did the per-paycheck amount make sense for your real bills?", "Was any step of setup confusing?", "Which fund or bill type was missing?"]),
 dict(slug="statecount", link=None,
      what="Keeps a day-by-day record of which state or country you're in and warns you before a limit you set, like 183 days. Your location never leaves your phone.",
      who="Snowbirds, remote workers and second-home owners who split the year between places and need to count the days.",
      ask=["Did it log the right place each day?", "Did battery use look normal over a week?", "Was anything about permissions, limits or the report unclear?"]),
 dict(slug="tabbed", link=None,
      what="Exam prep for the journeyman electrician or plumber license. Pick your trade at setup, then get daily questions with explanations, calculation and code lookup drills, and timed practice exams.",
      who="Electrical and plumbing apprentices getting ready for the journeyman exam, and the journeymen and instructors who help them. Tell us which trade you're studying.",
      ask=["Any answer you think is wrong (tell us the code section)", "Any explanation that didn't help", "Anything that slowed your studying down"]),
 dict(slug="fantasyqueens", link=None,
      what="Fantasy leagues for a Drag Race watch party: pick your queens, vote on the rules, call the lip sync and see who leads after every episode.",
      who="Watch-party groups of three or more friends who already gather for each episode.",
      ask=["What made episode night more fun?", "What slowed the group down or needed explaining?", "Did the TV view work on your setup?"]),
]

CSS = r'''
.thero{position:relative;z-index:1;max-width:760px;margin:0 auto;padding:40px 0 24px;text-align:center}
.thero .logo{margin:0 auto 26px;width:min(260px,70%)}
.thero .lede{margin-left:auto;margin-right:auto}
.thero .cta{justify-content:center}
.cards{position:relative;z-index:1;display:grid;gap:28px;padding:40px 0 24px}
.card{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:48px;align-items:center;padding:40px 48px;border-radius:36px;background:#fff;box-shadow:0 0 0 1px var(--line),0 30px 60px -44px var(--g);overflow:hidden;position:relative;isolation:isolate}
.card:before{content:"";position:absolute;right:-60px;top:-60px;width:420px;height:420px;border-radius:50%;background:var(--g);filter:blur(80px);opacity:.22;z-index:-1}
.card .head{margin-bottom:22px}
.card h2{font-size:clamp(1.7rem,3vw,2.2rem)}
.tag.open{background:var(--gf);color:var(--gi)}
.card dl{margin:0;display:grid;gap:16px}
.card dt{font:800 .78rem/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0 0 6px}
.card dd{margin:0}
.card ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.card li{position:relative;padding-left:26px;color:var(--soft)}
.card li:before{content:"";position:absolute;left:0;top:.42em;width:13px;height:13px;border-radius:4px;background:var(--g);box-shadow:inset 0 0 0 1px rgba(11,26,74,.2)}
.join{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:28px}
.join .go{margin:0}
.join .more{font-weight:700;color:var(--ink)}
.join .alt{flex-basis:100%;margin:0;font-size:.92rem;color:var(--soft)}
.join .alt b{color:var(--ink)}
.copy{font:700 .85rem/1 var(--body);border:0;border-radius:99px;padding:7px 14px;margin-left:6px;background:var(--ink);color:var(--bg);cursor:pointer}
.card .ph{width:100%;max-width:220px;justify-self:center}
.steps{counter-reset:s}
.steps h3:before{counter-increment:s;content:counter(s);display:grid;place-items:center;width:40px;height:40px;margin-bottom:14px;border-radius:12px;background:var(--cobalt);color:#fff;font:800 1.1rem var(--disp)}
.steps a{font-weight:700}
.know{max-width:980px;margin:56px auto 0;text-align:left;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 40px}
.know p{margin:0;color:var(--soft)}
.know strong{color:var(--ink)}
@media(max-width:960px){
  .card{grid-template-columns:minmax(0,1fr);gap:32px;padding:32px 28px}
  .card .ph{max-width:200px}
  .know{grid-template-columns:minmax(0,1fr)}
}
@media(max-width:560px){
  .thero{padding-top:28px}
  .card{padding:28px 22px;border-radius:30px}
  .card .ph{max-width:170px}
}
'''


def card(t):
    a = BY[t["slug"]]
    s = a["slug"]
    if t["link"]:
        tag = '<span class="tag open">Open now</span>'
        join = (f'<a class="go" href="{e(t["link"])}">Join the {e(a["name"])} beta</a>'
                f'<a class="more" href="/{s}/">About {e(a["name"])}</a>')
    else:
        tag = '<span class="tag">Invite only</span>'
        subject = f"Invite me to test {a['name']}"
        join = (f'<a class="go" href="mailto:{HELLO}?subject={urllib.parse.quote(subject)}">Ask for a {e(a["name"])} invite</a>'
                f'<a class="more" href="/{s}/">About {e(a["name"])}</a>'
                f'<p class="alt">No email app? Write to <b>{HELLO}</b> and say which app. '
                f'<button type="button" class="copy" data-copy="{HELLO}">Copy address</button></p>')
    ask = "".join(f"<li>{e(x)}</li>" for x in t["ask"])
    shot = phone([(s, f, alt) for f, alt in a["screens"][:1]], label=f"{a['name']} screen")
    return f'''
    <article class="card" id="{s}" style="--g:{a["g"]};--gf:{fill(a["g"], a["ink"])};--gi:{a["ink"]}" aria-labelledby="{s}-h">
      <div>
        <div class="head"><img src="/{s}/img/icon.png" alt="" width="72" height="72" loading="lazy"><div><h2 id="{s}-h">{e(a["name"])}</h2>{tag}{kick(a)}</div></div>
        <dl>
          <div><dt>What it is</dt><dd>{e(t["what"])}</dd></div>
          <div><dt>Who we're looking for</dt><dd>{e(t["who"])}</dd></div>
          <div><dt>What we'd love to hear</dt><dd><ul>{ask}</ul></dd></div>
        </dl>
        <div class="join">{join}</div>
      </div>
      {shot}
    </article>'''


def build():
    sky = "".join(f'<div class="sh {c}" style="{st}">{svg}</div>' for st, sp, c, svg in hub.SKY[2:4])
    cards = "".join(card(t) for t in TESTERS)
    desc = "Try Couch Co-Op Studios iPhone apps before they reach the App Store and tell us what to fix. Free, through Apple's TestFlight."
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Become a tester", "url": f"{SITE}/testers/", "description": desc,
          "publisher": {"@type": "Organization", "name": "Couch Co-Op Studios", "url": f"{SITE}/"}}
    og = f"{SITE}/assets/brand/couch-co-op-studios-primary.png"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#EEF1FB">
<title>Become a tester: Couch Co-Op Studios</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/testers/">
<link rel="icon" type="image/png" href="/assets/brand/couch-co-op-studios-mark-600.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Couch Co-Op Studios">
<meta property="og:title" content="Become a tester: Couch Co-Op Studios"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/testers/"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{og}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{hub.CSS}{CSS}</style>
</head>
<body>
<a class="skip" href="#apps">Skip to the apps</a>
<header class="top"><nav class="bar" aria-label="Site"><a href="/">All apps</a><a href="#how">How it works</a><a class="c" href="mailto:{HELLO}">Contact</a></nav></header>
<main>
<div class="sky" aria-hidden="true">{sky}</div>
<div class="wrap">
  <section class="thero" aria-labelledby="hero-h">
    <a href="/"><img class="logo" src="/assets/brand/couch-co-op-studios-mark-600.png" alt="Couch Co-Op Studios" width="607" height="380"></a>
    <h1 id="hero-h">Help us test our apps.</h1>
    <p class="lede">We're looking for people who will use one of our iPhone apps for real, before it reaches the App Store, and tell us what's confusing, broken or missing. Testing is free and invite-only for now: ask for an invite to the app you'd use, and we'll email you when there's a spot.</p>
    <div class="cta"><a class="btn" href="#apps">Pick an app</a><a class="btn alt" href="#how">How testing works</a></div>
  </section>
  <div class="cards" id="apps">{cards}
  </div>
  <section class="rules" id="how" aria-labelledby="how-h">
    <h2 id="how-h">How testing works</h2>
    <p>Testing runs through TestFlight, Apple's free app for trying apps before they launch.</p>
    <div class="cush steps">
      <div><h3>Ask for an invite</h3><p>Email us which app you'd use and how. We send invites in small batches.</p></div>
      <div><h3>Accept it on your iPhone</h3><p>Install <a href="{TESTFLIGHT_APP}">TestFlight</a> from the App Store, then open our invite on your iPhone and tap Accept and Install.</p></div>
      <div><h3>Use it, then tell us</h3><p>Use it the way you normally would. Take a screenshot in the app to send feedback, or email us.</p></div>
    </div>
    <div class="know">
      <p><strong>It's free.</strong> Purchases inside a test version are test purchases, and you're never charged for them.</p>
      <p><strong>Leave any time.</strong> Delete the app, or open TestFlight and tap Stop Testing.</p>
      <p><strong>What we see.</strong> TestFlight sends us crash reports and any feedback you choose to send. Each app's privacy page covers the rest.</p>
      <p><strong>What we do with it.</strong> We fix what you find, and we keep a dated log of what testers told us and what changed.</p>
    </div>
    <div class="help">
      <div><h3>Want an invite?</h3><p>Tell us which app you'd like to try and a little about how you'd use it.</p></div>
      <a class="btn" href="mailto:{HELLO}">Email {HELLO}</a>
    </div>
  </section>
</div>
</main>
<footer>
  <div class="wrap">
    <nav aria-label="Apps">{"".join(f'<a href="/{a["slug"]}/">{e(a["name"])}</a>' for a in hub.APPS)}</nav>
    <p>&copy; 2026 Couch Co-Op Studios. <a href="mailto:{SUPPORT}">{SUPPORT}</a></p>
    <p class="fine">Apple, the Apple logo, iPhone and TestFlight are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc.</p>
  </div>
</footer>
<script>
// Some browsers have no mail app set up, so a mailto link opens a blank window. The copy button gives them the address instead.
document.querySelectorAll('.copy').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var text = b.getAttribute('data-copy');
    function done() {{ b.textContent = 'Copied'; setTimeout(function () {{ b.textContent = 'Copy address'; }}, 2000); }}
    if (navigator.clipboard) {{ navigator.clipboard.writeText(text).then(done, function () {{ window.prompt('Copy this address:', text); }}); }}
    else {{ window.prompt('Copy this address:', text); }}
  }});
}});
</script>
</body>
</html>
'''


if __name__ == "__main__":
    out = ROOT / "testers" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build())
    print("wrote testers/index.html")
