# Private.Finance — Strategy & Phase-Wise Build Prompt

## 0. The idea (and why it wins)

**Concept:** *Private.Finance — "Your money. Your business."* A **privacy-first personal-finance platform**: free calculators that run 100% in the browser (nothing uploaded), long-form guides from budgeting to **private wealth** (private banking, wealth management, private credit, private equity), and a **free fee-only advisor-matching funnel** that turns high-intent readers into high-value leads.

**Why this angle beats a generic finance blog**

| Lever | Logic |
|---|---|
| Domain fit | "Private" = privacy-respecting tools **and** private-wealth topics. Both are literal readings of the name, so the brand needs no explanation. |
| Ad yield | Personal finance sits among the highest-CPC AdSense verticals; wealth-management, mortgage, retirement and advisor keywords sit at the top of it. Calculators get long time-on-page and repeat visits, which means more ad impressions per session. |
| Lead value | Advisor-matching leads are priced by investable assets. The funnel captures that one field and tags every lead (C → A++) so the best leads can be sold or routed to the best-paying partners. |
| Defensibility | "Your numbers never leave your device" is a claim most competitors can't make, because they gate calculators behind email capture. |
| Expandability | One Python generator with Markdown content. New guides and calculators are added as data, so the site scales to hundreds of pages without redesign. |

**Revenue model (planning assumptions, not guarantees)**

| Stream | Assumption | At 50k pageviews/mo |
|---|---|---|
| AdSense (Auto ads + manual slots) | Tier-1-heavy finance traffic, page RPM roughly $10–$30 | ≈ $500–$1,500/mo |
| Advisor-match leads | 0.5–1% of ~20k visitors convert; referral value ~$50–$200 per qualified lead | ≈ $5k–$40k/mo potential once partners are signed |
| Sponsorships (calculator, newsletter, contest) | 1–3 sponsors | $500–$5k/mo |
| Reader contributions | PayPal, one-off or monthly | Small, but builds goodwill and signals social proof |
| Domain/site sale | Inquiry banner on every page links to web.works/contact | Option value |

**The bold path:** treat this as a **lead-generation business that runs ads**, not an ad site that collects some leads. Signing 3–5 fee-only advisory partners (or a lead marketplace) is worth more than doubling traffic.

**The safe path:** AdSense plus a newsletter only. It needs no partner work, but its revenue ceiling is roughly 10× lower.

---

## 1. Phase-wise build prompt

> Use these prompts in order. Each phase is self-contained and testable.

### Phase 1 — Foundation & brand
"Build a static, dependency-free website for the domain **Private.Finance**, hostable on GitHub Pages (main branch, root, `.nojekyll`, `CNAME` = private.finance). Use a Python generator (`_src/build.py`) that renders Markdown guides and data-driven pages into directory-style URLs (`/guides/<slug>/`), with relative links. Design system: vault-ink (#0d1b1e), banknote cream (#f6f3ec), emerald (#0f5c4d), bullion gold (#c9a227); fonts Fraunces (display), Inter (body), JetBrains Mono (numbers). Include light/dark mode, a sticky header, a mobile menu, a `/` and Ctrl+K search modal backed by `search-index.json`, scroll-reveal motion, reduced-motion support and a sticky mobile CTA bar. **Every page** starts with a top strip: 'Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership' linking to https://web.works/contact."

### Phase 2 — AdSense readiness
"Add the AdSense script (`ca-pub-6620975821265271`) in every `<head>`, plus `<meta name="google-adsense-account">`, `ads.txt` (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), robots.txt, sitemap.xml and an HTML sitemap. Add labelled ad containers (top, in-article, sidebar, footer) that stay empty until slot IDs are added in one config object, so Auto ads work on day 1. Create About, Editorial Policy (including AI-assistance disclosure), Privacy Policy (Google advertising-cookie language, opt-out links, GDPR/CCPA/PIPEDA/DPDP rights), Cookie Policy, Terms, Disclaimer and a Trademark & Copyright disclosure. Add a cookie notice. Make sure there is no thin content: 15+ guides of 1,200+ words, each with an original worked example, a table and FAQs."

