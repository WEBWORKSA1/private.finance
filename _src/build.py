#!/usr/bin/env python3
"""Static site generator for Private.Finance.
Usage (from the repo root):  pip install markdown && python3 _src/build.py
Regenerates every page in the repo root from: _src/content/*.md (guides),
_src/tools_data.py, _src/glossary_data.py, _src/videos.json and _src/pages.py.
To add a guide: drop a new .md file (same frontmatter) into _src/content and rebuild.
"""
import os, re, json, shutil, base64, html
import markdown
from tools_data import TOOLS
from glossary_data import GLOSSARY

HERE = os.path.dirname(os.path.abspath(__file__))      # repo/_src
ROOT = os.path.dirname(HERE)                            # repo root = published site (GitHub Pages: main / root)
OUT = os.environ.get("PF_OUT", ROOT)
CONTENT = os.path.join(HERE, "content")
KEEP = {".git", ".github", "_src", "README.md", "BUILD-PROMPT.md", "RESEARCH.md", "LICENSE", ".gitignore"}
DOMAIN = "https://private.finance"
NAME = "Private.Finance"
UPDATED = "October 30, 2026"
ISO = "2026-10-30"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
WEBWORKS = "https://web.works/contact"
# Contact inbox is stored only in encoded form so it never appears in source or pages.
E1 = "MWFza3Jvd2Jldw=="
E2 = "Z21haWwuY29t"

esc = html.escape
PAGES = []          # for sitemap
SEARCH = []         # for search index

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="10" fill="#0d1b1e"/><circle cx="20" cy="20" r="11" fill="none" stroke="#c9a227" stroke-width="2.4"/><circle cx="20" cy="17.5" r="3.2" fill="#c9a227"/><path d="M18.3 19.5h3.4l1 6h-5.4z" fill="#c9a227"/><g stroke="#c9a227" stroke-width="2" stroke-linecap="round"><path d="M20 4.5v3"/><path d="M20 32.5v3"/><path d="M4.5 20h3"/><path d="M32.5 20h3"/></g></svg>'''

NAV = [("tools/", "Tools"), ("guides/", "Guides"), ("private-wealth/", "Private Wealth"), ("videos/", "Videos"),
       ("resources/", "Resources"), ("glossary/", "Glossary"), ("support/", "Support")]


def rel(path):
    return "../" * path.count("/")


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def head(path, title, desc, schema=None, ogtype="website"):
    P = rel(path)
    url = DOMAIN + "/" + (path[:-10] if path.endswith("index.html") else path)
    full = title if NAME in title else f"{title} | {NAME}"
    sch = "".join(jsonld(s) for s in (schema or []))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0d1b1e">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{P}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}assets/css/style.css">
<script>window.PF={{base:"{P}"}};try{{var t=localStorage.getItem("pf_theme");if(t)document.documentElement.setAttribute("data-theme",JSON.parse(t));}}catch(e){{}}</script>
{ADS}
{sch}
</head>'''


def header(path, active=""):
    P = rel(path)
    items = "".join(
        f'<li><a href="{P}{u}"{" aria-current=page" if active == u else ""}>{t}</a></li>' for u, t in NAV)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topstrip">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership — <a href="{WEBWORKS}" target="_blank" rel="noopener">contact here →</a></div>
<header class="site-header"><nav class="wrap nav" aria-label="Main">
<a class="brand" href="{P}" aria-label="{NAME} home">{LOGO}<span>Private<span class="dot">.</span>Finance</span></a>
<button class="icon-btn burger" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<ul class="menu">{items}
<li><button class="icon-btn" data-search aria-label="Search (press /)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button></li>
<li><button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button></li>
<li><a class="btn btn-primary btn-sm" href="{P}get-matched/" style="color:#fff">Get matched free</a></li></ul>
</nav></header>
<main id="main">'''


def footer(path, scripts=()):
    P = rel(path)
    tools = "".join(f'<li><a href="{P}tools/{t["slug"]}/">{t["name"].split(" (")[0].replace(" Calculator","").replace(" Planner","")}</a></li>' for t in TOOLS[:7])
    sc = "".join(f'<script src="{P}assets/js/{s}" defer></script>' for s in scripts)
    return f'''</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="{P}" style="color:#fff">{LOGO}<span>Private<span class="dot">.</span>Finance</span></a>
