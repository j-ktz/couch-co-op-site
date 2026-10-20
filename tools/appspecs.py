"""Per-app content and styling for tools/apppage.py. Copy comes from each app's
previous page and tools/landing.py, unchanged in substance. No em dashes."""
import landing
from appspecs2 import TABBED, FANTASYQUEENS, SITOUT

C = landing.C
NAVY, WHITE = "#0B1A4A", "#FFFFFF"


def faq(slug):
    return [(q, landing.esc(a)) for q, a in C[slug]["faq"]]


# ---------------------------------------------------------------- Music Video Night
MVN_CSS = r'''
.mvn-play{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:64px;align-items:center}
.mh-card{position:relative;background:#fff;color:#1A1033;border-radius:30px;padding:26px;box-shadow:0 0 0 1px rgba(255,255,255,.2),0 50px 90px -40px rgba(152,103,255,.8)}
.mh-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.mh-chip{font-weight:700;font-size:.82rem;padding:5px 12px;border-radius:99px;background:linear-gradient(90deg,#FF67A3,#9867FF);color:#fff}
.mh-state{font-weight:700;font-size:.82rem;color:#5B4B8A}
.mh-q{font:800 1.7rem/1.1 var(--disp);letter-spacing:-.03em;margin:0 0 6px;color:#1A1033}
.mh-hint{margin:0 0 18px;color:#5B4B8A}
.mh-list{display:grid;gap:10px}
.mh-opt{display:flex;align-items:center;gap:14px;width:100%;text-align:left;padding:10px;border:2px solid transparent;border-radius:18px;background:#F3EEFF;color:#1A1033;font:inherit;cursor:pointer;transition:transform .25s cubic-bezier(.3,1.5,.4,1),background .2s,border-color .2s,opacity .3s}
.mh-opt:hover{transform:translateX(4px);background:#EAE1FF}
.mh-opt img{width:84px;height:44px;border-radius:10px;object-fit:cover;flex:none}
.mh-t b,.mh-t i{display:block}.mh-t i{font-style:normal;color:#5B4B8A;font-size:.88rem}
.mh-by{margin-left:auto;font-size:.8rem;font-weight:700;color:#7A3FE0;text-align:right}
.done .mh-opt{opacity:.55;cursor:default;transform:none}
.done .mh-opt.pick{opacity:1;border-color:#9867FF;background:#EFE5FF}
.mh-again{margin-top:16px;border:0;border-radius:99px;padding:11px 20px;font:700 .95rem var(--body);background:#1A1033;color:#fff;cursor:pointer}
.mh-conf{position:absolute;left:50%;top:45%;pointer-events:none}
.mh-conf i{position:absolute;width:9px;height:14px;border-radius:2px;opacity:0;animation:conf 1.2s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes conf{0%{transform:translate(0,0) rotate(0);opacity:1}100%{transform:translate(var(--x),var(--y)) rotate(var(--r));opacity:0}}
.tvcatch{margin-top:26px;padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.1);font-size:.98rem}
@media(max-width:960px){.mvn-play{grid-template-columns:minmax(0,1fr);gap:36px}}
'''

MVN_PLAY = '''<section class="sec demo" id="play"><div class="wrap"><div class="mvn-play">
<div><h2>Play a round right here.</h2><p class="sub">Three videos, no names. Pick your favorite, then see who chose it. That reveal is the whole game.</p></div>
<div class="mh-card" id="mhCard" aria-label="Interactive demo: vote on a video, then see who picked it">
  <div class="mh-top"><span class="mh-chip">Guilty Pleasures</span><span class="mh-state" id="mhState">Blind vote</span></div>
  <h3 class="mh-q" id="mhQ">Which video wins tonight?</h3>
  <p class="mh-hint" id="mhHint">No names shown. Judge the video, not the picker. Tap one.</p>
  <div class="mh-list" id="mhList">
    <button class="mh-opt" type="button" data-by="Priya"><img src="img/v1.jpg" alt="" width="84" height="44"><span class="mh-t"><b>Rooftop Rewind</b><i>DJ Kassette</i></span><span class="mh-by"></span></button>
    <button class="mh-opt" type="button" data-by="Marcus"><img src="img/v2.jpg" alt="" width="84" height="44"><span class="mh-t"><b>Lasers On, Lights Off</b><i>Club Mirage</i></span><span class="mh-by"></span></button>
    <button class="mh-opt" type="button" data-by="Dev"><img src="img/v3.jpg" alt="" width="84" height="44"><span class="mh-t"><b>Neon Heartbreak</b><i>The Velvet Hours</i></span><span class="mh-by"></span></button>
  </div>
  <button class="mh-again" type="button" id="mhAgain" hidden>Vote again</button>
  <div class="mh-conf" id="mhConf" aria-hidden="true"></div>
</div></div></div></section>'''

APPSTORE_MVN = '<a href="https://apps.apple.com/app/id6811704618">Get the app from the App Store</a>'

