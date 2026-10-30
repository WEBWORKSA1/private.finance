# Page definitions — executed inside build.py's namespace

def choice(name, value, label, icon="", req=True, typ="radio"):
    return f'<label class="choice"><input type="{typ}" name="{name}" value="{value}"{" required" if req and typ=="radio" else ""}><span><em>{icon}</em>{label}</span></label>'


def quiz_q(n, q, opts, fix):
    o = "".join(choice(f"q{n}", pts, lab, req=False) for lab, pts in opts)
    return f'<div class="quiz-q" data-fix="{fix}"><p class="eyebrow">Question {n} of 6</p><h3>{q}</h3><div class="choices">{o}</div></div>'


def build_pages(guides):
    G = {g["slug"]: g for g in guides}

    # ------------------------------------------------------------ HOME
    path = "index.html"; P = ""
    tools_html = "".join(f'<a class="card tile reveal" href="tools/{t["slug"]}/"><span class="ico">{t["icon"]}</span><h3>{t["name"].split(" (")[0]}</h3><p>{t["short"]}</p></a>' for t in TOOLS[:8])
    feat = [G[s] for s in ["how-much-to-retire", "50-30-20-budget", "fee-only-financial-advisor", "index-funds-101", "debt-avalanche-vs-snowball", "financial-privacy"] if s in G]
    feat_html = "".join(f'<a class="card tile reveal" href="guides/{g["slug"]}/"><span class="tag">{g["category"]}</span><h3>{esc(g["title"])}</h3><p>{esc(g["description"])}</p><small class="muted">{g["read"]} min read</small></a>' for g in feat)
    pw = [G[s] for s in ["private-wealth-management", "private-banking", "private-credit", "private-equity-for-individuals"] if s in G]
    pw_html = "".join(f'<a class="card tile reveal" href="guides/{g["slug"]}/"><span class="tag" style="background:#3a3216;color:#e8c955">Private wealth</span><h3>{esc(g["title"])}</h3><p>{esc(g["description"][:120])}…</p></a>' for g in pw)
    vids = "".join(f'<div class="reveal">{video_card(v)}<p style="margin-top:10px;font-weight:600">{esc(v["title"])}</p><small class="muted">{esc(v["channel"])}</small></div>' for v in VIDEOS[:3])
    quiz = "".join([
        quiz_q(1, "How many months of essential expenses do you have saved in cash?", [("None yet", 0), ("Less than 1 month", 5), ("1–3 months", 10), ("3–6 months", 15), ("6+ months", 20)], "Build your emergency fund|tools/emergency-fund/"),
        quiz_q(2, "How much high-interest debt (credit cards, payday, overdraft) do you carry?", [("A lot — it's growing", 0), ("Some, slowly shrinking", 8), ("A small amount I clear soon", 14), ("None", 20)], "Plan your debt-free date|tools/debt-payoff/"),
        quiz_q(3, "What share of your take-home pay do you save or invest?", [("Nothing right now", 0), ("Under 5%", 5), ("5–10%", 10), ("10–20%", 15), ("Over 20%", 20)], "Set up a 50/30/20 budget|tools/budget/"),
        quiz_q(4, "How is your retirement saving going?", [("Haven't started", 0), ("Started, but behind", 7), ("Roughly on track", 15), ("Ahead of plan", 20)], "Find your retirement number|tools/retirement/"),
        quiz_q(5, "How do you track your spending?", [("I don't", 0), ("Now and then", 10), ("I review monthly", 15), ("Automated budget + monthly review", 20)], "Read the 50/30/20 guide|guides/50-30-20-budget/"),
        quiz_q(6, "Which protections do you have? (insurance, a will, credit freeze, strong passwords)", [("None of these", 0), ("One or two", 10), ("Most of them", 15), ("All of them", 20)], "Lock down your financial privacy|guides/financial-privacy/"),
    ])
    home_faq = [
        ("Is Private.Finance really free?", "Yes. Every calculator and guide is free. The site is funded by advertising, sponsorships, reader support and referral fees from professional firms when readers ask to be introduced — never by charging you."),
        ("What does 'private by design' mean?", "Our calculators run entirely in your browser. The numbers you type are never sent to our servers or anyone else's. The only data we receive is what you deliberately submit in a form, such as a request to be matched with an advisor."),
        ("How does the advisor matching work?", "You answer a few questions about your goals and situation. We review your request and introduce you to independent, fee-only professionals who fit. There is no fee and no obligation to hire anyone."),
        ("Which countries do you cover?", "Our guides explain concepts that apply everywhere and note where rules differ in the United States, Canada, the United Kingdom, India and Australia. Calculators support multiple currencies."),
        ("Is this financial advice?", "No. Everything here is general education. For advice about your specific situation, speak with a licensed professional."),
    ]
    org = {"@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": DOMAIN + "/", "logo": DOMAIN + "/favicon.svg"}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": DOMAIN + "/",
            "potentialAction": {"@type": "SearchAction", "target": DOMAIN + "/guides/?q={search_term_string}", "query-input": "required name=search_term_string"}}
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Private-by-design personal finance</span>
<h1>Your money.<br><em>Your business.</em></h1>
<p class="lede">Free calculators that never upload your numbers, plain-English guides from budgeting to private wealth, and a no-pressure way to meet a fee-only advisor.</p>
<div class="cta-row"><a class="btn btn-primary btn-lg" href="tools/">Explore free tools</a><a class="btn btn-ghost btn-lg" href="get-matched/">Get matched with an advisor</a></div>
<div class="trust"><span>No sign-up</span><span>No data uploaded</span><span>Multi-currency</span><span>Updated {UPDATED}</span></div></div>
<div class="card widget" id="hero-widget"><div style="display:flex;justify-content:space-between;align-items:center"><span class="eyebrow">Quick growth check</span><select data-currency aria-label="Currency" style="width:auto;padding:4px 8px;font-size:.85rem"><option>USD</option><option>CAD</option><option>GBP</option><option>EUR</option><option>INR</option><option>AUD</option><option>AED</option><option>LKR</option></select></div>
<div class="big" id="hw-out">—</div><p class="muted" style="margin:0 0 14px;font-size:.9rem">of which <b id="hw-int" class="mono">—</b> is growth on your money</p>
<div class="chart-box" style="height:150px"><canvas id="hw-chart" style="width:100%;height:100%"></canvas></div>
<div class="field" style="margin-top:14px"><label for="hw-m">Monthly investment <output for="hw-m" data-pre="cur"></output></label><input class="range" type="range" id="hw-m" min="50" max="5000" step="50" value="500"></div>
<div class="row"><div class="field"><label for="hw-r">Return <output for="hw-r" data-suffix="%"></output></label><input class="range" type="range" id="hw-r" min="1" max="12" step="0.5" value="7"></div>
<div class="field"><label for="hw-y">Years <output for="hw-y"></output></label><input class="range" type="range" id="hw-y" min="1" max="45" value="25"></div></div>
<a href="tools/compound-interest/" style="font-size:.9rem">Open the full compound interest calculator →</a></div>
</div></section>

<section class="band" style="padding:36px 0"><div class="wrap stats">
<div class="stat"><b>{len(TOOLS)}</b><span>free, private calculators</span></div>
<div class="stat"><b>{len(guides)}</b><span>in-depth guides</span></div>
<div class="stat"><b>0</b><span>bytes of calculator data uploaded</span></div>
<div class="stat"><b>5</b><span>countries' rules explained</span></div></div></section>

<section><div class="wrap"><div class="section-head"><div><span class="eyebrow">Tools</span><h2>Run the numbers — privately</h2></div><p>Every calculator runs on your device, supports eight currencies and explains its math.</p></div>
<div class="grid g4">{tools_html}</div><p class="center" style="margin-top:22px"><a class="btn btn-ghost" href="tools/">See all {len(TOOLS)} tools →</a></p></div></section>

{ad("top")}

<section style="padding-top:0"><div class="wrap"><div class="lead-banner reveal">
<div><span class="eyebrow" style="color:var(--gold-2)">Free advisor matching</span><h2>Find a fee-only advisor in about 60 seconds</h2>
<p>Tell us what you're working on. We'll introduce you to independent, fiduciary-minded professionals who fit your goals — no fee, no obligation, no spam.</p>
<ul class="list-check" style="color:#e9f5f1"><li>Fee-only and fiduciary focus</li><li>Virtual or in-person</li><li>Your details shared only with the advisors you're matched to</li></ul></div>
<form class="card" action="get-matched/" method="get"><input type="hidden" name="source" value="home">
<div class="field"><label for="hm-goal" style="color:#fff">What do you need help with?</label><select id="hm-goal" name="goal"><option value="retirement">Retirement planning</option><option value="investing">Investing</option><option value="wealth">Private wealth management</option><option value="tax">Tax planning</option><option value="debt">Getting out of debt</option><option value="home">Buying a home</option><option value="estate">Estate &amp; legacy planning</option><option value="business">Business owner planning</option></select></div>
<div class="field"><label for="hm-assets" style="color:#fff">Investable assets</label><select id="hm-assets" name="assets"><option value="under-50k">Under 50,000</option><option value="50k-250k">50,000 – 250,000</option><option value="250k-1m" selected>250,000 – 1 million</option><option value="1m-5m">1 – 5 million</option><option value="5m-plus">5 million +</option></select></div>
<button class="btn btn-gold btn-lg" type="submit" style="width:100%">Start matching →</button><p style="font-size:.8rem;margin:10px 0 0;color:#bfe0d6">Takes about a minute. No obligation.</p></form>
</div></div></section>

