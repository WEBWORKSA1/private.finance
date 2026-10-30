# Calculator definitions for Private.Finance
def rng(i, label, mn, mx, step, val, suffix=""):
    return (f'<div class="field"><label for="{i}">{label} <output for="{i}" data-suffix="{suffix}"></output></label>'
            f'<input class="range" type="range" id="{i}" min="{mn}" max="{mx}" step="{step}" value="{val}"></div>')

def num(i, label, val, cur=True, step="any", help_=""):
    pre = '<span class="pre" data-cur>$</span>' if cur else ''
    cls = "input-group" if cur else ""
    h = f'<small class="muted">{help_}</small>' if help_ else ''
    return (f'<div class="field"><label for="{i}">{label}</label><div class="{cls}">{pre}'
            f'<input type="number" inputmode="decimal" id="{i}" value="{val}" min="0" step="{step}"></div>{h}</div>')

def sel(i, label, opts, val=None):
    o = "".join(f'<option value="{v}"{" selected" if v == val else ""}>{t}</option>' for v, t in opts)
    return f'<div class="field"><label for="{i}">{label}</label><select id="{i}">{o}</select></div>'

def kpi(i, label, hl=False):
    return f'<div class="kpi{" hl" if hl else ""}"><small>{label}</small><b id="{i}">—</b></div>'

def chart(i):
    return f'<div class="chart-box"><canvas id="{i}-chart" style="width:100%;height:100%"></canvas></div><div class="legend" id="{i}-legend"></div>'