MVN = dict(
 name="Music Video Night", live=True, appid="6811704618", dark=True,
 bg="#140B26", bg2="#1C1036", a="#9867FF", ink=WHITE, a2="#FF67A3", a3="#58E1FF", band="#2A1660",
 nav=[("How a Night goes", "#how"), ("Pricing", "#pricing")],
 status="Free on the App Store",
 h1=["Everyone picks.", "Everyone votes.", "One person wins the Night."],
 lede="The music video party game. Friends in one room, one theme, one video each, watched together and voted on blind.",
 cta2=("How a Night goes", "#how"), note="Free download. iPhone, iOS 17 or later.",
 screens=["screen-themes.webp", "screen-playback.webp", "screen-voting.webp", "screen-results.webp"],
 trust=["Free to join, always", "No accounts, no login", "No server, no data collected", "Plays on your TV"],
 css=MVN_CSS, keep_js="legacy",
 blocks=[
  ("raw", MVN_PLAY),
  ("steps", dict(id="how", alt=True, h="Four screens, one winner",
   sub="A Night takes about as long as the videos do. Nobody installs anything but the app, nobody signs up for anything, and nobody has to be the DJ all evening.",
   items=[("Pick a theme, share the code", "The host picks tonight's theme and reads out a 5-letter code. Everyone else taps <b>Join with a Code</b>. Joining is free and only the host needs anything unlocked.", "screen-themes.webp"),
          ("Everyone submits one video", "One YouTube music video each, on theme. They play in sync on every phone at once while the room chats and flings emoji at the screen.", "screen-playback.webp"),
          ("Veto, then vote blind", "See something coming you can't sit through? Veto it before it plays. At the end everyone votes with no names attached, so you're judging the video, not your friend.", "screen-voting.webp"),
          ("Crown the winner", "Confetti, a crown, and the final standings. Every Night is saved to your history, and the Hall of Fame keeps score across all of them.", "screen-results.webp")])),
  ("band", dict(id="tv", h="Put it on the big screen", bg="#2A1660",
   sub="Mirror the host's iPhone and the TV shows a layout built for the room: the scoreboard, the chat and what's up next, while the video plays on the host's phone. Prefer the video itself on the TV? Turn TV mode off before you mirror and the TV becomes a plain mirror of the phone. Either way, everyone keeps their own phone for picking, chatting, vetoing and voting.",
   html='<div class="bandgrid" style="margin-top:36px"><ol><li>Start the Night on the host\'s iPhone.</li><li>Open Control Center, then Screen Mirroring, and pick your Apple TV.</li><li>Everyone keeps their phone for chat, reactions and the vote.</li></ol>'
        '<p class="tvcatch">One catch worth knowing: it\'s the video or the scoreboard, not both. When a video goes to the TV, iOS hands the whole screen to it, so the chat and reactions can\'t be drawn on top. That\'s an Apple TV limit, not a setting you\'ve missed.</p></div>')),
  ("cloud", dict(h="Twenty-six ways to argue about music",
   sub="The theme is the whole game. It's what makes someone dig for the perfect pick instead of playing their most-played. Four are free for hosts. Unlock Everything opens the rest, plus themes you invent, name and color yourself.",
   groups=[("Spooky SZN", [("🧟 Thriller Night", True), ("😈 Villain Era", False), ("🖤 Goth Night", False), ("🔮 Witchy Women", False), ("🔪 Horror Movie Bangers", False), ("👻 Creepy Music Videos", False)]),
           ("For the crowd", [("🏳️‍🌈 Gay Music Video Night", False), ("💅 Ladies' Night", False), ("🎧 Rap Music Video Night", False), ("🙈 Guilty Pleasures", True)]),
           ("By era", [("💃 80s Divas", False), ("🎤 90s Hip-Hop", False), ("💿 Y2K Pop", False), ("☄️ One-Hit Wonders", True)]),
           ("By vibe", [("🌴 Summer Anthems", False), ("🎶 Karaoke Bangers", False), ("😭 Sad Bangers", False), ("🪩 Dance Floor Fillers", False), ("🤘 Rock Gods", False), ("🔀 Remix Night", False), ("🎭 Cover Night", False), ("🎸 Live Not Studio", False), ("🎬 One-Take Wonders", False), ("🍿 Movie Soundtrack", False), ("⏱️ Under 3 Minutes", False), ("🃏 Wildcard", True)])])),
  ("plans", dict(h="Free to join. One price for the host.",
   sub="No subscription, no ads, no in-game currency, nothing that phones home. If someone else is hosting, you never pay anything.",
   items=[("Join a Night", "Free", "Always. No account, no trial, no catch.",
           ["Join any Night with a 5-letter code", "Submit, chat, react, veto and vote", "Host free Nights yourself on <b>Wildcard</b>, <b>Guilty Pleasures</b>, <b>One-Hit Wonders</b> and <b>Thriller Night</b>", "Your full Night history, saved on your phone", "A shareable recap card of every Night"], False, "Everyone"),
          ("Unlock Everything", "$4.99", "One-time purchase. Not a subscription.",
           ["All 26 built-in themes", "A gold VIP badge in chat when you host", "Custom themes you name and color yourself", "A recap video reel of the Night", "The cross-Night Hall of Fame leaderboard"], True, "Hosts")])),
  ("faq", dict(h="Questions people actually ask", items=[
   ("What is Music Video Night?", "A party game for iPhone played by people in the same room. The host picks a theme, everyone joins with a 5-letter code, and each player submits one YouTube music video that fits. The videos play in sync for everyone while people chat and react, then everyone votes blind for a favorite. Most votes wins the Night."),
   ("Do we need accounts or wifi?", "No accounts, ever. There's no login and no server of ours anywhere. Phones talk straight to each other over WiFi and Bluetooth using Apple's MultipeerConnectivity, so nothing about your Night leaves the room and nothing is collected about you. You do need an internet connection to stream the videos themselves from YouTube."),
   ("How many people can play?", "Anyone in the room with an iPhone and the host's code. Everyone takes a turn picking one video, so most Nights run three to six people."),
   ("How do we get it on the TV?", "Screen Mirroring from Control Center puts the Night on an Apple TV. With TV mode on, the TV shows the scoreboard, the chat and what's up next. With it off, the TV mirrors your phone, video and all.</p><p>There is no AirPlay button inside the video. YouTube's player doesn't offer one inside an app, so mirroring is the way."),
   ("Is it free?", "Joining is always free, and so is the app itself. Hosts get Wildcard, Guilty Pleasures, One-Hit Wonders and Thriller Night free along with their whole Night history. One optional $4.99 purchase, Unlock Everything, adds every theme, custom themes, the recap video reel and the Hall of Fame. The recap card is free for everyone. It's one-time, not a subscription, and only the host needs it."),
   ("What if a video won't play?", "Some artists and labels switch off embedding, so their videos can only be watched on YouTube itself. The app tells you when that happens: whoever picked it can swap it, the host can skip it, and anyone can open it in YouTube from the same screen."),
   ("What do we need to play?", "An iPhone running iOS 17 or later, for everyone playing. TV mode also needs an Apple TV to mirror to."),
   ("Someone sent me a code. What do I do?", f'{APPSTORE_MVN}, open it and tap <b>Join with a Code</b>, then type the 5 letters in. There\'s a walkthrough on the <a href="join.html">join page</a>.')])),
  ("more", ["fantasyqueens", "sitout", "mackro"]),
 ],
 finale=("Ready for a Night?", "Grab a theme, get everyone's phone out, and find out whose taste actually holds up."),
 links=[("Privacy", "privacy.html"), ("Support", "support.html"), ("Join a Night", "join.html")],
 legal=["No analytics, no trackers and no cookies on this site either. It seemed only fair.",
        "Music Video Night is not affiliated with, endorsed by or sponsored by YouTube, Google or Apple. Videos play through YouTube's official embedded player."],
)

