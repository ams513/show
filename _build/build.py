"""Build Stark Showcase: index.html (+ sw.js cache list) and the cheat-sheet HTML.
Usage: python build.py <segno_lib_dir> <cheat_html_out>
Run from anywhere; writes into the parent folder (show_site)."""
import sys, re, os, html, hashlib, pathlib
sys.path.insert(0, sys.argv[1])
import segno

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = "https://starkforall.com"
PLEDGE = "Pay once. Works offline. Your data stays on your computer."

COV = [("cov-patients", "Patient list (demo patients)"), ("cov-chart", "A patient chart (demo data)"),
       ("cov-emergency", "Emergency screen"), ("cov-emergency-phone", "Emergency screen on a phone"),
       ("cov-outcomes", "Outcomes"), ("cov-todo", "To-do list"), ("cov-safety", "Safety plan")]
FEL = [("fel-home", "Home"), ("fel-directory", "Directory"), ("fel-teams", "Teams and rotas"),
       ("fel-checkin", "Check-in"), ("fel-giving", "Giving records"), ("fel-statement", "Year-end statement"),
       ("fel-phone", "Check-in on a phone")]

A = [
 dict(k="clinic", name="Clinic", sub="Stark Covenant", price="From $25, one time",
  say="This keeps your patients' records on your own computer, not in someone else's cloud, and you pay once.",
  tap="Swipe the real screens", tap_url="#clinic-show", tap_local=True,
  how="Covenant is a desktop app, so there is no browser trial. These are its real screens.",
  show="Point at the patient chart and the emergency screen. All patients shown are demo data.",
  qr=B + "/covenant.html", qr_show="starkforall.com/covenant.html", gallery=COV, clip=None,
  ask=[("How much?", "From $25, one time. No subscription."),
       ("Is my data safe?", "Records stay on your own computers, encrypted by the operating system. Nothing is sent to us."),
       ("What will it not do?", "It is in beta and is not a certified EHR or medical device. We do not claim HIPAA compliance, so do your own review before real patient data. It does not diagnose.")]),
 dict(k="contractor", name="Contractor", sub="Stark Trades", price="$29, one time",
  say="This runs a trade business from your phone: jobs, subs and cash. Watch it forecast your cash thirteen weeks out.",
  tap="Open Trades", tap_url=B + "/try/trades/", tap_local=False,
  how="In the app: tap Try it with a sample company, then tap Cash radar.",
  show="Point at Lowest likely point and Chance of going short. It is built from the sample company's invoices.",
  qr=B + "/try/trades/", qr_show="starkforall.com/try/trades/", gallery=None, clip=None,
  ask=[("How much?", "$29, one time. The free trial holds 15 of your own jobs, and the sample company is free."),
       ("Is my data safe?", "Encrypted on your computer with your passphrase. No account, no cloud, and the app has no network code."),
       ("What will it not do?", "It is not payroll or accounting, it sends no invoices or texts by itself, and it is not legal or tax advice. Lien and licence rules differ by state.")]),
 dict(k="teacher", name="Parent or teacher", sub="Stark Math", price="$24, one time",
  say="This is a math and science tutor that works with no internet. Watch a ball fly, with the exact formula beside it.",
  tap="Open the physics simulator", tap_url=B + "/try/math/#/sim", tap_local=False,
  how="In the app: tap Launch. Bonus: change the planet to Moon and tap Launch again.",
  show="Point at the formula next to the simulation, then at how far it landed.",
  qr=B + "/try/math/#/sim", qr_show="starkforall.com/try/math/", gallery=None,
  clip=("clips/math-sim.mp4", "Math physics simulator", "portrait"),
  ask=[("How much?", "$24, one time. No subscription."),
       ("Is my child's data safe?", "No accounts, ads, analytics or network calls. Progress stays in the browser on your device."),
       ("What will it not do?", "Madeline is a rule-based guide, not an AI and not a person, so she cannot chat. Screen translations are machine drafts, and placement is a quick guide, not a formal assessment.")]),
 dict(k="church", name="Church or community", sub="Stark Fellowship", price="$49, pay once",
  say="This keeps your directory, rotas, check-in and giving records on one computer, locked with each person's passphrase.",
  tap="Swipe the real screens", tap_url="#church-show", tap_local=True,
  how="Then hand over the free trial: their turn is the next screen.",
  show="Point at the rota, the check-in screen and the year-end giving statement.",
  qr=B + "/try/fellowship/", qr_show="starkforall.com/try/fellowship/", gallery=FEL, clip=None,
  ask=[("How much?", "$49, pay once. The trial is free."),
       ("Is our data safe?", "It stays on one computer, encrypted with each person's passphrase. Private care notes open only for the Leader and Care team roles."),
       ("What will it not do?", "It takes no payments and sends no messages. It records gifts made elsewhere. It is not a child safeguarding system, and an accountant should check statement wording.")]),
 dict(k="family", name="Family or senior", sub="Stark Warden", price="$10, one time",
  say="If a debt collector or scammer calls, this shows you what to say. Here is a pushy collector call. You pick the reply.",
  tap="Start the practice call", tap_url=B + "/try/warden/#/practice/pushy", tap_local=False,
  how="In the app: tap the second answer, Oh no, I'm so sorry. Then tap the first answer, and compare.",
  show="Point at the Confidence bar and the coach's note after each reply.",
  qr=B + "/try/warden/#/practice/pushy", qr_show="starkforall.com/try/warden/", gallery=None,
  clip=("clips/warden-call.mp4", "Warden call practice", "landscape"),
  ask=[("How much?", "$10, one time. No subscription."),
       ("Is my data safe?", "It stays on your device. No account. Your log is not encrypted by default; the vault and backups are, with your passphrase."),
       ("What will it not do?", "It is general information, not legal advice, and it is for the United States. It cannot prove a collector is real or fake.")]),
 dict(k="anyone", name="Anyone", sub="The free trial gallery", price="Free to try",
  say="Everyone's searching Stark. We're the other one.",
  tap="Open the trial gallery", tap_url=B + "/try/", tap_local=False,
  how="Sixteen apps, each one free to try in the browser.",
  show="Scroll slowly. Let them pick the app that looks like their life.",
  qr=B + "/try/", qr_show="starkforall.com/try/", gallery=None, clip=None,
  ask=[("How much?", "Trials are free. Each app is paid once, and its price is on its own page."),
       ("Is my data safe?", "Trials run in your browser. Nothing is uploaded, and your data stays on your device."),
       ("What will it not do?", "A trial has a limit, such as 15 jobs in Trades. Some apps are desktop only, and nothing syncs through a cloud.")]),
]


