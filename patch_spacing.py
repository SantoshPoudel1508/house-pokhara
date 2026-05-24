path_css = 'css/style.css'
path_js  = 'js/budget.js'
path_html = 'budget.html'

# ── Read files ─────────────────────────────────────────────
with open(path_css,  'r', encoding='utf-8') as f: css  = f.read()
with open(path_js,   'r', encoding='utf-8') as f: js   = f.read()
with open(path_html, 'r', encoding='utf-8') as f: html = f.read()

# ══════════════════════════════════════════════════════════
# FIX 1 — Expense item redesign: equal spacing, clean rows
# ══════════════════════════════════════════════════════════
css = css.replace(
  '.expense-item { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; margin: 8px 0; display: flex; align-items: center; gap: 14px; box-shadow: var(--shadow-sm); transition: box-shadow .2s; }',
  '.expense-item { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border-bottom: 1px solid var(--border); transition: background .15s; }'
)
css = css.replace(
  '.expense-item:hover { box-shadow: var(--shadow-md); }',
  '.expense-item:hover { background: var(--accent-light); }\n.expense-item:last-child { border-bottom: none; }'
)

# ══════════════════════════════════════════════════════════
# FIX 2 — Nepal Standard Time (UTC+5:45) for expense date
# ══════════════════════════════════════════════════════════
js = js.replace(
  "function openModal()  { document.getElementById('expenseModal').classList.add('open'); document.getElementById('expDate').value = new Date().toISOString().split('T')[0]; }",
  """function getNPTDate() {
  // Nepal Standard Time = UTC + 5 hours 45 minutes
  const now    = new Date();
  const utcMs  = now.getTime() + now.getTimezoneOffset() * 60000;
  const nptMs  = utcMs + (5 * 60 + 45) * 60000;
  return new Date(nptMs).toISOString().split('T')[0];
}
function openModal()  {
  document.getElementById('expenseModal').classList.add('open');
  document.getElementById('expDate').value = getNPTDate();
}"""
)

# ══════════════════════════════════════════════════════════
# FIX 3 — Expense list container: equal padding all sides
# ══════════════════════════════════════════════════════════
html = html.replace(
  '''  <div id="expenseList" style="
    max-height: 600px;
    overflow-y: auto;
    scroll-behavior: smooth;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--card);
    box-shadow: var(--shadow-sm);
  ">''',
  '''  <div id="expenseList" style="
    max-height: 600px;
    overflow-y: auto;
    scroll-behavior: smooth;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--card);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    overflow-y: auto;
  ">'''
)

# ── Write files ────────────────────────────────────────────
with open(path_css,  'w', encoding='utf-8') as f: f.write(css)
with open(path_js,   'w', encoding='utf-8') as f: f.write(js)
with open(path_html, 'w', encoding='utf-8') as f: f.write(html)

checks = [
  ('expense-item clean rows',  'border-bottom: 1px solid var(--border)' in css),
  ('expense-item last-child',  'expense-item:last-child' in css),
  ('expense-item hover',       'expense-item:hover { background' in css),
  ('getNPTDate function',      'getNPTDate' in js),
  ('Nepal UTC+5:45',           '5 * 60 + 45' in js),
  ('openModal uses NPT',       'getNPTDate()' in js),
  ('container border-radius',  'border-radius: 14px' in html),
]
for name, ok in checks:
    print(f"  {'✓' if ok else '✗'} {name}")