# ---------------------------------------------------------------- Mackro
MACKRO_CSS = r'''
:root{--protein:#FF7A59;--carbs:#3FA7F5;--fat:#9B6BFF;--sun:#F5B82A}
.mfan{position:relative}
.mackhero{position:absolute;left:-12%;bottom:-6%;width:27%;z-index:5;filter:drop-shadow(0 24px 30px rgba(60,35,5,.35));animation:hover 5.5s ease-in-out infinite}
.kplay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:64px;align-items:center}
.kitchen{background:#fff;border-radius:32px;padding:26px;box-shadow:0 0 0 1px var(--line),0 50px 90px -46px rgba(120,80,0,.6)}
.kHead{display:flex;justify-content:space-between;align-items:center;font-weight:700;margin-bottom:16px}
.kHead button{border:0;border-radius:99px;padding:7px 14px;background:var(--bg2);color:var(--ink);font:700 .85rem var(--body);cursor:pointer}
.stats{display:grid;grid-template-columns:140px minmax(0,1fr);gap:22px;align-items:center}
.ring{position:relative;width:140px;height:140px}
.ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.ring .tr{stroke:#F3E9D2}.ring .pr{stroke:var(--sun);transition:stroke-dashoffset .8s cubic-bezier(.2,.8,.2,1)}
.ring .num{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.ring .num span{font:800 2rem/1 var(--disp);letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.ring .num small{font-size:.74rem;color:var(--soft)}
.bars{display:grid;gap:12px}
.bar b{display:flex;justify-content:space-between;font-size:.9rem;margin-bottom:5px}
.bar em{font-style:normal;color:var(--soft);font-weight:500;font-variant-numeric:tabular-nums}
.bar i{display:block;height:10px;border-radius:99px;background:#F3E9D2;overflow:hidden}
.bar u{display:block;height:100%;width:0;border-radius:99px;transition:width .8s cubic-bezier(.2,.8,.2,1)}
.kitchen .say{display:flex;align-items:center;gap:14px;margin:20px 0 16px;padding:12px 14px;border-radius:20px;background:#FFF4D6}
.kitchen .say img{width:62px;height:62px;flex:none}
.kitchen .say b,.kitchen .say small{display:block}.kitchen .say small{color:var(--soft)}
#mackImg.hop{animation:mhop .32s ease}
@keyframes mhop{50%{transform:translateY(-8px) rotate(-6deg)}}
.foods{display:flex;flex-wrap:wrap;gap:8px}
.food{border:0;border-radius:99px;padding:10px 14px;background:var(--bg2);color:var(--ink);font:700 .9rem var(--body);cursor:pointer;transition:transform .2s cubic-bezier(.3,1.6,.4,1),background .2s}
.food span{margin-left:8px;color:var(--soft);font-weight:500}
.food:hover{background:#FFE7A8}.food:active{transform:scale(.94)}
.eg{margin:14px 0 0;font-size:.82rem;color:var(--soft)}
#stage{position:relative}
#stage .iph{width:min(290px,76%)}
.float{position:absolute;display:flex;align-items:center;gap:8px;padding:9px 14px;border-radius:99px;background:#fff;font-weight:700;font-size:.92rem;box-shadow:0 18px 30px -16px rgba(60,35,5,.5);opacity:0;transform:translateY(16px) scale(.9);transition:opacity .6s,transform .7s cubic-bezier(.3,1.5,.4,1)}
.float i{width:10px;height:10px;border-radius:50%}
.float.f1{left:2%;top:30%}.float.f2{right:0;top:46%}.float.f3{left:6%;top:64%}
#stage.in .float{opacity:1;transform:none}#stage.in .f2{transition-delay:.15s}#stage.in .f3{transition-delay:.3s}
.macks{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}
.macks figure{margin:0;background:#fff;border-radius:26px;padding:16px 14px 18px;text-align:center;box-shadow:0 0 0 1px var(--line);transition:transform .35s cubic-bezier(.3,1.5,.4,1)}
.macks figure:hover{transform:translateY(-6px) rotate(-1.5deg)}
.macks img{width:100%;height:auto;aspect-ratio:1}
.macks figcaption{font-weight:700;font-size:.95rem;line-height:1.3}
@media(max-width:960px){.kplay{grid-template-columns:minmax(0,1fr);gap:36px}.macks{grid-template-columns:repeat(2,minmax(0,1fr))}.mackhero{left:-2%;bottom:-2%;width:30%}}
@media(max-width:560px){.stats{grid-template-columns:110px minmax(0,1fr)}.ring{width:110px;height:110px}}
'''

