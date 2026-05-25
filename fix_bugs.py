import glob

def r(f):
    with open(f, encoding='utf-8') as x: return x.read()
def w(f, c):
    with open(f, 'w', encoding='utf-8') as x: x.write(c)

# ── FIX 1: Remove the duplicate hard-coded budget link from docs.html ──
# docs.html sidebar has budget hard-coded AND app.js injects it again
c = r('docs.html')
before = c.count('href="budget.html"')
# Remove the ONE hard-coded budget link from docs.html sidebar
# Keep only the active docs link — let app.js inject budget link
c = c.replace(
    '  <a href="budget.html"><span class="nav-icon">💰</span><span class="nav-label">Budget Tracker</span><span class="nav-check"></span></a>\n  <a href="docs.html" class="active">',
    '  <a href="docs.html" class="active">'
)
after = c.count('href="budget.html"')
w('docs.html', c)
print(f'docs.html: budget links {before} → {after}')

# ── FIX 2: Strengthen app.js guard so it never injects duplicates ──
c = r('js/app.js')
old = 'if (!sidebar || document.querySelector(\'.sidebar a[href="budget.html"]\')) return;'
new = 'if (!sidebar || sidebar.querySelector(\'a[href="budget.html"]\') || sidebar.querySelector(\'a[href="docs.html"]\')) return;'
if old in c:
    c = c.replace(old, new)
    w('js/app.js', c)
    print('app.js: guard updated (checks both budget + docs)')
else:
    print('app.js: guard already updated or pattern changed')

# ── FIX 3: Scan all pages for any remaining duplicates ──
print('\nDuplicate scan:')
clean = True
for f in sorted(glob.glob('*.html')):
    c = r(f)
    b = c.count('href="budget.html"')
    d = c.count('href="docs.html"')
    if b > 1 or d > 1:
        print(f'  ISSUE {f}: budget={b} docs={d}')
        clean = False
if clean:
    print('  All clean — no duplicates found')
