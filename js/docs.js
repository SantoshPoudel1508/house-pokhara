/* ═══════════════════════════════════════════════════════════
   DOCUMENTS — Google Drive links stored in Firestore
   No Firebase Storage needed. Upload to Google Drive,
   share the link, paste here. Completely FREE.
═══════════════════════════════════════════════════════════ */

const DOC_CATEGORIES = [
  { id:'land',         label:'Land & Property',        icon:'🏛️', color:'#C8702A' },
  { id:'municipal',    label:'Municipal & Permits',     icon:'🏢', color:'#5F8269' },
  { id:'legal',        label:'Legal Documents',         icon:'⚖️', color:'#4A6EA8' },
  { id:'contracts',    label:'Contracts & Agreements',  icon:'📜', color:'#7C3AED' },
  { id:'technical',    label:'Technical Reports',       icon:'🔬', color:'#1E3040' },
  { id:'drawings',     label:'Drawings & Plans',        icon:'📐', color:'#2D5C3C' },
  { id:'photos',       label:'Photos & Site Progress',  icon:'📸', color:'#C46428' },
  { id:'quotations',   label:'Quotations & Estimates',  icon:'📊', color:'#0891B2' },
  { id:'bills',        label:'Bills & Receipts',        icon:'🧾', color:'#C48A18' },
  { id:'payments',     label:'Contractor Payments',     icon:'💳', color:'#8C4A22' },
  { id:'bank',         label:'Bank & Finance',          icon:'🏦', color:'#374151' },
  { id:'warranties',   label:'Warranties & Certificates',icon:'🏆',color:'#059669' },
  { id:'insurance',    label:'Insurance',               icon:'🛡️', color:'#16A34A' },
  { id:'utilities',    label:'Utility Connections',     icon:'⚡', color:'#6B7280' },
  { id:'other',        label:'Other Documents',         icon:'📄', color:'#78716C' },
];

let docDb, docAuth;
let docCurrentUser = null;
let docIsEditor    = false;
let allDocs        = [];
let activeDocCat   = '';
let unsubscribeDocs = null;

function catDocById(id) { return DOC_CATEGORIES.find(c => c.id === id) || DOC_CATEGORIES[DOC_CATEGORIES.length - 1]; }

// ── Screens ───────────────────────────────────────────────
function showDocLoginWall(reason) {
  document.getElementById('docLoginWall').style.display = reason === 'denied' ? 'none' : 'flex';
  document.getElementById('docDenied').style.display    = reason === 'denied' ? 'flex' : 'none';
  document.getElementById('docContent').style.display   = 'none';
}
function showDocContent() {
  document.getElementById('docLoginWall').style.display = 'none';
  document.getElementById('docDenied').style.display    = 'none';
  document.getElementById('docContent').style.display   = 'block';
}

// ── Firebase init ─────────────────────────────────────────
function initDocFirebase() {
  if (!IS_FIREBASE_READY) { showDocContent(); return; }
  try {
    try { docDb = firebase.firestore(); docAuth = firebase.auth(); }
    catch(e) { firebase.initializeApp(FIREBASE_CONFIG); docDb = firebase.firestore(); docAuth = firebase.auth(); }
    docAuth.onAuthStateChanged(user => {
      docCurrentUser = user;
      if (!user) { showDocLoginWall(); if (unsubscribeDocs) { unsubscribeDocs(); unsubscribeDocs = null; } return; }
      if (!ALLOWED_EDITORS.includes(user.email)) { showDocLoginWall('denied'); return; }
      docIsEditor = true;
      showDocContent();
      renderDocUserBar();
      loadDocs();
    });
  } catch(e) { console.error(e); }
}

function docSignIn()  { const p = new firebase.auth.GoogleAuthProvider(); docAuth.signInWithPopup(p).catch(err => alert('Login failed: ' + err.message)); }
function docSignOut() { if (unsubscribeDocs) { unsubscribeDocs(); unsubscribeDocs = null; } docAuth.signOut(); }

function renderDocUserBar() {
  const bar = document.getElementById('docUserBar');
  if (!bar || !docCurrentUser) return;
  bar.innerHTML = `<div class="user-info">
    <div class="user-avatar">${docCurrentUser.photoURL ? `<img src="${docCurrentUser.photoURL}" referrerpolicy="no-referrer"/>` : '👤'}</div>
    <span class="user-name">${docCurrentUser.displayName || docCurrentUser.email}</span>
    <span style="background:var(--accent);color:#fff;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:700;">Access</span>
    <button class="logout-btn" onclick="docSignOut()">Sign out</button>
  </div>`;
}

// ── Load docs (real-time) ─────────────────────────────────
function loadDocs() {
  unsubscribeDocs = docDb.collection('documents')
    .orderBy('addedAt', 'desc')
    .onSnapshot(snap => {
      allDocs = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderDocStats();
      renderDocList();
    }, err => console.error(err));
}

function renderDocStats() {
  const el = id => document.getElementById(id);
  if (el('docTotal')) el('docTotal').textContent = allDocs.length + ' document' + (allDocs.length !== 1 ? 's' : '');
}

// ── Filter ────────────────────────────────────────────────
function setDocFilter(cat) {
  activeDocCat = cat;
  document.querySelectorAll('.doc-cat-btn').forEach(b => b.classList.toggle('active', b.dataset.cat === cat));
  renderDocList();
}