MACKRO_PLAY = '''<section class="sec demo" id="try"><div class="wrap"><div class="kplay">
<div><h2>Try it. Tap what you ate.</h2><p class="sub">Mack keeps score, nudges you when you drift, and never judges a cheat day. Tap a few foods and watch.</p></div>
<div class="kitchen" aria-label="Interactive demo: tap foods to log them">
  <div class="kHead"><span>Today</span><button type="button" id="reset">Clear</button></div>
  <div class="stats">
    <div class="ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="tr" cx="60" cy="60" r="52" fill="none" stroke-width="13"/><circle class="pr" id="pr" cx="60" cy="60" r="52" fill="none" stroke-width="13" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="326.7"/></svg>
      <div class="num"><span id="cal">0</span><small>of 2,000 cal</small></div></div>
    <div class="bars">
      <div class="bar"><b>Protein <em><span id="pv">0</span> / 150g</em></b><i><u id="pb" style="background:var(--protein)"></u></i></div>
      <div class="bar"><b>Carbs <em><span id="cv">0</span> / 200g</em></b><i><u id="cb" style="background:var(--carbs)"></u></i></div>
      <div class="bar"><b>Fat <em><span id="fv">0</span> / 65g</em></b><i><u id="fb" style="background:var(--fat)"></u></i></div>
    </div>
  </div>
  <div class="say" aria-live="polite"><img id="mackImg" src="img/3d/mack-logging.webp" alt="" width="62" height="62"><div><b id="sayMain">Mack's ready when you are.</b><small id="saySub">Tap a food below.</small></div></div>
  <div class="foods" role="group" aria-label="Foods to log">
    <button class="food" type="button" data-c="220" data-p="20" data-k="24" data-f="4">Greek yogurt bowl<span>220</span></button>
    <button class="food" type="button" data-c="302" data-p="16" data-k="25" data-f="15">Eggs on toast<span>302</span></button>
    <button class="food" type="button" data-c="548" data-p="42" data-k="62" data-f="11">Chicken and rice<span>548</span></button>
    <button class="food" type="button" data-c="160" data-p="30" data-k="6" data-f="2">Protein shake<span>160</span></button>
    <button class="food" type="button" data-c="740" data-p="38" data-k="85" data-f="26">Burrito bowl<span>740</span></button>
    <button class="food" type="button" data-c="105" data-p="1" data-k="27" data-f="0">Banana<span>105</span></button>
  </div>
  <p class="eg">Example foods and targets with rounded numbers, just for the demo.</p>
</div></div></div></section>'''

MACKRO_STAGE = ('<div class="vis" id="stage">'
 '<div class="iph" role="img" aria-label="Mackro\'s Add food screen: a meal described in plain English and the macros Mack estimates" data-speed="-.04"><div class="scr"><img class="on" src="/mackro/img/describe.jpg" alt="" width="640" height="1390" loading="lazy"></div></div>'
 '<span class="float f1"><i style="background:var(--protein)"></i>16g protein</span><span class="float f2"><i style="background:var(--carbs)"></i>25g carbs</span><span class="float f3"><i style="background:var(--sun)"></i>302 cal</span></div>')

MACKS = [("mack-celebrating", "You hit protein. Mack did a lap."), ("mack-thinking", "Dinner's looking light. No rush."),
         ("mack-logging", "Rest day. Targets just came down."), ("mack-success", "Fourteen days in a row. Nice."),
         ("mack-cheatday", "Cheat day is allowed. Mack checked.")]
