/* ══════════════════════════════════════════════════════════
   BUDGET TRACKER — Firebase-powered
   Login with Google · Add/Edit/Delete expenses
   INR ⇄ NPR auto-conversion · Category breakdown
══════════════════════════════════════════════════════════ */

// ── State ─────────────────────────────────────────────────
let db, auth, currentUser = null;
let expenses = [];
let viewCurrency = 'NPR';
let conversionRate = DEFAULT_INR_TO_NPR; // from firebase-config.js
let totalBudgetNPR = 0;
let isEditor = false;

// ── Category config ───────────────────────────────────────
const CATEGORIES = [
  { id:'planning',      label:'Planning & Permits',   color:'#5A7EB8' },
  { id:'foundation',    label:'Foundation & Soil',    color:'#8C4A22' },
  { id:'structure',     label:'Structure (Columns/Beams)', color:'#3A6248' },
  { id:'plumbing',      label:'Plumbing',             color:'#208296' },
  { id:'electrical',    label:'Electrical',           color:'#C48A18' },
  { id:'waterproofing', label:'Waterproofing',        color:'#1E3040' },
  { id:'windows',       label:'Windows & Doors',      color:'#2D5C3C' },
  { id:'flooring',      label:'Flooring & Tiles',     color:'#7A5A18' },
  { id:'paint',         label:'Paint',                color:'#643A96' },
  { id:'kitchen',       label:'Kitchen & Wardrobes',  color:'#C8702A' },
  { id:'bathrooms',     label:'Bathrooms',            color:'#4A8A5A' },
  { id:'interiors',     label:'Interiors & Furniture','color':'#A8685C' },
  { id:'outdoor',       label:'Outdoor & Garden',     color:'#3D7A50' },
  { id:'labour',        label:'Labour & Wages',       color:'#7A3828' },
  { id:'misc',          label:'Miscellaneous',        color:'#78716C' },
];

function catById(id) { return CATEGORIES.find(c => c.id === id) || CATEGORIES[CATEGORIES.length - 1]; }

// ── Currency helpers ───────────────────────────────────────
function toNPR(amount, currency) {
  return currency === 'INR' ? amount * conversionRate : amount;
}
function toINR(amountNPR) { return amountNPR / conversionRate; }
function fmt(amountNPR, currency) {
  const val = currency === 'NPR' ? amountNPR : toINR(amountNPR);
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(val);
}
function sym(currency) { return currency === 'NPR' ? 'NPR' : '₹'; }

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
      isEditor    = user ? ALLOWED_EDITORS.includes(user.email) : false;
      renderAuth();
      if (user) {
        loadSettings();
        loadExpenses();
      } else {
        // Public view — still load data read-only
        loadSettings();
        loadExpenses();
      }
    });
  } catch (e) {
    console.error('Firebase init error:', e);
    showSetupGuide();
  }
}

// ── Auth ───────────────────────────────────────────────────
function signInGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider).catch(err => alert('Login failed: ' + err.message));
}
function signOut() {
  auth.signOut();
}

function renderAuth() {
  const authArea = document.getElementById('authArea');
  if (!authArea) return;
  if (currentUser) {
    const editorBadge = isEditor ? `<span style="background:var(--accent);color:#fff;font-size:10px;padding:2px 7px;border-radius:20px;font-weight:700;margin-left:4px;">Editor</span>` : `<span style="background:var(--bg-alt);color:var(--muted);font-size:10px;padding:2px 7px;border-radius:20px;margin-left:4px;">View only</span>`;
    authArea.innerHTML = `
      <div class="user-info">
        <div class="user-avatar">${currentUser.photoURL ? `<img src="${currentUser.photoURL}"/>` : '👤'}</div>
        <span class="user-name">${currentUser.displayName || currentUser.email} ${editorBadge}</span>
        <button class="logout-btn" onclick="signOut()" title="Sign out">✕</button>
      </div>`;
  } else {
    authArea.innerHTML = `<button class="login-btn" onclick="signInGoogle()"><span>🔐</span> Sign in with Google</button>`;
  }
  // Show/hide add expense button
  const addBtn = document.getElementById('addExpenseBtn');
  if (addBtn) addBtn.style.display = isEditor ? 'inline-flex' : 'none';
  // Show budget set button
  const setBudgetBtn = document.getElementById('setBudgetBtn');
  if (setBudgetBtn) setBudgetBtn.style.display = isEditor ? 'inline-flex' : 'none';
}