<p style="margin-top:14px;max-width:34ch">Private-by-design money tools and plain-English guides. Your numbers stay on your device.</p>
<form class="newsletter-form" data-pf data-subject="Newsletter signup" data-ok="You're in. Watch your inbox for the next issue."><label for="nl-{path.count('/')}" class="muted" style="font-size:.85rem">Weekly money brief — free</label>
<div class="newsletter"><input id="nl-{path.count('/')}" type="email" name="email" placeholder="you@email.com" required autocomplete="email"><input class="hp" name="_honey" tabindex="-1" autocomplete="off"><button class="btn btn-gold btn-sm" type="submit">Join</button></div></form></div>
<div><h4>Tools</h4><ul>{tools}<li><a href="{P}tools/">All tools →</a></li></ul></div>
<div><h4>Learn</h4><ul><li><a href="{P}guides/">Guides</a></li><li><a href="{P}private-wealth/">Private wealth hub</a></li><li><a href="{P}videos/">Videos</a></li><li><a href="{P}glossary/">Glossary</a></li><li><a href="{P}resources/">Official resources</a></li><li><a href="{P}get-matched/">Find an advisor</a></li></ul></div>
<div><h4>Community</h4><ul><li><a href="{P}support/">Support us / Donate</a></li><li><a href="{P}contests/">Contests &amp; prizes</a></li><li><a href="{P}careers/">Careers &amp; talent</a></li><li><a href="{P}advertise/">Advertise &amp; sponsor</a></li><li><a href="{P}contact/">Contact</a></li><li><a href="{WEBWORKS}" target="_blank" rel="noopener">Buy this domain</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{P}about/">About</a></li><li><a href="{P}editorial-policy/">Editorial policy</a></li><li><a href="{P}privacy-policy/">Privacy policy</a></li><li><a href="{P}cookie-policy/">Cookie policy</a></li><li><a href="{P}terms/">Terms of use</a></li><li><a href="{P}disclaimer/">Disclaimer</a></li><li><a href="{P}trademark/">Trademark &amp; copyright</a></li><li><a href="{P}sitemap/">Sitemap</a></li></ul></div>
</div>
<div class="legal-small">
<p><b>Not financial advice.</b> Content on {NAME} is for general education only and does not consider your personal circumstances. Consult a licensed professional before acting. Calculator results are estimates.</p>
<p><b>Advertising &amp; compensation disclosure:</b> {NAME} is supported by advertising (including Google AdSense), sponsorships, reader support and referral arrangements with professional firms. Compensation never determines our editorial conclusions. <a href="{P}about/#how-we-make-money">How we make money</a>.</p>
<p><b>Trademark &amp; copyright:</b> "{NAME}" is the name of this independent website and uses the words "private" and "finance" in their ordinary descriptive sense. It is not affiliated with, endorsed by or connected to any company, product or registered mark named "Private Finance" or similar. All third-party names and marks belong to their owners. © <span data-year>2026</span> {NAME}. All rights reserved. <a href="{P}trademark/">Full disclosure</a>.</p>
</div></div></footer>
<div class="mobile-cta"><a class="btn btn-ghost" href="{P}tools/">Free tools</a><a class="btn btn-primary" href="{P}get-matched/">Get matched</a></div>
<div class="cookie" role="dialog" aria-label="Cookie notice"><b>Cookies &amp; privacy</b><p style="margin:6px 0 0">Our calculators never upload your numbers. We and our advertising partners (including Google) use cookies to show and measure ads. See our <a href="{P}privacy-policy/">Privacy</a> and <a href="{P}cookie-policy/">Cookie</a> policies.</p><div class="btns"><button class="btn btn-primary btn-sm" data-cookie="all">Accept</button><button class="btn btn-ghost btn-sm" data-cookie="essential">Essential only</button></div></div>
<div class="search-modal" role="dialog" aria-label="Search"><div class="search-box"><input type="text" placeholder="Search tools, guides and terms…" aria-label="Search"><div class="search-results"></div></div></div>
<script src="{P}assets/js/main.js" defer></script>{sc}
</body></html>'''


def write(path, title, desc, body, active="", schema=None, scripts=(), ogtype="website", index=True, priority="0.7"):
    crumbs_schema = []
    doc = head(path, title, desc, (schema or []) + crumbs_schema, ogtype) + header(path, active) + body + footer(path, scripts)
    doc = doc.replace("__P__", rel(path))
    fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(doc)
    if index:
        PAGES.append((path[:-10] if path.endswith("index.html") else path, priority))


def ad(kind="inArticle"):
    return f'<div class="ad-wrap" data-ad="{kind}"></div>'


def crumbs(path, trail):
    P = rel(path)
    parts = [f'<a href="{P}">Home</a>'] + [f'<a href="{P}{u}">{t}</a>' if u else f'<span>{t}</span>' for u, t in trail]
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
    for i, (u, t) in enumerate(trail):
        items.append({"@type": "ListItem", "position": i + 2, "name": t, "item": DOMAIN + "/" + (u or (path[:-10] if path.endswith("index.html") else path))})
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>", {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs) + "</div>"


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def lead_inline(P, goal="investing", heading="Want a professional to check this plan?"):
    return f'''<div class="inline-lead"><span class="eyebrow">Free · No obligation</span><h3 style="margin-top:6px">{heading}</h3>
