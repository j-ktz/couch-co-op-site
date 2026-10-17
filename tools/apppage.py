#!/usr/bin/env python3
"""Builds each app's landing page (<slug>/index.html) on the studio app kit.

Run from the repo root:  python3 tools/apppage.py [slug ...]
TankLog is not built here: its page is owned by its maker and stays as it is.

Each page keeps the title, description, share tags and structured data it had
before the rebuild (saved once in tools/app-legacy.json), so search results don't
move. Copy comes from each app's spec in tools/appspecs.py. The shared look and
motion live in /assets/app.css and /assets/app.js. No em dashes (house style).
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import landing  # noqa: E402  (icons, more-apps names)
from hub import contrast, _mix  # noqa: E402

LEGACY = ROOT / "tools" / "app-legacy.json"
NAVY, WHITE = "#0B1A4A", "#FFFFFF"
e = lambda s: html.escape(s, quote=True)


# ------------------------------------------------------------ legacy head data
def _legacy_from(slug):
    h = (ROOT / slug / "index.html").read_text()
    head = h.split("</head>", 1)[0]
    keep = []
    for pat in (r'<meta name="description"[^>]*>', r'<link rel="canonical"[^>]*>', r'<meta property="og:[^"]+"[^>]*>',
                r'<meta name="twitter:[^"]+"[^>]*>', r'<meta name="apple-itunes-app"[^>]*>'):
        keep += re.findall(pat, head)
    return {
        "title": re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip(),
        "meta": keep,
        "ld": re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S),
        "js": [s for s in re.findall(r"<script(?![^>]*ld\+json)(?![^>]*src=)[^>]*>(.*?)</script>", h, re.S) if s.strip()],
    }


def legacy(slug):
    data = json.loads(LEGACY.read_text()) if LEGACY.exists() else {}
    if slug not in data:
        data[slug] = _legacy_from(slug)
        LEGACY.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    return data[slug]


def ver(p):
    import hashlib
    return hashlib.sha1((ROOT / p).read_bytes()).hexdigest()[:8]


# ------------------------------------------------------------ pieces
def fill(g, ink):
    toward = NAVY if ink == WHITE else WHITE
    t = 0.0
    while contrast(_mix(g, toward, t), ink) < 4.6 and t < 1:
        t += .02
    return _mix(g, toward, t)


def iph(slug, files, delay=0, label=None, lazy=True, attrs=""):
    imgs = "".join(f'<img{" class=\"on\"" if i == 0 else ""} src="/{slug}/img/{f}" alt="" width="640" height="1390"'
                   f'{" loading=\"lazy\" decoding=\"async\"" if lazy and i else ""}>' for i, f in enumerate(files))
    aria = f' role="img" aria-label="{e(label)}"' if label else ' aria-hidden="true"'
    return f'<div class="iph" data-delay="{delay}"{aria}{attrs}><div class="scr">{imgs}</div></div>'


SHAPES = (
 ('left:2%;top:260px;width:70px;height:70px', '.35', '<svg viewBox="0 0 74 74"><circle cx="37" cy="37" r="29" fill="none" stroke="var(--a)" stroke-width="10"/></svg>'),
 ('left:44%;top:300px;width:84px;height:84px', '-.18', '<svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="var(--a2)"/></svg>'),
 ('right:3%;top:250px;width:150px;height:58px', '.3', '<svg viewBox="0 0 150 58"><rect width="150" height="58" rx="29" fill="var(--a3)" transform="rotate(-18 75 29)"/></svg>'),
 ('left:47%;top:760px;width:64px;height:64px', '.45', '<svg viewBox="0 0 70 70"><path d="M35 0C38 22 48 32 70 35C48 38 38 48 35 70C32 48 22 38 0 35C22 32 32 22 35 0Z" fill="var(--a2)"/></svg>'),
 ('right:6%;top:850px;width:170px;height:50px', '.22', '<svg viewBox="0 0 170 50"><path d="M6 30C26 4 42 4 58 26S92 48 108 24S144 2 164 22" fill="none" stroke="var(--a)" stroke-width="11" stroke-linecap="round"/></svg>'),
 ('left:8%;top:900px;width:52px;height:52px', '.4', '<svg viewBox="0 0 58 58"><rect x="6" y="6" width="46" height="46" rx="12" fill="var(--a3)" transform="rotate(16 29 29)"/></svg>'),
)


def sky():
    return '<div class="sky" aria-hidden="true">' + "".join(
        f'<div class="sh" data-speed="{sp}" data-depth="{float(sp) * 40:.0f}" style="{st}">{svg}</div>' for st, sp, svg in SHAPES) + "</div>"


def hero_fan(slug, screens):
    n = len(screens)
    if n >= 3:
        sets = [screens[i:] + screens[:i] for i in (1, 0, 2)]
        cls, idx = "", (0, 1, 2)
    else:
        sets = [screens[1:] + screens[:1], screens]
        cls, idx = " duo", (0, 1)
    speeds = (".03", "-.04", ".06")
    out = "".join(f'<div class="fp f{k}" data-speed="{speeds[k]}"><div class="rise">{iph(slug, s, delay=k * 1100, lazy=False)}</div></div>'
                  for k, s in zip(idx, sets))
    return f'<div class="hfan{cls}" aria-hidden="true">{out}</div>'


def cta(s, where="hero"):
    if s["live"]:
        btn = (f'<a class="badge" href="https://apps.apple.com/app/id{s["appid"]}" aria-label="Download {e(s["name"])} on the App Store">'
               f'<img src="/assets/app-store-badge.svg" alt="" width="162" height="54"></a>')
    else:
        btn = f'<span class="soon">{e(s.get("soon", "Coming soon to the App Store"))}</span>'
    second = s.get("cta2")
    if second and where == "hero":
        btn += f'<a class="btn alt" href="{second[1]}">{e(second[0])}</a>'
    return f'<div class="cta">{btn}</div>'


def subp(d):
    return f'<p class="sub">{e(d["sub"])}</p>' if d.get("sub") else ""


def block(slug, b, s):
    kind = b[0]
    d = b[1] if len(b) > 1 else {}
    sid = f' id="{d["id"]}"' if isinstance(d, dict) and d.get("id") else ""
    if kind == "raw":
        return d
    if kind == "stories":
        rows = []
        for i, st in enumerate(d["items"]):
            vis = st.get("vis")
            if vis is None:
                shots = st["screens"]
                if st.get("two"):
                    vis = (f'<div class="vis two">{iph(slug, shots[0::2] or shots, 0, st.get("alt"), attrs=" data-speed=\"-.04\"")}'
                           f'{iph(slug, shots[1::2] or shots, 1500, None, attrs=" data-speed=\".05\"")}</div>')
                else:
                    vis = f'<div class="vis">{iph(slug, shots, i * 600, st.get("alt"), attrs=" data-speed=\"-.04\"")}</div>'
            body = st.get("html") or "".join(f"<p>{e(p)}</p>" for p in st.get("p", []))
            if st.get("bullets"):
                body += "<ul>" + "".join(f"<li>{x}</li>" for x in st["bullets"]) + "</ul>"
            rid = f' id="{st["id"]}"' if st.get("id") else ""
            hd = f'<h3 class="sth">{st["h"]}</h3>' if d.get("h") else f'<h2>{st["h"]}</h2>'
            rows.append(f'<div class="story{" flip" if i % 2 else ""}"{rid}><div class="txt">{hd}{body}</div>{vis}</div>')
        head = (f'<h2>{d["h"]}</h2>' if d.get("h") else "") + (f'<p class="sub">{e(d["sub"])}</p>' if d.get("sub") else "")
        return f'<section class="sec"{sid}><div class="wrap">{head}{"".join(rows)}</div></section>'
    if kind == "steps":
        items = "".join(
            f'<li>{iph(slug, [it[2]], k * 500) if len(it) > 2 and it[2] else ""}<h3>{e(it[0])}</h3><p>{it[1]}</p></li>'
            for k, it in enumerate(d["items"]))
        return (f'<section class="sec{" alt" if d.get("alt") else ""}"{sid}><div class="wrap{" center" if d.get("center") else ""}">'
                f'<h2>{e(d["h"])}</h2>{subp(d)}<ol class="steps">{items}</ol></div></section>')
    if kind == "feats":
        items = "".join(f'<div><span class="ic">{landing.icon(i, 22)}</span><h3>{e(t)}</h3><p>{x}</p></div>' for i, t, x in d["items"])
        sub = f'<p class="sub">{e(d["sub"])}</p>' if d.get("sub") else ""
        return f'<section class="sec{" alt" if d.get("alt") else ""}"{sid}><div class="wrap"><h2>{e(d["h"])}</h2>{sub}<div class="feats">{items}</div></div></section>'
    if kind == "who":
        items = "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in d["items"])
        return f'<section class="sec"{sid}><div class="wrap"><h2>{e(d.get("h", "Who it is for"))}</h2>{subp(d)}<div class="who">{items}</div></div></section>'
    if kind == "band":
        nos = "<ul class=\"nos\">" + "".join(f"<li>{e(x)}</li>" for x in d.get("nos", [])) + "</ul>" if d.get("nos") else ""
        inner = d.get("html", "")
        sub = f'<p class="sub">{d["sub"]}</p>' if d.get("sub") else ""
        return (f'<section class="band"{sid} style="--band:{d.get("bg", "var(--band)")}">'
                '<div class="blob b1" data-speed=".12" aria-hidden="true"></div><div class="blob b2" data-speed="-.1" aria-hidden="true"></div><div class="blob b3" data-speed=".08" aria-hidden="true"></div>'
                f'<div class="wrap"><h2>{e(d["h"])}</h2>{sub}{inner}{nos}</div></section>')
    if kind == "cloud":
        groups = "".join(f'<div><h3>{e(g)}</h3><ul>' + "".join(f'<li{" class=free" if free else ""}>{e(t)}{" · Free" if free else ""}</li>' for t, free in items) + "</ul></div>" for g, items in d["groups"])
        return f'<section class="sec alt"{sid}><div class="wrap"><h2>{e(d["h"])}</h2><p class="sub">{e(d["sub"])}</p><div class="cloud">{groups}</div></div></section>'
    if kind == "plans":
        cards = ""
        for p in d["items"]:
            name, price, per, items, hl = p[:5]
            whofor = p[5] if len(p) > 5 else ""
            cards += (f'<div class="plan{" hl" if hl else ""}">{f"<div class=who-for>{e(whofor)}</div>" if whofor else ""}<h3>{e(name)}</h3>'
                      f'<div class="price">{e(price)}</div><div class="per">{e(per)}</div><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>")
        fine = f'<p class="fine">{d["fine"]}</p>' if d.get("fine") else ""
        sub = f'<p class="sub">{e(d["sub"])}</p>' if d.get("sub") else ""
        return f'<section class="sec"{sid or " id=\"pricing\""}><div class="wrap center"><h2>{e(d["h"])}</h2>{sub}<div class="plans">{cards}</div>{fine}</div></section>'
    if kind == "faq":
        qa = "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in d["items"])
        extra = d.get("after", "")
        return f'<section class="sec alt" id="faq"><div class="wrap center"><h2>{e(d.get("h", "Questions people ask"))}</h2><div class="faq">{qa}</div>{extra}</div></section>'
    if kind == "guides":
        items = "".join(f'<a href="{h}"><b>{e(t)}</b><span>{e(x)}</span></a>' for h, t, x in d["items"])
        return f'<section class="sec"{sid}><div class="wrap"><h2>{e(d["h"])}</h2>{subp(d)}<div class="guides">{items}</div></div></section>'
    if kind == "more":
        tiles = "".join(f'<a href="/{x}/"><img src="/{x}/img/icon.png" alt="" width="56" height="56" loading="lazy"><div><b>{e(landing.APPS[x][0])}</b><span>{e(landing.APPS[x][1])}</span></div></a>' for x in d)
        return f'<section class="sec"><div class="wrap"><h2>More from our studio</h2><p class="sub">Small apps that each do one job well.</p><div class="more">{tiles}</div></div></section>'
    raise ValueError(kind)


def page(slug, s):
    L = legacy(slug)
    ink = s["ink"]
    af = fill(s["a"], ink)
    vars_ = (f'--bg:{s["bg"]};--bg2:{s.get("bg2", _mix(s["bg"], s["a"], .07))};--a:{s["a"]};--af:{af};--ai:{ink};'
             f'--a2:{s["a2"]};--a3:{s["a3"]};--band:{s.get("band", NAVY)};' + s.get("vars", ""))
    nav_links = "".join(f'<a class="hide-s" href="{h}">{e(t)}</a>' for t, h in s["nav"])
    nav_cta = (f'<a class="c" href="https://apps.apple.com/app/id{s["appid"]}">Get the app</a>' if s["live"]
               else f'<a class="c" href="#faq">Coming soon</a>')
    h1 = "".join(f"<span>{e(x)}</span>" for x in s["h1"])
    status = f'<span class="status">{e(s["status"])}</span>' if s.get("status") else ""
    body = "".join(block(slug, b, s) for b in s["blocks"])
    trust = '<ul class="trust" aria-label="At a glance">' + "".join(f"<li>{e(t)}</li>" for t in s["trust"]) + "</ul>" if s.get("trust") else ""
    links = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in s["links"])
    legal = "".join(f"<p>{x}</p>" for x in s.get("legal", []))
    old = L["js"] if s.get("keep_js") == "legacy" else []
    js = ("".join(f'<script src="{x}" defer></script>' for x in s.get("scripts", []))
          + "".join(f"<script>{x}</script>" for x in old) + (f"<script>{s['js']}</script>" if s.get("js") else ""))
    meta = "\n".join(L["meta"])
    return f'''<!doctype html>
<html lang="en"{' class="dark"' if s.get("dark") else ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{s["bg"]}">
<title>{L["title"]}</title>
{meta}
<link rel="icon" type="image/png" href="/{slug}/img/icon.png">
<link rel="apple-touch-icon" href="/{slug}/img/icon.png">
<link rel="stylesheet" href="/assets/app.css?v={ver("assets/app.css")}">
<style>:root{{{vars_}}}{s.get("css", "")}</style>
{(f"<!--gen:jsonld-->{''.join(L['ld'])}<!--/gen:jsonld-->" if s.get("ld_marker") else "".join(L["ld"]))}
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><nav class="bar" aria-label="{e(s["name"])}"><a class="home" href="#main"><img src="/{slug}/img/icon.png" alt="" width="30" height="30">{e(s.get("navname", s["name"]))}</a>{nav_links}{nav_cta}</nav></header>
<main id="main">
{sky()}
<div class="wrap">
  <section class="hero" aria-labelledby="h1">
    <div>
      <img class="hicon" src="/{slug}/img/icon.png" alt="" width="96" height="96">
      {status}
      <h1 id="h1">{h1}</h1>
      {s.get("hero_extra", "")}
      <p class="lede">{s["lede"]}</p>
      {cta(s)}
      {f'<p class="note">{s["note"]}</p>' if s.get("note") else ""}
    </div>
    {s["hero_wrap"].format(fan=hero_fan(slug, s["screens"])) if s.get("hero_wrap") else (s.get("hero_vis") or hero_fan(slug, s["screens"]))}
  </section>
  {trust}
</div>
{body}
<section class="finale">
  <div class="wrap">
    <img class="hicon" src="/{slug}/img/icon.png" alt="" width="110" height="110" loading="lazy">
    <h2>{e(s["finale"][0])}</h2>
    <p class="sub">{e(s["finale"][1])}</p>
    {cta(s, "end")}
  </div>
</section>
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <a class="studio" href="/"><img src="/assets/brand/couch-co-op-studios-mark-600.png" alt="Couch Co-Op Studios" width="54" height="34"></a>
      <nav aria-label="Pages">{links}<a href="mailto:support@couchcoopstudios.com">support@couchcoopstudios.com</a><a href="/">All apps</a></nav>
    </div>
    <div class="legal">{legal}<p>&copy; 2026 Couch Co-Op Studios. {e(landing.HOUSE_LINE)}</p><p>{e(landing.APPLE_CREDIT)}</p></div>
  </div>
</footer>
<script src="/assets/app.js?v={ver("assets/app.js")}" defer></script>
{js}
</body>
</html>
'''


if __name__ == "__main__":
    import appspecs
    want = sys.argv[1:] or list(appspecs.SPECS)
    for slug in want:
        if slug == "tanklog":
            raise SystemExit("TankLog is not built here.")
        legacy(slug)  # snapshot head data before the first overwrite
        (ROOT / slug / "index.html").write_text(page(slug, appspecs.SPECS[slug]))
        print("built", slug)
