import re

path = 'js/budget.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove doughnutChart variable and the entire renderPhaseChart function (old doughnut version)
# Replace with clean bars-only version
OLD = r'// ── Category chart \(doughnut \+ scaled bars\) ───────────────\nlet doughnutChart = null;\n\nfunction renderPhaseChart\(\) \{.*?\n\}'

NEW = '''// ── Category bars (scaled by value) ──────────────────────
function renderPhaseChart() {
  const chartEl = document.getElementById('phaseChart');
  if (!chartEl) return;

  const totals = {};
  expenses.forEach(e => { totals[e.category] = (totals[e.category] || 0) + (e.amountNPR || 0); });
  const active = CATEGORIES.filter(c => (totals[c.id] || 0) > 0);

  if (!active.length) {
    chartEl.innerHTML = '<p style="color:var(--muted);font-size:13.5px;">Add expenses to see the breakdown.</p>';
    return;
  }

  const totalSpent = active.reduce((s, c) => s + totals[c.id], 0);
  const maxVal     = Math.max(...active.map(c => totals[c.id]));

  chartEl.innerHTML = active
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
    }).join('');
}'''

result = re.sub(OLD, NEW, content, flags=re.DOTALL)
if result == content:
    print("Pattern not matched — trying line-based replacement")
    # fallback: find start and end lines
    lines = content.split('\n')
    start = next((i for i, l in enumerate(lines) if '// ── Category chart (doughnut' in l), None)
    end   = next((i for i in range(start+1, len(lines)) if lines[i] == '}' and i > start+5), None) if start else None
    if start and end:
        lines[start:end+1] = NEW.split('\n')
        result = '\n'.join(lines)
        print(f"Replaced lines {start}–{end}")
    else:
        print(f"Could not find section. start={start} end={end}")
else:
    print("Regex replacement succeeded")

with open(path, 'w', encoding='utf-8') as f:
    f.write(result)
