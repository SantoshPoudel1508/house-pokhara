/* ══════════════════════════════════════════════════
   House Guide — App JS
   10 Themes · Checklist · Comments · Progress · Images
══════════════════════════════════════════════════ */

// ── 10 THEMES ───────────────────────────────────────
const THEMES = [
  { id:'ivory',    label:'Warm Ivory',     dot:'#C8702A', tip:'Warm Ivory & Terracotta — house wall colour' },
  { id:'sage',     label:'Sage Forest',    dot:'#3D7A50', tip:'Sage Forest — house garden/plant wall' },
  { id:'rose',     label:'Dusty Rose',     dot:'#A8685C', tip:'Dusty Rose — house blush pink palette' },
  { id:'wheat',    label:'Golden Wheat',   dot:'#C48A18', tip:'Golden Wheat — house warm amber tones' },
  { id:'stone',    label:'Stone Modern',   dot:'#4A6EA8', tip:'Stone Modern — house study/bathroom palette' },
  { id:'midnight', label:'Midnight Dark',  dot:'#E8934A', tip:'Midnight Dark — warm dark mode' },
  { id:'clay',     label:'Clay & Hemp',    dot:'#B46432', tip:'Clay & Hemp — earthy warm tones' },
  { id:'copper',   label:'Copper Glow',    dot:'#C46428', tip:'Copper Glow — rich metallic warmth' },
  { id:'ocean',    label:'Ocean Teal',     dot:'#208296', tip:'Ocean Teal — peacock blue-green' },
  { id:'lavender', label:'Lavender Mist',  dot:'#825AB4', tip:'Lavender Mist — soft purple/mauve' },
];

function applyTheme(id) {
  document.documentElement.setAttribute('data-theme', id);
  localStorage.setItem('hg_theme', id);
  document.querySelectorAll('.theme-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.theme === id)
  );
}

function injectThemeSwitcher() {
  const topbar = document.querySelector('.topbar');
  if (!topbar || document.querySelector('.theme-switcher')) return;
  const wrap = document.createElement('div');
  wrap.className = 'theme-switcher';
  wrap.innerHTML = `<span class="ts-label">Theme</span>` +
    THEMES.map(t => `<button class="theme-btn" data-theme="${t.id}" title="${t.tip}" style="background:${t.dot}"></button>`).join('');
  const printBtn = topbar.querySelector('.print-btn');
  printBtn ? topbar.insertBefore(wrap, printBtn) : topbar.appendChild(wrap);
  wrap.querySelectorAll('.theme-btn').forEach(btn =>
    btn.addEventListener('click', () => applyTheme(btn.dataset.theme))
  );
}

// ── SIDEBAR ──────────────────────────────────────────
function toggleSidebar() {
  document.querySelector('.sidebar')?.classList.toggle('open');
  document.querySelector('.sidebar-overlay')?.classList.toggle('open');
}

// Inject budget link into sidebar dynamically
function injectBudgetLink() {
  const sidebar = document.querySelector('.sidebar');
  if (!sidebar || document.querySelector('.sidebar a[href="budget.html"]')) return;
  const last = sidebar.querySelector('a:last-of-type');
  if (!last) return;
  // Add divider + budget link
  const div = document.createElement('div');
  div.className = 'divider';
  // Docs link
  const docsA = document.createElement('a');
  docsA.href = 'docs.html';
  if (window.location.pathname.endsWith('docs.html')) docsA.classList.add('active');
  docsA.innerHTML = `<span class="nav-icon">📁</span><span class="nav-label">Documents</span><span class="nav-check"></span>`;
  last.after(docsA);

  const a = document.createElement('a');
  a.href = 'budget.html';
  if (window.location.pathname.endsWith('budget.html')) a.classList.add('active');
  a.innerHTML = `<span class="nav-icon">💰</span><span class="nav-label">Budget Tracker</span><span class="nav-check"></span>`;
  last.after(div, a);
}

// ── SECTIONS ─────────────────────────────────────────
function toggle(id) { document.getElementById(id)?.classList.toggle('open'); }
function openAll()  { document.querySelectorAll('.sec').forEach(s => s.classList.add('open')); }
function closeAll() { document.querySelectorAll('.sec').forEach(s => s.classList.remove('open')); }

// ── CHECKLIST ─────────────────────────────────────────
function markDone(cb, id) {
  const item = document.getElementById(id);
  if (!item) return;
  item.classList.toggle('done', cb.checked);
  localStorage.setItem('hg_cb_' + id, cb.checked ? '1' : '0');
  refreshProgress();
  refreshSidebarBadges();
}

// ── COMMENTS ──────────────────────────────────────────
const _st = {};
function saveComment(key, val) {
  clearTimeout(_st[key]);
  _st[key] = setTimeout(() => {
    localStorage.setItem('hg_cmt_' + key, val);
    const s = document.getElementById('saved_' + key);
    if (s) { s.style.display = 'block'; setTimeout(() => s.style.display = 'none', 2000); }
  }, 700);
}

