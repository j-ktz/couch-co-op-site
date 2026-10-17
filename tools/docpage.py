#!/usr/bin/env python3
"""Puts every reading page (privacy, support, terms, photos, guides) in the studio frame.

Run from the repo root, after any tool that writes those pages (tools/guides.py,
Sitout's Tools/site-tables/regen.sh):  python3 tools/docpage.py

Safe to run again: a page it already framed is recognized by its <!--cc:content-->
markers and only re-wrapped. The page's own words, head tags (title, description,
share tags, structured data) and any <!--gen:...--> blocks are kept as they are.
Not touched: TankLog (its maker owns it), the join pages (they run invite-code
scripts), and the hub and app landing pages (tools/hub.py, tools/apppage.py).
"""
import hashlib, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import landing  # noqa: E402
from apppage import fill, NAVY, WHITE  # noqa: E402
from appspecs import SPECS  # noqa: E402

e = lambda s: html.escape(s, quote=True)
SKIP = {"mvn/join.html"}
KIND = {"privacy.html": "Privacy", "support.html": "Support", "terms.html": "Terms", "photos.html": "Queen photos"}


def ver(p):
    return hashlib.sha1((ROOT / p).read_bytes()).hexdigest()[:8]


def pages():
    out = []
    for slug in SPECS:
        for p in sorted((ROOT / slug).rglob("*.html")):
            rel = p.relative_to(ROOT).as_posix()
            if rel == f"{slug}/index.html" or rel in SKIP or "/img/" in rel:
                continue
            out.append((slug, rel))
    return out


def head_bits(head):
    """Keep the tags that matter for search and sharing, in order; keep <!--gen--> blocks whole."""
    gens = re.findall(r"<!--gen:([\w-]+)-->.*?<!--/gen:\1-->", head, re.S)
    gen_blocks = [m.group(0) for m in re.finditer(r"<!--gen:([\w-]+)-->.*?<!--/gen:\1-->", head, re.S)]
    rest = re.sub(r"<!--gen:([\w-]+)-->.*?<!--/gen:\1-->", "", head, flags=re.S)
    keep = []
    for pat in (r'<meta name="(?:description|robots|apple-itunes-app)"[^>]*>', r'<link rel="canonical"[^>]*>', r'<meta property="og:[^"]+"[^>]*>',
                r'<meta name="twitter:[^"]+"[^>]*>', r'<script type="application/ld\+json">.*?</script>'):
        keep += re.findall(pat, rest, re.S)
    title = re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip()
    return title, keep + gen_blocks


def extract(h):
    if "<!--cc:content-->" in h:
        content = h.split("<!--cc:content-->", 1)[1].split("<!--/cc:content-->", 1)[0].strip()
        h1 = re.search(r'<h1 id="dh1">(.*?)</h1>', h, re.S).group(1)
        hidden = re.search(r"<!--cc:gens-->(.*?)<!--/cc:gens-->", h, re.S)
        wide = 'class="prose wide"' in h
        return h1, content, hidden.group(1) if hidden else "", wide
    body = h.split("<body", 1)[1].split(">", 1)[1].rsplit("</body>", 1)[0]
    body = re.sub(r"<!-- lp:legal -->.*?<!-- /lp:legal -->", "", body, flags=re.S)
    # gen blocks outside <main> (old header/footer) are kept, hidden, so Sitout's generator still finds them
    m = re.search(r"<main\b([^>]*)>(.*)</main>", body, re.S)
    outside = body if not m else body[:m.start()] + body[m.end():]
    hidden = "".join(x.group(0) for x in re.finditer(r"<!--gen:([\w-]+)-->.*?<!--/gen:\1-->", outside, re.S))
    wide = bool(m and "wide" in m.group(1))
    content = m.group(2) if m else body
    if not m:
        content = re.sub(r"<header\b.*?</header>", "", content, flags=re.S)
        content = re.sub(r"<footer\b.*?</footer>", "", content, flags=re.S)
        content = re.sub(r'^\s*<div class="(?:wrap|container)">(.*)</div>\s*$', r"\1", content, flags=re.S)
    content = re.sub(r"<script(?![^>]*ld\+json).*?</script>", "", content, flags=re.S)
    content = re.sub(r'<nav class="crumbs".*?</nav>|<p class="crumbs">.*?</p>', "", content, count=1, flags=re.S)
    content = re.sub(r'<a[^>]*class="back"[^>]*>.*?</a>', "", content, flags=re.S)
    content = re.sub(r'<p>\s*<a href="[^"]*">\s*(?:&larr;|←)[^<]*</a>\s*</p>', "", content)
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.S)
    h1 = h1m.group(1).strip() if h1m else ""
    if h1m:
        content = content[:h1m.start()] + content[h1m.end():]
    content = re.sub(r'<footer\b.*?</footer>', "", content, flags=re.S)
    return h1, content.strip(), hidden, wide