// ── Render list ───────────────────────────────────────────
function renderDocList() {
  const list = document.getElementById('docList');
  const countEl = document.getElementById('docCount');
  if (!list) return;
  const items = activeDocCat ? allDocs.filter(d => d.category === activeDocCat) : allDocs;
  if (countEl) countEl.textContent = items.length ? items.length + ' file' + (items.length !== 1 ? 's' : '') : '';
  if (!items.length) {
    list.innerHTML = `<div class="doc-empty"><div style="font-size:40px;margin-bottom:10px;">📂</div>
      <p>No documents added yet${activeDocCat ? ' in this category' : ''}.</p>
      <p style="font-size:12px;color:var(--muted);margin-top:4px;">Click "Add Document" to save a link.</p></div>`;
    return;
  }
  list.innerHTML = items.map(d => {
    const cat  = catDocById(d.category);
    const icon = getDocIcon(d.name || '');
    const date = d.addedAt?.toDate ? d.addedAt.toDate().toLocaleDateString('en-IN') : '';
    const previewUrl = makePreviewUrl(d.url || '');
    return `<div class="doc-card">
      <div class="doc-card-top" style="border-left:4px solid ${cat.color};">
        <div class="doc-icon">${icon}</div>
        <div class="doc-info">
          <div class="doc-name" title="${d.name}">${d.name}</div>
          <div class="doc-meta">
            <span style="background:${cat.color}20;color:${cat.color};padding:2px 7px;border-radius:20px;font-size:10px;font-weight:700;">${cat.icon} ${cat.label}</span>
            ${date ? `<span style="color:var(--muted);font-size:11px;">Added ${date}</span>` : ''}
            <span style="color:var(--muted);font-size:11px;">by ${d.addedByName || d.addedBy || ''}</span>
          </div>
          ${d.description ? `<div style="font-size:12px;color:var(--muted);margin-top:3px;">${d.description}</div>` : ''}
        </div>
        <div class="doc-actions">
          ${previewUrl ? `<button class="btn-edit" onclick="previewDoc('${d.id}')" title="Preview inside website">👁</button>` : ''}
          <a class="btn-edit" href="${d.url}" target="_blank" rel="noopener" title="Open in Google Drive / new tab">🔗</a>
          <button class="btn-delete" onclick="deleteDoc('${d.id}')" title="Remove from list">🗑</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function getDocIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  if (['jpg','jpeg','png','gif','webp','heic'].includes(ext)) return '🖼️';
  if (ext === 'pdf') return '📕';
  if (['doc','docx'].includes(ext)) return '📘';
  if (['xls','xlsx'].includes(ext)) return '📗';
  if (['ppt','pptx'].includes(ext)) return '📙';
  return '📄';
}

// Convert Google Drive share URL → embed/preview URL
function makePreviewUrl(url) {
  if (!url) return null;
  // Google Drive: https://drive.google.com/file/d/FILE_ID/view?...
  const m = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/);
  if (m) return `https://drive.google.com/file/d/${m[1]}/preview`;
  // Google Docs/Sheets/Slides share link
  if (url.includes('docs.google.com')) return url.replace('/edit', '/preview').replace('/pub?', '/preview?');
  return null;
}

// ── Preview modal ─────────────────────────────────────────
function previewDoc(id) {
  const d = allDocs.find(x => x.id === id);
  if (!d) return;
  const previewUrl = makePreviewUrl(d.url);
  const modal = document.getElementById('previewModal');
  document.getElementById('previewTitle').textContent = d.name;
  document.getElementById('previewBody').innerHTML = previewUrl
    ? `<iframe src="${previewUrl}" style="width:100%;height:70vh;border:none;border-radius:8px;"></iframe>`
    : `<div style="text-align:center;padding:40px;">
        <p style="color:var(--muted);">Preview not available for this link.</p>
        <a href="${d.url}" target="_blank" style="color:var(--accent);font-weight:700;">Open document →</a>
       </div>`;
  modal.classList.add('open');
}
function closePreview() {
  document.getElementById('previewModal').classList.remove('open');
  document.getElementById('previewBody').innerHTML = '';
}

// ── Add doc modal ─────────────────────────────────────────
function openAddModal()  { document.getElementById('addModal').classList.add('open'); }
function closeAddModal() { document.getElementById('addModal').classList.remove('open'); document.getElementById('addForm').reset(); }

// ── Delete ────────────────────────────────────────────────
async function deleteDoc(id) {
  if (!docIsEditor || !confirm('Remove this document from the list?')) return;
  try { await docDb.collection('documents').doc(id).delete(); }
  catch(e) { alert('Error: ' + e.message); }
}

// ── Init ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initDocFirebase();

  // Category filters
  const filters = document.getElementById('docCatFilters');
  if (filters) {
    filters.innerHTML = `<button class="doc-cat-btn active" data-cat="" onclick="setDocFilter('')">All</button>` +
      DOC_CATEGORIES.sort((a,b) => a.label.localeCompare(b.label))
        .map(c => `<button class="doc-cat-btn" data-cat="${c.id}" onclick="setDocFilter('${c.id}')" style="border-color:${c.color};color:${c.color};">${c.icon} ${c.label}</button>`).join('');
  }

  // Add form
  const form = document.getElementById('addForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!docIsEditor) return;
      const name = document.getElementById('docName').value.trim();
      const url  = document.getElementById('docUrl').value.trim();
      const cat  = document.getElementById('docCat').value;
      const desc = document.getElementById('docDesc').value.trim();
      const btn  = form.querySelector('button[type=submit]');
      btn.disabled = true;
      try {
        await docDb.collection('documents').add({
          name, url, category: cat, description: desc,
          addedBy:     docCurrentUser.email,
          addedByName: docCurrentUser.displayName || docCurrentUser.email,
          addedAt:     firebase.firestore.FieldValue.serverTimestamp()
        });
        closeAddModal();
      } catch(err) { alert('Error: ' + err.message); }
      finally { btn.disabled = false; }
    });
  }
});