def qr_svg(url):
    s = segno.make(url, error="m").svg_inline(scale=1, border=2, dark="#000", light="#fff")
    s = re.sub(r'width="(\d+)" height="(\d+)"', r'viewBox="0 0 \1 \2" shape-rendering="crispEdges" role="img" aria-label="QR code"', s, 1)
    assert "style=" not in s
    return s


e = html.escape


def beat_gallery(a):
    k = a["k"]
    figs = "".join(f'<figure><img src="img/{f}.png" alt="{e(c)}"><figcaption>{e(c)}</figcaption></figure>' for f, c in a["gallery"])
    return f'<div class="gal" data-gal tabindex="0" aria-label="Screenshots, swipe sideways">{figs}</div><p class="gcount" data-gcount>1 / {len(a["gallery"])}</p>'


def audience(a):
    k = a["k"]
    clip = ""
    if a["clip"]:
        f, lab, o = a["clip"]
        clip = f'<button class="btn alt" type="button" data-clip="{f}" data-o="{o}">No signal? Play the clip</button>'
    tap_attr = "" if a["tap_local"] else ' target="_blank" rel="noopener"'
    gal = beat_gallery(a) if a["gallery"] else ""
    asks = "".join(f"<div><h3>{e(q)}</h3><p>{e(r)}</p></div>" for q, r in a["ask"])
    return f'''<section id="{k}" class="view aud" hidden>
<article class="beat" id="{k}-say"><p class="k">1 &middot; SAY</p><p class="big">{e(a["say"])}</p><a class="next" href="#{k}-tap">Next</a></article>
<article class="beat" id="{k}-tap"><p class="k">2 &middot; TAP</p><a class="btn go" href="{e(a["tap_url"])}"{tap_attr}>{e(a["tap"])}</a><p class="how">{e(a["how"])}</p>{clip}<a class="next" href="#{k}-show">Next</a></article>
<article class="beat" id="{k}-show"><p class="k">3 &middot; SHOW</p><p class="big">{e(a["show"])}</p>{gal}<a class="next" href="#{k}-turn">Their turn</a></article>
<article class="beat qrbeat" id="{k}-turn"><p class="k">THEIR TURN &middot; scan with your phone</p><div class="qr">{qr_svg(a["qr"])}</div><p class="url">{e(a["qr_show"])}</p><p class="price">{e(a["price"])}</p><p class="pledge">{PLEDGE}</p><a class="next" href="#{k}-ask">If they ask</a></article>
<article class="beat" id="{k}-ask"><p class="k">IF THEY ASK</p><div class="asks">{asks}</div><a class="next" href="#home">Done</a></article>
</section>'''


def index():
    btns = "".join(f'<a class="pick" href="#{a["k"]}"><span class="pn">{e(a["name"])}</span><span class="ps">{e(a["sub"])}</span></a>' for a in A)
    auds = "".join(audience(a) for a in A)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self'; connect-src 'self'; manifest-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'; object-src 'none'">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#08090b">