<p class="muted">Tell us your goal and we'll introduce you to independent, fee-only advisors who fit. Takes about 60 seconds.</p>
<div class="row"><select id="il-assets" aria-label="Investable assets"><option value="under-50k">Under 50k</option><option value="50k-250k">50k – 250k</option><option value="250k-1m" selected>250k – 1M</option><option value="1m-5m">1M – 5M</option><option value="5m-plus">5M+</option></select>
<a class="btn btn-primary" href="{P}get-matched/?goal={goal}&amp;source=inline" onclick="this.href=this.href.split('&amp;assets')[0]+'&amp;assets='+document.getElementById('il-assets').value">Get matched free →</a></div></div>'''


# ---------------------------------------------------------------- guides
def load_guides():
    gs = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".md"):
            continue
        raw = open(os.path.join(CONTENT, fn), encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            continue
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        meta["body"] = m.group(2)
        meta["read"] = int(re.sub(r"\D", "", meta.get("read", "8")) or 8)
        gs.append(meta)
    order = ["private-wealth-management", "fee-only-financial-advisor", "how-much-to-retire", "compound-interest", "50-30-20-budget",
             "emergency-fund", "index-funds-101", "private-banking", "private-credit", "private-equity-for-individuals",
             "private-mortgage-insurance", "debt-avalanche-vs-snowball", "credit-score-basics", "private-student-loans", "financial-privacy"]
    gs.sort(key=lambda g: order.index(g["slug"]) if g["slug"] in order else 99)
    return gs


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render_guide(g, guides):
    path = f"guides/{g['slug']}/index.html"
    P = rel(path)
    body = g["body"]
    # split FAQ
    faqs = []
    fm = re.search(r"^##\s*FAQ.*?$(.*)", body, re.S | re.M)
    if fm:
        faq_txt = fm.group(1)
        body = body[:fm.start()]
        for q, a in re.findall(r"^###\s*(.+?)\s*$\n+(.*?)(?=^###|\Z)", faq_txt, re.S | re.M):
            faqs.append((q.strip(), " ".join(a.split())))
    h = markdown.markdown(body, extensions=["tables", "sane_lists"])
    # ids on h2
    def addid(m):
        t = re.sub("<.*?>", "", m.group(1))
        return f'<h2 id="{slugify(t)}">{m.group(1)}</h2>'
    h = re.sub(r"<h2>(.*?)</h2>", addid, h)
    # wrap key takeaways
    h = re.sub(r'(<h2 id="key-takeaways">.*?</h2>\s*<ul>.*?</ul>)', r'<div class="takeaways">\1</div>', h, flags=re.S)
    # insert ad + tool CTA after 3rd and 5th h2
    tool = next((t for t in TOOLS if t["slug"] == g.get("tool")), TOOLS[0])
    tool_box = f'<div class="note" style="margin:28px 0"><b>{tool["icon"]} Try it with your numbers:</b> <a href="{P}tools/{tool["slug"]}/">{tool["name"]}</a> — free, private, runs in your browser.</div>'
    parts = re.split(r'(?=<h2 id=)', h)
    out = []
    for i, p in enumerate(parts):
        if i == 3:
            out.append(ad("inArticle"))
        if i == 5:
            out.append(tool_box)
        out.append(p)
    h = "".join(out)
    goal = {"Wealth": "wealth", "Retirement": "retirement", "Investing": "investing", "Debt": "debt", "Real Estate": "home", "Banking": "wealth", "Budgeting": "investing", "Credit": "debt", "Privacy": "wealth"}.get(g["category"], "investing")
    related = [x for x in guides if x["slug"] != g["slug"] and x["category"] == g["category"]][:2]
    related += [x for x in guides if x["slug"] != g["slug"] and x not in related][: 3 - len(related)]
    rel_html = "".join(f'<a class="card tile" href="{P}guides/{r["slug"]}/"><span class="tag">{r["category"]}</span><h3>{esc(r["title"])}</h3><p>{esc(r["description"])}</p></a>' for r in related)
    vid = VIDEO_BY_TOPIC.get(g["slug"])
    vid_html = ""
    if vid:
        vid_html = f'<h2 id="watch">Watch: a visual explainer</h2>{video_card(vid)}<p class="muted" style="font-size:.85rem">Video by {esc(vid["channel"])}, embedded via YouTube. {NAME} is not affiliated with the creator.</p>'
    cr, crs = crumbs(path, [("guides/", "Guides"), (None, g["title"])])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["description"],
           "datePublished": ISO, "dateModified": ISO, "author": {"@type": "Organization", "name": f"{NAME} Editorial Team", "url": DOMAIN + "/about/"},
           "publisher": {"@type": "Organization", "name": NAME, "logo": {"@type": "ImageObject", "url": DOMAIN + "/favicon.svg"}},
           "mainEntityOfPage": DOMAIN + "/" + path[:-10]}
    sch = [art, crs] + ([faq_schema(faqs)] if faqs else [])
    words = len(re.sub("<.*?>", " ", h).split())
    page = f'''<article>
