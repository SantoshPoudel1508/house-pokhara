with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

OLD_CSS = (
    '.expense-actions button { background: none; border: none; cursor: pointer; color: var(--muted); '
    'padding: 4px 8px; border-radius: 6px; font-size: 14px; transition: all .15s; }\n'
    '.expense-actions button:hover { background: var(--red-light); color: var(--red); }'
)
NEW_CSS = (
    '.expense-actions { display:flex; gap:4px; align-items:center; }\n'
    '.expense-actions button {\n'
    '  background: none; border: none; cursor: pointer;\n'
    '  width: 34px; height: 34px; border-radius: 8px;\n'
    '  font-size: 17px; opacity: .40;\n'
    '  display: flex; align-items: center; justify-content: center;\n'
    '  transition: all .18s ease; flex-shrink: 0;\n'
    '}\n'
    '.expense-actions button:hover { opacity: 1; transform: scale(1.18); }\n'
    '.expense-actions .btn-edit:hover   { background: var(--accent-light); }\n'
    '.expense-actions .btn-delete:hover { background: var(--red-light); }'
)

if OLD_CSS in css:
    css = css.replace(OLD_CSS, NEW_CSS)
    print('  ✓ CSS updated')
else:
    print('  ✗ CSS pattern not found')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# ── JS: add btn-edit / btn-delete classes ─────────────────
with open('js/budget.js', 'r', encoding='utf-8') as f:
    js = f.read()

OLD_JS = (
    '          <button onclick="editExpense(\'${e.id}\')" '
    'title="Edit expense" style="color:var(--accent-dark);">✏️</button>\n'
    '          <button onclick="deleteExpense(\'${e.id}\')" '
    'title="Delete expense">🗑</button>'
)
NEW_JS = (
    '          <button class="btn-edit"   onclick="editExpense(\'${e.id}\')"   title="Edit">✏️</button>\n'
    '          <button class="btn-delete" onclick="deleteExpense(\'${e.id}\')" title="Delete">🗑</button>'
)

if OLD_JS in js:
    js = js.replace(OLD_JS, NEW_JS)
    print('  ✓ JS updated')
else:
    print('  ✗ JS pattern not found — trying partial match')
    # Debug: show what the buttons look like
    import re
    matches = re.findall(r'<button[^>]*editExpense[^<]*</button>', js)
    for m in matches[:3]:
        print('    found:', repr(m[:80]))

with open('js/budget.js', 'w', encoding='utf-8') as f:
    f.write(js)
