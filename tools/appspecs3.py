"""App page spec for Wishmallow (tools/apppage.py). No em dashes (house style)."""
import landing

NAVY = "#0B1A4A"
URL = "https://couchcoopstudios.com/wishmallow/"
TITLE = "Wishmallow: Cozy Dollhouse Life Sim for iPhone | Couch Co-Op Studios"
DESC = ("Wishmallow is a cozy 3D dollhouse for iPhone. Build a little house, make a wish for any piece of furniture, "
        "and watch your pals cook, nap and chat. Pay once. No ads, no timers.")

WISHMALLOW = dict(
 name="Wishmallow", live=False, soon="Coming soon on the App Store",
 head=dict(
  title=TITLE,
  meta=[f'<meta name="description" content="{DESC}">',
        f'<link rel="canonical" href="{URL}">',
        '<meta property="og:title" content="Wishmallow: a cozy dollhouse that grants wishes">',
        '<meta property="og:description" content="Build a little 3D house, wish for any piece of furniture and watch your pals live in it. Pay once. No ads, no timers.">',
        f'<meta property="og:url" content="{URL}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:image" content="{URL}img/icon.png">',
        '<meta name="twitter:card" content="summary">'],
  ld=[], js=[]),
 bg="#FBF3E4", bg2="#F4E6CF", a="#F6A9B8", ink=NAVY, a2="#FFD25E", a3="#7DB36A", band="#2C2A4A",
 nav=[("Wishes", "#wish"), ("Pricing", "#pricing")],
 status="A cozy 3D dollhouse",
 h1=["A little house", "that grants wishes."],
 lede="Build a cozy house room by room, wish for any piece of furniture you can dream up, and watch your pals cook, nap, read and chat in it.",
 note="Made for iPhone, and for iPhone Duo. Pay once. No ads, no timers.",
 screens=["room.jpg", "build.jpg", "wish.jpg"],
 trust=["No ads", "No timers or energy", "No account", "Pay once"],
 blocks=[
  ("stories", dict(id="wish", items=[
   dict(h="Wish for anything.", p=["Type a wish like \"a strawberry bed\" or \"a sleepy cloud lamp\" and it appears with a poof, ready to place. You can wish for new pals too."],
        screens=["wish.jpg"], alt="The Make a wish screen, with a strawberry bed under My wishes"),
   dict(h="Your pals live their own little lives.", p=["Pals cook, eat, nap, watch TV, read, dance and chat with each other. Each one has moods, likes and a bedtime, and they take the stairs like anyone else."],
        screens=["room.jpg"], alt="Mochi and Pip eating lunch together at the kitchen table"),
   dict(h="Build it your way.", p=["Add rooms and floors, paint the walls, lay the floors and arrange every piece. Then set your house in a meadow, on a beach, in the mountains, on a city rooftop or in Future Tokyo."],
        screens=["build.jpg"], alt="Build mode in the kitchen, with the furniture drawer open and Pip cooking"),
  ])),
  ("feats", dict(alt=True, h="Small comforts, all the way down.", items=[
   ("spark", "Day, night and weather", "The light follows a gentle clock from sunrise to the lamps coming on at night. Pick rain or snow in Settings for a cozier day."),
   ("camera", "Photo mode", "Hide every button for a clean picture of your house, then save it to Photos or share it."),
   ("home", "A pal on your Home Screen", "A widget shows how a pal is doing. Give them a snack or a pat without opening the game."),
   ("repeat", "Made for iPhone Duo", "Fold it shut to peek in on your pals, open it up to build."),
  ])),
  ("plans", dict(id="pricing", h="Free to play. Pay once for more.", items=[
   ("Free", "$0", "The whole game, a little smaller", ["One floor and up to 5 rooms", "Up to 3 pals", "3 furniture wishes and 1 pal wish a day", "Photo mode and the Home Screen widget"], False),
   ("Mallow Magic", "$6.99", "One-time purchase", ["Up to 3 floors and 15 rooms", "Up to 8 pals", "30 furniture wishes and 10 pal wishes a day", "Restore it any time on a new phone"], True)],
   fine="Mallow Magic is a one-time purchase, not a subscription. There are no coins, no energy and no timers to pay down. Prices in US dollars.")),
  ("band", dict(h="No account. No ads. No tracking.", bg="#2C2A4A",
   sub="Your house is saved on your iPhone. The only thing that ever leaves it is a wish you choose to make, and you can turn wishes off.",
   html='<p style="margin-top:18px"><a href="privacy.html">Read exactly what it stores and sends</a></p>', nos=["No account", "No ads", "No analytics", "No tracking"])),
  ("faq", dict(h="Frequently asked questions", items=[
   ("How do wishes work?", "You type a few words. They go to our wish helper, where Claude, an AI from Anthropic, picks the shape, colors and pattern from the game's own pieces. If the helper can't be reached, the game designs the piece on your phone instead."),
   ("Is it safe for kids?", "Wishmallow is made for all ages. The wish helper keeps everything cute and turns down wishes that aren't, and every wished item has a Report button."),
   ("Do I need an account?", "No. There's no sign-up and nothing to log in to. Your house is saved on your phone."),
   ("Is it a subscription?", "No. Mallow Magic is a one-time $6.99, and the free game never runs out or makes you wait."),
  ])),
 ],
 finale=("A little house that grants wishes.", "Coming soon on the App Store. Free to play, with no ads and no timers."),
 links=[("Support", "support.html"), ("Privacy", "privacy.html")],
 legal=["Claude is a trademark of Anthropic. Wishmallow is not affiliated with or endorsed by Anthropic."],
)