<section id="health-score"><div class="wrap"><div class="grid g2" style="align-items:center">
<div><span class="eyebrow">2-minute check-up</span><h2>What's your Financial Health Score?</h2><p class="muted">Six quick questions. Get a score out of 100 and the three moves that would improve it most. Your answers never leave your device.</p>
<div class="privacy-note" style="max-width:420px">Scored locally in your browser.</div></div>
<div class="card" id="quiz"><div class="progress"><span id="quiz-bar"></span></div>{quiz}
<div id="quiz-result" style="display:none;text-align:center">
<svg class="score-ring" viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="none" stroke="var(--line)" stroke-width="10"/><circle id="quiz-ring" cx="60" cy="60" r="52" fill="none" stroke="#0f5c4d" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="326.7" transform="rotate(-90 60 60)" style="transition:stroke-dashoffset 1s"/><text x="60" y="68" text-anchor="middle" font-size="28" font-weight="700" fill="currentColor" font-family="JetBrains Mono,monospace" id="quiz-score">0</text></svg>
<h3><span id="quiz-band"></span></h3><p class="muted" id="quiz-msg"></p><p><b>Your top moves:</b></p><ul id="quiz-fixes" class="list-check" style="text-align:left;max-width:360px;margin:0 auto 16px"></ul>
<div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="get-matched/?source=quiz">Get a free professional review</a><button class="btn btn-ghost" id="quiz-restart" type="button">Retake</button></div></div>
</div></div></div></section>

<section><div class="wrap"><div class="section-head"><div><span class="eyebrow">Guides</span><h2>Start with the essentials</h2></div><p>Researched, balanced and written in plain English — with country notes where the rules differ.</p></div>
<div class="grid g3">{feat_html}</div><p class="center" style="margin-top:22px"><a class="btn btn-ghost" href="guides/">Browse all guides →</a></p></div></section>

<section class="band"><div class="wrap"><div class="section-head"><div><span class="eyebrow" style="color:var(--gold-2)">The Private Wealth hub</span><h2>How the wealthy actually manage money</h2></div><p class="muted">Private banking, wealth managers, private credit and private equity — what they cost, who they're for and the questions to ask before you sign.</p></div>
<div class="grid g4">{pw_html}</div><p style="margin-top:22px"><a class="btn btn-gold" href="private-wealth/">Enter the Private Wealth hub →</a></p></div></section>

<section><div class="wrap"><div class="section-head"><div><span class="eyebrow">Watch &amp; learn</span><h2>Curated video explainers</h2></div><p>Hand-picked from respected educators. Videos load only when you press play.</p></div>
<div class="grid g3">{vids}</div><p class="center" style="margin-top:22px"><a class="btn btn-ghost" href="videos/">All videos →</a></p></div></section>

<section style="padding-top:0"><div class="wrap grid g3">
<a class="card tile reveal" href="support/"><span class="ico">💛</span><h3>Support independent finance education</h3><p>Help keep every tool free — fund hosting, expert review, marketing and new hires.</p></a>
<a class="card tile reveal" href="contests/"><span class="ico">🏆</span><h3>Money Moves Challenge</h3><p>Share your best money-saving idea and compete for cash prizes and a featured spot.</p></a>
<a class="card tile reveal" href="careers/"><span class="ico">🧑‍💼</span><h3>Work with us</h3><p>We're recruiting finance writers, credentialed reviewers, video creators and growth talent.</p></a>
</div></section>