TOOLS = [
 dict(slug="compound-interest", name="Compound Interest Calculator", icon="📈", cat="Investing",
  short="See how a lump sum plus monthly contributions grows over time.",
  desc="Free compound interest calculator with monthly contributions, compounding frequency, a year-by-year table and growth chart. Runs privately in your browser.",
  inputs=num("ci-p","Starting amount",10000)+num("ci-m","Monthly contribution",500)+rng("ci-r","Annual return",0,15,0.1,7,"%")+rng("ci-y","Years",1,50,1,25," yrs")+sel("ci-n","Compounding",[("12","Monthly"),("1","Annually"),("4","Quarterly"),("365","Daily")],"12"),
  results='<div class="kpis">'+kpi("ci-fv","Future value",True)+kpi("ci-c","Total contributed")+kpi("ci-i","Interest earned")+kpi("ci-x","Money multiple")+'</div>'+chart("ci")+
   '<details style="margin-top:16px"><summary><b>Year-by-year table</b></summary><div class="table-scroll" style="margin-top:10px"><table><thead><tr><th>Year</th><th class=num>Contributed</th><th class=num>Interest</th><th class=num>Balance</th></tr></thead><tbody id="ci-table"></tbody></table></div></details>',
  how="""<p>The calculator grows your balance month by month. Each month, the balance earns the monthly equivalent of your annual rate (adjusted for the compounding frequency you choose), and then your monthly contribution is added. The general formula for a single deposit is <span class="mono">A = P × (1 + r/n)<sup>n×t</sup></span>, where <em>P</em> is principal, <em>r</em> the annual rate, <em>n</em> the compounding periods per year and <em>t</em> the number of years. Regular contributions are layered on top as a growing annuity.</p>
<p>The gold portion of the chart is the interest earned on earlier interest — the "snowball" that makes time the most powerful variable. Notice how the gold band is thin for the first decade and then dominates: that is why starting early often matters more than contributing a lot later.</p>
<p>Returns are assumed constant for illustration. Real markets fluctuate, and fees and taxes reduce the result. Try lowering the return by 1% to see how much a typical fund fee costs you over the full period.</p>""",
  faq=[("What return should I assume?","Many planners use a conservative long-run real (after-inflation) return of roughly 4–6% for a diversified stock-heavy portfolio and lower for bond-heavy or cash savings. Use several scenarios rather than one optimistic number."),
       ("Does compounding frequency matter much?","Less than most people expect. Moving from annual to monthly compounding raises the effective rate slightly; your contribution amount, the rate itself and time invested matter far more."),
       ("Is my data saved?","No. The math runs entirely in your browser. Nothing you type is sent to us or anyone else.")],
  guides=["compound-interest","index-funds-101","private-wealth-management"]),

 dict(slug="retirement", name="Retirement & FIRE Calculator", icon="🏖️", cat="Retirement",
  short="Find your nest-egg target and the monthly savings needed to reach it.",
  desc="Free retirement calculator: estimate your FIRE number with inflation and a safe-withdrawal rate, project your savings and see the monthly amount needed to close the gap.",
  inputs='<div class="row">'+num("rt-age","Current age",32,False)+num("rt-ret","Retirement age",60,False)+'</div>'+num("rt-sav","Current retirement savings",60000)+num("rt-m","Monthly contribution",900)+num("rt-inc","Desired yearly income in retirement (today's money)",60000,help_="Subtract expected government pensions for a more precise number.")+rng("rt-r","Expected annual return",0,12,0.1,6.5,"%")+rng("rt-inf","Inflation",0,8,0.1,2.5,"%")+rng("rt-wr","Withdrawal rate",2,6,0.1,4,"%"),
  results='<div class="kpis">'+kpi("rt-target","Target nest egg",True)+kpi("rt-proj","Projected at retirement")+kpi("rt-gap","Gap")+kpi("rt-need","Needed monthly")+'</div><p class="muted" style="font-size:.9rem">Target in today\'s money: <b id="rt-today" class="mono">—</b> · Progress: <b id="rt-pct" class="mono">—</b></p><div class="progress"><span id="rt-bar"></span></div>'+chart("rt"),
  how="""<p>First, your desired income is inflated to the year you retire. Dividing that by your withdrawal rate gives the portfolio size that could sustain it — at a 4% rate, that is 25× your annual spending, the classic "FIRE number." Next, your current savings and monthly contributions are projected forward at your expected return. The difference is your gap, and the calculator solves for the monthly contribution that would close it exactly by your target age.</p>
<p>The 4% guideline comes from studies of historical US market returns over 30-year retirements. Early retirees with 40–50-year horizons, or people retiring into weak markets, often use 3–3.5% for extra safety. Government pensions (Social Security, CPP/OAS, the UK State Pension, EPF/NPS, the Age Pension) reduce how much you must fund yourself — subtract them from the income figure.</p>""",
  faq=[("What is a FIRE number?","It is the invested amount that could fund your annual spending indefinitely at a chosen withdrawal rate. At 4%, multiply annual spending by 25; at 3.5%, by about 28.6."),
       ("Should I use nominal or real returns?","This calculator uses nominal returns and inflates your income target separately, so enter an expected nominal return (before inflation)."),
       ("How accurate is this?","It is a planning estimate with constant returns. Real results depend on market sequence, taxes, fees and spending changes. Revisit it yearly or ask a fee-only advisor to stress-test it.")],
  guides=["how-much-to-retire","private-equity-for-individuals","fee-only-financial-advisor"]),

 dict(slug="mortgage", name="Mortgage Calculator with PMI", icon="🏡", cat="Real Estate",
  short="Monthly payment, total interest, taxes, insurance and PMI in one view.",
  desc="Free mortgage calculator with PMI, property tax and insurance. See your full monthly payment, total interest, when PMI drops off and a yearly amortization schedule.",
  inputs=num("mg-price","Home price",450000)+rng("mg-dp","Down payment",0,60,1,10,"%")+rng("mg-rate","Interest rate",0,12,0.05,6.5,"%")+sel("mg-term","Loan term",[("30","30 years"),("25","25 years"),("20","20 years"),("15","15 years"),("10","10 years")],"30")+rng("mg-tax","Property tax (yearly % of price)",0,3,0.05,1.1,"%")+num("mg-ins","Home insurance per year",1800)+rng("mg-pmi","PMI / mortgage insurance rate (if <20% down)",0,2,0.05,0.6,"%"),
  results='<div class="kpis">'+kpi("mg-total","Total monthly",True)+kpi("mg-pi","Principal & interest")+kpi("mg-int","Total interest")+kpi("mg-loan","Loan amount")+'</div><p class="muted" style="font-size:.92rem">Down payment: <b id="mg-dp-out" class="mono">—</b> · PMI: <b id="mg-pmi-out" class="mono">—</b></p>'+chart("mg")+
   '<details style="margin-top:16px"><summary><b>Yearly amortization schedule</b></summary><div class="table-scroll" style="margin-top:10px"><table><thead><tr><th>Year</th><th class=num>Principal</th><th class=num>Interest</th><th class=num>Balance</th></tr></thead><tbody id="mg-table"></tbody></table></div></details>',
  how="""<p>Principal and interest use the standard amortization formula <span class="mono">M = P × r / (1 − (1 + r)<sup>−n</sup>)</span>, with <em>r</em> the monthly rate and <em>n</em> the number of payments. Property tax and insurance are added monthly. If your down payment is under 20%, mortgage insurance is estimated as a yearly percentage of the loan and dropped once the balance reaches 78% of the original price — the automatic-termination point for conventional loans in the US.</p>
<p>In Canada, mortgage default insurance for down payments under 20% is usually a one-time premium added to the loan rather than a monthly charge; in Australia, lenders mortgage insurance (LMI) works similarly. If that applies to you, set the PMI rate to 0 and add the premium to the home price instead.</p>""",
  faq=[("How can I avoid PMI?","Put 20% or more down, ask about lender-paid options, or plan to request cancellation once your loan reaches 80% of the home's original value. Read our PMI guide for the details."),
       ("15-year or 30-year?","A 15-year loan has a higher payment but dramatically lower total interest. Compare both here — the difference in total interest is often six figures."),
       ("Does this include closing costs?","No. Budget separately for closing costs, which commonly run a few percent of the price depending on where you live.")],
  guides=["private-mortgage-insurance","credit-score-basics","emergency-fund"]),

 dict(slug="debt-payoff", name="Debt Payoff Planner (Avalanche vs Snowball)", icon="⛓️", cat="Debt",
  short="Compare avalanche and snowball side by side and see your debt-free date.",
  desc="Free debt payoff calculator comparing the avalanche and snowball methods. Add your debts, set an extra payment and see your debt-free date and total interest.",
  inputs='<div class="table-scroll" style="border:0;background:none"><table><thead><tr><th>Debt</th><th>Balance</th><th>APR %</th><th>Min/mo</th><th></th></tr></thead><tbody id="dp-rows"></tbody></table></div><button type="button" class="btn btn-ghost btn-sm" id="dp-add" style="margin:10px 0 16px">+ Add a debt</button>'+num("dp-extra","Extra payment each month",200),
  results='<div class="grid g2"><div class="card" style="box-shadow:none"><span class="tag">Avalanche</span><div class="kpis" style="margin-top:12px">'+kpi("dp-a-time","Debt-free in",True)+kpi("dp-a-int","Total interest")+'</div><small class="muted">Order: <span id="dp-a-order"></span></small></div><div class="card" style="box-shadow:none"><span class="tag">Snowball</span><div class="kpis" style="margin-top:12px">'+kpi("dp-s-time","Debt-free in")+kpi("dp-s-int","Total interest")+'</div><small class="muted">Order: <span id="dp-s-order"></span></small></div></div><p style="margin:14px 0">Avalanche saves you <b id="dp-save" class="mono">—</b> in interest versus snowball.</p><p id="dp-warn" class="note" style="display:none">At least one plan doesn\'t finish within 50 years — your payments may not cover the interest. Increase the extra payment.</p>'+chart("dp"),
  how="""<p>Each month the planner charges interest on every balance, pays each minimum, then sends everything left over — your extra payment plus minimums freed up from debts already paid off — to a single target debt. <b>Avalanche</b> targets the highest interest rate first, which mathematically minimizes interest. <b>Snowball</b> targets the smallest balance first, which produces quick wins that help many people stay motivated.</p>
<p>The gap between the two is often small when rates are similar and large when one debt (usually a credit card) has a much higher APR. If the savings are minor, pick the method you will actually stick with. If they are large, avalanche is usually worth it.</p>""",
  faq=[("Which method is better?","Avalanche always costs the same or less interest. Snowball can be better for you if early wins keep you committed. Use the numbers above to see what the motivation premium costs."),
       ("Should I consolidate instead?","A lower-rate consolidation loan or balance transfer can help if you stop adding new debt and the fees are lower than the interest saved. Run both scenarios here by editing the APRs."),
       ("Is my debt information stored?","No. Everything stays in this browser tab.")],
  guides=["debt-avalanche-vs-snowball","credit-score-basics","50-30-20-budget"]),

 dict(slug="budget", name="50/30/20 Budget Calculator", icon="🧮", cat="Budgeting",
  short="Split take-home pay into needs, wants and savings — and compare to reality.",
  desc="Free 50/30/20 budget calculator. Split your take-home pay into needs, wants and savings, customize the ratios and compare your actual spending against the targets.",
  inputs=num("bg-inc","Monthly take-home pay",5200)+rng("bg-np","Needs",30,70,1,50,"%")+rng("bg-wp","Wants",0,40,1,30,"%")+rng("bg-sp","Savings & extra debt payments",5,50,1,20,"%")+'<p class="muted" style="font-size:.88rem">Total: <b id="bg-tot" class="mono">100%</b> — keep it at 100%.</p><h4 style="margin-top:20px">Optional: your actual monthly spending</h4>'+num("bg-an","Actual needs",0)+num("bg-aw","Actual wants",0)+num("bg-as","Actual savings",0),
  results='<div class="kpis">'+kpi("bg-n","Needs target",True)+kpi("bg-w","Wants target")+kpi("bg-s","Savings target")+kpi("bg-yr","Saved per year")+'</div><div class="grid g2"><div>'+chart("bg")+'</div><div id="bg-feedback"></div></div>',
  how="""<p>The 50/30/20 rule divides after-tax income into three buckets: about half for <b>needs</b> (housing, utilities, groceries, insurance, minimum debt payments, transport to work), about 30% for <b>wants</b> (dining out, subscriptions, travel, hobbies) and about 20% for <b>savings and extra debt repayment</b>. It is a starting framework, not a law — in high-cost cities, needs can legitimately exceed 50%, and aggressive savers may flip wants and savings.</p>
<p>Adjust the sliders to your own split, then enter what you actually spend to get specific feedback on where the gap is.</p>""",
  faq=[("Is 50/30/20 based on gross or net income?","Net (take-home) income — what lands in your account after taxes and payroll deductions. If you contribute to a workplace retirement plan before tax, you can count that toward the 20%."),
       ("What if my needs are over 50%?","That is common in expensive housing markets. Reduce wants first, then look for structural fixes such as a roommate, refinancing or a cheaper commute."),
       ("Where should the 20% go?","Typically in order: a starter emergency fund, any employer match, high-interest debt, a full emergency fund, then long-term investing.")],
  guides=["50-30-20-budget","emergency-fund","debt-avalanche-vs-snowball"]),

 dict(slug="emergency-fund", name="Emergency Fund Calculator", icon="🛟", cat="Budgeting",
  short="Find your safety-net target and how long it'll take to build.",
  desc="Free emergency fund calculator. Add up essential monthly expenses, choose 3–12 months of coverage based on job stability and see your target and time to fully fund it.",
  inputs='<div class="row">'+num("ef-1","Housing",1600).replace('id="ef-1"','id="ef-1" class="ef-exp"')+num("ef-2","Utilities & phone",250).replace('id="ef-2"','id="ef-2" class="ef-exp"')+'</div><div class="row">'+num("ef-3","Groceries",550).replace('id="ef-3"','id="ef-3" class="ef-exp"')+num("ef-4","Transport",300).replace('id="ef-4"','id="ef-4" class="ef-exp"')+'</div><div class="row">'+num("ef-5","Insurance",220).replace('id="ef-5"','id="ef-5" class="ef-exp"')+num("ef-6","Minimum debt payments",200).replace('id="ef-6"','id="ef-6" class="ef-exp"')+'</div>'+num("ef-7","Other essentials",150).replace('id="ef-7"','id="ef-7" class="ef-exp"')+sel("ef-stab","Income stability",[("stable","Very stable (dual income, secure job)"),("average","Average"),("variable","Variable / commission"),("self","Self-employed / single income with dependants")],"average")+rng("ef-months","Months of coverage",1,12,1,6," mo")+num("ef-have","Already saved",2500)+num("ef-save","Can save per month",400),
  results='<div class="kpis">'+kpi("ef-goal","Emergency fund target",True)+kpi("ef-total","Essential expenses / mo")+kpi("ef-left","Still to save")+kpi("ef-time","Time to fully fund")+'</div><p class="muted">Coverage: <b id="ef-months-o" class="mono"></b> · Funded: <b id="ef-pct" class="mono"></b></p><div class="progress"><span id="ef-bar"></span></div><div class="note">Tip: keep this money in a separate high-interest savings account — accessible within a day or two, but not linked to your everyday debit card.</div>',
  how="""<p>An emergency fund covers <b>essential</b> expenses — not your full lifestyle — if income stops or a large unexpected bill arrives. The calculator totals the essentials you enter and multiplies by your chosen months of coverage. A common guideline is three to six months; people with variable income, a single household income or dependants often aim for six to twelve.</p>
<p>If the target feels huge, start with a mini-goal of one month, or a fixed starter amount, then keep building while you pay down high-interest debt.</p>""",
  faq=[("Should I invest my emergency fund?","Generally no. Its job is stability and access, not growth. High-interest savings accounts, money-market funds or short-term deposits are typical homes for it."),
       ("Do I need one if I have credit cards?","Credit is not a safety net — it turns an emergency into high-interest debt. A cash buffer protects your credit score and your choices."),
       ("What counts as an emergency?","Job loss, urgent medical or dental costs, essential car or home repairs, and urgent travel. Planned expenses like holidays or annual bills belong in separate sinking funds.")],
  guides=["emergency-fund","50-30-20-budget","financial-privacy"]),

 dict(slug="loan", name="Loan & EMI Calculator", icon="💳", cat="Debt",
  short="Monthly payment (EMI), total interest and true cost of any loan.",
  desc="Free loan and EMI calculator for personal, car, education and student loans. See your monthly payment, total interest and the true cost of borrowing instantly.",
  inputs=num("ln-p","Loan amount",25000)+rng("ln-r","Interest rate (APR)",0,30,0.1,9.5,"%")+'<div class="row">'+num("ln-t","Term",5,False)+sel("ln-unit","Unit",[("years","Years"),("months","Months")],"years")+'</div>',
  results='<div class="kpis">'+kpi("ln-pm","Monthly payment (EMI)",True)+kpi("ln-int","Total interest")+kpi("ln-tot","Total repaid")+kpi("ln-n","Payments")+'</div>'+chart("ln"),
  how="""<p>EMI (equated monthly instalment) is the fixed monthly payment that repays a loan in full over its term. It is calculated as <span class="mono">EMI = P × r × (1 + r)<sup>n</sup> / ((1 + r)<sup>n</sup> − 1)</span>, where <em>P</em> is the principal, <em>r</em> the monthly rate and <em>n</em> the number of months. Early payments are mostly interest; later ones are mostly principal.</p>
<p>The donut shows how much extra you pay over the principal. Try shortening the term: the monthly payment rises, but total interest usually drops sharply. Always compare loans by APR, which includes most fees, rather than the headline rate.</p>""",
  faq=[("What is a good interest rate?","It depends on the loan type, your credit profile and current central-bank rates. Get at least three quotes and compare APRs on identical terms."),
       ("Does prepaying help?","Usually yes — extra payments reduce principal and future interest. Check for prepayment penalties first."),
       ("Private or government student loan?","Government loans in many countries offer protections private loans lack. Read our private student loans guide before borrowing.")],
  guides=["private-student-loans","credit-score-basics","debt-avalanche-vs-snowball"]),

 dict(slug="net-worth", name="Net Worth Calculator", icon="⚖️", cat="Wealth",
  short="Add up assets and liabilities. Optionally save it on this device only.",
  desc="Free private net worth calculator. Total your assets and liabilities, see your debt-to-asset ratio and optionally save your figures only on your own device.",
  inputs='<h4>Assets</h4>'+"".join(num(f"nw-a{i}",l,v).replace(f'id="nw-a{i}"',f'id="nw-a{i}" class="nw-a"') for i,(l,v) in enumerate([("Cash & savings",15000),("Investments (taxable)",40000),("Retirement accounts",85000),("Home value",0),("Vehicles",12000),("Other assets",0)]))+'<h4>Liabilities</h4>'+"".join(num(f"nw-l{i}",l,v).replace(f'id="nw-l{i}"',f'id="nw-l{i}" class="nw-l"') for i,(l,v) in enumerate([("Mortgage",0),("Car loans",9000),("Student loans",18000),("Credit cards",3500),("Other debts",0)]))+'<label class="check"><input type="checkbox" id="nw-remember"> Remember my numbers on this device (stored only in your browser)</label><button type="button" class="btn btn-ghost btn-sm" id="nw-clear" style="margin-top:10px">Clear all</button>',
  results='<div class="kpis">'+kpi("nw-nw","Net worth",True)+kpi("nw-a","Total assets")+kpi("nw-l","Total liabilities")+kpi("nw-ratio","Debt-to-asset ratio")+'</div>'+chart("nw")+'<div class="note" style="margin-top:14px">Track this number every quarter. Direction matters more than the absolute figure — a rising net worth means your plan is working.</div>',
  how="""<p>Net worth is simply everything you own minus everything you owe. Use current market values for assets (what you could sell them for today, not what you paid) and current balances for debts. Retirement accounts can be counted at their full balance, though you may want to mentally discount them for future taxes.</p>
<p>The debt-to-asset ratio shows how leveraged you are. Below roughly 30–40% is generally considered comfortable for households with a mortgage; a ratio above 100% means you owe more than you own, which is common early in a career with student debt and not a reason to panic — just a baseline to improve from.</p>""",
  faq=[("Where is my data saved?","Only if you tick the box, and then only in your own browser's local storage on this device. We never receive it. Clearing your browser data removes it."),
       ("Should I include my home?","Yes, at a realistic market value, and include the mortgage as a liability. Some people also track net worth excluding their home to see liquid wealth."),
       ("What is a good net worth for my age?","Averages vary hugely by country and are skewed by the very wealthy. Compare yourself to your own past numbers instead.")],
  guides=["private-banking","financial-privacy","private-wealth-management"]),

 dict(slug="savings-goal", name="Savings Goal Calculator", icon="🎯", cat="Budgeting",
  short="How much to save each month to hit any goal by a deadline.",
  desc="Free savings goal calculator. Enter a target, timeline and interest rate to find exactly how much to save per month and per week to reach it.",
  inputs=num("sg-goal","Goal amount",30000)+num("sg-have","Already saved",3000)+rng("sg-y","Years to goal",0.5,30,0.5,4," yrs")+rng("sg-r","Interest / return",0,12,0.1,4,"%"),
  results='<div class="kpis">'+kpi("sg-pm","Save per month",True)+kpi("sg-wk","Save per week")+kpi("sg-int","Interest does for you")+'</div>'+chart("sg"),
  how="""<p>The calculator grows what you already have at your chosen rate, works out the shortfall at your deadline and solves for the level monthly deposit that closes it. For goals under about three years — a down payment, a car, a wedding — a high-interest savings account or short-term deposit is usually more appropriate than investing, because there is little time to recover from a market drop.</p>""",
  faq=[("What rate should I use?","For short goals, use the rate on your savings account. For goals 7+ years away that you would invest toward, use a conservative long-run return."),
       ("Can I automate this?","Yes — schedule a transfer on payday to a separate, named savings account. Automation is the single most reliable savings habit."),
       ("Is anything stored?","No. Use the share button to keep your inputs in a link instead.")],
  guides=["emergency-fund","50-30-20-budget","compound-interest"]),

 dict(slug="inflation", name="Inflation Calculator", icon="🎈", cat="Investing",
  short="What today's money will cost — and be worth — years from now.",
  desc="Free inflation calculator. See how much things will cost in the future and how much purchasing power today's money loses at any inflation rate.",
  inputs=num("in-amt","Amount today",1000)+rng("in-r","Average inflation rate",0,15,0.1,3,"%")+rng("in-y","Years",1,50,1,20," yrs"),
  results='<div class="kpis">'+kpi("in-fut","Future cost",True)+kpi("in-pow","Future purchasing power")+kpi("in-loss","Value lost")+'</div>'+chart("in"),
  how="""<p>Inflation compounds just like interest — in reverse for savers. At a constant rate <em>i</em>, the future cost of something is <span class="mono">today × (1 + i)<sup>years</sup></span>, and today's money is worth <span class="mono">today ÷ (1 + i)<sup>years</sup></span> in future terms. At 3% inflation, prices roughly double in 24 years (the rule of 72: 72 ÷ 3 = 24).</p>
<p>This is why cash under the mattress quietly loses value, and why long-term savings generally need to earn more than inflation after fees and taxes.</p>""",
  faq=[("What inflation rate should I use?","Many central banks target about 2% a year, but actual inflation varies widely by country and period. Use 2.5–3% for long-range planning in most developed economies and higher where historical inflation has been higher."),
       ("Does inflation affect debt?","Yes — fixed-rate debt becomes cheaper in real terms as inflation rises, while savers earning below inflation lose purchasing power."),
       ("How do I protect against inflation?","Diversified investing, inflation-linked bonds where available and growing your income generally outpace inflation over long periods.")],
  guides=["compound-interest","index-funds-101","how-much-to-retire"]),
]
