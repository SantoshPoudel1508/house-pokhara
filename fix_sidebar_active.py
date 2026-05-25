"""Fix sidebar order in the 3 affected pages + redesign docs to use links (no Firebase Storage)"""

# ── Exact line templates ──────────────────────────────────
WP  = '  <a href="phase-5.html" {CLS} data-page="phase-5"><span class="nav-icon">🛡️</span><span class="nav-label">Phase 3 — Waterproofing</span><span class="nav-check"></span></a>\n'
PLM = '  <a href="phase-3.html" {CLS} data-page="phase-3"><span class="nav-icon">💧</span><span class="nav-label">Phase 4 — Plumbing</span><span class="nav-check"></span></a>\n'
ELC = '  <a href="phase-4.html" {CLS} data-page="phase-4"><span class="nav-icon">⚡</span><span class="nav-label">Phase 5 — Electrical</span><span class="nav-check"></span></a>\n'

def sidebar_block(wp_active=False, plm_active=False, elc_active=False):
    def cls(active): return 'class="active"' if active else 'class=""'
    return (
        WP.replace('{CLS}',  cls(wp_active))  +
        PLM.replace('{CLS}', cls(plm_active)) +
        ELC.replace('{CLS}', cls(elc_active))
    )

FIXES = [
    # (file, old_block, new_block)
    (
        'phase-5.html',  # Waterproofing — should be active
        (  # old: plumbing(no), electrical(no), waterproofing(ACTIVE) — wrong order + wrong labels
            '  <a href="phase-3.html" class="" data-page="phase-3"><span class="nav-icon">💧</span><span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-4.html" class="" data-page="phase-4"><span class="nav-icon">⚡</span><span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-5.html" class="active" data-page="phase-5"><span class="nav-icon">🛡️</span><span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n'
        ),
        sidebar_block(wp_active=True)   # waterproofing active, correct order
    ),
    (
        'phase-3.html',  # Plumbing — should be active
        (  # old: plumbing(ACTIVE), electrical(no), waterproofing(no) — wrong order + wrong labels
            '  <a href="phase-3.html" class="active" data-page="phase-3"><span class="nav-icon">💧</span><span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-4.html" class="" data-page="phase-4"><span class="nav-icon">⚡</span><span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-5.html" class="" data-page="phase-5"><span class="nav-icon">🛡️</span><span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n'
        ),
        sidebar_block(plm_active=True)  # plumbing active, correct order
    ),
    (
        'phase-4.html',  # Electrical — should be active
        (  # old: plumbing(no), electrical(ACTIVE), waterproofing(no) — wrong order + wrong labels
            '  <a href="phase-3.html" class="" data-page="phase-3"><span class="nav-icon">💧</span><span class="nav-label">Phase 3 — Plumbing</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-4.html" class="active" data-page="phase-4"><span class="nav-icon">⚡</span><span class="nav-label">Phase 4 — Electrical</span><span class="nav-check"></span></a>\n'
            '  <a href="phase-5.html" class="" data-page="phase-5"><span class="nav-icon">🛡️</span><span class="nav-label">Phase 5 — Waterproofing</span><span class="nav-check"></span></a>\n'
        ),
        sidebar_block(elc_active=True)  # electrical active, correct order
    ),
]

for fname, old, new in FIXES:
    with open(fname, 'r', encoding='utf-8') as f: c = f.read()
    if old in c:
        with open(fname, 'w', encoding='utf-8') as f: f.write(c.replace(old, new))
        print(f'  ✓ {fname} sidebar fixed')
    else:
        print(f'  ✗ {fname} — pattern not matched, showing actual content:')
        # show the three links for debug
        lines = [l for l in c.split('\n') if 'phase-3\|phase-4\|phase-5' in l or ('phase-' in l and 'nav-label' in l and ('Phase 3\|Phase 4\|Phase 5' in l))]
        for l in lines[:6]: print('    ', repr(l[:100]))
