"""
Correct construction phase order:
  WRONG: Structure → Plumbing → Electrical → Waterproofing → Windows
  RIGHT: Structure → Waterproofing → Plumbing → Electrical → Windows

Changes:
  1. Sidebar in ALL html files: swap order + renumber labels
  2. phase-2.html next button
  3. phase-5.html: tag "Phase 3", prev=2, next=phase-3
  4. phase-3.html: tag "Phase 4", prev=phase-5, next=4
  5. phase-4.html: tag "Phase 5", prev=phase-3, next=6
  6. phase-6.html: prev label update
"""
import glob

# ── Helper ─────────────────────────────────────────────────
def patch(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if old in c:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c.replace(old, new))
        return True
    return False

# ── 1. Sidebar reorder in ALL html files ──────────────────
# The three links appear in every sidebar in this exact order.
# We need to handle two variants: active class and empty class.
# The active class can be on any of the three links depending on which page we're on.

SIDEBAR_OLD = (
  '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
  '<span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
  '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
  '<span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
  '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
  '<span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n'
)
SIDEBAR_NEW = (
  '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
  '<span class="nav-label">Phase 3 — Waterproofing</span><span class="nav-check"></span></a>\n'
  '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
  '<span class="nav-label">Phase 4 — Plumbing</span><span class="nav-check"></span></a>\n'
  '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
  '<span class="nav-label">Phase 5 — Electrical</span><span class="nav-check"></span></a>\n'
)

# Also handle active variants (when one of the three IS the current page)
ACTIVE_VARIANTS = [
  # phase-5 active (current page is waterproofing)
  (
    '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-5.html" class="active" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n',
    '  <a href="phase-5.html" class="active" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 3 — Waterproofing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 4 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 5 — Electrical</span><span class="nav-check"></span></a>\n'
  ),
  # phase-3 active (current page is plumbing)
  (
    '  <a href="phase-3.html" class="active" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n',
    '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 3 — Waterproofing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-3.html" class="active" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 4 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 5 — Electrical</span><span class="nav-check"></span></a>\n'
  ),
  # phase-4 active (current page is electrical)
  (
    '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" class="active" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n',
    '  <a href="phase-5.html" data-page="phase-5"><span class="nav-icon">🛡️</span>'
    '<span class="nav-label">Phase 3 — Waterproofing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-3.html" data-page="phase-3"><span class="nav-icon">💧</span>'
    '<span class="nav-label">Phase 4 — Plumbing</span><span class="nav-check"></span></a>\n'
    '  <a href="phase-4.html" class="active" data-page="phase-4"><span class="nav-icon">⚡</span>'
    '<span class="nav-label">Phase 5 — Electrical</span><span class="nav-check"></span></a>\n'
  ),
]

sidebar_updated = 0
for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()

    changed = False
    # Try standard (no active)
    if SIDEBAR_OLD in c:
        c = c.replace(SIDEBAR_OLD, SIDEBAR_NEW)
        changed = True
    else:
        # Try active variants
        for old_v, new_v in ACTIVE_VARIANTS:
            if old_v in c:
                c = c.replace(old_v, new_v)
                changed = True
                break

    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(c)
        sidebar_updated += 1

print(f'  ✓ Sidebar reordered in {sidebar_updated} files')

# ── 2. phase-2.html: next → Waterproofing ─────────────────
ok = patch('phase-2.html',
  '<a class="nav-btn next" href="phase-3.html">Phase 3: Plumbing → &rarr;</a>',
  '<a class="nav-btn next" href="phase-5.html">Phase 3: Waterproofing → &rarr;</a>'
)
print(f'  {"✓" if ok else "✗"} phase-2.html next button updated')

# ── 3. phase-5.html: renumber + fix nav ───────────────────
p = 'phase-5.html'
ok1 = patch(p, '<div class="phase-tag">Phase 5</div>', '<div class="phase-tag">Phase 3</div>')
ok2 = patch(p, '<title>Phase 5 — Waterproofing', '<title>Phase 3 — Waterproofing')
ok3 = patch(p, '<h1>Phase 5 — Waterproofing', '<h1>Phase 3 — Waterproofing')
ok4 = patch(p, '<a class="nav-btn" href="phase-4.html">&larr; ← Phase 4</a>', '<a class="nav-btn" href="phase-2.html">&larr; ← Phase 2</a>')
ok5 = patch(p, '<a class="nav-btn next" href="phase-6.html">Phase 6: Windows → &rarr;</a>', '<a class="nav-btn next" href="phase-3.html">Phase 4: Plumbing → &rarr;</a>')
print(f'  {"✓" if all([ok1,ok2,ok3,ok4,ok5]) else "✗"} phase-5.html updated (tag+title+h1+prev+next)')

# ── 4. phase-3.html: renumber + fix nav ───────────────────
p = 'phase-3.html'
ok1 = patch(p, '<div class="phase-tag">Phase 3</div>', '<div class="phase-tag">Phase 4</div>')
ok2 = patch(p, '<title>Phase 3 — Plumbing', '<title>Phase 4 — Plumbing')
ok3 = patch(p, '<h1>Phase 3 — Plumbing', '<h1>Phase 4 — Plumbing')
ok4 = patch(p, '<a class="nav-btn" href="phase-2.html">&larr; ← Phase 2</a>', '<a class="nav-btn" href="phase-5.html">&larr; ← Phase 3: Waterproofing</a>')
ok5 = patch(p, '<a class="nav-btn next" href="phase-4.html">Phase 4: Electrical → &rarr;</a>', '<a class="nav-btn next" href="phase-4.html">Phase 5: Electrical → &rarr;</a>')
print(f'  {"✓" if all([ok1,ok2,ok3,ok4,ok5]) else "✗"} phase-3.html updated (tag+title+h1+prev+next)')

# ── 5. phase-4.html: renumber + fix nav ───────────────────
p = 'phase-4.html'
ok1 = patch(p, '<div class="phase-tag">Phase 4</div>', '<div class="phase-tag">Phase 5</div>')
ok2 = patch(p, '<title>Phase 4 — Electrical', '<title>Phase 5 — Electrical')
ok3 = patch(p, '<h1>Phase 4 — Electrical', '<h1>Phase 5 — Electrical')
ok4 = patch(p, '<a class="nav-btn" href="phase-3.html">&larr; ← Phase 3</a>', '<a class="nav-btn" href="phase-3.html">&larr; ← Phase 4: Plumbing</a>')
ok5 = patch(p, '<a class="nav-btn next" href="phase-5.html">Phase 5: Waterproofing → &rarr;</a>', '<a class="nav-btn next" href="phase-6.html">Phase 6: Windows → &rarr;</a>')
print(f'  {"✓" if all([ok1,ok2,ok3,ok4,ok5]) else "✗"} phase-4.html updated (tag+title+h1+prev+next)')

# ── 6. phase-6.html: prev label only ─────────────────────
ok = patch('phase-6.html',
  '<a class="nav-btn" href="phase-5.html">&larr; ← Phase 5</a>',
  '<a class="nav-btn" href="phase-4.html">&larr; ← Phase 5: Electrical</a>'
)
print(f'  {"✓" if ok else "✗"} phase-6.html prev button updated')

print('\nDone. Correct order: 0→1→2→Waterproofing→Plumbing→Electrical→6→7→8→9→10→11→12')