MACKRO_MEET = ('<section class="sec alt" id="mack"><div class="wrap center"><h2>Meet Mack. He\'s got your back.</h2>'
 '<p class="sub">A squirrel with a headband and zero judgment. He checks in, celebrates the wins and shrugs off the rough days.</p><div class="macks">'
 + "".join(f'<figure><img src="img/3d/{f}.webp" alt="" width="640" height="640" loading="lazy"><figcaption>{t}</figcaption></figure>' for f, t in MACKS)
 + "</div></div></section>")

MACKRO = dict(
 name="Mackro", live=True, appid="6771991453",
 bg="#FFF7E3", bg2="#FCEFCB", a="#F5B82A", ink="#2A1B0A", a2="#FF8A4C", a3="#7BC96F", band="#2A1B0A",
 vars="--ink:#2A1B0A;--soft:#5C482B;--line:rgba(42,27,10,.13);--shadow:rgba(80,50,5,.5);",
 nav=[("How it works", "#log"), ("Pricing", "#pricing")],
 status="Free on the App Store",
 h1=["Hit your macros.", "Skip the homework."],
 lede="Scan it, search it, log it. Mack keeps score, nudges you when you drift, and never judges a cheat day.",
 cta2=("Try it", "#try"), note="Free to start. No ads, no account.",
 screens=["today.jpg", "describe.jpg", "trends.jpg", "photo.jpg", "training.jpg"],
 trust=[t for _, t in C["mackro"]["trust"]],
 css=MACKRO_CSS, keep_js="legacy",
 blocks=[
  ("raw", MACKRO_PLAY),
  ("stories", dict(id="log", h="Log it however you eat it.", sub="Barcodes and search are free. Describe a meal or snap a photo with Pro.", items=[
   dict(h='Scan it or search it.<span class="tag">Free</span>', p=["Point at a barcode and the nutrition fills itself in. Or search a huge food database, plus your own foods in seconds."], screens=["today.jpg"], alt="Mackro's Today screen with calories, macros and Mack"),
   dict(h='Describe it.<span class="tag">Pro</span>', p=["Type what you ate like you'd text a friend. Mack parses it."], vis=MACKRO_STAGE),
   dict(h='Snap it.<span class="tag">Pro</span>', p=["Take a photo of your plate. Mack estimates the macros in seconds. It's an estimate, so mixed dishes can be off, and you can edit any entry."], screens=["photo.jpg"], alt="Logging a meal from a photo"),
  ])),
  ("raw", MACKRO_MEET),
  ("stories", dict(items=[dict(h="See the trend, not the noise.", p=["One heavy dinner isn't a bad week. Mackro shows what your last 30 days actually look like."],
   bullets=['Calories, macros and water, every day <span class="tag">Free</span>', 'Streaks and daily check-ins from Mack <span class="tag">Free</span>', '7-day trends <span class="tag">Free</span>',
            '30 and 90-day trends, full history <span class="tag">Pro</span>', 'Weekly targets that follow your weight trend <span class="tag">Pro</span>', 'Training day and rest day targets <span class="tag">Pro</span>',
            'Apple Health sync <span class="tag">Pro</span>', 'Meal templates and smart re-logs <span class="tag">Pro</span>'],
   screens=["trends.jpg", "training.jpg"], two=True, alt="Trends: 30 days of calories, macro averages and consistency")])),
  ("who", dict(items=C["mackro"]["who"])),
  ("band", dict(h=C["mackro"]["priv"][0], bg="#2A1B0A", sub=" ".join(C["mackro"]["priv"][1]),
   html='<p style="margin-top:18px"><a href="privacy.html">Read the privacy policy</a></p>', nos=["No ads, ever", "No account", "Barcode and search are free", "Your log stays in your iCloud"])),
  ("plans", dict(h="Pricing", items=[(n, p, per, items, hl) for n, p, per, items, hl in C["mackro"]["plans"]], fine=C["mackro"]["fine"] + " Pro features come with Mackro 2.1 and need the latest version of the app.")),
  ("faq", dict(items=faq("mackro"))),
  ("more", C["mackro"]["more"]),
 ],
 finale=("Mack's ready when you are.", "Free to start. Your food log stays yours."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html")],
 legal=["Mackro is not medical or diet advice. Targets are estimates from what you enter."],
)
MACKRO["hero_vis"] = None  # filled in apppage via hero_wrap below
MACKRO["hero_wrap"] = '<div class="mfan">{fan}<img class="mackhero" src="img/3d/mack-success.webp" alt="" width="640" height="640"></div>'

# ---------------------------------------------------------------- Stashday
STASH_CSS = r'''
.big{display:block;font:800 clamp(3.6rem,8vw,6.4rem)/1 var(--disp);letter-spacing:-.05em;color:#0F8A63;margin:-6px 0 18px;font-variant-numeric:tabular-nums}
.scene{position:relative;height:330vh;z-index:1;border-top:1px solid var(--line)}
.scene .sticky{position:sticky;top:0;height:100vh;max-width:1180px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:72px;align-items:center}
.ledger{background:#fff;border-radius:32px;padding:30px;box-shadow:0 0 0 1px var(--line),0 50px 90px -46px rgba(10,80,55,.55)}
.ledger h3{margin:0;color:var(--soft);font-size:1rem}
.ledger .left{font:800 3.4rem/1.1 var(--disp);letter-spacing:-.04em;margin:6px 0 20px;font-variant-numeric:tabular-nums;transition:color .4s}
.ledger .left.done{color:#0F8A63}
.ledger .row{display:grid;grid-template-columns:40px minmax(0,1fr) auto 34px;align-items:center;gap:10px;padding:14px 12px;border-radius:18px;background:var(--bg);margin-top:8px;transition:background .4s}
.ledger .emo{font-size:1.4rem}.ledger .nm{font-weight:700}.ledger .amt{font-variant-numeric:tabular-nums;color:var(--soft);font-weight:700}
.ledger .tick{width:30px;height:30px;border-radius:50%;box-shadow:inset 0 0 0 2px var(--line);display:grid;place-items:center;transition:background .35s,box-shadow .35s}
.ledger .tick svg{width:15px;height:15px;fill:none;stroke:#fff;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;opacity:0;transform:scale(.4);transition:opacity .3s,transform .4s cubic-bezier(.3,1.6,.4,1)}
.ledger .row.on{background:#DDF5EA}.ledger .row.on .amt{text-decoration:line-through}
.ledger .row.on .tick{background:#0F8A63;box-shadow:none}.ledger .row.on .tick svg{opacity:1;transform:none}
.scene .say{position:relative;min-height:260px}
.scene .step{position:absolute;inset:0 0 auto;opacity:0;transform:translateY(24px);transition:opacity .5s,transform .6s cubic-bezier(.2,.8,.2,1)}
.scene .step.on{opacity:1;transform:none}
.scene .step p{font-size:1.2rem;color:var(--soft);max-width:26em}
.scene .dots{position:absolute;left:0;bottom:-10px;display:flex;gap:8px}
.scene .dots i{width:9px;height:9px;border-radius:50%;background:var(--line);transition:background .3s,width .3s}
.scene .dots i.on{width:26px;border-radius:9px;background:#0F8A63}
@media(max-width:960px){.scene .sticky{grid-template-columns:minmax(0,1fr);gap:20px;align-content:center}.scene .say{min-height:200px}.ledger .left{font-size:2.6rem}}
@media(max-width:560px){.scene .step h2{font-size:2rem}.ledger{padding:20px}.ledger .row{padding:10px}}
@media(prefers-reduced-motion:reduce){.scene{height:auto}.scene .sticky{position:static;height:auto;padding:80px 24px}.scene .step{position:static;opacity:1;transform:none;margin-bottom:22px}.scene .dots{display:none}}
'''
STASH_SCENE = '''<section class="scene" id="scene" aria-label="How a payday works">
  <div class="sticky">
    <div class="ledger" role="img" aria-label="Payday checklist: three funds ticked off one at a time until the amount left reaches zero">
      <h3>Left to set aside</h3>
      <p class="left" id="left">$299.36</p>
      <div class="row" data-v="13.64"><span class="emo">🚗</span><span class="nm">Car registration</span><span class="amt">$13.64</span><span class="tick"><svg viewBox="0 0 16 16"><path d="M2 8.5 6 12.5 14 3.5"/></svg></span></div>
      <div class="row" data-v="200"><span class="emo">🎁</span><span class="nm">Holidays</span><span class="amt">$200.00</span><span class="tick"><svg viewBox="0 0 16 16"><path d="M2 8.5 6 12.5 14 3.5"/></svg></span></div>
      <div class="row" data-v="85.72"><span class="emo">🛡️</span><span class="nm">Car insurance</span><span class="amt">$85.72</span><span class="tick"><svg viewBox="0 0 16 16"><path d="M2 8.5 6 12.5 14 3.5"/></svg></span></div>
    </div>
    <div class="say" id="say">
      <div class="step on"><h2>It's payday.</h2><p>Tell Stashday how often you get paid and what's coming up. It works out each fund's share of this check.</p></div>
      <div class="step"><h2>Move the money.</h2><p>Set each fund's amount aside, in your own bank, however you like. Stashday never touches it.</p></div>
      <div class="step"><h2>Tick it off.</h2><p>Check each fund as you go. The number left to set aside counts down with you.</p></div>
      <div class="step"><h2>Covered.</h2><p>Zero left. When a bill finally arrives, tap Paid it and Stashday starts saving for the next one.</p></div>
      <div class="dots" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i></div>
    </div>
  </div>
</section>'''

STASHDAY = dict(
 name="Stashday", live=False,
 bg="#EEF8F3", bg2="#DFF2E9", a="#34C79A", ink=NAVY, a2="#FFB547", a3="#7C8CFF", band="#0E3B2E",
 nav=[("How it works", "#scene"), ("Pricing", "#pricing")],
 status="Coming soon",
 h1=["Payday has", "one number."],
 hero_extra='<span class="big" id="big" aria-label="299 dollars and 36 cents">$299.36</span>',
 lede="Set that aside and car registration, holidays, insurance and the vet are covered. Stashday does the math every payday.",
 note="iPhone, no account.",
 screens=["number.jpg", "checklist.jpg", "fund.jpg", "share.jpg"],
 trust=[t for _, t in C["stashday"]["trust"]],
 css=STASH_CSS, keep_js="legacy",
 blocks=[
  ("raw", STASH_SCENE),
  ("stories", dict(h="Every bill gets its own ring.", sub="Big friendly numbers, one color per fund, and a clear answer to “am I on track?”", items=[
   dict(h="Your number.", p=["One amount per paycheck covers every bill you add. Stashday works it out from your pay schedule and each bill's due date."], screens=["number.jpg"], alt="Your number: the amount to set aside"),
   dict(h="The payday checklist.", p=["Tick each fund off as you move the money. The amount left to set aside counts down with you."], screens=["checklist.jpg"], alt="The payday checklist"),
   dict(h="Every fund, on track.", p=["A ring for each fund shows what's saved and when it's due, so you can see what is on track at a glance."], screens=["fund.jpg"], alt="A fund's detail screen"),
   dict(h="A summary to share.", p=["Share a summary card of your funds when someone else should be in the loop."], screens=["share.jpg"], alt="A summary card you can share"),
  ])),
  ("who", dict(items=C["stashday"]["who"])),
  ("band", dict(h="Your money stays on your phone.", bg="#0E3B2E",
   sub="Stashday never connects to your bank. You type in your bills once and it does the math. Your funds stay on your iPhone, and the App Store privacy label is Data Not Collected.",
   html='<p style="margin-top:18px"><a href="privacy.html">Read the privacy policy</a></p>', nos=["No accounts", "No bank links", "No ads", "No analytics"])),
  ("plans", dict(h="Free for good. Pro when you outgrow it.", items=[
   ("Free", "$0", "Everything you need to start", ["3 funds", "The payday checklist", "Reminders and Siri", "A shareable summary"], False),
   ("Stashday Pro", "$14.99/yr", "Or $29.99 once. 7-day free trial on the yearly plan.", ["Unlimited funds", "Home and Lock Screen widgets with check-off", "CSV export"], True)],
   fine="No bank login. Data Not Collected. No ads. Works with weekly, every 2 weeks, twice a month or monthly pay.")),
  ("faq", dict(items=faq("stashday"), after='<p class="fine" style="margin:26px auto 0">Guide: <a href="guide/sinking-funds-biweekly-paycheck.html">How to plan sinking funds on a biweekly paycheck</a></p>')),
  ("more", C["stashday"]["more"]),
 ],
 finale=("One number, every payday.", "Coming soon to the App Store. Free for up to 3 funds."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html"), ("Terms", "terms.html"), ("Sinking funds guide", "guide/sinking-funds-biweekly-paycheck.html")],
 legal=["Stashday does the arithmetic for the bills you enter. It is not financial advice."],
)

# ---------------------------------------------------------------- Statecount
SC_CSS = r'''
.scplay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:center}
.limits{background:#fff;border-radius:32px;padding:28px;box-shadow:0 0 0 1px var(--line),0 50px 90px -46px rgba(13,42,79,.5)}
.limits h3{color:var(--soft);font-size:.95rem;margin:0 0 14px}
.lim{padding:16px 0;border-top:1px solid var(--line)}
.lim:first-of-type{border-top:0;padding-top:0}
.lim .lt{display:flex;justify-content:space-between;align-items:baseline;font-weight:700}
.lim .left{font-variant-numeric:tabular-nums}
.lim i{display:block;height:10px;border-radius:99px;background:var(--bg2);margin:10px 0 6px;overflow:hidden}
.lim u{display:block;height:100%;width:0;border-radius:99px;transition:width 1.4s cubic-bezier(.2,.8,.2,1)}
.lim small{color:var(--soft);font-variant-numeric:tabular-nums}
.others{list-style:none;margin:14px 0 0;padding:14px 0 0;border-top:1px solid var(--line);display:grid;gap:8px}
.others li{display:flex;justify-content:space-between}
.others li span:before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--c);margin-right:9px}
.scnote{font-size:.85rem;color:var(--soft);margin:14px 0 0}
.why p{font-size:1.15rem;max-width:44em}
@media(max-width:960px){.scplay{grid-template-columns:minmax(0,1fr);gap:36px}}
'''
SC_PLAY = '''<section class="sec demo" id="limits"><div class="wrap"><div class="scplay">
<div><h2>Know how many days you have left.</h2><p class="sub">Set a limit, like 183 days in New York. Statecount counts days used and days left, and gives you a heads-up at 30, 14 and 7 days left.</p></div>
<div class="limits" id="lims" aria-label="Example limits: New York 165 of 183 days, Florida 121 of 183 days">
  <h3>This year</h3>
  <div class="lim"><div class="lt"><span>New York</span><span class="left"><b data-to="18">18</b> days left</span></div><i><u style="background:#F08A3C" data-w="90"></u></i><small><span data-to="165">165</span> of 183 days</small></div>
  <div class="lim"><div class="lt"><span>Florida</span><span class="left"><b data-to="62">62</b> days left</span></div><i><u style="background:#2F6FD0" data-w="66"></u></i><small><span data-to="121">121</span> of 183 days</small></div>
  <ul class="others"><li><span style="--c:#3BB273">Canada</span><b>7 days</b></li><li><span style="--c:#E0559A">Massachusetts</span><b>2 days</b></li><li><span style="--c:#8E6BE0">New Jersey</span><b>1 day</b></li></ul>
  <p class="scnote">Example data. You choose each limit. Statecount doesn't know which rules apply to you.</p>
</div></div></div></section>'''
SC_JS = r'''
(function(){var c=document.getElementById('lims');if(!c)return;var red=matchMedia('(prefers-reduced-motion: reduce)').matches;
function go(){c.querySelectorAll('u[data-w]').forEach(function(u){u.style.width=u.dataset.w+'%'});
if(red)return;c.querySelectorAll('[data-to]').forEach(function(el){var to=+el.dataset.to,t0=performance.now();(function f(t){var k=Math.min(1,(t-t0)/1400);el.textContent=Math.round(to*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(f)})(t0)})}
if(!('IntersectionObserver' in window)||red){go();return}
var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){go();io.disconnect()}},{threshold:.4});io.observe(c)})();
'''

STATECOUNT = dict(
 name="Statecount", live=False,
 bg="#EEF3FB", bg2="#E1E9F7", a="#4A8FD6", ink=NAVY, a2="#F08A3C", a3="#3BB273", band="#0D2A4F",
 nav=[("How it works", "#how"), ("Pricing", "#pricing")],
 status="Coming soon",
 h1=["Count your days", "in every state."],
 lede="If you split your year between places, Statecount keeps a day-by-day record of where you were, and warns you before you reach a day limit you set, like 183 days.",
 note="iPhone. No account, no servers, no analytics.",
 screens=["home.jpg", "calendar.jpg"],
 trust=["Your location never leaves your phone", "Data Not Collected", "Alerts at 30, 14 and 7 days left", "A PDF and CSV report"],
 css=SC_CSS, js=SC_JS,
 blocks=[
  ("raw", SC_PLAY),
  ("who", dict(h="Who it's for", items=[("Snowbirds", "Who winter in Florida, Arizona or Texas and spend the rest of the year up north."), ("Remote workers", "Who work from different states through the year."),
                                          ("Second-home owners", "Who divide their time between two houses."), ("Frequent travelers", "Who keep an eye on days spent in a country.")])),
  ("band", dict(id="why", h="Why keep a record of your days?", bg="#0D2A4F",
   sub="Many states and countries use the number of days you spend there to decide whether you count as a resident for tax purposes. The rules differ from place to place, and you may be asked to show where you were on particular days. Memory and a rough spreadsheet are hard to rely on. A day-by-day record, with where each entry came from, is much easier to stand behind.",
   html='<p style="margin-top:18px;font-size:1.1rem">Statecount keeps that record for you on your phone, tells you how many days you have left before a limit you set, and never sends your location anywhere.</p><p class="fine">Statecount doesn\'t know which rules apply to you. Ask a tax professional about your situation.</p>')),
  ("stories", dict(items=[
   dict(h="Days used, days left.", p=["Every limit shows days used and days left, with alerts at 30, 14 and 7 days left, before you reach it."], screens=["home.jpg"], alt="Days tab: New York 165 of 183 days with 18 days left, Florida 121 of 183 (example data)"),
   dict(h="Every day, with its source.", p=["Each record shows whether it came from your phone's location or was entered or edited by you. Days with no record are flagged so you can fill them in. A week in Canada shows as Canada."], screens=["calendar.jpg"], alt="Calendar: July, each day colored by state, with a week in Canada (example data)"),
  ])),
  ("feats", dict(alt=True, h="Built to stand behind.", items=[
   ("lock", "Your location never leaves your phone", "The state or country is worked out on your iPhone. No account, no servers, no analytics. Data Not Collected."),
   ("pin", "Matched on the phone", "Your iPhone's location is matched against map boundaries built into the app (US Census and Natural Earth data). The app makes no network calls of its own."),
   ("bell", "Limits and alerts", "Days used and days left for every limit, with alerts at 30, 14 and 7 days left."),
   ("doc", "A report for your tax professional", "Export every day of the year as a PDF and CSV.")])),
  ("steps", dict(id="how", h="How it works", items=[(a, landing.esc(b)) for a, b in C["statecount"]["steps"]])),
  ("plans", dict(h="Pricing", items=[(n, p, per, items, hl) for n, p, per, items, hl in C["statecount"]["plans"]], fine=C["statecount"]["fine"])),
  ("faq", dict(items=faq("statecount"), after='<p class="fine" style="margin:26px auto 0">Guide: <a href="guide/how-the-183-day-rule-counts-a-day.html">How the 183-day rule counts a day</a></p>')),
  ("more", C["statecount"]["more"]),
 ],
 finale=("Know your days.", "Coming soon to the App Store. Screenshots show example data."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html"), ("183-day rule guide", "guide/how-the-183-day-rule-counts-a-day.html")],
 legal=["Statecount keeps records. It is not tax or legal advice."],
)

SPECS = {"mvn": MVN, "mackro": MACKRO, "stashday": STASHDAY, "statecount": STATECOUNT,
         "tabbed": TABBED, "fantasyqueens": FANTASYQUEENS, "sitout": SITOUT}
