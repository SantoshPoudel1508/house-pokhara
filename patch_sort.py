import re

path = 'js/budget.js'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# ── FIX 1: Add sort state before activeFilter ──────────────────────────
OLD_FILTER = "let activeFilter = '';"
NEW_FILTER = """let activeFilter = '';
let sortMode = 'date-desc'; // date-desc | date-asc | amount-desc | amount-asc | category

function setSort(mode) {
  sortMode = mode;
  document.querySelectorAll('.sort-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.sort === mode)
  );
  renderExpenses();
}

function sortExpenses(items) {
  const arr = [...items];
  switch (sortMode) {
    case 'date-desc':   return arr.sort((a,b) => (b.date||'').localeCompare(a.date||''));
    case 'date-asc':    return arr.sort((a,b) => (a.date||'').localeCompare(b.date||''));
    case 'amount-desc': return arr.sort((a,b) => (b.amountNPR||0) - (a.amountNPR||0));
    case 'amount-asc':  return arr.sort((a,b) => (a.amountNPR||0) - (b.amountNPR||0));
    case 'category':    return arr.sort((a,b) => (a.category||'').localeCompare(b.category||''));
    default:            return arr;
  }
}"""

c = c.replace(OLD_FILTER, NEW_FILTER)

# ── FIX 2: Use sortExpenses in renderExpenses ──────────────────────────
c = c.replace(
  "  const items = activeFilter ? expenses.filter(e => e.category === activeFilter) : expenses;",
  "  const raw   = activeFilter ? expenses.filter(e => e.category === activeFilter) : expenses;\n  const items = sortExpenses(raw);"
)

# ── FIX 3: Fix renderPhaseChart — show % outside bar for ALL bars ──────
OLD_CHART = '''chartEl.innerHTML = active
    .sort((a, b) => totals[b.id] - totals[a.id])  // biggest first
    .map(c => {
      const val   = totals[c.id];
      const barW  = Math.round(val / maxVal * 100);  // scaled to biggest = 100%
      const share = Math.round(val / totalSpent * 100);
      const disp  = `${sym(viewCurrency)} ${fmt(val, viewCurrency)}`;
      return `
        <div style="margin:14px 0;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <span style="font-size:13px;color:var(--text-soft);display:flex;align-items:center;gap:7px;">
              <span style="width:10px;height:10px;border-radius:3px;background:${c.color};display:inline-block;flex-shrink:0;"></span>
              ${c.label}
            </span>
            <span style="font-size:13px;font-weight:700;color:var(--text);">${disp} <span style="font-size:11px;font-weight:600;color:var(--muted);">(${share}%)</span></span>
          </div>
          <div style="background:var(--border);border-radius:20px;height:12px;overflow:hidden;">
            <div style="
              width:${barW}%;
              height:12px;
              border-radius:20px;
              background:${c.color};
              transition:width .7s cubic-bezier(.4,0,.2,1);
              min-width:${val > 0 ? '6px' : '0'};
            "></div>
          </div>
        </div>`;
    }).join('');'''

NEW_CHART = '''chartEl.innerHTML = active
    .sort((a, b) => totals[b.id] - totals[a.id])
    .map(c => {
      const val   = totals[c.id];
      const barW  = Math.round(val / maxVal * 100);
      const share = Math.round(val / totalSpent * 100);
      const disp  = `${sym(viewCurrency)} ${fmt(val, viewCurrency)}`;
      return `
        <div style="margin:16px 0;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;gap:8px;">
            <span style="font-size:13px;color:var(--text-soft);display:flex;align-items:center;gap:7px;min-width:0;flex:1;">
              <span style="width:10px;height:10px;border-radius:3px;background:${c.color};display:inline-block;flex-shrink:0;"></span>
              <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${c.label}</span>
            </span>
            <span style="font-size:13px;font-weight:700;color:var(--text);white-space:nowrap;flex-shrink:0;">
              ${disp}
            </span>
            <span style="font-size:12px;font-weight:700;color:var(--accent-dark);white-space:nowrap;flex-shrink:0;min-width:36px;text-align:right;">
              ${share}%
            </span>
          </div>
          <div style="background:var(--border);border-radius:20px;height:11px;overflow:hidden;">
            <div style="
              width:${barW}%;
              height:11px;
              border-radius:20px;
              background:${c.color};
              transition:width .7s cubic-bezier(.4,0,.2,1);
              min-width:${val > 0 ? '4px' : '0'};
            "></div>
          </div>
        </div>`;
    }).join('');'''

c = c.replace(OLD_CHART, NEW_CHART)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

checks = [
  ('sort state', 'let sortMode' in c),
  ('setSort fn', 'function setSort' in c),
  ('sortExpenses', 'function sortExpenses' in c),
  ('renderExpenses uses sort', 'sortExpenses(raw)' in c),
  ('chart % always visible', 'text-align:right' in c),
]
for name, ok in checks:
    print(f"  {'✓' if ok else '✗'} {name}")