<meta name="color-scheme" content="dark">
<title>Stark Showcase</title>
<link rel="icon" href="img/eyes.jpg">
<link rel="stylesheet" href="css/show.css">
</head><body>
<a id="back" class="back" href="#home" hidden>&lsaquo; Home</a>
<main>
<section id="home" class="view home"><img class="eyes" src="img/eyes.jpg" alt="" width="96" height="96">
<h1>Stark Showcase</h1><p class="lede">Who are you talking to?</p><nav class="picks">{btns}</nav>
<p class="fine">Owner's tool. Open once with signal and it works offline.</p></section>
{auds}
</main>
<dialog id="clipbox"><button type="button" class="btn" id="clipclose">Close</button><video id="clipvid" controls playsinline preload="none"></video></dialog>
<noscript><p class="fine">This page needs JavaScript to switch screens.</p></noscript>
<script src="js/show.js"></script>
</body></html>'''


def cheat():
    cards = ""
    for a in A:
        asks = " ".join(f"<b>{e(q)}</b> {e(r)}" for q, r in a["ask"][:1])
        cards += f'''<div class="c"><h2>{e(a["name"])} <span>{e(a["sub"])} &middot; {e(a["price"])}</span></h2>
<p><b>SAY</b> {e(a["say"])}</p><p><b>TAP</b> {e(a["tap"])}{"" if a["tap_local"] else " (" + e(a["qr_show"]) + ")"}. {e(a["how"])}</p>
<p><b>SHOW</b> {e(a["show"])}</p><p class="s"><b>THEIR TURN</b> Full-screen QR to {e(a["qr_show"])}. {PLEDGE}</p></div>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Stark Showcase cheat sheet</title><style>
@page{{size:Letter;margin:.4in}}*{{box-sizing:border-box}}body{{margin:0;font:10.5pt/1.3 Arial,Helvetica,sans-serif;color:#000}}
h1{{font-size:18pt;margin:0 0 2pt}}.t{{margin:0 0 8pt;font-size:10pt}}.g{{display:grid;grid-template-columns:1fr 1fr;gap:7pt}}
.c{{border:1.5pt solid #000;border-radius:5pt;padding:6pt 8pt;break-inside:avoid}}h2{{font-size:12.5pt;margin:0 0 3pt}}h2 span{{font-weight:400;font-size:9pt}}
p{{margin:0 0 3pt}}b{{display:inline-block;min-width:44pt;font-size:8.5pt;letter-spacing:.05em}}.s{{font-size:9pt;margin:0}}
.f{{margin-top:7pt;font-size:9pt}}</style></head><body><h1>Stark Showcase: 60 seconds</h1>
<p class="t">Open <b style="min-width:0">starkforall.com/show/</b> on your phone. Say it, tap it, show it, then hand over the QR. Pay once. Works offline. Your data stays on your computer.</p>
<div class="g">{cards}</div>
<p class="f">Trades: tap Try it with a sample company, then Cash radar. Warden: tap the second answer, then the first. Math: tap Launch. No signal: Math and Warden have a clip button. Never promise legal, tax or medical outcomes.</p></body></html>'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    pathlib.Path(sys.argv[2]).write_text(cheat(), encoding="utf-8")
    files = ["./", "index.html", "css/show.css", "js/show.js", "img/eyes.jpg"] + [f"img/{f}.png" for g in (COV, FEL) for f, _ in g] + ["clips/math-sim.mp4", "clips/warden-call.mp4"]
    h = hashlib.sha1()
    for f in files[1:]:
        h.update((ROOT / f).read_bytes())
    (ROOT / "sw.js").write_text(f'''/* Stark Showcase service worker: caches only this folder's own files. */
const V = "show-{h.hexdigest()[:10]}", FILES = {files!r};
self.addEventListener("install", e => {{ self.skipWaiting(); e.waitUntil(caches.open(V).then(c => Promise.all(FILES.map(f => c.add(f).catch(() => 0))))); }});
self.addEventListener("activate", e => {{ e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== V).map(x => caches.delete(x)))).then(() => self.clients.claim())); }});
self.addEventListener("fetch", e => {{
  const r = e.request, u = new URL(r.url);
  if (r.method !== "GET" || u.origin !== self.location.origin) return;
  e.respondWith(caches.open(V).then(async c => {{
    let m = await c.match(r, {{ ignoreSearch: true }});
    if (!m) {{ try {{ m = await fetch(r); if (m.ok && m.status === 200) c.put(r, m.clone()); return m; }} catch (x) {{ return (await c.match("index.html")) || Response.error(); }} }}
    const rg = r.headers.get("range");
    if (!rg) return m;
    const b = await m.blob(), mm = /bytes=(\\d*)-(\\d*)/.exec(rg), s = mm[1] ? +mm[1] : 0, en = mm[2] ? Math.min(+mm[2], b.size - 1) : b.size - 1;
    return new Response(b.slice(s, en + 1), {{ status: 206, headers: {{ "Content-Type": m.headers.get("Content-Type") || "video/mp4", "Content-Range": `bytes ${{s}}-${{en}}/${{b.size}}`, "Content-Length": en + 1 - s }} }});
  }}));
}});
''', encoding="utf-8")
    print("built", h.hexdigest()[:10])
