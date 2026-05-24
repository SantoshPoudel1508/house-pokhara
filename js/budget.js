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

// ── Categories ────────────────────────────────────────────
const CATEGORIES = [
  { id:'planning',      label:'Planning & Permits',        color:'#5A7EB8' },
  { id:'foundation',    label:'Foundation & Soil',         color:'#8C4A22' },
  { id:'structure',     label:'Structure (Columns/Beams)', color:'#3A6248' },
  { id:'plumbing',      label:'Plumbing',                  color:'#208296' },
  { id:'electrical',    label:'Electrical',                color:'#C48A18' },
  { id:'waterproofing', label:'Waterproofing',             color:'#1E3040' },
  { id:'windows',       label:'Windows & Doors',           color:'#2D5C3C' },
  { id:'flooring',      label:'Flooring & Tiles',          color:'#7A5A18' },
  { id:'paint',         label:'Paint',                     color:'#643A96' },
  { id:'kitchen',       label:'Kitchen & Wardrobes',       color:'#C8702A' },
  { id:'bathrooms',     label:'Bathrooms',                 color:'#4A8A5A' },
  { id:'interiors',     label:'Interiors & Furniture',     color:'#A8685C' },
  { id:'outdoor',       label:'Outdoor & Garden',          color:'#3D7A50' },
  { id:'labour',        label:'Labour & Wages',            color:'#7A3828' },
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
      loadSettings();
      loadExpenses();
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

// ── Load settings ──────────────────────────────────────────
async function loadSettings() {
  try {
    const doc = await db.collection('settings').doc('main').get();
    if (doc.exists) {
      const d = doc.data();
      totalBudgetNPR = d.totalBudgetNPR || 0;
      conversionRate = d.conversionRate || DEFAULT_INR_TO_NPR;
      const rateEl = document.getElementById('rateDisplay');
      if (rateEl) rateEl.textContent = `1 INR = ${conversionRate.toFixed(2)} NPR`;
    }
    renderStats();
  } catch (e) { console.error('loadSettings error:', e); }
}

// ── Load expenses (real-time) ──────────────────────────────
function loadExpenses() {
  unsubscribeExpenses = db.collection('expenses')
    .orderBy('date', 'desc')
    .onSnapshot(snap => {
      expenses = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderStats();
      renderExpenses();
      renderPhaseChart();
    }, err => console.error('loadExpenses error:', err));
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

// ── Category chart ─────────────────────────────────────────
function renderPhaseChart() {
  const chartEl = document.getElementById('phaseChart');
  if (!chartEl) return;
  const totals = {};
  expenses.forEach(e => { totals[e.category] = (totals[e.category] || 0) + (e.amountNPR || 0); });
  const max = Math.max(...Object.values(totals), 1);
  chartEl.innerHTML = CATEGORIES.map(cat => {
    const val = totals[cat.id] || 0;
    if (!val) return '';
    const pct = Math.round(val / max * 100);
    return `
      <div class="phase-bar-item">
        <div class="phase-bar-label">${cat.label}</div>
        <div class="phase-bar-track"><div class="phase-bar-fill" style="width:${pct}%;background:${cat.color}"></div></div>
        <div class="phase-bar-val">${sym(viewCurrency)} ${fmt(val, viewCurrency)}</div>
      </div>`;
  }).filter(Boolean).join('') || '<p style="color:var(--muted);font-size:13.5px;">No expenses recorded yet.</p>';
}

// ── Currency toggle ────────────────────────────────────────
function setCurrency(cur) {
  viewCurrency = cur;
  document.querySelectorAll('.currency-toggle button').forEach(b =>
    b.classList.toggle('active', b.dataset.cur === cur)
  );
  renderStats();
  renderExpenses();
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
