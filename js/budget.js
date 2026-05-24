/* ══════════════════════════════════════════════════════════
   BUDGET TRACKER — Private (login required to view anything)
   Only ALLOWED_EDITORS can see and interact with budget data.
══════════════════════════════════════════════════════════ */

// ── State ─────────────────────────────────────────────────
let db, auth, currentUser = null;
let expenses = [];
let viewCurrency = 'NPR';
let conversionRate = DEFAULT_INR_TO_NPR;
let totalBudgetNPR = 0;
let isEditor = false;
let unsubscribeExpenses = null;
let unsubscribeSettings = null;

// ── Categories ────────────────────────────────────────────
const CATEGORIES = [
  // ── Construction Phases ──
  { id:'planning',      label:'Planning & Permits',        color:'#5A7EB8' },
  { id:'foundation',    label:'Foundation & Soil',         color:'#8C4A22' },
  { id:'structure',     label:'Structure (Columns/Beams)', color:'#3A6248' },
  { id:'plumbing',      label:'Plumbing',                  color:'#208296' },
  { id:'electrical',    label:'Electrical',                color:'#C48A18' },
  { id:'waterproofing', label:'Waterproofing',             color:'#1E3040' },
  { id:'windows',       label:'Windows & Doors',           color:'#2D5C3C' },
  { id:'flooring',      label:'Flooring & Tiles',          color:'#7A5A18' },
  { id:'paint',         label:'Paint & Plastering',        color:'#643A96' },
  { id:'kitchen',       label:'Kitchen & Wardrobes',       color:'#C8702A' },
  { id:'bathrooms',     label:'Bathrooms & Fittings',      color:'#4A8A5A' },
  { id:'interiors',     label:'Interiors & Furniture',     color:'#A8685C' },
  { id:'outdoor',       label:'Outdoor & Garden',          color:'#3D7A50' },
  // ── People ──
  { id:'labour',        label:'Labour & Wages',            color:'#7A3828' },
  { id:'professionals', label:'Professional Fees',         color:'#4A5A8A' },
  // ── Operational ──
  { id:'travel',        label:'Travel & Transport',        color:'#2E7DAF' },
  { id:'food',          label:'Food & Refreshments',       color:'#D97706' },
  { id:'equipment',     label:'Equipment & Tool Rental',   color:'#6B7280' },
  { id:'utilities',     label:'Site Utilities (Power/Water)', color:'#0891B2' },
  // ── Protection ──
  { id:'insurance',     label:'Insurance',                 color:'#059669' },
  { id:'security',      label:'Security (CCTV/Locks)',     color:'#374151' },
  // ── Admin & Legal ──
  { id:'legal',         label:'Legal & Documentation',     color:'#7C3AED' },
  { id:'taxes',         label:'Taxes & Government Fees',   color:'#B45309' },
  // ── Safety Net ──
  { id:'contingency',   label:'Contingency / Emergency',   color:'#DC2626' },
  { id:'misc',          label:'Miscellaneous',             color:'#78716C' },
];
function catById(id) { return CATEGORIES.find(c => c.id === id) || CATEGORIES[CATEGORIES.length - 1]; }

// ── Currency helpers ───────────────────────────────────────
function toNPR(amount, currency) { return currency === 'INR' ? amount * conversionRate : amount; }
function toINR(amountNPR)        { return amountNPR / conversionRate; }
function fmt(amountNPR, currency) {
  const val = currency === 'NPR' ? amountNPR : toINR(amountNPR);
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(val);
}
function sym(currency) { return currency === 'NPR' ? 'NPR' : '₹'; }

// ── Show / hide screens ────────────────────────────────────
function showLoginWall(reason) {
  document.getElementById('loginWall').style.display    = 'flex';
  document.getElementById('budgetContent').style.display = 'none';
  document.getElementById('accessDenied').style.display  = 'none';
  if (reason === 'denied') {
    document.getElementById('loginWall').style.display   = 'none';
    document.getElementById('accessDenied').style.display = 'flex';
  }
}
function showBudgetContent() {
  document.getElementById('loginWall').style.display    = 'none';
  document.getElementById('accessDenied').style.display  = 'none';
  document.getElementById('budgetContent').style.display = 'block';
}

