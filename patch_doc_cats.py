with open('js/docs.js', 'r', encoding='utf-8') as f: c = f.read()

OLD = """const DOC_CATEGORIES = [
  { id:'land',         label:'Land & Property',       icon:'🏛️',  color:'#C8702A' },
  { id:'legal',        label:'Legal Documents',        icon:'⚖️',  color:'#4A6EA8' },
  { id:'municipal',    label:'Municipal & Government', icon:'🏛️',  color:'#5F8269' },
  { id:'construction', label:'Construction & Design',  icon:'🏗️',  color:'#8C4A22' },
  { id:'bills',        label:'Bills & Receipts',       icon:'🧾',  color:'#C48A18' },
  { id:'insurance',    label:'Insurance',              icon:'🛡️',  color:'#059669' },
  { id:'contracts',    label:'Contracts & Agreements', icon:'📜',  color:'#7C3AED' },
  { id:'other',        label:'Other Documents',        icon:'📄',  color:'#78716C' },
];"""

NEW = """const DOC_CATEGORIES = [
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
];"""

c = c.replace(OLD, NEW)
with open('js/docs.js', 'w', encoding='utf-8') as f: f.write(c)
print('  ✓ js/docs.js categories updated')

with open('docs.html', 'r', encoding='utf-8') as f: h = h = f.read()

OLD_SELECT = """          <option value="">Select category...</option>
          <option value="bills">Bills &amp; Receipts</option>
          <option value="contracts">Contracts &amp; Agreements</option>
          <option value="construction">Construction &amp; Design</option>
          <option value="insurance">Insurance</option>
          <option value="land">Land &amp; Property</option>
          <option value="legal">Legal Documents</option>
          <option value="municipal">Municipal &amp; Government</option>
          <option value="other">Other</option>"""

NEW_SELECT = """          <option value="">Select category...</option>
          <option value="bank">Bank &amp; Finance</option>
          <option value="bills">Bills &amp; Receipts</option>
          <option value="payments">Contractor Payments</option>
          <option value="contracts">Contracts &amp; Agreements</option>
          <option value="drawings">Drawings &amp; Plans</option>
          <option value="insurance">Insurance</option>
          <option value="land">Land &amp; Property</option>
          <option value="legal">Legal Documents</option>
          <option value="municipal">Municipal &amp; Permits</option>
          <option value="photos">Photos &amp; Site Progress</option>
          <option value="quotations">Quotations &amp; Estimates</option>
          <option value="technical">Technical Reports (Soil, Structural)</option>
          <option value="utilities">Utility Connections</option>
          <option value="warranties">Warranties &amp; Certificates</option>
          <option value="other">Other</option>"""

h = h.replace(OLD_SELECT, NEW_SELECT)
with open('docs.html', 'w', encoding='utf-8') as f: f.write(h)
print('  ✓ docs.html dropdown updated (15 categories, A-Z)')