<header class="article-head"><div class="wrap">{cr}<span class="tag">{g["category"]}</span>
<h1 style="max-width:22ch;margin-top:12px">{esc(g["title"])}</h1><p class="lede" style="max-width:62ch">{esc(g["description"])}</p>
<div class="byline"><span>By <b>{NAME} Editorial Team</b></span><span>·</span><span>Updated <time datetime="{ISO}">{UPDATED}</time></span><span>·</span><span>{g["read"]} min read</span><span>·</span><a href="{P}editorial-policy/">How we write &amp; fact-check</a></div></div></header>
<div class="wrap article-layout" style="padding-bottom:40px">
<div class="prose">{h}{vid_html}
{"<h2 id='faq'>Frequently asked questions</h2>" + faq_html(faqs) if faqs else ""}
<div class="disclosure"><b>Educational content only.</b> This guide is general information, not personal financial, tax or legal advice. Rules, limits and rates vary by country and change over time — confirm details with official sources or a licensed professional. See our <a href="{P}disclaimer/">disclaimer</a>.</div>
{lead_inline(P, goal)}
{ad("footer")}
</div>
<aside class="aside"><div class="sticky">
<div class="card"><b class="eyebrow">On this page</b><nav class="toc" data-auto style="margin-top:10px"></nav></div>
<div class="card"><span style="font-size:1.6rem">{tool["icon"]}</span><h3 style="margin-top:8px">{tool["name"]}</h3><p class="muted" style="font-size:.93rem">{tool["short"]}</p><a class="btn btn-ghost btn-sm" href="{P}tools/{tool["slug"]}/">Open calculator →</a></div>
<div class="card" style="background:var(--ink);color:#efeadb;border-color:var(--ink)"><b style="color:var(--gold-2)">Talk to a fee-only advisor</b><p style="font-size:.93rem;margin:8px 0 14px;color:#c8d3d0">Free introductions to independent professionals. No obligation.</p><a class="btn btn-gold btn-sm" href="{P}get-matched/?goal={goal}&amp;source=sidebar">Get matched →</a></div>
{ad("sidebar")}
</div></aside></div>
<section style="padding-top:0"><div class="wrap"><h2>Keep reading</h2><div class="grid g3">{rel_html}</div></div></section>
</article>'''
    write(path, g["title"], g["description"], page, "guides/", sch, ogtype="article", priority="0.8")
    SEARCH.append({"t": g["title"], "d": g["description"], "c": "Guide · " + g["category"], "u": f"guides/{g['slug']}/", "k": g["category"]})
    return words


# ---------------------------------------------------------------- videos
VIDEOS = []
VIDEO_BY_TOPIC = {}


def load_videos():
    fp = os.path.join(HERE, "videos.json")
    if os.path.exists(fp):
        VIDEOS.extend(json.load(open(fp)))
    for v in VIDEOS:
        for s in v.get("guides", []):
            VIDEO_BY_TOPIC.setdefault(s, v)


def video_card(v):
    return f'''<div class="vid" data-id="{v["id"]}" data-title="{esc(v["title"])}" role="button" tabindex="0" aria-label="Play video: {esc(v["title"])}"><img loading="lazy" src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" alt="{esc(v["title"])}" width="480" height="360"><div class="play"><span>▶</span></div></div>'''