// ── Firebase init ──────────────────────────────────────────
function initFirebase() {
  if (!IS_FIREBASE_READY) {
    showSetupGuide();
    return;
  }
  try {
    firebase.initializeApp(FIREBASE_CONFIG);
    db   = firebase.firestore();
    auth = firebase.auth();

    auth.onAuthStateChanged(user => {
      currentUser = user;

      if (!user) {
        // Not logged in — show login wall
        isEditor = false;
        showLoginWall();
        if (unsubscribeExpenses) { unsubscribeExpenses(); unsubscribeExpenses = null; }
        return;
      }

      // Logged in — check if email is allowed
      if (!ALLOWED_EDITORS.includes(user.email)) {
        // Unknown email — deny access
        isEditor = false;
        showLoginWall('denied');
        return;
      }

      // ✅ Authorised user — show everything
      isEditor = true;
      showBudgetContent();
      renderUserBar();
      startSettingsListener();
      startExpensesListener();
    });
  } catch (e) {
    console.error('Firebase init error:', e);
    showSetupGuide();
  }
}

// ── Auth ───────────────────────────────────────────────────
function signInGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider).catch(err => {
    alert('Login failed: ' + err.message);
  });
}
function signOut() {
  if (unsubscribeExpenses) { unsubscribeExpenses(); unsubscribeExpenses = null; }
  if (unsubscribeSettings) { unsubscribeSettings(); unsubscribeSettings = null; }
  auth.signOut();
}

function renderUserBar() {
  const bar = document.getElementById('userBar');
  if (!bar || !currentUser) return;
  bar.innerHTML = `
    <div class="user-info">
      <div class="user-avatar">
        ${currentUser.photoURL
          ? `<img src="${currentUser.photoURL}" referrerpolicy="no-referrer"/>`
          : '👤'}
      </div>
      <span class="user-name">${currentUser.displayName || currentUser.email}</span>
      <span style="background:var(--accent);color:#fff;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:700;">Editor</span>
      <button class="logout-btn" onclick="signOut()" title="Sign out">Sign out</button>
    </div>`;
}

// ── Real-time settings listener (2-way binding) ────────────
function startSettingsListener() {
  if (unsubscribeSettings) { unsubscribeSettings(); }
  setLiveStatus('connecting');
  unsubscribeSettings = db.collection('settings').doc('main')
    .onSnapshot(doc => {
      if (doc.exists) {
        const d = doc.data();
        totalBudgetNPR = d.totalBudgetNPR || 0;
        conversionRate  = d.conversionRate  || DEFAULT_INR_TO_NPR;
        const rateEl = document.getElementById('rateDisplay');
        if (rateEl) rateEl.textContent = `1 INR = ${conversionRate.toFixed(2)} NPR`;
      }
      renderStats();
      setLiveStatus('live');
    }, err => {
      console.error('Settings listener error:', err);
      setLiveStatus('error');
    });
}

// ── Real-time expenses listener (2-way binding) ────────────
function startExpensesListener() {
  if (unsubscribeExpenses) { unsubscribeExpenses(); }
  unsubscribeExpenses = db.collection('expenses')
    .orderBy('date', 'desc')
    .onSnapshot(snap => {
      expenses = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderStats();
      renderExpenses();
      renderPhaseChart();
      setLiveStatus('live');
    }, err => {
      console.error('Expenses listener error:', err);
      setLiveStatus('error');
    });
}