def frame(slug, rel, h):
    s = SPECS[slug]
    head = h.split("</head>", 1)[0]
    title, keep = head_bits(head)
    h1, content, hidden, wide = extract(h)
    ink = s["ink"]
    vars_ = (f'--bg:{s["bg"]};--bg2:{s.get("bg2", s["bg"])};--a:{s["a"]};--af:{fill(s["a"], ink)};--ai:{ink};'
             f'--a2:{s["a2"]};--a3:{s["a3"]};' + s.get("vars", ""))
    name = s["name"]
    page_name = KIND.get(rel.rsplit("/", 1)[1], "Guides" if "/how-to/" in rel or "/guide/" in rel else "")
    crumbs = [("Couch Co-Op Studios", "/"), (name, f"/{slug}/")]
    if "/how-to/" in rel and not rel.endswith("how-to/index.html"):
        crumbs.append(("Guides", f"/{slug}/how-to/"))
    crumbs_html = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in crumbs) + f'<li aria-current="page">{e(page_name or "Page")}</li>'
    links = [("Support", f"/{slug}/support.html"), ("Privacy", f"/{slug}/privacy.html")]
    nav_links = "".join(f'<a class="hide-s" href="{u}">{t}</a>' for t, u in links if u != f"/{rel}")
    cta = (f'<a class="c" href="https://apps.apple.com/app/id{s["appid"]}">Get the app</a>' if s["live"] else f'<a class="c" href="/{slug}/">See the app</a>')
    foot_links = "".join(f'<a href="{u}">{e(t)}</a>' for t, u in [(name, f"/{slug}/")] + links)
    legal = "".join(f"<p>{x}</p>" for x in s.get("legal", []))
    hid = f'<div hidden><!--cc:gens-->{hidden}<!--/cc:gens--></div>' if hidden else ""
    return f'''<!doctype html>
<html lang="en"{' class="dark"' if s.get("dark") else ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{s["bg"]}">
<title>{title}</title>
{chr(10).join(keep)}
<link rel="icon" type="image/png" href="/{slug}/img/icon.png">
<link rel="stylesheet" href="/assets/app.css?v={ver("assets/app.css")}">
<link rel="stylesheet" href="/assets/doc.css?v={ver("assets/doc.css")}">
<style>:root{{{vars_}}}</style>
</head>
<body>
<a class="skip" href="#doc">Skip to content</a>
<header class="top"><nav class="bar" aria-label="{e(name)}"><a class="home" href="/{slug}/"><img src="/{slug}/img/icon.png" alt="" width="30" height="30">{e(s.get("navname", name))}</a>{nav_links}{cta}</nav></header>
<main id="doc">
<div class="sky" aria-hidden="true"></div>
<header class="dhead"><div class="wrap">
  <ol class="crumbs" aria-label="Breadcrumb">{crumbs_html}</ol>
  <img class="dicon" src="/{slug}/img/icon.png" alt="" width="72" height="72">
  <h1 id="dh1">{h1}</h1>
</div></header>
<div class="doc"><div class="wrap"><article class="prose{" wide" if wide else ""}"><!--cc:content-->
{content}
<!--/cc:content--></article></div></div>
</main>
{hid}
<footer>
  <div class="wrap">
    <div class="foot">
      <a class="studio" href="/"><img src="/assets/brand/couch-co-op-studios-mark-600.png" alt="Couch Co-Op Studios" width="54" height="34"></a>
      <nav aria-label="Pages">{foot_links}<a href="mailto:support@couchcoopstudios.com">support@couchcoopstudios.com</a><a href="/">All apps</a></nav>
    </div>
    <div class="legal">{legal}<p>&copy; 2026 Couch Co-Op Studios. {e(landing.HOUSE_LINE)}</p><p>{e(landing.APPLE_CREDIT)}</p></div>
  </div>
</footer>
</body>
</html>
'''


if __name__ == "__main__":
    for slug, rel in pages():
        p = ROOT / rel
        p.write_text(frame(slug, rel, p.read_text()))
        print("framed", rel)