// ── Load settings (budget + rate) ─────────────────────────
async function loadSettings() {
  try {
    const doc = await db.collection('settings').doc('main').get();
    if (doc.exists) {
      const d = doc.data();
      totalBudgetNPR = d.totalBudgetNPR || 0;
      conversionRate = d.conversionRate || DEFAULT_INR_TO_NPR;
      document.getElementById('rateDisplay').textContent = `1 INR = ${conversionRate.toFixed(2)} NPR`;
    }
    renderStats();
  } catch (e) { console.error(e); }
}

// ── Load expenses ──────────────────────────────────────────
function loadExpenses() {
  db.collection('expenses')
    .orderBy('date', 'desc')
    .onSnapshot(snap => {
      expenses = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderStats();
      renderExpenses();
      renderPhaseChart();
    }, err => console.error(err));
}

// ── Stats ──────────────────────────────────────────────────
function renderStats() {
  const totalSpentNPR = expenses.reduce((s, e) => s + (e.amountNPR || 0), 0);
  const remaining     = totalBudgetNPR - totalSpentNPR;
  const pct           = totalBudgetNPR > 0 ? Math.min(100, Math.round(totalSpentNPR / totalBudgetNPR * 100)) : 0;
  const cur = viewCurrency;

  document.getElementById('statBudget').textContent   = totalBudgetNPR ? `${sym(cur)} ${fmt(totalBudgetNPR, cur)}` : 'Not set';
  document.getElementById('statSpent').textContent    = `${sym(cur)} ${fmt(totalSpentNPR, cur)}`;
  document.getElementById('statRemaining').textContent= totalBudgetNPR ? `${sym(cur)} ${fmt(remaining, cur)}` : '—';
  document.getElementById('statPct').textContent      = totalBudgetNPR ? `${pct}% used` : '—';

  const spentBar = document.getElementById('spentBar');
  if (spentBar) { spentBar.style.width = pct + '%'; }
  const remaining_el = document.getElementById('statRemaining').closest('.bstat');
  if (remaining_el) remaining_el.className = 'bstat ' + (remaining < 0 ? 'warn-stat' : 'good-stat');
}

// ── Expense list ───────────────────────────────────────────
function renderExpenses(filter = '') {
  const list = document.getElementById('expenseList');
  if (!list) return;
  let items = expenses;
  if (filter) items = items.filter(e => e.category === filter);
  if (items.length === 0) {
    list.innerHTML = `<div style="text-align:center;padding:40px;color:var(--muted);">No expenses yet${filter ? ' in this category' : ''}.</div>`;
    return;
  }
  list.innerHTML = items.map(e => {
    const cat = catById(e.category);
    const cur = viewCurrency;
    const amt = viewCurrency === 'NPR' ? e.amountNPR : toINR(e.amountNPR);
    return `<div class="expense-item">
      <div class="expense-cat-dot" style="background:${cat.color}"></div>
      <div class="expense-info">
        <div class="expense-desc">${e.description || 'Expense'}</div>
        <div class="expense-meta">${cat.label} · ${e.date || ''} · Added by ${e.addedByName || 'someone'}</div>
      </div>
      <div class="expense-amount">${sym(cur)} ${new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(amt)}</div>
      ${isEditor ? `<div class="expense-actions"><button onclick="deleteExpense('${e.id}')" title="Delete">🗑</button></div>` : ''}
    </div>`;
  }).join('');
}

// ── Phase/Category chart ───────────────────────────────────
function renderPhaseChart() {
  const chartEl = document.getElementById('phaseChart');
  if (!chartEl) return;
  const totals = {};
  expenses.forEach(e => { totals[e.category] = (totals[e.category] || 0) + (e.amountNPR || 0); });
  const max = Math.max(...Object.values(totals), 1);
  const cur = viewCurrency;
  chartEl.innerHTML = CATEGORIES.map(cat => {
    const val = totals[cat.id] || 0;
    if (!val) return '';
    const pct = Math.round(val / max * 100);
    return `<div class="phase-bar-item">
      <div class="phase-bar-label">${cat.label}</div>
      <div class="phase-bar-track"><div class="phase-bar-fill" style="width:${pct}%;background:${cat.color}"></div></div>
      <div class="phase-bar-val">${sym(cur)} ${fmt(val, cur)}</div>
    </div>`;
  }).filter(Boolean).join('');
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
let activeFilter = '';
function setFilter(cat) {
  activeFilter = cat;
  document.querySelectorAll('.cat-filter-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.cat === cat)
  );
  renderExpenses(cat);
}

// ── Add expense modal ──────────────────────────────────────
function openModal() {
  if (!isEditor) return;
  document.getElementById('expenseModal').classList.add('open');
  document.getElementById('expDate').value = new Date().toISOString().split('T')[0];
}
function closeModal() { document.getElementById('expenseModal').classList.remove('open'); }

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('expenseForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!isEditor) return;
      const amount   = parseFloat(document.getElementById('expAmount').value);
      const currency = document.getElementById('expCurrency').value;
      const cat      = document.getElementById('expCategory').value;
      const desc     = document.getElementById('expDesc').value;
      const date     = document.getElementById('expDate').value;
      const amountNPR = toNPR(amount, currency);
      try {
        await db.collection('expenses').add({
          amount, currency, amountNPR,
          amountINR: currency === 'INR' ? amount : toINR(amountNPR),
          category: cat,
          description: desc,
          date,
          addedBy:     currentUser.email,
          addedByName: currentUser.displayName || currentUser.email,
          createdAt:   firebase.firestore.FieldValue.serverTimestamp()
        });
        form.reset();
        closeModal();
      } catch (err) { alert('Error saving expense: ' + err.message); }
    });
  }
});