// ── Live status dot ────────────────────────────────────────
function setLiveStatus(state) {
  const el = document.getElementById('liveStatus');
  if (!el) return;
  const cfg = {
    connecting: { color:'#f59e0b', label:'Connecting...',  anim:false },
    live:       { color:'#22c55e', label:'Live',            anim:true  },
    error:      { color:'#ef4444', label:'Offline',         anim:false },
  }[state] || { color:'#22c55e', label:'Live', anim:true };
  el.innerHTML = `<span style="display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:var(--muted);">
    <span style="width:7px;height:7px;border-radius:50%;background:${cfg.color};display:inline-block;${cfg.anim?'animation:livePulse 2s ease-in-out infinite;':''}"></span>
    ${cfg.label}
  </span>`;
}

// ── Stats ──────────────────────────────────────────────────
function renderStats() {
  const totalSpentNPR = expenses.reduce((s, e) => s + (e.amountNPR || 0), 0);
  const remaining     = totalBudgetNPR - totalSpentNPR;
  const pct           = totalBudgetNPR > 0 ? Math.min(100, Math.round(totalSpentNPR / totalBudgetNPR * 100)) : 0;

  const el = id => document.getElementById(id);
  if (!el('statBudget')) return;

  el('statBudget').textContent    = totalBudgetNPR ? `${sym(viewCurrency)} ${fmt(totalBudgetNPR, viewCurrency)}` : 'Not set yet';
  el('statSpent').textContent     = `${sym(viewCurrency)} ${fmt(totalSpentNPR, viewCurrency)}`;
  el('statRemaining').textContent = totalBudgetNPR ? `${sym(viewCurrency)} ${fmt(remaining, viewCurrency)}` : '—';
  el('statPct').textContent       = totalBudgetNPR ? `${pct}% used` : '—';

  const spentBar = el('spentBar');
  if (spentBar) spentBar.style.width = pct + '%';

  const remCard = el('statRemaining')?.closest?.('.bstat');
  if (remCard) remCard.className = 'bstat ' + (remaining < 0 ? 'warn-stat' : 'good-stat');
}

// ── Expense list ───────────────────────────────────────────
let activeFilter = '';
function renderExpenses() {
  const list = document.getElementById('expenseList');
  if (!list) return;
  const items = activeFilter ? expenses.filter(e => e.category === activeFilter) : expenses;
  if (!items.length) {
    list.innerHTML = `<div class="empty-state"><div class="es-icon">💸</div><h3>No expenses yet${activeFilter ? ' in this category' : ''}</h3><p>Click "Add Expense" to record your first construction cost.</p></div>`;
    return;
  }
  list.innerHTML = items.map(e => {
    const cat = catById(e.category);
    const amt = viewCurrency === 'NPR' ? e.amountNPR : toINR(e.amountNPR);
    return `
      <div class="expense-item">
        <div class="expense-cat-dot" style="background:${cat.color}"></div>
        <div class="expense-info">
          <div class="expense-desc">${e.description || 'Expense'}</div>
          <div class="expense-meta">${cat.label} · ${e.date || ''} · ${e.addedByName || e.addedBy || ''}</div>
        </div>
        <div class="expense-amount">${sym(viewCurrency)} ${new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(amt)}</div>
        <div class="expense-actions">
          <button onclick="deleteExpense('${e.id}')" title="Delete expense">🗑</button>
        </div>
      </div>`;
  }).join('');
}

// ── Category chart (doughnut + scaled bars) ───────────────
let doughnutChart = null;

