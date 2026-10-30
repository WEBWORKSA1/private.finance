# Private.Finance

**Your money. Your business.** A privacy-first personal-finance website: 10 free calculators that run entirely in the browser, 15 long-form guides (budgeting → private wealth), a Financial Health Score quiz, a fee-only advisor-matching lead funnel, a video library, a glossary, and community pages for donations, contests, careers and sponsorships.

- **Live:** https://private.finance (GitHub Pages, `main` branch, root)
- **Monetization:** Google AdSense (`ca-pub-6620975821265271`), advisor-match leads, sponsorships, reader contributions
- **Strategy & phase-wise build prompt:** [BUILD-PROMPT.md](BUILD-PROMPT.md)
- **Competitive research (42 sites):** [RESEARCH.md](RESEARCH.md)

## Structure

```
/                     ← generated static site (served by GitHub Pages)
  index.html, tools/, guides/, private-wealth/, get-matched/, videos/, resources/,
  glossary/, support/, advertise/, contests/, careers/, contact/, about/, legal pages
  assets/css/style.css, assets/js/{main,calc,lead}.js
  ads.txt, robots.txt, sitemap.xml, search-index.json, CNAME, .nojekyll
_src/                 ← generator and content (edit here)
  build.py            ← run: pip install markdown && python3 _src/build.py
  pages.py            ← home, hubs, lead funnel, community and legal pages
  tools_data.py       ← the 10 calculators (inputs, outputs, explainers, FAQs)
  glossary_data.py, videos.json
  content/*.md        ← guides (frontmatter: slug, title, description, category, read, tool)
  assets/             ← source CSS/JS (copied to /assets on build)
```

## Go-live checklist

1. **Pages:** Settings → Pages → Source *Deploy from a branch* → `main` / `(root)` → Save. Custom domain: `private.finance` → Enforce HTTPS.
2. **DNS:** A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME → `webworksa1.github.io`.
3. **Forms:** submit any form once on the live site, then click FormSubmit's activation email. Optionally paste the alias it gives you into `PF.config.formAlias` (in `_src/assets/js/main.js`, then rebuild, or edit `assets/js/main.js` directly).
4. **AdSense:** add the site, keep Auto ads on and enable *Privacy & messaging* (GDPR consent). For manual units, paste slot IDs into `PF.config.adSlots`.
5. **Search Console:** submit `https://private.finance/sitemap.xml`.

## Adding content

- **New guide:** add `_src/content/<slug>.md` with the same frontmatter → rebuild.
- **New calculator:** add an entry to `_src/tools_data.py` and a function to `calcs` in `_src/assets/js/calc.js` → rebuild.
- **New video:** add `{id, title, channel, topic, guides}` to `_src/videos.json` → rebuild.

## Privacy & contact

All forms and the email button route to a single protected inbox. The address is stored encoded and is assembled only at click or submit time. It never appears in the HTML or in this repository.

## Trademark & copyright

"Private.Finance" is the name of this independent website and uses "private" and "finance" descriptively. It is not affiliated with any company, product or mark named "Private Finance" or similar. Third-party names and marks belong to their owners; embedded videos remain the property of their creators. © 2026 Private.Finance.

Interested in this website, domain name, sponsorship, advertising or partnership? → https://web.works/contact
