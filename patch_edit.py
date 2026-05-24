"""
1. Add edit button to each expense item
2. Pre-fill modal for editing, update Firestore on save
3. Category color on left border for ALL items (not just first 3)
"""

with open('js/budget.js', 'r', encoding='utf-8') as f:
    js = f.read()

# ── FIX 1: Add editingId state variable ──────────────────
js = js.replace(
    "let unsubscribeExpenses = null;\nlet unsubscribeSettings = null;",
    "let unsubscribeExpenses = null;\nlet unsubscribeSettings = null;\nlet editingId = null; // null = new, string = editing existing"
)

# ── FIX 2: Replace openModal to support editing ──────────
js = js.replace(
    """function openModal()  {
  document.getElementById('expenseModal').classList.add('open');
  document.getElementById('expDate').value = getNPTDate();
}""",
    """function openModal(expense) {
  editingId = expense ? expense.id : null;
  const modal  = document.getElementById('expenseModal');
  const title  = modal.querySelector('h3');
  const btn    = modal.querySelector('button[type=submit]');
  modal.classList.add('open');

  if (expense) {
    // Pre-fill all fields for editing
    document.getElementById('expAmount').value   = expense.amount || '';
    document.getElementById('expCurrency').value = expense.currency || 'NPR';
    document.getElementById('expCategory').value = expense.category || '';
    document.getElementById('expDesc').value     = expense.description || '';
    document.getElementById('expDate').value     = expense.date || getNPTDate();
    if (title) title.textContent = '✏️ Edit Expense';
    if (btn)   btn.textContent   = '💾 Update Expense';
  } else {
    document.getElementById('expenseForm').reset();
    document.getElementById('expDate').value = getNPTDate();
    if (title) title.textContent = '➕ Add New Expense';
    if (btn)   btn.textContent   = '💾 Save Expense';
  }
}

function editExpense(id) {
  const e = expenses.find(x => x.id === id);
  if (e) openModal(e);
}"""
)

# ── FIX 3: Form submit — create OR update ────────────────
js = js.replace(
    """      try {
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
      }""",
    """      try {
        if (editingId) {
          // Update existing document
          await db.collection('expenses').doc(editingId).update({
            amount, currency, amountNPR,
            amountINR:      currency === 'INR' ? amount : toINR(amountNPR),
            category:       cat,
            description:    desc,
            date,
            lastEditedBy:   currentUser.email,
            lastEditedAt:   firebase.firestore.FieldValue.serverTimestamp()
          });
        } else {
          // Create new document
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
        }
        editingId = null;
        form.reset();
        closeModal();
      } catch (err) {
        alert('Error saving expense: ' + err.message);
      } finally {
        btn.disabled    = false;
        btn.textContent = editingId ? '💾 Update Expense' : '💾 Save Expense';
      }"""
)

# ── FIX 4: Category color on ALL items + edit button ─────
js = js.replace(
    """    return `
      <div class="expense-item" style="${i < 3 ? 'border-left:3px solid var(--accent);' : ''}">
        <div class="expense-cat-dot" style="background:${cat.color}"></div>
        <div class="expense-info">
          <div class="expense-desc">${e.description || 'Expense'}</div>
          <div class="expense-meta">${cat.label} · ${e.date || ''} · ${e.addedByName || e.addedBy || ''}</div>
        </div>
        <div class="expense-amount">${sym(viewCurrency)} ${new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(amt)}</div>
        <div class="expense-actions">
          <button onclick="deleteExpense('${e.id}')" title="Delete expense">🗑</button>
        </div>
      </div>`;""",
    """    return `
      <div class="expense-item" style="border-left:4px solid ${cat.color};">
        <div class="expense-info">
          <div class="expense-desc">${e.description || 'Expense'}</div>
          <div class="expense-meta" style="display:flex;align-items:center;gap:6px;margin-top:2px;">
            <span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:${cat.color};flex-shrink:0;"></span>
            ${cat.label} · ${e.date || ''} · ${e.addedByName || e.addedBy || ''}
          </div>
        </div>
        <div class="expense-amount">${sym(viewCurrency)} ${new Intl.NumberFormat('en-IN',{maximumFractionDigits:0}).format(amt)}</div>
        <div class="expense-actions">
          <button onclick="editExpense('${e.id}')" title="Edit expense" style="color:var(--accent-dark);">✏️</button>
          <button onclick="deleteExpense('${e.id}')" title="Delete expense">🗑</button>
        </div>
      </div>`;"""
)

# ── FIX 5: Reset editingId when modal is closed ───────────
js = js.replace(
    "function closeModal() { document.getElementById('expenseModal').classList.remove('open'); }",
    "function closeModal() { document.getElementById('expenseModal').classList.remove('open'); editingId = null; }"
)

with open('js/budget.js', 'w', encoding='utf-8') as f:
    f.write(js)

checks = [
    ('editingId state',        'let editingId = null' in js),
    ('openModal supports edit','function editExpense' in js),
    ('editExpense fn',         'expenses.find(x => x.id' in js),
    ('Firestore update',       'doc(editingId).update' in js),
    ('category color all',     'border-left:4px solid ${cat.color}' in js),
    ('edit button',            'editExpense' in js and '✏️' in js),
    ('closeModal resets id',   "editingId = null; }" in js),
]
for name, ok in checks:
    print(f"  {'✓' if ok else '✗'} {name}")