function renderPhaseChart() {
  const chartEl  = document.getElementById('phaseChart');
  const canvas   = document.getElementById('doughnutChart');
  const legendEl = document.getElementById('chartLegend');
  if (!chartEl || !canvas) return;

  // Calculate totals per category (only non-zero)
  const totals = {};
  expenses.forEach(e => { totals[e.category] = (totals[e.category] || 0) + (e.amountNPR || 0); });
  const active = CATEGORIES.filter(c => (totals[c.id] || 0) > 0);

  if (active.length === 0) {
    chartEl.innerHTML = '<p style="color:var(--muted);font-size:13.5px;">Add expenses to see the breakdown.</p>';
    if (doughnutChart) { doughnutChart.destroy(); doughnutChart = null; }
    canvas.style.display = 'none';
    if (legendEl) legendEl.innerHTML = '';
    return;
  }

  canvas.style.display = 'block';
  const totalSpent = active.reduce((s, c) => s + totals[c.id], 0);
  const labels  = active.map(c => c.label);
  const data    = active.map(c => totals[c.id]);
  const colors  = active.map(c => c.color);

  // ── Doughnut chart ──
  if (doughnutChart) {
    doughnutChart.data.labels                  = labels;
    doughnutChart.data.datasets[0].data        = data;
    doughnutChart.data.datasets[0].backgroundColor = colors;
    doughnutChart.update('active');
  } else {
    doughnutChart = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data, backgroundColor: colors,
          borderWidth: 2,
          borderColor: 'var(--card)',
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: false,
        cutout: '68%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => {
                const val = ctx.raw;
                const pct = Math.round(val / totalSpent * 100);
                return ` ${sym(viewCurrency)} ${fmt(val, viewCurrency)}  (${pct}%)`;
              }
            }
          }
        }
      }
    });
  }

  // ── Custom legend ──
  if (legendEl) {
    legendEl.innerHTML = active.map(c => {
      const pct = Math.round(totals[c.id] / totalSpent * 100);
      return `<div style="display:flex;align-items:center;gap:7px;margin:5px 0;font-size:12px;">
        <span style="width:10px;height:10px;border-radius:3px;background:${c.color};flex-shrink:0;"></span>
        <span style="flex:1;color:var(--text-soft);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${c.label}</span>
        <span style="font-weight:700;color:var(--text);font-size:11px;">${pct}%</span>
      </div>`;
    }).join('');
  }

  // ── Horizontal bars (scaled by value — biggest = full width) ──
  const maxVal = Math.max(...data);
  chartEl.innerHTML = active.map(c => {
    const val    = totals[c.id];
    const pct    = Math.round(val / maxVal * 100);   // relative to max category
    const share  = Math.round(val / totalSpent * 100); // share of total
    return `
      <div style="margin:10px 0;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
          <span style="font-size:13px;color:var(--text-soft);display:flex;align-items:center;gap:6px;">
            <span style="width:9px;height:9px;border-radius:2px;background:${c.color};display:inline-block;"></span>
            ${c.label}
          </span>
          <span style="font-size:12.5px;font-weight:700;color:var(--text);">${sym(viewCurrency)} ${fmt(val, viewCurrency)}</span>
        </div>
        <div style="background:var(--border);border-radius:20px;height:10px;overflow:hidden;">
          <div style="
            width:${pct}%;height:10px;border-radius:20px;
            background:${c.color};
            transition:width .6s ease;
            position:relative;
          ">
            <span style="
              position:absolute;right:6px;top:50%;transform:translateY(-50%);
              font-size:9px;font-weight:800;color:#fff;white-space:nowrap;
              display:${pct > 20 ? 'block' : 'none'};
            ">${share}%</span>
          </div>
        </div>
      </div>`;
  }).join('');
}

// ── Currency toggle ────────────────────────────────────────
function setCurrency(cur) {
  viewCurrency = cur;
  document.querySelectorAll('.currency-toggle button').forEach(b =>
    b.classList.toggle('active', b.dataset.cur === cur)
  );
  renderStats();
  renderExpenses();
  // Destroy chart so it rebuilds with new currency amounts in tooltips
  if (doughnutChart) { doughnutChart.destroy(); doughnutChart = null; }
  renderPhaseChart();
}

// ── Category filter ────────────────────────────────────────
function setFilter(cat) {
  activeFilter = cat;
  document.querySelectorAll('.cat-filter-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.cat === cat)
  );
  renderExpenses();
}

// ── Add expense modal ──────────────────────────────────────
function openModal()  { document.getElementById('expenseModal').classList.add('open'); document.getElementById('expDate').value = new Date().toISOString().split('T')[0]; }
function closeModal() { document.getElementById('expenseModal').classList.remove('open'); }

