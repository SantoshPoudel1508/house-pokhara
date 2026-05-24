"""Fix nav labels + inject docs link + create docs page"""
import glob

with open('js/app.js', 'r', encoding='utf-8') as f: app = f.read()

# Inject docs link into sidebar (after budget link)
if 'docs.html' not in app:
    app = app.replace(
        "  const a = document.createElement('a');\n  a.href = 'budget.html';",
        """  // Docs link
  const docsA = document.createElement('a');
  docsA.href = 'docs.html';
  if (window.location.pathname.endsWith('docs.html')) docsA.classList.add('active');
  docsA.innerHTML = `<span class="nav-icon">📁</span><span class="nav-label">Documents</span><span class="nav-check"></span>`;
  last.after(docsA);

  const a = document.createElement('a');
  a.href = 'budget.html';"""
    )
    with open('js/app.js', 'w', encoding='utf-8') as f: f.write(app)
    print('  ✓ Docs link injected into sidebar')
else:
    print('  ✓ Docs link already in sidebar')

# Fix nav labels — add names to all prev/next buttons
FIXES = [
    # (file, old_text, new_text)
    ('phase-1.html', '← Phase 0</a>', '← Phase 0: Planning</a>'),
    ('phase-2.html', '← Phase 1</a>', '← Phase 1: Foundation</a>'),
    ('phase-5.html', '← Phase 2</a>', '← Phase 2: Structure</a>'),
    ('phase-7.html', '← Phase 6</a>', '← Phase 6: Windows &amp; Doors</a>'),
    ('phase-8.html', '← Phase 7</a>', '← Phase 7: Flooring</a>'),
    ('phase-9.html', '← Phase 8</a>', '← Phase 8: Paint</a>'),
    ('phase-10.html', '← Phase 9</a>', '← Phase 9: Kitchen</a>'),
    ('phase-11.html', '← Phase 10</a>', '← Phase 10: Bathrooms</a>'),
    ('phase-12.html', '← Phase 11</a>', '← Phase 11: Interiors</a>'),
    ('scams.html',    '← Phase 12</a>', '← Phase 12: Outdoor</a>'),
]
nav_fixed = 0
for fname, old, new in FIXES:
    try:
        with open(fname, 'r', encoding='utf-8') as f: c = f.read()
        if old in c:
            with open(fname, 'w', encoding='utf-8') as f: f.write(c.replace(old, new))
            print(f'  ✓ {fname} — nav label updated')
            nav_fixed += 1
    except FileNotFoundError:
        print(f'  ? {fname} not found')

print(f'\n  {nav_fixed} nav labels updated')
