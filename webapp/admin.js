/* ================================================================
 * Sahayak Admin Panel — Logic
 * ================================================================ */

let API_BASE = localStorage.getItem('sahayak_api_base') || 'http://localhost:5000';
let currentTab = 'forms';
let formsData = [];
let docTypesData = {};
let fieldsData = [];
let editingId = null; // null = creating new, string = editing existing

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

function apiUrl(path) { return API_BASE.replace(/\/$/, '') + path; }

/* ── Toast ───────────────────────────────────────────────────── */
function showToast(message, type = 'info') {
  const container = $('#toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ── Tab Switching ───────────────────────────────────────────── */
$$('.nav-item[data-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    currentTab = btn.getAttribute('data-tab');
    $$('.nav-item[data-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    $$('.tab-panel').forEach(p => p.classList.remove('active'));
    $(`#tab-${currentTab}`).classList.add('active');
    const titles = { forms: 'Forms Catalog', doctypes: 'Document Types', fields: 'Field Library' };
    $('#tabTitle').textContent = titles[currentTab] || 'Admin';
  });
});

/* ── API Helpers ─────────────────────────────────────────────── */
async function apiGet(path) {
  const res = await fetch(apiUrl(path));
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(apiUrl(path), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function apiPut(path, body) {
  const res = await fetch(apiUrl(path), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function apiDelete(path) {
  const res = await fetch(apiUrl(path), { method: 'DELETE' });
  return res.json();
}

/* ── Load Data ───────────────────────────────────────────────── */
async function loadForms() {
  try {
    const data = await apiGet('/api/forms');
    if (data.success) {
      formsData = data.forms;
      renderFormsTable();
    }
  } catch (e) { showToast('Could not load forms', 'error'); }
}

async function loadDocTypes() {
  try {
    const data = await apiGet('/api/admin/document-types');
    if (data.success) {
      docTypesData = data.document_types;
      renderDocTypesTable();
    }
  } catch (e) { showToast('Could not load document types', 'error'); }
}

async function loadFields() {
  try {
    const data = await apiGet('/api/admin/fields');
    if (data.success) {
      fieldsData = data.fields;
      renderFieldsTable();
    }
  } catch (e) { showToast('Could not load fields', 'error'); }
}

/* ── Render Tables ───────────────────────────────────────────── */
function renderFormsTable() {
  const body = $('#formsTableBody');
  if (formsData.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="7">No forms yet</td></tr>';
    return;
  }
  body.innerHTML = formsData.map((f, i) => `
    <tr>
      <td class="col-no">${i + 1}</td>
      <td><code style="font-size:12px">${esc(f.id)}</code></td>
      <td>${esc(f.name)}</td>
      <td><span class="cat-badge">${esc(f.category)}</span></td>
      <td class="count-chip">${f.documents.length} docs</td>
      <td class="count-chip">${f.fields.length} fields</td>
      <td>
        <div class="row-actions">
          <button class="btn-icon" title="Edit" onclick="editForm('${esc(f.id)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon" title="Delete" onclick="deleteForm('${esc(f.id)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

function renderDocTypesTable() {
  const body = $('#docTypesTableBody');
  const entries = Object.entries(docTypesData);
  if (entries.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="4">No document types</td></tr>';
    return;
  }
  body.innerHTML = entries.map(([key, label], i) => `
    <tr>
      <td class="col-no">${i + 1}</td>
      <td><code style="font-size:12px">${esc(key)}</code></td>
      <td>${esc(label)}</td>
      <td>
        <div class="row-actions">
          <button class="btn-icon" title="Edit" onclick="editDocType('${esc(key)}', '${esc(label)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon" title="Delete" onclick="deleteDocType('${esc(key)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

function renderFieldsTable() {
  const body = $('#fieldsTableBody');
  if (fieldsData.length === 0) {
    body.innerHTML = '<tr class="empty-row"><td colspan="6">No fields</td></tr>';
    return;
  }
  body.innerHTML = fieldsData.map((f, i) => `
    <tr>
      <td class="col-no">${i + 1}</td>
      <td><code style="font-size:12px">${esc(f.field_key)}</code></td>
      <td>${esc(f.label)}</td>
      <td class="muted" style="font-size:12px">${f.source_key || '—'}</td>
      <td><span class="req-dot ${f.required ? 'yes' : 'no'}"></span></td>
      <td>
        <div class="row-actions">
          <button class="btn-icon" title="Edit" onclick="editField('${esc(f.field_key)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button class="btn-icon" title="Delete" onclick="deleteField('${esc(f.field_key)}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="16" height="16"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

/* ── Modal Helpers ────────────────────────────────────────────── */
function openModal(id) {
  $(id).classList.remove('hidden');
  $('#modalOverlay').classList.remove('hidden');
}

function closeModals() {
  $$('.modal').forEach(m => m.classList.add('hidden'));
  $('#modalOverlay').classList.add('hidden');
  editingId = null;
}

$$('.modal-close-btn').forEach(btn => btn.addEventListener('click', closeModals));
$('#modalOverlay').addEventListener('click', closeModals);

/* ── Add Button ──────────────────────────────────────────────── */
$('#addBtn').addEventListener('click', () => {
  editingId = null;
  if (currentTab === 'forms') {
    $('#formModalTitle').textContent = 'Add Form';
    $('#fmId').value = '';
    $('#fmId').disabled = false;
    $('#fmName').value = '';
    $('#fmCategory').value = '';
    $('#fmDocs').value = '';
    $('#fmFields').value = '';
    showChipHelpers();
    openModal('#formModal');
  } else if (currentTab === 'doctypes') {
    $('#docTypeModalTitle').textContent = 'Add Document Type';
    $('#dtKey').value = '';
    $('#dtKey').disabled = false;
    $('#dtLabel').value = '';
    openModal('#docTypeModal');
  } else if (currentTab === 'fields') {
    $('#fieldModalTitle').textContent = 'Add Field';
    $('#flKey').value = '';
    $('#flKey').disabled = false;
    $('#flLabel').value = '';
    $('#flSource').value = '';
    $('#flRequired').checked = false;
    openModal('#fieldModal');
  }
});

/* ── Chip Helpers (show available doc/field keys for form editor) ── */
function showChipHelpers() {
  const docKeys = Object.keys(docTypesData);
  const fieldKeys = fieldsData.map(f => f.field_key);

  $('#fmDocsHelp').innerHTML = docKeys.map(k =>
    `<span class="chip" onclick="appendChip('fmDocs','${k}')">${k}</span>`
  ).join('');

  $('#fmFieldsHelp').innerHTML = fieldKeys.map(k =>
    `<span class="chip" onclick="appendChip('fmFields','${k}')">${k}</span>`
  ).join('');
}

window.appendChip = function(inputId, key) {
  const input = $(`#${inputId}`);
  const vals = input.value ? input.value.split(',').map(s => s.trim()).filter(Boolean) : [];
  if (!vals.includes(key)) {
    vals.push(key);
    input.value = vals.join(', ');
  }
};

/* ── Forms CRUD ──────────────────────────────────────────────── */
window.editForm = function(formId) {
  const form = formsData.find(f => f.id === formId);
  if (!form) return;
  editingId = formId;
  $('#formModalTitle').textContent = 'Edit Form';
  $('#fmId').value = form.id;
  $('#fmId').disabled = true;
  $('#fmName').value = form.name;
  $('#fmCategory').value = form.category;
  $('#fmDocs').value = form.documents.join(', ');
  $('#fmFields').value = form.fields.join(', ');
  showChipHelpers();
  openModal('#formModal');
};

window.deleteForm = async function(formId) {
  if (!confirm(`Delete form "${formId}"? This cannot be undone.`)) return;
  const data = await apiDelete(`/api/admin/forms/${encodeURIComponent(formId)}`);
  if (data.success) {
    showToast('Form deleted', 'success');
    await loadForms();
  } else {
    showToast('Delete failed: ' + (data.error || 'unknown'), 'error');
  }
};

$('#formEditorForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = $('#fmId').value.trim();
  const name = $('#fmName').value.trim();
  const category = $('#fmCategory').value.trim();
  const docs = $('#fmDocs').value.split(',').map(s => s.trim()).filter(Boolean);
  const fields = $('#fmFields').value.split(',').map(s => s.trim()).filter(Boolean);

  if (!id || !name || !category) {
    showToast('Please fill all required fields', 'error');
    return;
  }

  let data;
  if (editingId) {
    data = await apiPut(`/api/admin/forms/${encodeURIComponent(editingId)}`, { name, category, documents: docs, fields });
  } else {
    data = await apiPost('/api/admin/forms', { id, name, category, documents: docs, fields });
  }

  if (data.success) {
    showToast(editingId ? 'Form updated' : 'Form created', 'success');
    closeModals();
    await loadForms();
  } else {
    showToast('Error: ' + (data.error || 'unknown'), 'error');
  }
});

/* ── Document Types CRUD ─────────────────────────────────────── */
window.editDocType = function(key, label) {
  editingId = key;
  $('#docTypeModalTitle').textContent = 'Edit Document Type';
  $('#dtKey').value = key;
  $('#dtKey').disabled = true;
  $('#dtLabel').value = label;
  openModal('#docTypeModal');
};

window.deleteDocType = async function(key) {
  if (!confirm(`Delete document type "${key}"?`)) return;
  const data = await apiDelete(`/api/admin/document-types/${encodeURIComponent(key)}`);
  if (data.success) {
    showToast('Document type deleted', 'success');
    await loadDocTypes();
  } else {
    showToast('Delete failed: ' + (data.error || 'unknown'), 'error');
  }
};

$('#docTypeEditorForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const key = $('#dtKey').value.trim();
  const label = $('#dtLabel').value.trim();
  if (!key || !label) return;

  const data = await apiPost('/api/admin/document-types', { type_key: key, label });
  if (data.success) {
    showToast(editingId ? 'Document type updated' : 'Document type added', 'success');
    closeModals();
    await loadDocTypes();
  } else {
    showToast('Error: ' + (data.error || 'unknown'), 'error');
  }
});

/* ── Fields CRUD ─────────────────────────────────────────────── */
window.editField = function(fieldKey) {
  const field = fieldsData.find(f => f.field_key === fieldKey);
  if (!field) return;
  editingId = fieldKey;
  $('#fieldModalTitle').textContent = 'Edit Field';
  $('#flKey').value = field.field_key;
  $('#flKey').disabled = true;
  $('#flLabel').value = field.label;
  $('#flSource').value = field.source_key || '';
  $('#flRequired').checked = field.required;
  openModal('#fieldModal');
};

window.deleteField = async function(fieldKey) {
  if (!confirm(`Delete field "${fieldKey}"?`)) return;
  const data = await apiDelete(`/api/admin/fields/${encodeURIComponent(fieldKey)}`);
  if (data.success) {
    showToast('Field deleted', 'success');
    await loadFields();
  } else {
    showToast('Delete failed: ' + (data.error || 'unknown'), 'error');
  }
};

$('#fieldEditorForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const key = $('#flKey').value.trim();
  const label = $('#flLabel').value.trim();
  const source = $('#flSource').value.trim() || null;
  const required = $('#flRequired').checked;
  if (!key || !label) return;

  const data = await apiPost('/api/admin/fields', { field_key: key, label, source_key: source, required });
  if (data.success) {
    showToast(editingId ? 'Field updated' : 'Field added', 'success');
    closeModals();
    await loadFields();
  } else {
    showToast('Error: ' + (data.error || 'unknown'), 'error');
  }
});

/* ── Util ─────────────────────────────────────────────────────── */
function esc(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/* ── Boot ─────────────────────────────────────────────────────── */
async function bootstrap() {
  await Promise.all([loadForms(), loadDocTypes(), loadFields()]);
}

bootstrap();