# ---------------------------------------------------------------- tools
def render_tool(t, guides):
    path = f"tools/{t['slug']}/index.html"
    P = rel(path)
    gmap = {g["slug"]: g for g in guides}
    rg = "".join(f'<li><a href="{P}guides/{s}/">{esc(gmap[s]["title"])}</a></li>' for s in t["guides"] if s in gmap)
    cr, crs = crumbs(path, [("tools/", "Tools"), (None, t["name"])])
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": DOMAIN + "/" + path[:-10],
           "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "description": t["desc"],
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    goal = {"Retirement": "retirement", "Real Estate": "home", "Debt": "debt", "Wealth": "wealth"}.get(t["cat"], "investing")
    others = "".join(f'<a class="card tile" href="{P}tools/{o["slug"]}/"><span class="ico">{o["icon"]}</span><h3>{o["name"]}</h3><p>{o["short"]}</p></a>' for o in TOOLS if o["slug"] != t["slug"])[:0]
    other_list = [o for o in TOOLS if o["slug"] != t["slug"]][:4]
    others = "".join(f'<a class="card tile" href="{P}tools/{o["slug"]}/"><span class="ico">{o["icon"]}</span><h3>{o["name"]}</h3><p>{o["short"]}</p></a>' for o in other_list)
    body = f'''<section style="padding-top:36px"><div class="wrap">{cr}
<div class="section-head"><div><span class="tag">{t["cat"]}</span><h1 style="font-size:clamp(2rem,4vw,2.8rem);margin-top:10px">{t["icon"]} {t["name"]}</h1><p class="lede" style="max-width:60ch">{t["desc"]}</p></div>
<label class="currency-pick">Currency <select data-currency aria-label="Currency"><option>USD</option><option>CAD</option><option>GBP</option><option>EUR</option><option>INR</option><option>AUD</option><option>AED</option><option>LKR</option></select></label></div>
<div class="calc" data-calc="{t["slug"]}">
<form class="card" onsubmit="return false" aria-label="Calculator inputs">{t["inputs"]}
<div class="privacy-note">Private by design: calculations run on your device. Nothing is uploaded.</div></form>
<div class="card results" aria-live="polite">{t["results"]}
<div class="pill-list" style="margin-top:16px"><button type="button" id="calc-share">Copy shareable link</button><button type="button" id="calc-print">Print / save PDF</button></div></div>
</div>
{ad("top")}
<div class="article-layout" style="margin-top:40px"><div class="prose"><h2 id="how-it-works">How this calculator works</h2>{t["how"]}
<h2 id="faq">Frequently asked questions</h2>{faq_html(t["faq"])}
{lead_inline(P, goal)}</div>
<aside class="aside"><div class="card"><b class="eyebrow">Learn more</b><ul style="padding-left:1.1em;margin:10px 0 0">{rg}</ul></div>{ad("sidebar")}</aside></div>
<h2 style="margin-top:48px">More free tools</h2><div class="grid g4">{others}</div>
<p class="disclosure">Results are estimates for educational purposes based on the inputs and assumptions shown; they are not a guarantee or a recommendation. Last reviewed {UPDATED}.</p>
</div></section>'''
    write(path, t["name"] + " — Free & Private", t["desc"], body, "tools/", [app, crs, faq_schema(t["faq"])], scripts=("calc.js",), priority="0.9")
    SEARCH.append({"t": t["name"], "d": t["short"], "c": "Tool · " + t["cat"], "u": f"tools/{t['slug']}/", "k": t["cat"] + " calculator"})


