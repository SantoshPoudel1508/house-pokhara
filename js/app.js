
// ── SIDEBAR TOGGLE ──
function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('open');
  document.querySelector('.sidebar-overlay').classList.toggle('open');
}

// ── SECTION TOGGLE ──
function toggle(id) {
  document.getElementById(id).classList.toggle('open');
}
function openAll() { document.querySelectorAll('.sec').forEach(s => s.classList.add('open')); }
function closeAll() { document.querySelectorAll('.sec').forEach(s => s.classList.remove('open')); }

// ── CHECKLIST ──
function markDone(cb, id) {
  const item = document.getElementById(id);
  if (cb.checked) item.classList.add('done'); else item.classList.remove('done');
  localStorage.setItem('cb_' + id, cb.checked ? '1' : '0');
  refreshProgress();
  refreshSidebarBadges();
}

// ── COMMENTS ──
const saveTimers = {};
function saveComment(key, val) {
  clearTimeout(saveTimers[key]);
  saveTimers[key] = setTimeout(() => {
    localStorage.setItem('comment_' + key, val);
    const s = document.getElementById('saved_' + key);
    if (s) { s.style.display = 'block'; setTimeout(() => s.style.display = 'none', 2000); }
  }, 800);
}

// ── RESTORE ──
function restore() {
  document.querySelectorAll('.cl-item[id]').forEach(item => {
    if (localStorage.getItem('cb_' + item.id) === '1') {
      const cb = item.querySelector('input[type=checkbox]');
      if (cb) { cb.checked = true; item.classList.add('done'); }
    }
  });
  document.querySelectorAll('.comment-area textarea[id]').forEach(ta => {
    const saved = localStorage.getItem('comment_' + ta.id.replace('comment-',''));
    if (saved) ta.value = saved;
  });
}

// ── PROGRESS (this page) ──
function refreshProgress() {
  const all  = document.querySelectorAll('.cl-item input[type=checkbox]');
  const done = document.querySelectorAll('.cl-item input[type=checkbox]:checked');
  const pct  = all.length ? Math.round(done.length / all.length * 100) : 0;
  const fill = document.getElementById('progressBar');
  const text = document.getElementById('progressText');
  if (fill) fill.style.width = pct + '%';
  if (text) text.textContent = done.length + ' of ' + all.length + ' done';
  // store for home page
  const page = document.body.dataset.page;
  if (page) localStorage.setItem('pg_' + page, JSON.stringify({done: done.length, total: all.length}));
}

// ── SIDEBAR PHASE COMPLETION BADGES ──
function refreshSidebarBadges() {
  document.querySelectorAll('.sidebar a[data-page]').forEach(link => {
    const pg   = link.dataset.page;
    const data = JSON.parse(localStorage.getItem('pg_' + pg) || 'null');
    const badge = link.querySelector('.nav-check');
    if (!badge) return;
    if (data && data.total > 0 && data.done === data.total) {
      badge.textContent = '✓';
    } else if (data && data.done > 0) {
      badge.textContent = data.done + '/' + data.total;
    } else {
      badge.textContent = '';
    }
  });
}

// ── GLOBAL PROGRESS (for topbar, calculated from all pages) ──
function calcGlobalProgress() {
  const pages = ['phase-0','phase-1','phase-2','phase-3','phase-4','phase-5',
                 'phase-6','phase-7','phase-8','phase-9','phase-10','phase-11','phase-12',
                 'scams','questions'];
  let totalDone = 0, totalAll = 0;
  pages.forEach(p => {
    const d = JSON.parse(localStorage.getItem('pg_' + p) || 'null');
    if (d) { totalDone += d.done; totalAll += d.total; }
  });
  return { done: totalDone, total: totalAll };
}

// ── RESET ──
function resetAll() {
  if (!confirm('Reset ALL checkboxes and notes? This cannot be undone.')) return;
  localStorage.clear(); location.reload();
}

// ── INIT ──
window.addEventListener('DOMContentLoaded', () => {
  restore();
  refreshProgress();
  refreshSidebarBadges();
  // first section open
  const first = document.querySelector('.sec');
  if (first) first.classList.add('open');
  // sidebar overlay click
  const overlay = document.querySelector('.sidebar-overlay');
  if (overlay) overlay.addEventListener('click', toggleSidebar);
});