<section style="padding-top:0"><div class="wrap narrow"><h2 class="center">Questions, answered</h2>{faq_html(home_faq)}</div></section>
'''
    write(path, f"{NAME} — Private-by-Design Money Tools, Guides & Advisor Matching", "Free private calculators, plain-English guides to budgeting, investing, retirement and private wealth, plus free matching with fee-only financial advisors.", body, "", [org, site, faq_schema(home_faq)], scripts=("calc.js",), priority="1.0")

    # ------------------------------------------------------------ TOOLS INDEX
    path = "tools/index.html"; P = "../"
    cats = {}
    for t in TOOLS: cats.setdefault(t["cat"], []).append(t)
    tl = "".join(f'<a class="card tile" href="{P}tools/{t["slug"]}/"><span class="ico">{t["icon"]}</span><span class="tag">{t["cat"]}</span><h3>{t["name"]}</h3><p>{t["short"]}</p></a>' for t in TOOLS)
    cr, crs = crumbs(path, [(None, "Tools")])
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Free · Private · No sign-up</span><h1>Money calculators that respect your privacy</h1>
<p class="lede" style="max-width:62ch">Every tool below runs entirely in your browser. Nothing you enter is uploaded, logged or sold. Switch currency on any tool and copy a shareable link that keeps your inputs in the URL only.</p>
<div class="grid g3" style="margin-top:28px">{tl}</div>{ad("top")}
<div class="card" style="margin-top:30px"><h2>Why "private by design" matters</h2><p>Many financial websites ask for your income, debts and email before showing a result — and that data can end up with lenders and marketers. Our calculators are plain JavaScript that run on your device, so there's nothing to collect. If you want a human to look at your numbers, you choose to share them through our <a href="{P}get-matched/">advisor matching form</a>.</p></div>
</div></section>'''
    write(path, "Free Private Financial Calculators", "10 free financial calculators — compound interest, retirement/FIRE, mortgage with PMI, debt payoff, budget, emergency fund, loan EMI, net worth and more. No data uploaded.", body, "tools/", [crs], priority="0.9")

    # ------------------------------------------------------------ GUIDES INDEX
    path = "guides/index.html"; P = "../"
    catlist = sorted(set(g["category"] for g in guides))
    pills = '<button class="on" data-f="all">All</button>' + "".join(f'<button data-f="{c}">{c}</button>' for c in catlist)
    gl = "".join(f'<a class="card tile" data-cat="{g["category"]}" href="{P}guides/{g["slug"]}/"><span class="tag">{g["category"]}</span><h3>{esc(g["title"])}</h3><p>{esc(g["description"])}</p><small class="muted">{g["read"]} min read · Updated {UPDATED}</small></a>' for g in guides)
    cr, crs = crumbs(path, [(None, "Guides")])
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Learn</span><h1>Personal finance guides</h1><p class="lede" style="max-width:62ch">In-depth, balanced explainers on budgeting, debt, investing, retirement, credit, real estate and private wealth — with notes for the US, Canada, UK, India and Australia.</p>
<div class="pill-list" id="gfilter" style="margin:24px 0">{pills}</div><div class="grid g3" id="glist">{gl}</div>{ad("top")}</div></section>
<script>(function(){{var b=document.getElementById("gfilter");b.addEventListener("click",function(e){{var t=e.target.closest("button");if(!t)return;b.querySelectorAll("button").forEach(function(x){{x.classList.toggle("on",x===t);}});var f=t.dataset.f;document.querySelectorAll("#glist [data-cat]").forEach(function(c){{c.style.display=(f==="all"||c.dataset.cat===f)?"":"none";}});}});var q=new URLSearchParams(location.search).get("q");if(q){{q=q.toLowerCase();document.querySelectorAll("#glist [data-cat]").forEach(function(c){{c.style.display=c.textContent.toLowerCase().indexOf(q)>-1?"":"none";}});}}}})();</script>'''
    write(path, "Personal Finance Guides", "Plain-English personal finance guides: budgeting, emergency funds, debt payoff, credit scores, index funds, retirement, mortgages and private wealth.", body, "guides/", [crs], priority="0.9")

    # ------------------------------------------------------------ PRIVATE WEALTH HUB
    path = "private-wealth/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Private Wealth")])
    pwl = "".join(f'<a class="card tile" href="{P}guides/{g["slug"]}/"><span class="tag">{g["category"]}</span><h3>{esc(g["title"])}</h3><p>{esc(g["description"])}</p></a>' for g in pw + [G[s] for s in ["fee-only-financial-advisor"] if s in G])
    ladder = [("Under 100k", "Robo-advisor or DIY index funds; hourly or flat-fee planner for a one-off plan", "Low-cost core portfolio, emergency fund, debt payoff"),
              ("100k – 1M", "Fee-only planner (flat or AUM), premium bank tier", "Tax-efficient accounts, insurance review, retirement projection"),
              ("1M – 5M", "Private wealth manager, private-banking entry tier", "Tax and estate coordination, lending against assets, alternatives access"),
              ("5M – 25M", "Private bank, multi-family office", "Trusts, philanthropy, private equity/credit allocations, family governance"),
              ("25M+", "Single- or multi-family office", "Full-service family CFO: investments, legal, tax, concierge")]
    lt = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in ladder)
    hub_faq = [("Do I need to be rich to use a wealth manager?", "No. Minimums vary widely. Many fee-only planners work on flat or hourly fees with no minimum, while traditional private wealth firms often start somewhere around the high six or low seven figures."),
               ("What's the difference between a private bank and a wealth manager?", "A private bank combines banking and lending with investment services under one relationship manager. A wealth manager focuses on investment and planning advice and may hold your assets at an independent custodian."),
               ("Are private equity and private credit suitable for individuals?", "They can play a small role for investors who understand the illiquidity, fees and complexity, and who meet any eligibility rules. Most individuals are well served by low-cost public-market portfolios.")]
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Private Wealth hub</span><h1>Private wealth, demystified</h1>
<p class="lede" style="max-width:64ch">Private banking, wealth management, family offices, private credit and private equity were once whispered about behind closed doors. Here's what they actually do, what they cost and how to tell whether you need them.</p>
<div class="grid g3" style="margin-top:28px">{pwl}</div>{ad("top")}
<h2 style="margin-top:48px">The wealth-service ladder</h2><p class="muted">A rough guide to which services typically make sense at different levels of investable assets. Thresholds vary by firm and country.</p>
<div class="table-scroll"><table><thead><tr><th>Investable assets</th><th>Typical providers</th><th>What you're usually paying for</th></tr></thead><tbody>{lt}</tbody></table></div>
<div class="grid g2" style="margin-top:40px"><div class="card"><h3>Questions to ask any wealth firm</h3><ul class="list-check"><li>Are you a fiduciary at all times, in writing?</li><li>How exactly are you paid — and by whom?</li><li>What is my all-in annual cost, including fund fees?</li><li>Who holds my assets (the custodian)?</li><li>Do you sell proprietary products?</li><li>How will you measure success for me?</li></ul></div>
<div class="card" style="background:var(--ink);color:#efeadb;border-color:var(--ink)"><h3 style="color:#fff">Get introduced to the right firm</h3><p style="color:#c8d3d0">Share your goals and asset range. We'll introduce you to independent, fee-only professionals suited to your level — from flat-fee planners to private wealth teams.</p><a class="btn btn-gold" href="{P}get-matched/?goal=wealth&amp;source=hub">Get matched free →</a></div></div>
<h2 style="margin-top:40px">FAQ</h2>{faq_html(hub_faq)}</div></section>'''
    write(path, "Private Wealth Hub: Private Banking, Wealth Management & Alternatives", "Understand private banking, private wealth management, family offices, private credit and private equity — costs, minimums and the questions to ask.", body, "private-wealth/", [crs, faq_schema(hub_faq)], priority="0.9")
    SEARCH.append({"t": "Private Wealth hub", "d": "Private banking, wealth management, private credit and private equity explained", "c": "Hub", "u": "private-wealth/", "k": "wealth private banking"})

    # ------------------------------------------------------------ GET MATCHED (lead gen)
    path = "get-matched/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Get matched")])
    g1 = "".join(choice("goal", v, l, i) for v, l, i in [("retirement", "Retirement planning", "🏖️"), ("investing", "Investing & portfolio review", "📈"), ("wealth", "Private wealth management", "🏛️"), ("tax", "Tax planning", "🧾"), ("debt", "Getting out of debt", "⛓️"), ("home", "Buying a home / mortgage", "🏡"), ("estate", "Estate & legacy planning", "📜"), ("business", "Business owner planning", "💼")])
    g2 = "".join(choice("assets", v, l, i) for v, l, i in [("under-50k", "Under 50,000", "🌱"), ("50k-250k", "50,000 – 250,000", "🌿"), ("250k-1m", "250,000 – 1 million", "🌳"), ("1m-5m", "1 – 5 million", "🏛️"), ("5m-plus", "5 million +", "💎")])
    g3 = "".join(choice("age", v, l) for v, l in [("under-30", "Under 30"), ("30-44", "30 – 44"), ("45-59", "45 – 59"), ("60-plus", "60 +")])
    g3b = "".join(choice("income", v, l) for v, l in [("under-75k", "Under 75k / yr"), ("75k-150k", "75k – 150k"), ("150k-300k", "150k – 300k"), ("300k-plus", "300k +")])
    g4 = "".join(choice("meeting", v, l, i) for v, l, i in [("virtual", "Video / phone", "💻"), ("in-person", "In person", "🤝"), ("either", "Either is fine", "✨")])
    g5 = "".join(choice("timing", v, l) for v, l in [("asap", "As soon as possible"), ("1-3-months", "Within 1–3 months"), ("researching", "Just researching for now")])
    countries = "".join(f"<option>{c}</option>" for c in ["United States", "Canada", "United Kingdom", "India", "Australia", "United Arab Emirates", "Singapore", "Sri Lanka", "Ireland", "New Zealand", "Other"])
    lead_faq = [("Is this really free?", "Yes. There is no fee to be matched and no obligation to hire anyone. Advisors you choose to work with will explain their own fees before you commit."),
                ("Who will see my information?", "Only our team and the advisor(s) we introduce you to. We do not sell your details to data brokers or mass-marketing lists. See our privacy policy."),
                ("How does Private.Finance make money from this?", "We may receive a referral fee from professional firms when we introduce clients. That never changes what you pay, and we prioritise fee-only, fiduciary-minded professionals."),
                ("What should I ask on the first call?", "Ask whether they are a fiduciary at all times, how they are paid, their all-in cost, who holds your assets and what a typical client looks like. Our fee-only advisor guide has a full checklist.")]
    nav = lambda back=True, nxt="Continue →": f'<p class="step-err form-msg err" role="alert"></p><div class="step-nav">{"<button class=\'btn btn-ghost\' data-prev>← Back</button>" if back else "<span></span>"}<button class="btn btn-primary" data-next>{nxt}</button></div>'
    body = f'''<section style="padding-top:36px"><div class="wrap">{cr}
<div class="lead-shell"><div>
<span class="eyebrow">Free advisor matching · No obligation</span><h1 style="font-size:clamp(2rem,4vw,3rem)">Meet a fee-only advisor who fits your goals</h1>
<p class="lede" style="max-width:56ch">Answer six quick questions. We'll review your request and introduce you to independent professionals suited to your situation — usually within one business day.</p>
<form id="lead-form" class="card" data-subject="New advisor-match lead" novalidate style="margin-top:20px;scroll-margin-top:100px">
<div style="display:flex;justify-content:space-between;font-size:.85rem" class="muted"><span id="lead-step">Step 1 of 6</span><span>🔒 Encrypted in transit · Never sold</span></div>
<div class="progress"><span id="lead-bar"></span></div>
<input type="hidden" name="source" value="direct"><input type="hidden" name="health_score" id="lead-health" value=""><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">What would you like help with?</h2></legend><div class="choices" data-req-group data-auto-next>{g1}</div>{nav(False)}</fieldset>
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">Roughly how much do you have in savings and investments?</h2></legend><p class="muted" style="font-size:.9rem">Excluding your home. This helps us match you with professionals who serve clients at your level.</p><div class="choices" data-req-group data-auto-next>{g2}</div>{nav()}</fieldset>
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">A little about you</h2></legend><p><b>Your age</b></p><div class="choices" data-req-group>{g3}</div><p style="margin-top:18px"><b>Household income</b></p><div class="choices" data-req-group>{g3b}</div>{nav()}</fieldset>
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">Where are you located?</h2></legend>
<div class="row"><div class="field"><label for="ld-country">Country</label><select id="ld-country" name="country" required>{countries}</select></div><div class="field"><label for="ld-region">City / State / Province</label><input id="ld-region" name="region" type="text" required autocomplete="address-level2" placeholder="e.g. Toronto, ON"></div></div>
<p><b>How would you like to meet?</b></p><div class="choices" data-req-group>{g4}</div>{nav()}</fieldset>
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">When are you hoping to start?</h2></legend><div class="choices" data-req-group>{g5}</div>
<div class="field" style="margin-top:18px"><label for="ld-notes">Anything an advisor should know? (optional)</label><textarea id="ld-notes" name="notes" placeholder="e.g. Selling a business next year, want to retire at 55, inherited a portfolio…"></textarea></div>{nav()}</fieldset>
<fieldset class="step" style="border:0;padding:0;margin:0"><legend><h2 style="font-size:1.5rem">Where should we send your introductions?</h2></legend>
<div class="row"><div class="field"><label for="ld-fn">First name</label><input id="ld-fn" name="first_name" type="text" required autocomplete="given-name"></div><div class="field"><label for="ld-ln">Last name</label><input id="ld-ln" name="last_name" type="text" required autocomplete="family-name"></div></div>
<div class="field"><label for="ld-em">Email</label><input id="ld-em" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="ld-ph">Phone (optional — speeds things up)</label><input id="ld-ph" name="phone" type="tel" autocomplete="tel"></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that Private.Finance may contact me about my request and share my answers with up to three professional advisors it introduces me to. I can withdraw consent at any time. See the <a href="{P}privacy-policy/">privacy policy</a>.</label>
<p class="step-err form-msg err" role="alert"></p><div class="step-nav"><button class="btn btn-ghost" data-prev>← Back</button><button class="btn btn-gold btn-lg" type="submit">Get my free matches →</button></div></fieldset>
<div id="lead-done" style="display:none;text-align:center;padding:20px 0"><div style="font-size:3rem">✅</div><h2>Request received</h2><p class="muted">Thank you. We'll review your answers and reach out within one business day with your introductions. While you wait, check your numbers with our <a href="{P}tools/retirement/">retirement calculator</a>.</p></div>
</form>
<p class="disclosure"><b>Referral disclosure:</b> Private.Finance is an independent publisher, not a registered investment adviser, broker or bank, and does not provide personalised advice. We may receive compensation from professional firms we introduce you to; this does not affect what you pay. Always verify an advisor's registration with your national regulator before hiring.</p>
</div>
<aside><div class="card"><h3>How it works</h3><ol class="steps-list"><li><b>Tell us your goals</b><br><span class="muted">Six quick questions, about a minute.</span></li><li><b>We review your request</b><br><span class="muted">A real person looks at what you need.</span></li><li><b>Meet your matches</b><br><span class="muted">Free intro calls with up to three professionals. Hire only if it feels right.</span></li></ol></div>
<div class="card" style="margin-top:20px"><h3>What we look for in advisors</h3><ul class="list-check"><li>Fee-only or transparent fees</li><li>Fiduciary duty to clients</li><li>Recognised credentials (e.g. CFP®, CFA, CPA)</li><li>Clean regulatory record</li></ul></div>
<div class="card" style="margin-top:20px"><h3>Not ready to talk?</h3><p class="muted">Explore on your own with our <a href="{P}tools/">free calculators</a> or read <a href="{P}guides/fee-only-financial-advisor/">how to choose a fee-only advisor</a>.</p></div></aside>
</div>
<div class="narrow" style="margin:48px auto 0"><h2>Advisor matching FAQ</h2>{faq_html(lead_faq)}</div></div></section>'''
    write(path, "Get Matched With a Fee-Only Financial Advisor — Free", "Answer six quick questions and get free introductions to independent, fee-only financial advisors for retirement, investing, tax and private wealth. No obligation.", body, "", [crs, faq_schema(lead_faq)], scripts=("lead.js",), priority="0.9")
    SEARCH.append({"t": "Get matched with an advisor", "d": "Free introductions to fee-only financial advisors", "c": "Lead", "u": "get-matched/", "k": "advisor planner wealth manager"})

    # ------------------------------------------------------------ VIDEOS
    path = "videos/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Videos")])
    topics = []
    for v in VIDEOS:
        if v["topic"] not in topics: topics.append(v["topic"])
    vp = '<button class="on" data-f="all">All</button>' + "".join(f'<button data-f="{t}">{t}</button>' for t in topics)
    vg = "".join(f'<div data-cat="{v["topic"]}">{video_card(v)}<p style="margin:10px 0 2px;font-weight:600">{esc(v["title"])}</p><small class="muted">{esc(v["channel"])} · {v["topic"]}</small>{"".join(f" · <a href=\"{P}guides/{s}/\">Read the guide</a>" for s in v["guides"][:1] if s in G)}</div>' for v in VIDEOS)
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Watch &amp; learn</span><h1>Personal finance video library</h1>
<p class="lede" style="max-width:62ch">Short, well-made explainers from respected educators, paired with our written guides. Videos use YouTube's privacy-enhanced mode and load only when you press play.</p>
<div class="pill-list" id="vfilter" style="margin:24px 0">{vp}</div><div class="grid g3" id="vlist">{vg}</div>{ad("top")}
<p class="disclosure">All videos are the property of their respective creators and are embedded using YouTube's standard embedded player under YouTube's Terms of Service. {NAME} is not affiliated with, sponsored by or endorsed by these creators. Inclusion is not an endorsement of every view expressed. Creators can request removal via our <a href="{P}contact/">contact page</a>.</p></div></section>
<script>(function(){{var b=document.getElementById("vfilter");b.addEventListener("click",function(e){{var t=e.target.closest("button");if(!t)return;b.querySelectorAll("button").forEach(function(x){{x.classList.toggle("on",x===t);}});document.querySelectorAll("#vlist [data-cat]").forEach(function(c){{c.style.display=(t.dataset.f==="all"||c.dataset.cat===t.dataset.f)?"":"none";}});}});}})();</script>'''
    vschema = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"https://www.youtube.com/watch?v={v['id']}", "name": v["title"]} for i, v in enumerate(VIDEOS)]}
    write(path, "Personal Finance Video Library", "Curated personal finance videos on compound interest, index funds, budgeting, debt payoff, credit scores, retirement, private equity and private credit.", body, "videos/", [crs, vschema], priority="0.7")
    SEARCH.append({"t": "Video library", "d": "Curated finance explainer videos", "c": "Page", "u": "videos/", "k": "youtube video watch"})

    # ------------------------------------------------------------ RESOURCES
    path = "resources/index.html"; P = "../"
    R = [("United States", [("Consumer Financial Protection Bureau", "https://www.consumerfinance.gov/", "Complaints, guides and tools on credit, mortgages and debt."), ("Investor.gov (SEC)", "https://www.investor.gov/", "Investor education and the SEC's adviser search."), ("FINRA BrokerCheck", "https://brokercheck.finra.org/", "Check a broker's or firm's registration and disciplinary history."), ("SEC Investment Adviser Search", "https://adviserinfo.sec.gov/", "Look up registered investment advisers and their Form ADV."), ("IdentityTheft.gov (FTC)", "https://www.identitytheft.gov/", "Report identity theft and get a recovery plan."), ("AnnualCreditReport.com", "https://www.annualcreditreport.com/", "The official site for free credit reports."), ("CFP Board — Let's Make a Plan", "https://www.letsmakeaplan.org/", "Find and verify CFP® professionals.")]),
         ("Canada", [("Financial Consumer Agency of Canada", "https://www.canada.ca/en/financial-consumer-agency.html", "Banking, credit and budgeting guidance."), ("CIRO", "https://www.ciro.ca/", "Canadian Investment Regulatory Organization — check advisors."), ("Canadian Securities Administrators", "https://www.securities-administrators.ca/", "National registration search for advisers and dealers.")]),
         ("United Kingdom", [("MoneyHelper", "https://www.moneyhelper.org.uk/", "Free, impartial money and pensions guidance."), ("FCA Financial Services Register", "https://register.fca.org.uk/", "Check that a firm or adviser is authorised.")]),
         ("India", [("SEBI", "https://www.sebi.gov.in/", "Securities regulator — verify registered investment advisers."), ("Reserve Bank of India", "https://www.rbi.org.in/", "Banking regulation and consumer awareness.")]),
         ("Australia", [("Moneysmart (ASIC)", "https://moneysmart.gov.au/", "Free calculators and guidance from the regulator."), ("ASIC Professional Register", "https://asic.gov.au/", "Check financial advisers and licensees.")]),
         ("Global", [("OECD Financial Education", "https://www.oecd.org/financial/education/", "International research on financial literacy.")])]
    rhtml = "".join(f'<h2 style="margin-top:36px">{c}</h2><div class="grid g3">' + "".join(f'<a class="card tile" href="{u}" target="_blank" rel="noopener nofollow"><h3>{esc(n)} ↗</h3><p>{esc(d)}</p></a>' for n, u, d in items) + "</div>" for c, items in R)
    cr, crs = crumbs(path, [(None, "Resources")])
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Official sources</span><h1>Trusted financial resources by country</h1><p class="lede" style="max-width:62ch">Regulators, government guidance and official registers we rely on in our research — including where to verify an advisor before you hire one.</p>{rhtml}
<p class="disclosure">External links open in a new tab. {NAME} is not affiliated with these organisations and is not responsible for their content.</p>{ad("footer")}</div></section>'''
    write(path, "Official Financial Resources & Advisor Verification", "Official regulators and consumer resources in the US, Canada, UK, India and Australia, including where to verify a financial advisor's registration.", body, "resources/", [crs], priority="0.6")
    SEARCH.append({"t": "Official resources", "d": "Regulators and advisor verification by country", "c": "Page", "u": "resources/", "k": "regulator brokercheck sebi fca"})

    # ------------------------------------------------------------ GLOSSARY
    path = "glossary/index.html"; P = "../"
    letters = sorted(set(t[0][0].upper() for t in GLOSSARY))
    az = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters)
    gh = ""; cur = ""
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        L = term[0].upper()
        if L != cur:
            gh += f'<h2 id="letter-{L}" style="margin-top:28px">{L}</h2>'; cur = L
        gh += f'<div class="term" id="{slugify(term)}"><h3>{esc(term)}</h3><p>{esc(d)}</p></div>'
    dset = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": f"{NAME} Glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    cr, crs = crumbs(path, [(None, "Glossary")])
    body = f'''<section style="padding-top:40px"><div class="wrap narrow">{cr}<span class="eyebrow">Reference</span><h1>Personal finance glossary</h1><p class="lede">{len(GLOSSARY)} essential money terms — from APR to the J-curve — defined in plain English.</p><div class="az">{az}</div>{gh}{ad("footer")}</div></section>'''
    write(path, "Personal Finance Glossary", f"{len(GLOSSARY)} personal finance and private wealth terms explained in plain English: APR, compound interest, fiduciary, PMI, private credit, safe withdrawal rate and more.", body, "glossary/", [crs, dset], priority="0.6")

    # ------------------------------------------------------------ SUPPORT / DONATE
    path = "support/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Support")])
    alloc = [("Operations & hosting", 30, "#0f5c4d"), ("Content & expert review", 30, "#2c6e9b"), ("Promotion & marketing", 15, "#c9a227"), ("Hiring talent", 15, "#7a5ea8"), ("Contests & prizes", 10, "#b4443a")]
    ab = "".join(f'<span style="width:{p}%;background:{c}" title="{n} {p}%"></span>' for n, p, c in alloc)
    al = "".join(f'<li><i style="display:inline-block;width:12px;height:12px;border-radius:3px;background:{c};margin-right:8px"></i><b>{p}%</b> {n}</li>' for n, p, c in alloc)
    tiers = [(5, "☕", "Coffee", "Covers a day of hosting"), (25, "📚", "Supporter", "Funds a guide update"), (100, "🏛️", "Patron", "Sponsors a new calculator feature"), (500, "💎", "Founding sponsor", "Recognition on our supporters page")]
    th = "".join(f'<div class="card tier{" sel" if a == 25 else ""}" data-amt="{a}" role="button" tabindex="0"><span style="font-size:1.6rem">{i}</span><b><span class="cur-sym">$</span>{a}</b><span style="font-weight:600">{n}</span><small class="muted" style="display:block">{d}</small></div>' for a, i, n, d in tiers)
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}
<div class="grid g2" style="align-items:start"><div><span class="eyebrow">Support independent finance education</span><h1>Keep financial knowledge free and private</h1>
<p class="lede">{NAME} has no paywall, no sign-up and no data harvesting. Reader support funds the work that keeps it that way — and lets us grow faster.</p>
<h3 style="margin-top:28px">Where your support goes</h3><div class="alloc">{ab}</div><ul style="list-style:none;padding:0">{al}</ul><p class="muted" style="font-size:.88rem">Planned allocation of reader contributions. We publish updates on how funds are used in our newsletter.</p>
<div class="card" style="margin-top:24px"><h3>Other ways to help</h3><ul class="list-check"><li>Share a calculator with a friend who needs it</li><li><a href="{P}advertise/">Sponsor a tool or guide</a> for your brand</li><li><a href="{P}careers/">Contribute</a> as a writer, reviewer or creator</li><li><a href="{P}contests/">Fund a prize</a> for the Money Moves Challenge</li></ul></div></div>
<div class="card" id="donate"><h2 style="font-size:1.6rem">Make a contribution</h2>
<div class="tiers" id="tiers" style="grid-template-columns:repeat(2,1fr)">{th}</div>
<div class="row" style="margin-top:16px"><div class="field"><label for="dn-amt">Custom amount</label><input id="dn-amt" type="number" min="1" value="25"></div><div class="field"><label for="dn-cur">Currency</label><select id="dn-cur"><option>USD</option><option>CAD</option><option>GBP</option><option>EUR</option><option>AUD</option><option>INR</option></select></div></div>
<div class="field"><label for="dn-purpose">Direct my support to</label><select id="dn-purpose"><option>General operations</option><option>Content &amp; expert review</option><option>Promotion &amp; marketing</option><option>Hiring talent</option><option>Contests &amp; prizes</option></select></div>
<label class="check"><input type="checkbox" id="dn-monthly"> Make it monthly</label>
<button class="btn btn-gold btn-lg" id="dn-go" type="button" style="width:100%;margin-top:16px">Contribute securely with PayPal →</button>
<p class="muted" style="font-size:.82rem;margin-top:10px">Processed securely by PayPal (cards accepted). {NAME} is not a registered charity, so contributions are not tax-deductible. Contributions are voluntary and do not purchase goods or services.</p>
<hr style="border:0;border-top:1px solid var(--line);margin:22px 0">
<h3>Larger gift, bank transfer or sponsorship pledge?</h3>
<form data-pf data-subject="Donation / sponsorship pledge" data-ok="Thank you! We'll reply within 1–2 business days with transfer details."><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<div class="row"><div class="field"><label for="pl-name">Name / organisation</label><input id="pl-name" name="name" required></div><div class="field"><label for="pl-email">Email</label><input id="pl-email" name="email" type="email" required></div></div>
<div class="row"><div class="field"><label for="pl-amt">Pledge amount</label><input id="pl-amt" name="amount" required></div><div class="field"><label for="pl-use">Purpose</label><select id="pl-use" name="purpose"><option>Operations</option><option>Promotions &amp; marketing</option><option>Hiring talent</option><option>Contest prize pool</option><option>Named sponsorship</option></select></div></div>
<div class="field"><label for="pl-msg">Message (optional)</label><textarea id="pl-msg" name="message"></textarea></div>
<button class="btn btn-primary" type="submit">Send pledge</button></form></div></div></div></section>
<script>(function(){{var t=document.getElementById("tiers"),a=document.getElementById("dn-amt");t.addEventListener("click",function(e){{var c=e.target.closest(".tier");if(!c)return;t.querySelectorAll(".tier").forEach(function(x){{x.classList.toggle("sel",x===c);}});a.value=c.dataset.amt;}});t.addEventListener("keydown",function(e){{if(e.key==="Enter"&&e.target.classList.contains("tier"))e.target.click();}});
document.getElementById("dn-cur").addEventListener("change",function(e){{var s={{USD:"$",CAD:"C$",GBP:"£",EUR:"€",AUD:"A$",INR:"₹"}}[e.target.value]||"";document.querySelectorAll(".cur-sym").forEach(function(x){{x.textContent=s;}});}});
document.getElementById("dn-go").addEventListener("click",function(){{PF.donate(+a.value,document.getElementById("dn-purpose").value,document.getElementById("dn-cur").value,document.getElementById("dn-monthly").checked);}});}})();</script>'''
    write(path, "Support Private.Finance — Donate", "Support free, private personal finance education. Contributions fund operations, expert review, marketing, hiring and contest prizes.", body, "support/", [crs], priority="0.6")
    SEARCH.append({"t": "Support / Donate", "d": "Contribute to keep the tools free", "c": "Page", "u": "support/", "k": "donate donation support paypal"})

    # ------------------------------------------------------------ ADVERTISE
    path = "advertise/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Advertise & sponsor")])
    pk = [("🧮", "Calculator sponsorship", "Your brand as the presenting sponsor of a high-intent calculator, with a clearly labelled sponsor message beside results."),
          ("📰", "Sponsored guide", "A clearly labelled sponsored explainer, written to our editorial standards, on a topic relevant to your audience."),
          ("✉️", "Newsletter sponsorship", "A native placement in our weekly money brief, sent to readers who opted in."),
          ("🤝", "Lead partnership", "Advisory, wealth, lending or insurance firms: receive consented, qualified introductions from our matching flow."),
          ("🏆", "Contest prize partner", "Fund the Money Moves Challenge prize pool and get named recognition across the campaign."),
          ("🌐", "Domain & website acquisition", "Interested in acquiring Private.Finance or partnering on the platform itself? Let's talk.")]
    pkh = "".join(f'<div class="card"><span style="font-size:1.6rem">{i}</span><h3 style="margin-top:8px">{n}</h3><p class="muted">{d}</p></div>' for i, n, d in pk)
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Advertise · Sponsor · Partner</span><h1>Reach people actively making money decisions</h1>
<p class="lede" style="max-width:64ch">Visitors arrive at {NAME} mid-decision — sizing a mortgage, planning retirement, comparing advisors. Put your brand beside those moments, with transparent labelling that builds trust instead of eroding it.</p>
<div class="cta-row"><a class="btn btn-gold btn-lg" href="{WEBWORKS}" target="_blank" rel="noopener">Contact about domain / sponsorship →</a><a class="btn btn-ghost btn-lg" href="#adform">Request rates</a></div>
<div class="grid g3" style="margin-top:20px">{pkh}</div>
<div class="grid g2" style="margin-top:40px;align-items:start"><div><h2>Our standards</h2><ul class="list-check"><li>Every paid placement is labelled "Sponsored" or "Advertisement"</li><li>Sponsors never edit or approve our editorial content</li><li>No predatory lending, unregistered investments or get-rich-quick offers</li><li>Lead partners must be appropriately licensed in the client's jurisdiction</li></ul></div>
<form class="card" id="adform" data-pf data-subject="Advertising / sponsorship / partnership inquiry"><h3>Request our media kit &amp; rates</h3><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<div class="row"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="name" required></div><div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required></div></div>
<div class="row"><div class="field"><label for="ad-em">Work email</label><input id="ad-em" name="email" type="email" required></div><div class="field"><label for="ad-web">Website</label><input id="ad-web" name="website" type="url" placeholder="https://"></div></div>
<div class="field"><label for="ad-type">Interested in</label><select id="ad-type" name="interest"><option>Calculator sponsorship</option><option>Sponsored guide</option><option>Newsletter sponsorship</option><option>Lead partnership</option><option>Contest prize partner</option><option>Domain / website acquisition</option><option>Other partnership</option></select></div>
<div class="field"><label for="ad-budget">Monthly budget</label><select id="ad-budget" name="budget"><option>Under 1,000</option><option>1,000 – 5,000</option><option>5,000 – 20,000</option><option>20,000 +</option><option>Not sure yet</option></select></div>
<div class="field"><label for="ad-msg">Goals</label><textarea id="ad-msg" name="message"></textarea></div>
<button class="btn btn-primary" type="submit">Send inquiry</button></form></div></div></section>'''
    write(path, "Advertise, Sponsor or Partner With Private.Finance", "Advertising, calculator sponsorships, sponsored guides, newsletter placements, lead partnerships and domain acquisition inquiries for Private.Finance.", body, "", [crs], priority="0.6")
    SEARCH.append({"t": "Advertise & sponsor", "d": "Sponsorships, ads, partnerships, domain inquiries", "c": "Page", "u": "advertise/", "k": "advertise sponsor partnership domain"})

    # ------------------------------------------------------------ CONTESTS
    path = "contests/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Contests")])
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}
<div class="grid g2" style="align-items:start"><div><span class="eyebrow">Money Moves Challenge</span><h1>Share your best money move. Win cash prizes.</h1>
<p class="lede">Each round we ask readers one practical question — like "What's the single change that saved you the most money this year?" The most useful, original answers win, and the best get featured on {NAME}.</p>
<div class="grid g3" style="margin:24px 0"><div class="card center"><div style="font-size:2rem">🥇</div><b class="price">$250</b><p class="muted" style="margin:0">1st prize + feature</p></div><div class="card center"><div style="font-size:2rem">🥈</div><b class="price">$100</b><p class="muted" style="margin:0">2nd prize</p></div><div class="card center"><div style="font-size:2rem">🥉</div><b class="price">$50</b><p class="muted" style="margin:0">3rd prize</p></div></div>
<p class="muted" style="font-size:.9rem">Prizes paid in USD or local-currency equivalent, by PayPal or gift card. Prize pools grow with <a href="{P}support/">reader support</a> and <a href="{P}advertise/">prize partners</a>.</p>
<h2>Current round: "The $100 a month fix"</h2><p>In 300 words or fewer, describe one specific, repeatable change that frees up at least $100 a month (or local equivalent) — and how you made it stick. Judged on <b>usefulness (40%)</b>, <b>originality (30%)</b> and <b>clarity (30%)</b>.</p>
<h3>How to enter</h3><ol><li>Subscribe to the newsletter (free) so we can announce winners.</li><li>Submit your entry using the form.</li><li>Winners are announced in the newsletter and on this page when the round closes.</li></ol></div>
<form class="card" data-pf data-subject="Contest entry — Money Moves Challenge" data-ok="Entry received! Good luck — we'll email you when results are announced."><h2 style="font-size:1.5rem">Submit your entry</h2><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<div class="row"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required></div><div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required></div></div>
<div class="row"><div class="field"><label for="ct-country">Country</label><input id="ct-country" name="country" required></div><div class="field"><label for="ct-display">Display name if featured</label><input id="ct-display" name="display_name" placeholder="e.g. Priya from Pune"></div></div>
<div class="field"><label for="ct-entry">Your money move (max 300 words)</label><textarea id="ct-entry" name="entry" required maxlength="2200" style="min-height:180px"></textarea></div>
<label class="check"><input type="checkbox" name="age_confirm" value="yes" required> I confirm I am at least 18 years old (or the age of majority where I live).</label>
<label class="check" style="margin-top:8px"><input type="checkbox" name="rules_ok" value="yes" required> I have read and agree to the official rules below, and the entry is my own original work.</label>
<button class="btn btn-gold btn-lg" type="submit" style="margin-top:16px;width:100%">Submit entry</button></form></div>
<div class="card narrow" style="margin:48px auto 0" id="rules"><h2>Official rules (summary)</h2><div class="prose" style="font-size:.95rem">
<p><b>No purchase or payment necessary to enter or win.</b> A purchase or donation does not improve your chances.</p>
<p><b>Eligibility:</b> open to individuals aged 18+ (or the age of majority in their jurisdiction). Void where prohibited or restricted by law. Employees and contractors of {NAME} and their immediate families are not eligible.</p>
<p><b>Skill-based contest:</b> winners are selected by a judging panel using the published criteria; no element of chance is involved. Where required by local law (for example in Canada), a winner may need to correctly answer a time-limited skill-testing question.</p>
<p><b>Entries:</b> one entry per person per round. Entries must be original, not previously published, and must not contain personal financial details of others, defamatory content or promotional links.</p>
<p><b>Prizes:</b> as listed for the round, non-transferable, with no cash alternative other than as stated. Winners are responsible for any taxes. Unclaimed prizes after 30 days of notification may be forfeited.</p>
<p><b>Licence:</b> by entering you grant {NAME} a non-exclusive, royalty-free licence to publish your entry (edited for length and clarity) with your chosen display name.</p>
<p><b>Privacy:</b> entry data is used only to administer the contest, as described in our <a href="{P}privacy-policy/">privacy policy</a>.</p>
<p><b>Sponsor:</b> {NAME}. The contest is not sponsored, endorsed or administered by, or associated with, any social media platform. We may modify or cancel a round if it cannot run as planned, with notice on this page.</p></div></div></div></section>'''
    write(path, "Money Moves Challenge — Contests & Prizes", "Enter the Private.Finance Money Moves Challenge: share a practical money-saving idea and compete for cash prizes and a feature. Skill-based, free to enter.", body, "", [crs], priority="0.6")
    SEARCH.append({"t": "Contests & prizes", "d": "Money Moves Challenge — win cash prizes", "c": "Page", "u": "contests/", "k": "contest prize giveaway challenge"})

    # ------------------------------------------------------------ CAREERS
    path = "careers/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Careers")])
    roles = [("Freelance personal finance writer", "Remote · Per article", "Write clear, accurate, well-sourced guides. Experience in personal finance or financial journalism preferred."),
             ("Credentialed expert reviewer", "Remote · Per review", "CFP®, CFA, CPA, chartered or equivalent professionals to fact-check and co-sign guides in your jurisdiction."),
             ("Video creator / editor", "Remote · Project", "Produce short explainers and calculator walkthroughs for YouTube and social."),
             ("SEO & growth marketer", "Remote · Contract", "Own keyword strategy, technical SEO and distribution for a fast-growing finance publication."),
             ("Partnerships lead", "Remote · Commission-based", "Build relationships with advisory firms, fintechs and sponsors."),
             ("Front-end developer (JS)", "Remote · Project", "Build new privacy-first calculators in vanilla JavaScript.")]
    rh = "".join(f'<div class="card"><span class="tag">{m}</span><h3 style="margin-top:10px">{n}</h3><p class="muted">{d}</p></div>' for n, m, d in roles)
    ro = "".join(f"<option>{n}</option>" for n, _, _ in roles) + "<option>Other / general application</option>"
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<span class="eyebrow">Careers &amp; talent</span><h1>Help millions make better money decisions</h1>
<p class="lede" style="max-width:62ch">We're a small, remote-first team building the most trustworthy, privacy-respecting personal finance resource on the web. We hire for clarity, accuracy and craft — wherever you live.</p>
<div class="grid g3" style="margin-top:24px">{rh}</div>
<div class="grid g2" style="margin-top:40px;align-items:start"><div><h2>What we offer</h2><ul class="list-check"><li>Fully remote, flexible hours</li><li>Fair, prompt payment for freelance work</li><li>Bylines and portfolio-quality work</li><li>A mission you can be proud of</li></ul><p class="muted">We welcome applicants of every background. We don't ask for — and you shouldn't send — ID numbers or bank details in an application.</p></div>
<form class="card" data-pf data-subject="Job application" data-ok="Application received — thank you! We review every application and reply if there's a fit."><h3>Apply</h3><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<div class="field"><label for="jb-role">Role</label><select id="jb-role" name="role">{ro}</select></div>
<div class="row"><div class="field"><label for="jb-name">Full name</label><input id="jb-name" name="name" required></div><div class="field"><label for="jb-email">Email</label><input id="jb-email" name="email" type="email" required></div></div>
<div class="row"><div class="field"><label for="jb-loc">Country / time zone</label><input id="jb-loc" name="location" required></div><div class="field"><label for="jb-cred">Credentials (if any)</label><input id="jb-cred" name="credentials" placeholder="e.g. CFP®, CFA"></div></div>
<div class="field"><label for="jb-link">Portfolio / LinkedIn URL</label><input id="jb-link" name="portfolio" type="url" placeholder="https://" required></div>
<div class="field"><label for="jb-msg">Why you're a fit</label><textarea id="jb-msg" name="message" required></textarea></div>
<button class="btn btn-primary" type="submit">Send application</button></form></div></div></section>'''
    jobs = [{"@context": "https://schema.org", "@type": "JobPosting", "title": n, "description": d, "datePosted": ISO, "employmentType": "CONTRACTOR", "jobLocationType": "TELECOMMUTE", "applicantLocationRequirements": {"@type": "Country", "name": "Worldwide"}, "hiringOrganization": {"@type": "Organization", "name": NAME, "sameAs": DOMAIN}} for n, m, d in roles]
    write(path, "Careers — Writers, Reviewers, Creators & Growth Talent", "Join Private.Finance: remote roles for personal finance writers, credentialed expert reviewers, video creators, SEO marketers, partnerships and developers.", body, "", [crs] + jobs, priority="0.5")
    SEARCH.append({"t": "Careers", "d": "Remote roles for writers, reviewers, creators", "c": "Page", "u": "careers/", "k": "jobs hiring careers talent"})

    # ------------------------------------------------------------ CONTACT
    path = "contact/index.html"; P = "../"
    cr, crs = crumbs(path, [(None, "Contact")])
    body = f'''<section style="padding-top:40px"><div class="wrap">{cr}<div class="grid g2" style="align-items:start">
<div><span class="eyebrow">Contact</span><h1>Get in touch</h1><p class="lede">Questions, corrections, partnership ideas or press inquiries — we read everything and usually reply within 1–2 business days.</p>
<div class="card" style="margin-top:24px"><h3>Prefer email?</h3><p class="muted">Click below to open a pre-addressed email in your mail app.</p><a href="#" class="btn btn-ghost" data-mail="Private.Finance inquiry">✉️ Email us</a></div>
<div class="card" style="margin-top:20px;background:var(--ink);color:#efeadb;border-color:var(--ink)"><h3 style="color:#fff">Interested in this website or domain?</h3><p style="color:#c8d3d0">For acquisition of the Private.Finance domain/website, sponsorship, advertising or partnership.</p><a class="btn btn-gold" href="{WEBWORKS}" target="_blank" rel="noopener">Contact the owner →</a></div>
<p class="muted" style="margin-top:20px;font-size:.9rem">Looking for financial advice? We can't advise on individual situations, but we can <a href="{P}get-matched/">introduce you to a fee-only advisor</a>.</p></div>
<form class="card" data-pf data-subject="Contact form"><h2 style="font-size:1.5rem">Send a message</h2><input class="hp" name="_honey" tabindex="-1" autocomplete="off">
<div class="row"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div><div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>General question</option><option>Correction / feedback on content</option><option>Advertising</option><option>Sponsorship</option><option>Partnership</option><option>Domain / website acquisition</option><option>Press / media</option><option>Privacy or data request</option><option>Copyright / removal request</option></select></div>
<div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that my message may be stored to respond to me, as described in the <a href="{P}privacy-policy/">privacy policy</a>.</label>
<button class="btn btn-primary" type="submit" style="margin-top:14px">Send message</button></form></div></div></section>'''
    write(path, "Contact Private.Finance", "Contact Private.Finance with questions, corrections, advertising, sponsorship, partnership, press or domain acquisition inquiries.", body, "", [crs], priority="0.5")
    SEARCH.append({"t": "Contact", "d": "Send us a message", "c": "Page", "u": "contact/", "k": "contact email"})

    # ------------------------------------------------------------ ABOUT & POLICIES
    simple("about/index.html", "About Private.Finance", "Private.Finance is an independent, privacy-first personal finance publication with free calculators, plain-English guides and advisor matching.", f'''
<p>{NAME} exists for one reason: <b>good money decisions shouldn't require handing over your data.</b> Most financial websites gate their calculators behind email forms and sell the results to lenders and marketers. We built the opposite — tools that run entirely on your device, guides that explain trade-offs honestly, and an optional, transparent way to talk to a professional when you want one.</p>
<h2 id="what-we-do">What we do</h2><ul><li><b>Free, private calculators</b> for budgeting, debt, saving, investing, retirement and real estate.</li><li><b>In-depth guides</b> that cover the fundamentals and the world of private wealth — private banking, wealth management, private credit and private equity.</li><li><b>Advisor matching</b> that introduces readers who ask for help to independent, fee-only professionals.</li><li><b>A global lens</b> — we note where rules differ in the US, Canada, UK, India and Australia.</li></ul>
<h2 id="how-we-make-money">How we make money</h2><p>We are funded by: (1) display advertising, including Google AdSense; (2) clearly labelled sponsorships; (3) referral fees from professional firms when a reader asks to be introduced; and (4) voluntary reader contributions. None of these sources can buy a favourable review, change a calculator's math or edit our guides. Sponsored content is always labelled.</p>
<h2 id="independence">Editorial independence</h2><p>Our editorial team decides what we cover and what we conclude. Advertisers and partners have no input. Read our <a href="__P__editorial-policy/">editorial policy</a> to see how we research, write, fact-check and correct.</p>
<h2 id="team">Our team</h2><p>{NAME} is produced by a small, remote editorial team, and we work with freelance writers and credentialed reviewers. We are <a href="__P__careers/">hiring</a>.</p>
<h2 id="contact">Contact</h2><p>Use our <a href="__P__contact/">contact page</a>. For inquiries about acquiring this domain or website, sponsorship, advertising or partnership, <a href="{WEBWORKS}" target="_blank" rel="noopener">contact the owner here</a>.</p>''', eyebrow="About us", lede="Independent, privacy-first personal finance — free tools, honest guides and transparent advisor matching.")

    simple("editorial-policy/index.html", "Editorial Policy & Fact-Checking", "How Private.Finance researches, writes, reviews, updates and corrects its personal finance content, and how we keep advertising separate from editorial.", f'''
<p>Money content can change lives, so we hold ourselves to a high standard. This policy explains how we work.</p>
<h2 id="principles">Our principles</h2><ul><li><b>Accuracy first.</b> Claims about rules, limits, fees and rates are checked against primary sources — regulators, government agencies, statutes and official product documents.</li><li><b>Balance.</b> We explain trade-offs and who a product or strategy is <em>not</em> right for.</li><li><b>Clarity.</b> Plain English, worked examples and defined terms.</li><li><b>Global awareness.</b> We flag where rules differ by country rather than assuming one market.</li><li><b>No hype.</b> We never promise returns or use fear to sell.</li></ul>
<h2 id="process">Our process</h2><ol><li><b>Research</b> using primary sources and established financial principles.</li><li><b>Drafting</b> by our editorial team. We may use software tools, including AI writing assistants, to help research, outline and draft; they never replace human editorial judgment.</li><li><b>Fact-check</b> of every figure, threshold and worked example; calculations are re-run independently.</li><li><b>Editing</b> for clarity, balance and compliance with this policy.</li><li><b>Review & updates</b> — guides are reviewed at least annually and whenever rules change. Each page shows its last-updated date.</li></ol>
<h2 id="calculators">Calculator methodology</h2><p>Every calculator page explains its formula and assumptions. Results are estimates based on constant rates and the inputs you provide; they are not predictions or guarantees.</p>
<h2 id="advertising">Advertising and editorial separation</h2><p>Advertising (including Google AdSense), sponsorships and referral relationships are managed separately from editorial. Sponsored content is labelled "Sponsored". Ads are labelled "Advertisement". Partners cannot review or approve editorial content before publication.</p>
<h2 id="corrections">Corrections</h2><p>If you spot an error, tell us via our <a href="__P__contact/">contact page</a> (topic: "Correction"). We review every report, correct confirmed errors promptly and note significant corrections on the page.</p>
<h2 id="not-advice">Not personal advice</h2><p>Our content is educational and general. It does not account for your personal circumstances and is not a substitute for advice from a licensed professional.</p>''', eyebrow="Trust & transparency")

    simple("privacy-policy/index.html", "Privacy Policy", "How Private.Finance handles personal data, cookies, advertising (including Google AdSense), forms, and your privacy rights under GDPR, CCPA, PIPEDA and other laws.", f'''
<p><b>Last updated:</b> {UPDATED}</p>
<p>This policy explains what information {NAME} ("we", "us") collects, how it is used and your choices. Our guiding principle is data minimisation: we collect as little as possible.</p>
<h2 id="calculators">1. Calculators and quizzes</h2><p>Our calculators and the Financial Health Score run entirely in your browser. The numbers you enter are <b>not transmitted to us</b>. If you choose "remember my numbers" on a tool, the values are stored only in your own browser's local storage on that device; you can clear them at any time.</p>
<h2 id="forms">2. Information you submit</h2><p>When you submit a form (contact, advisor matching, newsletter, contest entry, job application or pledge) we receive the information you provide, such as your name, email, phone number, location and your answers. Form submissions are delivered to our inbox through a third-party form-processing service (FormSubmit). We use this information only to respond to you and provide the service you asked for.</p>
<p><b>Advisor matching:</b> if you request introductions and give consent, we share your answers and contact details with up to three professional advisors or firms we introduce you to. We may receive a referral fee. We do not sell your information to data brokers or mass-marketing lists.</p>
<h2 id="advertising">3. Advertising and Google AdSense</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.</p>
<p>You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a> (or <a href="https://www.youronlinechoices.eu/" target="_blank" rel="noopener">youronlinechoices.eu</a> in Europe). Learn <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<p>Visitors in the European Economic Area, the United Kingdom and Switzerland are shown a consent message, where required, before personalised ads or non-essential cookies are used.</p>
<h2 id="video">4. Embedded videos</h2><p>Videos are embedded using YouTube's privacy-enhanced mode (youtube-nocookie.com) and load only when you click play. Once played, YouTube's own privacy policy applies.</p>
<h2 id="payments">5. Contributions</h2><p>Donations are processed by PayPal. We do not receive or store your card details. PayPal's privacy policy applies to the payment.</p>
<h2 id="logs">6. Hosting and technical data</h2><p>Our hosting provider may process standard technical data (such as IP address and browser type) to deliver and secure the website. We do not run our own analytics trackers on calculator inputs.</p>
<h2 id="retention">7. Retention</h2><p>We keep form submissions only as long as needed for the purpose you submitted them for, then delete them, unless we must keep them longer by law.</p>
<h2 id="rights">8. Your rights</h2><p>Depending on where you live (for example under the GDPR, UK GDPR, California CCPA/CPRA, Canada's PIPEDA, India's DPDP Act or Australia's Privacy Act), you may have the right to access, correct, delete or port your data, to object to or restrict processing, to withdraw consent and to opt out of the "sale" or "sharing" of personal information. To exercise these rights, contact us via our <a href="__P__contact/">contact page</a> (topic: "Privacy or data request"). We will not discriminate against you for exercising your rights.</p>
<h2 id="children">9. Children</h2><p>{NAME} is intended for adults and is not directed to children under 16. We do not knowingly collect personal information from children.</p>
<h2 id="changes">10. Changes</h2><p>We may update this policy. The "last updated" date shows the latest version.</p>
<h2 id="contact">11. Contact</h2><p>Questions about privacy? Reach us through our <a href="__P__contact/">contact page</a>.</p>''', eyebrow="Legal")

    simple("cookie-policy/index.html", "Cookie Policy", "Which cookies and local storage Private.Finance uses, including Google AdSense advertising cookies, and how to control them.", f'''
<p><b>Last updated:</b> {UPDATED}</p>
<h2 id="what">What are cookies?</h2><p>Cookies are small text files stored by your browser. "Local storage" is a similar browser feature. We use both sparingly.</p>
<h2 id="ours">What we store</h2><div class="table-scroll"><table><thead><tr><th>Name</th><th>Purpose</th><th>Type</th></tr></thead><tbody>
<tr><td class="mono">pf_cookie_ok</td><td>Remembers your cookie-notice choice</td><td>Essential (local storage)</td></tr>
<tr><td class="mono">pf_theme</td><td>Remembers light/dark mode</td><td>Preference (local storage)</td></tr>
<tr><td class="mono">pf_currency</td><td>Remembers your calculator currency</td><td>Preference (local storage)</td></tr>
<tr><td class="mono">pf_networth, pf_health_score</td><td>Only if you choose to save them — stays on your device</td><td>Preference (local storage)</td></tr>
<tr><td>Google AdSense cookies</td><td>Serve, personalise and measure ads; fraud prevention</td><td>Advertising (third party)</td></tr></tbody></table></div>
<h2 id="third">Third-party cookies</h2><p>Google and its partners may set cookies to serve ads based on your visits to this and other sites. See our <a href="__P__privacy-policy/#advertising">privacy policy</a> for opt-out links. YouTube may set cookies only after you play an embedded video.</p>
<h2 id="control">Your control</h2><p>You can block or delete cookies in your browser settings, choose "Essential only" in our notice, and manage ad personalisation at <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>.</p>''', eyebrow="Legal")

    simple("terms/index.html", "Terms of Use", "The terms that govern use of the Private.Finance website, calculators, guides, forms, contests and advisor matching service.", f'''
<p><b>Last updated:</b> {UPDATED}</p>
<h2 id="acceptance">1. Acceptance</h2><p>By using {NAME} (the "Site") you agree to these Terms. If you do not agree, please do not use the Site.</p>
<h2 id="education">2. Educational purpose only</h2><p>All content, calculators and tools are provided for general educational and informational purposes. Nothing on the Site is financial, investment, tax, legal or insurance advice, or a recommendation to buy or sell any product. No advisor–client or fiduciary relationship is created by your use of the Site.</p>
<h2 id="calculators">3. Calculators</h2><p>Results are estimates based on your inputs and simplifying assumptions. They may not reflect actual outcomes. You are responsible for verifying any figures before relying on them.</p>
<h2 id="matching">4. Advisor matching</h2><p>{NAME} is not a registered investment adviser, broker-dealer, bank, lender or insurer. When you request introductions, we pass your information to independent professionals. We do not guarantee their services, and any engagement is solely between you and them. Verify credentials and registration independently.</p>
<h2 id="ip">5. Intellectual property</h2><p>The Site's original text, code, design and graphics are owned by {NAME} and protected by copyright. You may share links and quote brief excerpts with attribution. You may not republish substantial portions without written permission. See our <a href="__P__trademark/">trademark &amp; copyright disclosure</a>.</p>
<h2 id="conduct">6. Acceptable use</h2><p>Do not misuse the Site, submit false or unlawful content, attempt to disrupt its operation, or scrape it in a way that burdens our systems.</p>
<h2 id="third">7. Third-party content and links</h2><p>Ads, embedded videos and external links are provided by third parties. We are not responsible for their content, products or practices.</p>
<h2 id="contests">8. Contests and contributions</h2><p>Contests are governed by their <a href="__P__contests/#rules">official rules</a>. Contributions are voluntary, non-refundable except where required by law, and not tax-deductible.</p>
<h2 id="liability">9. Disclaimer of warranties and limitation of liability</h2><p>The Site is provided "as is" without warranties of any kind. To the fullest extent permitted by law, {NAME} is not liable for any loss arising from your use of, or reliance on, the Site.</p>
<h2 id="changes">10. Changes and law</h2><p>We may update these Terms at any time. Continued use means acceptance. These Terms are governed by applicable law in the operator's jurisdiction, without regard to conflict-of-law rules.</p>
<h2 id="contact">11. Contact</h2><p>Questions? Use our <a href="__P__contact/">contact page</a>.</p>''', eyebrow="Legal")

    simple("disclaimer/index.html", "Financial Disclaimer", "Private.Finance provides general educational information only — not personalised financial, investment, tax or legal advice. Read our full disclaimer.", f'''
<p>{NAME} publishes general information to help readers understand personal finance. <b>It is not personalised financial, investment, tax, legal or insurance advice</b>, and it does not take into account your objectives, financial situation or needs.</p>
<ul><li>Past performance does not guarantee future results. All investing involves risk, including possible loss of principal.</li><li>Rules, tax treatment, contribution limits, interest rates and product terms vary by country and change over time. Information may not be current or applicable to you.</li><li>Calculator outputs are hypothetical illustrations, not predictions.</li><li>Mentions of account types, strategies or categories of products are for education, not endorsement.</li><li>Before making decisions, consult a qualified, licensed professional in your jurisdiction.</li></ul>
<h2 id="advertising">Advertising and compensation</h2><p>We display third-party advertising and may receive compensation from sponsors and from professional firms we introduce readers to. This may influence which partners appear on the Site but never our editorial conclusions. See <a href="__P__about/#how-we-make-money">how we make money</a>.</p>
<h2 id="external">External content</h2><p>Embedded videos and linked resources are created by third parties. Their views are their own.</p>''', eyebrow="Legal")

    simple("trademark/index.html", "Trademark & Copyright Disclosure", "Trademark and copyright disclosure for Private.Finance: independent website, descriptive use of 'private finance', third-party marks and content, and takedown requests.", f'''
<h2 id="name">Our name</h2><p>"{NAME}" is the name and domain of this independent website. The words "private" and "finance" are used in their ordinary, generic and descriptive sense — to describe personal and private finance topics and privacy-respecting tools.</p>
<p><b>{NAME} is not affiliated with, endorsed by, sponsored by or connected to any company, firm, product, service or registered or unregistered trademark that uses the name "Private Finance", "PrivateFinance" or any similar name or mark</b>, in any country. No such association should be inferred. If you represent a rights holder and have a concern, please contact us and we will respond promptly.</p>
<h2 id="third-party">Third-party trademarks</h2><p>All product names, logos, brands and trademarks mentioned on this site (for example, names of regulators, credentials such as CFP®, or video channels) are the property of their respective owners. Use of these names is for identification and educational reference only and does not imply endorsement. CFP® and CERTIFIED FINANCIAL PLANNER™ are certification marks owned by their respective certification bodies.</p>
<h2 id="copyright">Copyright</h2><p>© 2026 {NAME}. All original text, calculators, source code, graphics and site design are protected by copyright. Brief quotations with attribution and a link are welcome; republishing substantial portions requires written permission.</p>
<h2 id="videos">Embedded videos</h2><p>Videos are hosted by YouTube and remain the property of their creators. They are displayed using YouTube's standard embedded player in accordance with YouTube's Terms of Service. {NAME} does not claim ownership of embedded videos.</p>
<h2 id="takedown">Copyright and trademark complaints</h2><p>If you believe content on this site infringes your copyright or trademark, send a notice via our <a href="__P__contact/">contact page</a> (topic: "Copyright / removal request") including: identification of the work or mark; the URL of the material; your contact information; a statement of good-faith belief that the use is unauthorised; and a statement that the information is accurate and that you are the rights holder or authorised to act for them. We will review and act promptly, including removal where appropriate.</p>''', eyebrow="Legal")

    # ------------------------------------------------------------ HTML SITEMAP
    groups = [("Tools", [(f"tools/{t['slug']}/", t["name"]) for t in TOOLS]), ("Guides", [(f"guides/{g['slug']}/", g["title"]) for g in guides]),
              ("Explore", [("private-wealth/", "Private Wealth hub"), ("get-matched/", "Get matched with an advisor"), ("videos/", "Videos"), ("resources/", "Resources"), ("glossary/", "Glossary")]),
              ("Community", [("support/", "Support / donate"), ("contests/", "Contests & prizes"), ("careers/", "Careers"), ("advertise/", "Advertise & sponsor"), ("contact/", "Contact")]),
              ("Company & legal", [("about/", "About"), ("editorial-policy/", "Editorial policy"), ("privacy-policy/", "Privacy policy"), ("cookie-policy/", "Cookie policy"), ("terms/", "Terms of use"), ("disclaimer/", "Disclaimer"), ("trademark/", "Trademark & copyright")])]
    sm = "".join(f"<h2>{h}</h2><ul>" + "".join(f'<li><a href="__P__{u}">{esc(t)}</a></li>' for u, t in items) + "</ul>" for h, items in groups)
    simple("sitemap/index.html", "Sitemap", "Every page on Private.Finance: calculators, guides, hubs, community pages and policies.", sm)

    # ------------------------------------------------------------ 404
    body = '''<section style="padding:80px 0"><div class="wrap narrow center"><div style="font-size:4rem">🔒</div><h1>This page is in a vault we can't open</h1><p class="lede" style="margin:0 auto 24px">The page you're looking for doesn't exist or has moved.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="/">Go home</a><a class="btn btn-ghost" href="/tools/">Free tools</a><a class="btn btn-ghost" href="/guides/">Guides</a></div></div></section>'''
    write("404.html", "Page not found", "Page not found.", body, index=False)
    fp = os.path.join(OUT, "404.html")
    s = open(fp, encoding="utf-8").read().replace("<head>", '<head>\n<base href="/">', 1).replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    open(fp, "w", encoding="utf-8").write(s)
