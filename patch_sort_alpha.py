"""
Sort categories alphabetically:
1. budget.js  — sort CATEGORIES array + filter buttons sort at render time
2. budget.html — sort options within every optgroup alphabetically
"""

# ─────────────────────────────────────────────────────────
# 1. budget.js — sort CATEGORIES by label and sort filter buttons
# ─────────────────────────────────────────────────────────
with open('js/budget.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Sort filter button generation alphabetically
js = js.replace(
    "filterWrap.innerHTML =\n      `<button class=\"cat-filter-btn active\" data-cat=\"\" onclick=\"setFilter('')\">All</button>` +\n      CATEGORIES.map(c =>\n        `<button class=\"cat-filter-btn\" data-cat=\"${c.id}\" onclick=\"setFilter('${c.id}')\" style=\"border-color:${c.color};color:${c.color};\">${c.label}</button>`\n      ).join('');",
    "const sortedCats = [...CATEGORIES].sort((a,b) => a.label.localeCompare(b.label));\n    filterWrap.innerHTML =\n      `<button class=\"cat-filter-btn active\" data-cat=\"\" onclick=\"setFilter('')\">All</button>` +\n      sortedCats.map(c =>\n        `<button class=\"cat-filter-btn\" data-cat=\"${c.id}\" onclick=\"setFilter('${c.id}')\" style=\"border-color:${c.color};color:${c.color};\">${c.label}</button>`\n      ).join('');"
)

with open('js/budget.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('  ✓ budget.js filter buttons sorted alphabetically')

# ─────────────────────────────────────────────────────────
# 2. budget.html — sort options within each optgroup
# ─────────────────────────────────────────────────────────
with open('budget.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire category select with a sorted version
OLD_SELECT = '''      <select id="expCategory" required>
          <option value="">Select category...</option>
          <optgroup label="Construction">
            <option value="planning">Planning &amp; Permits</option>
            <option value="foundation">Foundation &amp; Soil Test</option>
            <option value="structure">Structure (Columns, Beams, Slab)</option>
            <option value="plumbing">Plumbing</option>
            <option value="electrical">Electrical</option>
            <option value="waterproofing">Waterproofing</option>
            <option value="windows">Windows &amp; Doors</option>
            <option value="flooring">Flooring &amp; Tiles</option>
            <option value="paint">Paint &amp; Plastering</option>
            <option value="kitchen">Kitchen &amp; Wardrobes</option>
            <option value="bathrooms">Bathrooms &amp; Fittings</option>
            <option value="interiors">Interiors &amp; Furniture</option>
            <option value="outdoor">Outdoor &amp; Garden</option>
          </optgroup>
          <optgroup label="People">
            <option value="labour">Labour &amp; Wages</option>
            <option value="professionals">Professional Fees (Architect, Engineer, Legal)</option>
          </optgroup>
          <optgroup label="Operational">
            <option value="travel">Travel &amp; Transport</option>
            <option value="food">Food &amp; Refreshments</option>
            <option value="equipment">Equipment &amp; Tool Rental</option>
            <option value="utilities">Site Utilities (Power/Water)</option>
          </optgroup>
          <optgroup label="Protection">
            <option value="insurance">Insurance</option>
            <option value="security">Security (CCTV/Locks/Gate)</option>
          </optgroup>
          <optgroup label="Admin &amp; Legal">
            <option value="legal">Legal &amp; Documentation</option>
            <option value="taxes">Taxes &amp; Government Fees</option>
          </optgroup>
          <optgroup label="Safety Net">
            <option value="contingency">Contingency / Emergency Fund</option>
            <option value="misc">Miscellaneous</option>
          </optgroup>
        </select>'''

NEW_SELECT = '''      <select id="expCategory" required>
          <option value="">Select category...</option>
          <optgroup label="Construction">
            <option value="bathrooms">Bathrooms &amp; Fittings</option>
            <option value="electrical">Electrical</option>
            <option value="flooring">Flooring &amp; Tiles</option>
            <option value="foundation">Foundation &amp; Soil Test</option>
            <option value="interiors">Interiors &amp; Furniture</option>
            <option value="kitchen">Kitchen &amp; Wardrobes</option>
            <option value="outdoor">Outdoor &amp; Garden</option>
            <option value="paint">Paint &amp; Plastering</option>
            <option value="planning">Planning &amp; Permits</option>
            <option value="plumbing">Plumbing</option>
            <option value="structure">Structure (Columns, Beams, Slab)</option>
            <option value="waterproofing">Waterproofing</option>
            <option value="windows">Windows &amp; Doors</option>
          </optgroup>
          <optgroup label="People">
            <option value="labour">Labour &amp; Wages</option>
            <option value="professionals">Professional Fees (Architect, Engineer, Legal)</option>
          </optgroup>
          <optgroup label="Operational">
            <option value="equipment">Equipment &amp; Tool Rental</option>
            <option value="food">Food &amp; Refreshments</option>
            <option value="utilities">Site Utilities (Power/Water)</option>
            <option value="travel">Travel &amp; Transport</option>
          </optgroup>
          <optgroup label="Protection">
            <option value="insurance">Insurance</option>
            <option value="security">Security (CCTV/Locks/Gate)</option>
          </optgroup>
          <optgroup label="Admin &amp; Legal">
            <option value="legal">Legal &amp; Documentation</option>
            <option value="taxes">Taxes &amp; Government Fees</option>
          </optgroup>
          <optgroup label="Safety Net">
            <option value="contingency">Contingency / Emergency Fund</option>
            <option value="misc">Miscellaneous</option>
          </optgroup>
        </select>'''

if OLD_SELECT in html:
    html = html.replace(OLD_SELECT, NEW_SELECT)
    print('  ✓ budget.html dropdown options sorted alphabetically within groups')
else:
    print('  ✗ dropdown not found — check whitespace')

with open('budget.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone.')
