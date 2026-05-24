/* ═══════════════════════════════════════════════════════════
   DOCUMENTS — Firebase Storage + Firestore
   Private: only ALLOWED_EDITORS can view and manage docs
═══════════════════════════════════════════════════════════ */

const DOC_CATEGORIES = [
  { id: 'land',         label: 'Land & Property',         icon: '🏛️', color: '#C8702A' },
  { id: 'legal',        label: 'Legal Documents',          icon: '⚖️', color: '#4A6EA8' },
  { id: 'municipal',    label: 'Municipal & Government',   icon: '🏛️', color: '#5F8269' },
  { id: 'construction', label: 'Construction & Design',    icon: '🏗️', color: '#8C4A22' },
  { id: 'bills',        label: 'Bills & Receipts',         icon: '🧾', color: '#C48A18' },
  { id: 'insurance',    label: 'Insurance',                icon: '🛡️', color: '#059669' },
  { id: 'contracts',    label: 'Contracts & Agreements',   icon: '📜', color: '#7C3AED' },
  { id: 'other',        label: 'Other Documents',          icon: '📄', color: '#78716C' },
];

let docDb, docAuth, docStorage;
let docCurrentUser = null;
let docIsEditor    = false;
let allDocs        = [];
let activeDocCat   = '';
let unsubscribeDocs = null;

function catDocById(id) {
  return DOC_CATEGORIES.find(c => c.id === id) || DOC_CATEGORIES[DOC_CATEGORIES.length - 1];
}

// ── Screens ────────────────────────────────────────────────
function showDocLoginWall(reason) {
  document.getElementById('docLoginWall').style.display = reason === 'denied' ? 'none'    : 'flex';
  document.getElementById('docDenied').style.display    = reason === 'denied' ? 'flex'    : 'none';
  document.getElementById('docContent').style.display   = 'none';
}
function showDocContent() {
  document.getElementById('docLoginWall').style.display = 'none';
  document.getElementById('docDenied').style.display    = 'none';
  document.getElementById('docContent').style.display   = 'block';
}

// ── Firebase init ─────────────────────────────────────────
function initDocFirebase() {
  if (!IS_FIREBASE_READY) {
    document.getElementById('docContent').style.display = 'block';
    document.getElementById('docLoginWall').style.display = 'none';
    document.getElementById('docList').innerHTML = '<div class="doc-empty"><div>🔧</div><p>Firebase not configured. Open js/firebase-config.js and add your config.</p></div>';
    return;
  }
  try {
    // Reuse existing Firebase app if already initialised
    try { docDb = firebase.firestore(); docAuth = firebase.auth(); docStorage = firebase.storage(); }
    catch(e) { firebase.initializeApp(FIREBASE_CONFIG); docDb = firebase.firestore(); docAuth = firebase.auth(); docStorage = firebase.storage(); }

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
  bar.innerHTML = `
    <div class="user-info">
      <div class="user-avatar">${docCurrentUser.photoURL ? `<img src="${docCurrentUser.photoURL}" referrerpolicy="no-referrer"/>` : '👤'}</div>
      <span class="user-name">${docCurrentUser.displayName || docCurrentUser.email}</span>
      <span style="background:var(--accent);color:#fff;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:700;">Access</span>
      <button class="logout-btn" onclick="docSignOut()">Sign out</button>
    </div>`;
}

// ── Load documents (real-time) ────────────────────────────
function loadDocs() {
  unsubscribeDocs = docDb.collection('documents')
    .orderBy('uploadedAt', 'desc')
    .onSnapshot(snap => {
      allDocs = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      renderDocStats();
      renderDocList();
    }, err => console.error(err));
}

// ── Stats ─────────────────────────────────────────────────
function renderDocStats() {
  const total = allDocs.length;
  const totalSize = allDocs.reduce((s, d) => s + (d.size || 0), 0);
  const el = id => document.getElementById(id);
  if (el('docTotal')) el('docTotal').textContent = total + ' document' + (total !== 1 ? 's' : '');
  if (el('docSize'))  el('docSize').textContent  = formatBytes(totalSize);
}

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  if (bytes < 1024)       return bytes + ' B';
  if (bytes < 1024*1024)  return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/(1024*1024)).toFixed(1) + ' MB';
}