// ── PROGRESS ──────────────────────────────────────────
function refreshProgress() {
  const all  = document.querySelectorAll('.cl-item input[type=checkbox]');
  const done = [...all].filter(c => c.checked);
  const pct  = all.length ? Math.round(done.length / all.length * 100) : 0;
  const fill = document.getElementById('progressBar');
  const text = document.getElementById('progressText');
  if (fill) fill.style.width = pct + '%';
  if (text) text.textContent = done.length + ' of ' + all.length + ' done';
  const page = document.body.dataset.page;
  if (page) localStorage.setItem('hg_pg_' + page, JSON.stringify({ done: done.length, total: all.length }));
}

function refreshSidebarBadges() {
  document.querySelectorAll('.sidebar a[data-page]').forEach(link => {
    const data  = JSON.parse(localStorage.getItem('hg_pg_' + link.dataset.page) || 'null');
    const badge = link.querySelector('.nav-check');
    if (!badge) return;
    if (data?.total > 0 && data.done === data.total)   badge.textContent = '✓';
    else if (data?.done > 0) badge.textContent = data.done + '/' + data.total;
    else badge.textContent = '';
  });
}

// ── RESTORE ───────────────────────────────────────────
function restore() {
  document.querySelectorAll('.cl-item[id]').forEach(item => {
    if (localStorage.getItem('hg_cb_' + item.id) === '1') {
      const cb = item.querySelector('input[type=checkbox]');
      if (cb) { cb.checked = true; item.classList.add('done'); }
    }
  });
  document.querySelectorAll('.comment-area textarea[id]').forEach(ta => {
    const saved = localStorage.getItem('hg_cmt_' + ta.id.replace('comment-', ''));
    if (saved) ta.value = saved;
  });
}

// ── RESET ─────────────────────────────────────────────
function resetAll() {
  if (!confirm('Reset ALL checkboxes and notes? This cannot be undone.')) return;
  Object.keys(localStorage).filter(k => k.startsWith('hg_')).forEach(k => localStorage.removeItem(k));
  location.reload();
}

// ── HOME DASHBOARD ────────────────────────────────────
function loadHomeDashboard() {
  const pages = ['phase-0','phase-1','phase-2','phase-3','phase-4','phase-5',
                 'phase-6','phase-7','phase-8','phase-9','phase-10','phase-11',
                 'phase-12','scams','questions'];
  pages.forEach(p => {
    const data = JSON.parse(localStorage.getItem('hg_pg_' + p) || 'null');
    const bar  = document.getElementById('pcbar-' + p);
    const cnt  = document.getElementById('pccount-' + p);
    if (!data || data.total === 0) { if (cnt) cnt.textContent = 'Not started yet'; return; }
    const pct = Math.round(data.done / data.total * 100);
    if (bar) bar.style.width = pct + '%';
    if (cnt) cnt.textContent = data.done + ' of ' + data.total + ' done (' + pct + '%)';
  });
}

// ── CONCEPT IMAGES ────────────────────────────────────
const IMG_MAP = {
  foundation:  'photo-1504307651254-35680f356dfd',
  concrete:    'photo-1590856029826-c7a73142bbf1',
  kitchen:     'photo-1556909114-f6e7ad7d3136',
  bathroom:    'photo-1552321554-5fefe8c9ef14',
  tiles:       'photo-1584622650111-993a426fbf0a',
  windows:     'photo-1558036117-15d82a90b9b1',
  painting:    'photo-1562259949-e8e7689d7828',
  electrical:  'photo-1558618047-3c8c76ca7d13',
  entrance:    'photo-1600585154340-be6161a56a0c',
  garden:      'photo-1416879595882-3373a0480b5b',
  wardrobe:    'photo-1558769132-cb1aea458c5e',
  exterior:    'photo-1568605114967-8130f3a36994',
  interiors:   'photo-1586023492125-27b2c045efd7',
  plumbing:    'photo-1607400201515-c2c41c3cf3fa',
};
function loadConceptImages() {
  document.querySelectorAll('.concept-img[data-img]').forEach(div => {
    const id = IMG_MAP[div.dataset.img];
    if (!id) return;
    const url = `https://images.unsplash.com/${id}?w=800&q=75&auto=format&fit=crop`;
    const img = new Image();
    img.onload = () => { div.style.backgroundImage = `url('${url}')`; };
    img.src = url;
  });
}

// ── INIT ──────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  // Theme
  injectThemeSwitcher();
  applyTheme(localStorage.getItem('hg_theme') || 'ivory');
  // Sidebar
  document.querySelector('.sidebar-overlay')?.addEventListener('click', toggleSidebar);
  injectBudgetLink();
  // State
  restore();
  refreshProgress();
  refreshSidebarBadges();
  // Open ALL sections by default so every section is visible without clicking
  document.querySelectorAll('.sec').forEach(s => s.classList.add('open'));
  // Images
  loadConceptImages();
  // Home
  if (document.body.dataset.page === '') loadHomeDashboard();
});