# ---------------------------------------------------------------- simple pages
def simple(path, title, desc, inner, active="", lede="", schema=None, eyebrow=""):
    cr, crs = crumbs(path, [(None, title)])
    body = f'''<section style="padding-top:40px"><div class="wrap narrow">{cr}{f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ''}<h1>{esc(title)}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}<div class="prose" style="margin-top:24px">{inner}</div></div></section>'''
    write(path, title, desc, body, active, (schema or []) + [crs], priority="0.5")
    SEARCH.append({"t": title, "d": desc, "c": "Page", "u": path[:-10], "k": ""})


exec(open(os.path.join(HERE, "pages.py"), encoding="utf-8").read())


def main():
    if os.path.exists(OUT):
        for item in os.listdir(OUT):
            if item in KEEP:
                continue
            fp = os.path.join(OUT, item)
            shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
    mj = os.path.join(OUT, "assets/js/main.js")
    s = open(mj).read().replace("__E1__", E1).replace("__E2__", E2)
    open(mj, "w").write(s)
    load_videos()
    guides = load_guides()
    total = 0
    for g in guides:
        total += render_guide(g, guides)
    for t in TOOLS:
        render_tool(t, guides)
    build_pages(guides)
    for term, d in GLOSSARY:
        SEARCH.append({"t": term, "d": d[:110] + ("…" if len(d) > 110 else ""), "c": "Glossary", "u": "glossary/#" + slugify(term), "k": "definition"})
    json.dump(SEARCH, open(os.path.join(OUT, "search-index.json"), "w"), ensure_ascii=False)
    # sitemap / robots / ads.txt etc.
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in PAGES:
        sm.append(f"<url><loc>{DOMAIN}/{u}</loc><lastmod>{ISO}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT, "ads.txt"), "w").write("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    open(os.path.join(OUT, "CNAME"), "w").write("private.finance\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "favicon.svg"), "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    json.dump({"name": NAME, "short_name": "Private.Finance", "start_url": "./", "display": "standalone", "background_color": "#f6f3ec",
               "theme_color": "#0d1b1e", "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
              open(os.path.join(OUT, "site.webmanifest"), "w"), indent=1)
    print(f"Built {len(PAGES)} pages, {len(guides)} guides (~{total:,} words), {len(TOOLS)} tools → {OUT}")


if __name__ == "__main__":
    main()