async function deleteExpense(id) {
  if (!isEditor) return;
  if (!confirm('Delete this expense?')) return;
  await db.collection('expenses').doc(id).delete();
}

// ── Set Budget modal ───────────────────────────────────────
function openBudgetModal() {
  if (!isEditor) return;
  document.getElementById('budgetModal').classList.add('open');
  document.getElementById('budgetAmount').value = viewCurrency === 'NPR'
    ? Math.round(totalBudgetNPR) : Math.round(toINR(totalBudgetNPR));
}
function closeBudgetModal() { document.getElementById('budgetModal').classList.remove('open'); }

document.addEventListener('DOMContentLoaded', () => {
  const bForm = document.getElementById('budgetForm');
  if (bForm) {
    bForm.addEventListener('submit', async e => {
      e.preventDefault();
      if (!isEditor) return;
      const amount   = parseFloat(document.getElementById('budgetAmount').value);
      const currency = document.getElementById('budgetCurrency').value;
      const rate     = parseFloat(document.getElementById('convRate').value) || DEFAULT_INR_TO_NPR;
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
        document.getElementById('rateDisplay').textContent = `1 INR = ${rate.toFixed(2)} NPR`;
        renderStats();
        closeBudgetModal();
      } catch (err) { alert('Error saving budget: ' + err.message); }
    });
  }
});

// ── Setup guide ────────────────────────────────────────────
function showSetupGuide() {
  const main = document.getElementById('budgetMain');
  if (!main) return;
  main.innerHTML = `
    <div class="setup-card">
      <h3>🔧 Firebase Setup Required</h3>
      <p>To enable the Budget Tracker, you need to connect it to a free Firebase database. This takes about 10 minutes and is free forever for your use.</p>
      <div class="setup-steps">
        <ol>
          <li>Go to <a href="https://console.firebase.google.com" target="_blank" style="color:var(--accent);font-weight:600;">console.firebase.google.com</a></li>
          <li>Click <strong>"Create a project"</strong> → name it <code>house-pokhara</code></li>
          <li>Click <strong>"Firestore Database"</strong> in left menu → <strong>Create database</strong> → choose <strong>Start in test mode</strong></li>
          <li>Click <strong>"Authentication"</strong> in left menu → <strong>Get started</strong> → Enable <strong>Google</strong> sign-in</li>
          <li>Click the ⚙️ gear icon → <strong>Project settings</strong> → scroll to <strong>Your apps</strong> → click <strong>&lt;/&gt;</strong> (web app)</li>
          <li>Name it <code>house-guide</code>, click <strong>Register app</strong></li>
          <li>Copy the <code>firebaseConfig</code> object values</li>
          <li>Open the file <code>js/firebase-config.js</code> in your computer and paste the values</li>
          <li>Also add your Gmail address to <code>ALLOWED_EDITORS</code> list</li>
          <li>Save the file and push to GitHub (I can do this for you!)</li>
        </ol>
      </div>
      <p style="font-size:13px;color:var(--muted);">Ask me in the chat and I will walk you through each step or even do it for you if you share the config values.</p>
    </div>`;
}

// ── Start ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initFirebase();
  setCurrency('NPR');
  // Category filter buttons
  const filterWrap = document.getElementById('catFilters');
  if (filterWrap) {
    filterWrap.innerHTML = `<button class="cat-filter-btn active" data-cat="" onclick="setFilter('')" style="border-color:var(--border);">All</button>` +
      CATEGORIES.map(c => `<button class="cat-filter-btn" data-cat="${c.id}" onclick="setFilter('${c.id}')" style="border-color:${c.color};color:${c.color};">${c.label}</button>`).join('');
  }
});