// ── Set budget modal ───────────────────────────────────────
function openBudgetModal()  {
  document.getElementById('budgetModal').classList.add('open');
  document.getElementById('budgetAmount').value = viewCurrency === 'NPR' ? Math.round(totalBudgetNPR) : Math.round(toINR(totalBudgetNPR));
  document.getElementById('convRate').value = conversionRate.toFixed(2);
}
function closeBudgetModal() { document.getElementById('budgetModal').classList.remove('open'); }

// ── Delete expense ─────────────────────────────────────────
async function deleteExpense(id) {
  if (!confirm('Delete this expense? This cannot be undone.')) return;
  try { await db.collection('expenses').doc(id).delete(); }
  catch (err) { alert('Error: ' + err.message); }
}

// ── Setup guide (if Firebase not configured) ───────────────
function showSetupGuide() {
  const main = document.getElementById('budgetContent');
  if (!main) return;
  showBudgetContent();
  main.innerHTML = `<div class="setup-card">
    <h3>🔧 Firebase Setup Required</h3>
    <p>Open <code>js/firebase-config.js</code> and paste your Firebase project config values.</p>
  </div>`;
}

// ── Form submissions ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Add expense form
  const form = document.getElementById('expenseForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!isEditor) return;
      const amount    = parseFloat(document.getElementById('expAmount').value);
      const currency  = document.getElementById('expCurrency').value;
      const cat       = document.getElementById('expCategory').value;
      const desc      = document.getElementById('expDesc').value.trim();
      const date      = document.getElementById('expDate').value;
      const amountNPR = toNPR(amount, currency);
      const btn       = form.querySelector('button[type=submit]');
      btn.disabled    = true;
      btn.textContent = 'Saving...';
      try {
        await db.collection('expenses').add({
          amount, currency, amountNPR,
          amountINR:   currency === 'INR' ? amount : toINR(amountNPR),
          category:    cat,
          description: desc,
          date,
          addedBy:     currentUser.email,
          addedByName: currentUser.displayName || currentUser.email,
          createdAt:   firebase.firestore.FieldValue.serverTimestamp()
        });
        form.reset();
        closeModal();
      } catch (err) {
        alert('Error saving expense: ' + err.message);
      } finally {
        btn.disabled    = false;
        btn.textContent = '💾 Save Expense';
      }
    });
  }

  // Budget form
  const bForm = document.getElementById('budgetForm');
  if (bForm) {
    bForm.addEventListener('submit', async e => {
      e.preventDefault();
      if (!isEditor) return;
      const amount    = parseFloat(document.getElementById('budgetAmount').value);
      const currency  = document.getElementById('budgetCurrency').value;
      const rate      = parseFloat(document.getElementById('convRate').value) || DEFAULT_INR_TO_NPR;
      const amountNPR = toNPR(amount, currency);
      try {
        await db.collection('settings').doc('main').set({
          totalBudgetNPR: amountNPR,
          totalBudgetINR: toINR(amountNPR),
          conversionRate: rate,
          updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        }, { merge: true });
        conversionRate = rate;
        totalBudgetNPR = amountNPR;
        const rateEl = document.getElementById('rateDisplay');
        if (rateEl) rateEl.textContent = `1 INR = ${rate.toFixed(2)} NPR`;
        renderStats();
        closeBudgetModal();
      } catch (err) { alert('Error saving budget: ' + err.message); }
    });
  }

  // Category filter buttons
  const filterWrap = document.getElementById('catFilters');
  if (filterWrap) {
    filterWrap.innerHTML =
      `<button class="cat-filter-btn active" data-cat="" onclick="setFilter('')">All</button>` +
      CATEGORIES.map(c =>
        `<button class="cat-filter-btn" data-cat="${c.id}" onclick="setFilter('${c.id}')" style="border-color:${c.color};color:${c.color};">${c.label}</button>`
      ).join('');
  }

  // Init Firebase
  initFirebase();
  setCurrency('NPR');
});
