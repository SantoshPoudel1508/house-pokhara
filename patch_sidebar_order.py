import glob

# The OLD three lines (with class="" variant) that appear in most pages
OLD = (
    '  <a href="phase-3.html" class="" data-page="phase-3">'
    '<span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 3 — Plumbing</span>'
    '<span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" class="" data-page="phase-4">'
    '<span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 4 — Electrical</span>'
    '<span class="nav-check"></span></a>\n'
    '  <a href="phase-5.html" class="" data-page="phase-5">'
    '<span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 5 — Waterproofing</span>'
    '<span class="nav-check"></span></a>\n'
)
NEW = (
    '  <a href="phase-5.html" class="" data-page="phase-5">'
    '<span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 3 — Waterproofing</span>'
    '<span class="nav-check"></span></a>\n'
    '  <a href="phase-3.html" class="" data-page="phase-3">'
    '<span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 4 — Plumbing</span>'
    '<span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" class="" data-page="phase-4">'
    '<span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 5 — Electrical</span>'
    '<span class="nav-check"></span></a>\n'
)

updated = 0
for path in glob.glob('*.html'):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if OLD in c:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c.replace(OLD, NEW))
        print(f'  ✓ {path}')
        updated += 1

print(f'\n  Total: {updated} files updated')