### Phase 3 — Privacy-first calculators (10)
"Build 10 vanilla-JS calculators that run entirely in the browser, with currency switching (USD, CAD, GBP, EUR, INR, AUD, AED, LKR), canvas charts, shareable URL-hash links and print/PDF: compound interest, retirement/FIRE, mortgage with PMI and amortization, debt avalanche vs snowball, 50/30/20 budget, emergency fund, loan/EMI, net worth (optional local-only save), savings goal and inflation. Each page has: inputs left, results right, KPIs, a chart, a 'how it works' formula explainer, FAQs (FAQPage schema), WebApplication schema, related guides and an inline advisor-match CTA."

### Phase 4 — Content engine
"Write 15 original long-form guides (Wealth, Banking, Investing, Debt, Budgeting, Retirement, Credit, Privacy, Real Estate) with frontmatter (slug, title, description, category, read, tool). Render them with breadcrumbs, a byline, an updated date, an auto table of contents, a key-takeaways box, an in-article ad, a mid-article calculator CTA, an embedded explainer video, a FAQ accordion with schema, an educational-content disclosure, an inline lead form and related reading. Note US/Canada/UK/India/Australia differences. Never fabricate statistics."

### Phase 5 — Lead generation (the money page)
"Build `/get-matched/`: a six-step, one-question-per-screen advisor-matching funnel (goal → investable assets → age and income → country, region and meeting preference → timing and notes → contact plus explicit consent). Add a progress bar, auto-advance, a back button, prefill from URL params (`?goal=&assets=&source=`), a honeypot, a lead tier (C/B/A/A+/A++) computed from assets, and the Financial Health Score passed through as a hidden field. Put the trust stack in a sidebar ('How it works', advisor standards, referral disclosure). Feed it from a homepage teaser (goal + assets selects), a sidebar card and inline CTA on every guide and calculator, and the Financial Health Score quiz result."

### Phase 6 — Engagement
"Add a six-question Financial Health Score quiz on the homepage (scored locally, animated ring, top three fixes linked to tools, CTA into the funnel), a homepage hero growth widget, a curated YouTube library using youtube-nocookie click-to-load facades with topic filters (verify every video ID), a 50-term glossary with DefinedTermSet schema, an official-resources directory by country (regulators and advisor-verification registers) and a Private Wealth hub with a 'wealth-service ladder' table."

### Phase 7 — Community & monetization pages
"Build: **Support** (tiered PayPal contributions, purpose selector for operations / marketing / hiring / contests, monthly option, transparent allocation bar, pledge form for large gifts, clear 'not tax-deductible' note); **Advertise** (sponsorship packages, standards, media-kit form, domain-acquisition CTA); **Contests** (skill-based Money Moves Challenge, prize ladder, entry form, official rules with no-purchase-necessary, eligibility and skill-testing-question clauses); **Careers** (six remote roles, JobPosting schema, application form); **Contact** (topic-routed form plus a hidden-address email button)."

### Phase 8 — Protected inbox
"Route every form to a single inbox through FormSubmit's AJAX endpoint. The address must never appear in HTML, source or the repo: store it encoded, reverse and base64 it, assemble it only at click or submit time, and fall back to a pre-filled `mailto:` built the same way if sending fails. Do the same for PayPal donate links. Verify with `grep -r` that the address appears nowhere."

### Phase 9 — QA
"With Playwright: load every page and fail on JS errors, HTTP errors or NaN in KPIs; complete the quiz, the full lead funnel (with a mocked endpoint, asserting the payload) and the contact fallback; check mobile (390px) for horizontal overflow and that the menu works; take desktop and mobile screenshots."

### Phase 10 — Launch & growth
1. GitHub → Settings → Pages → *Deploy from a branch* → `main` / `(root)`; set the custom domain `private.finance` and enforce HTTPS.
2. DNS at the registrar: A records → 185.199.108.153, .109.153, .110.153, .111.153; `www` CNAME → `webworksa1.github.io`.
3. Submit the site to AdSense, Google Search Console (sitemap.xml) and Bing Webmaster Tools. In AdSense, enable Auto ads and **Privacy & messaging** (a Google-certified CMP for EEA/UK visitors).
4. First form submission: FormSubmit emails an activation link. Click it once, then optionally paste the alias it provides into `PF.config.formAlias` in `assets/js/main.js` (`_src/assets/js/main.js` for rebuilds).
5. Growth: publish 2 guides a week (targets: "best time to hire a financial advisor", "AUM fee calculator", "private bank minimums by bank", "rent vs buy"); add an AUM-fee calculator and rent-vs-buy calculator; pitch three fee-only firms for paid lead routing; create YouTube walkthroughs of each calculator.