// ── Document list ─────────────────────────────────────────
function setDocFilter(cat) {
  activeDocCat = cat;
  document.querySelectorAll('.doc-cat-btn').forEach(b => b.classList.toggle('active', b.dataset.cat === cat));
  renderDocList();
}

function renderDocList() {
  const list  = document.getElementById('docList');
  const countEl = document.getElementById('docCount');
  if (!list) return;
  const items = activeDocCat ? allDocs.filter(d => d.category === activeDocCat) : allDocs;
  if (countEl) countEl.textContent = items.length ? items.length + ' file' + (items.length !== 1 ? 's' : '') : '';
  if (!items.length) {
    list.innerHTML = `<div class="doc-empty"><div style="font-size:40px;margin-bottom:10px;">📂</div><p>No documents yet${activeDocCat ? ' in this category' : ''}.</p><p style="font-size:12px;color:var(--muted);margin-top:4px;">Click "Upload Document" to add your first file.</p></div>`;
    return;
  }
  list.innerHTML = items.map(d => {
    const cat     = catDocById(d.category);
    const ext     = (d.name || '').split('.').pop().toLowerCase();
    const icon    = getFileIcon(ext, d.type || '');
    const date    = d.uploadedAt?.toDate ? d.uploadedAt.toDate().toLocaleDateString('en-IN') : (d.uploadedAt || '');
    const isImage = (d.type || '').startsWith('image/');
    const isPDF   = ext === 'pdf' || (d.type || '') === 'application/pdf';
    return `
    <div class="doc-card">
      <div class="doc-card-top" style="border-left:4px solid ${cat.color};">
        <div class="doc-icon">${icon}</div>
        <div class="doc-info">
          <div class="doc-name" title="${d.name}">${d.name}</div>
          <div class="doc-meta">
            <span style="background:${cat.color}20;color:${cat.color};padding:2px 7px;border-radius:20px;font-size:10px;font-weight:700;">${cat.icon} ${cat.label}</span>
            <span style="color:var(--muted);font-size:11px;">${formatBytes(d.size)} · ${date}</span>
          </div>
          ${d.description ? `<div style="font-size:12px;color:var(--muted);margin-top:3px;">${d.description}</div>` : ''}
        </div>
        <div class="doc-actions">
          ${isImage || isPDF ? `<button class="btn-edit" onclick="previewDoc('${d.id}')" title="Preview">👁</button>` : ''}
          <a class="btn-edit" href="${d.url}" target="_blank" download="${d.name}" title="Download">⬇️</a>
          <button class="btn-delete" onclick="deleteDoc('${d.id}','${d.storagePath}')" title="Delete">🗑</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function getFileIcon(ext, mime) {
  if (['jpg','jpeg','png','gif','webp','heic'].includes(ext) || mime.startsWith('image/')) return '🖼️';
  if (ext === 'pdf') return '📕';
  if (['doc','docx'].includes(ext)) return '📘';
  if (['xls','xlsx'].includes(ext)) return '📗';
  if (['ppt','pptx'].includes(ext)) return '📙';
  if (['zip','rar','7z'].includes(ext)) return '🗜️';
  return '📄';
}

// ── Preview modal ─────────────────────────────────────────
function previewDoc(id) {
  const doc = allDocs.find(d => d.id === id);
  if (!doc) return;
  const modal = document.getElementById('previewModal');
  const body  = document.getElementById('previewBody');
  const title = document.getElementById('previewTitle');
  if (title) title.textContent = doc.name;
  const ext  = (doc.name || '').split('.').pop().toLowerCase();
  const isPDF   = ext === 'pdf' || (doc.type || '') === 'application/pdf';
  const isImage = (doc.type || '').startsWith('image/');
  if (isImage) {
    body.innerHTML = `<img src="${doc.url}" style="max-width:100%;max-height:70vh;border-radius:8px;display:block;margin:0 auto;" alt="${doc.name}"/>`;
  } else if (isPDF) {
    body.innerHTML = `<iframe src="${doc.url}" style="width:100%;height:70vh;border:none;border-radius:8px;"></iframe>`;
  } else {
    body.innerHTML = `<p style="text-align:center;padding:40px;color:var(--muted);">Preview not available for this file type.<br/><a href="${doc.url}" target="_blank" download="${doc.name}" style="color:var(--accent);font-weight:700;">Click here to download</a></p>`;
  }
  modal.classList.add('open');
}
function closePreview() {
  document.getElementById('previewModal').classList.remove('open');
  document.getElementById('previewBody').innerHTML = '';
}

// ── Upload modal ──────────────────────────────────────────
function openUploadModal() { document.getElementById('uploadModal').classList.add('open'); }
function closeUploadModal() { document.getElementById('uploadModal').classList.remove('open'); document.getElementById('uploadForm').reset(); resetProgress(); }

function resetProgress() {
  const bar = document.getElementById('uploadBar');
  const pct = document.getElementById('uploadPct');
  if (bar) bar.style.width = '0%';
  if (pct) pct.textContent = '';
  const prog = document.getElementById('uploadProgress');
  if (prog) prog.style.display = 'none';
}

// ── Upload logic ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initDocFirebase();

  // Category filter buttons
  const filters = document.getElementById('docCatFilters');
  if (filters) {
    filters.innerHTML = `<button class="doc-cat-btn active" data-cat="" onclick="setDocFilter('')">All</button>` +
      DOC_CATEGORIES.map(c => `<button class="doc-cat-btn" data-cat="${c.id}" onclick="setDocFilter('${c.id}')" style="border-color:${c.color};color:${c.color};">${c.icon} ${c.label}</button>`).join('');
  }

  // Upload form
  const form = document.getElementById('uploadForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!docIsEditor) return;
      const file    = document.getElementById('docFile').files[0];
      const cat     = document.getElementById('docCategory').value;
      const desc    = document.getElementById('docDesc').value.trim();
      if (!file) return;
      const btn = form.querySelector('button[type=submit]');
      btn.disabled = true;
      btn.textContent = 'Uploading...';
      const progress = document.getElementById('uploadProgress');
      const bar      = document.getElementById('uploadBar');
      const pct      = document.getElementById('uploadPct');
      if (progress) progress.style.display = 'block';
      const storagePath = `documents/${Date.now()}_${file.name.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
      const ref  = docStorage.ref(storagePath);
      const task = ref.put(file);
      task.on('state_changed',
        snapshot => {
          const p = Math.round(snapshot.bytesTransferred / snapshot.totalBytes * 100);
          if (bar) bar.style.width = p + '%';
          if (pct) pct.textContent = p + '%';
        },
        err => { alert('Upload failed: ' + err.message); btn.disabled = false; btn.textContent = '📤 Upload'; resetProgress(); },
        async () => {
          const url = await task.snapshot.ref.getDownloadURL();
          await docDb.collection('documents').add({
            name:         file.name,
            url,
            storagePath,
            category:     cat,
            description:  desc,
            size:         file.size,
            type:         file.type,
            uploadedBy:   docCurrentUser.email,
            uploadedName: docCurrentUser.displayName || docCurrentUser.email,
            uploadedAt:   firebase.firestore.FieldValue.serverTimestamp()
          });
          btn.disabled = false;
          btn.textContent = '📤 Upload Document';
          closeUploadModal();
        }
      );
    });
  }
});

// ── Delete doc ─────────────────────────────────────────────
async function deleteDoc(id, storagePath) {
  if (!docIsEditor || !confirm('Delete this document permanently? This cannot be undone.')) return;
  try {
    await docDb.collection('documents').doc(id).delete();
    if (storagePath) await docStorage.ref(storagePath).delete().catch(() => {});
  } catch(err) { alert('Error: ' + err.message); }
}
