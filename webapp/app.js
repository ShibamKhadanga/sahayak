/* ================================================================
 * Sahayak Operator Console — App Logic
 * ================================================================
 * Talks to the same Flask backend the WhatsApp bot talks to. There is
 * no separate "dashboard state" — every view here is a fetch against
 * /api/sessions or /api/session/<id>, which read the one shared
 * session_store.py file. Polling every few seconds is what makes a
 * document sent on WhatsApp show up here without a page reload.
 * ================================================================ */

let API_BASE = localStorage.getItem('sahayak_api_base') || 'http://localhost:5000';
let currentSessions = [];
let openSessionId = null;
let pollTimer = null;
const POLL_MS = 4000;

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

function apiUrl(path){ return API_BASE.replace(/\/$/, '') + path; }

/* ── API helpers ─────────────────────────────────────────────────── */
async function apiGet(path){
  const res = await fetch(apiUrl(path));
  return res.json();
}

async function apiPostJson(path, body){
  const res = await fetch(apiUrl(path), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body || {}),
  });
  return res.json();
}

async function apiPostForm(path, formData){
  const res = await fetch(apiUrl(path), { method: 'POST', body: formData });
  return res.json();
}

/* ── Toast notification system ───────────────────────────────────── */
function showToast(message, type = 'info'){
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

/* ── Backend status ──────────────────────────────────────────────── */
async function checkBackend(){
  const dot = $('#statusDot');
  const text = $('#statusText');
  try {
    const data = await apiGet('/api/health');
    if(data && data.status === 'healthy'){
      dot.className = 'status-dot ok';
      text.textContent = 'Backend connected';
    } else {
      throw new Error('unexpected response');
    }
  } catch(e){
    dot.className = 'status-dot error';
    text.textContent = 'Backend unreachable';
  }
}

/* ── Forms catalog ───────────────────────────────────────────────── */
let formsCatalog = [];

async function loadForms(){
  try {
    const data = await apiGet('/api/forms');
    if(!data.success) return;
    formsCatalog = data.forms;

    const select = $('#formSelect');
    select.innerHTML = formsCatalog.map(f => `<option value="${f.id}">${f.name}</option>`).join('');

    const list = $('#formsList');
    list.innerHTML = formsCatalog.map(f => `
      <li>
        <span class="fname">${f.name}</span>
        <span class="fcat muted">${f.category} · ${f.documents.length} docs · ${f.fields.length} fields</span>
      </li>
    `).join('');
  } catch(e){
    // Forms will load on next poll
  }
}

$('#startSessionBtn').addEventListener('click', async () => {
  const formId = $('#formSelect').value;
  if(!formId) return;
  const data = await apiPostJson('/api/session/start', { form_id: formId });
  if(data.success){
    showToast('Session started successfully', 'success');
    await refreshSessions();
    openSession(data.session.id);
  } else {
    showToast('Could not start session: ' + (data.error || 'unknown error'), 'error');
  }
});

/* ── Sessions ledger ─────────────────────────────────────────────── */
function fmtTime(iso){
  if(!iso) return '';
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' · ' + d.toLocaleDateString();
}

function statusLabel(state){
  return {
    SELECT_FORM: 'Choosing form',
    COLLECT_DOCS: 'Collecting docs',
    COLLECT_FIELDS: 'Collecting fields',
    COMPLETE: 'Complete',
  }[state] || state;
}

async function refreshSessions(){
  try {
    const data = await apiGet('/api/sessions');
    if(!data.success) return;
    currentSessions = data.sessions;
    renderLedger();
    updateStats();

    if(openSessionId){
      const still = currentSessions.find(s => s.id === openSessionId);
      if(still) renderDetail(still);
    }
  } catch(e){
    // Will retry on next poll
  }
}

function updateStats(){
  const total = currentSessions.length;
  const complete = currentSessions.filter(s => s.state === 'COMPLETE').length;
  const inProgress = total - complete;
  const whatsapp = currentSessions.filter(s => s.channel === 'whatsapp').length;

  $('#statTotal').textContent = total;
  $('#statInProgress').textContent = inProgress;
  $('#statComplete').textContent = complete;
  $('#statWhatsApp').textContent = whatsapp;
  $('#sessionCount').textContent = `${total} session${total === 1 ? '' : 's'}`;
}

function renderLedger(){
  const body = $('#ledgerBody');

  if(currentSessions.length === 0){
    body.innerHTML = `<tr class="empty-row"><td colspan="8">No sessions yet — start one from the sidebar, or message the WhatsApp line.</td></tr>`;
    return;
  }

  body.innerHTML = currentSessions.map((s, i) => {
    const p = s.progress || { percent: 0 };
    const chanClass = s.channel === 'whatsapp' ? 'chan-whatsapp' : 'chan-web';
    const chanLabel = s.channel === 'whatsapp' ? 'WhatsApp' : 'Web';
    return `
      <tr data-id="${s.id}">
        <td class="col-no">${i + 1}</td>
        <td><span class="chan-badge ${chanClass}">${chanLabel}</span></td>
        <td class="mono" style="font-size:12px">${s.id}</td>
        <td>${s.form_name || '<span class="muted">not chosen</span>'}</td>
        <td>
          <span class="progress-mini-track"><span class="progress-mini-fill" style="width:${p.percent}%"></span></span>
          <span class="muted" style="font-size:12px">${p.percent}%</span>
        </td>
        <td><span class="status-tag status-${s.state}">${statusLabel(s.state)}</span></td>
        <td class="muted" style="font-size:12px">${fmtTime(s.updated_at)}</td>
        <td>
          <button class="btn-danger btn-delete" data-delete-id="${s.id}" title="Delete session">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="12" height="12"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
            Delete
          </button>
        </td>
      </tr>
    `;
  }).join('');

  // Row click → open detail (but not on delete button)
  $$('#ledgerBody tr[data-id]').forEach(row => {
    row.addEventListener('click', (e) => {
      if(e.target.closest('.btn-delete')) return;
      openSession(row.getAttribute('data-id'));
    });
  });

  // Delete buttons
  $$('.btn-delete[data-delete-id]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const sid = btn.getAttribute('data-delete-id');
      if(!confirm(`Delete session ${sid}? This cannot be undone.`)) return;
      try {
        const res = await fetch(apiUrl(`/api/session/${encodeURIComponent(sid)}/delete`), { method: 'POST' });
        const data = await res.json();
        if(data.success){
          if(openSessionId === sid) closeDetail();
          showToast('Session deleted', 'success');
          await refreshSessions();
        } else {
          showToast('Delete failed: ' + (data.error || 'unknown error'), 'error');
        }
      } catch(err){
        showToast('Delete failed: ' + err.message, 'error');
      }
    });
  });
}

/* ── Detail panel ────────────────────────────────────────────────── */
function openSession(sessionId){
  openSessionId = sessionId;
  const session = currentSessions.find(s => s.id === sessionId);
  if(session) renderDetail(session);
  $('#detailPanel').classList.remove('hidden');
  $('#detailOverlay').classList.remove('hidden');
}

function closeDetail(){
  openSessionId = null;
  $('#detailPanel').classList.add('hidden');
  $('#detailOverlay').classList.add('hidden');
}

$('#closeDetailBtn').addEventListener('click', closeDetail);
$('#detailOverlay').addEventListener('click', closeDetail);

function renderDetail(session){
  $('#detailFormName').textContent = session.form_name || 'No form chosen yet';
  $('#detailSessionId').textContent = session.id;

  const p = session.progress || { percent: 0 };
  $('#detailProgressFill').style.width = p.percent + '%';
  $('#detailProgressLabel').textContent = p.percent + '%';

  // Documents
  $('#detailDocs').innerHTML = (session.doc_rows || []).map(d => `
    <li>
      <span class="doc-status ${d.received ? 'received' : 'pending'}">${d.received ? '✓' : '○'}</span>
      <span class="doc-name">${d.label}${d.filename ? ` <span class="muted">(${d.filename})</span>` : ''}</span>
      ${!d.received ? `<label class="doc-upload-label">Upload
          <input type="file" hidden class="doc-upload-input" data-doc-type="${d.type}">
        </label>` : ''}
    </li>
  `).join('') || '<li class="muted">No form chosen yet</li>';

  $$('.doc-upload-input').forEach(input => {
    input.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if(!file) return;
      const docType = input.getAttribute('data-doc-type');
      const fd = new FormData();
      fd.append('file', file);
      fd.append('doc_type', docType);
      const data = await apiPostForm(`/api/session/${encodeURIComponent(session.id)}/document`, fd);
      if(data.success){
        showToast('Document uploaded', 'success');
        await refreshSessions();
      } else {
        showToast('Upload failed: ' + (data.error || 'unknown error'), 'error');
      }
    });
  });

  // Fields
  $('#detailFields').innerHTML = (session.field_rows || []).map(f => `
    <div class="field-row">
      <label>
        <span>${f.label}${f.required ? ' *' : ''}</span>
        ${f.source ? `<span class="field-source-tag ${f.source}">${f.source === 'document' ? 'from doc' : 'manual'}</span>` : ''}
      </label>
      <input type="text" data-field-key="${f.key}" value="${(f.value || '').replace(/"/g, '&quot;')}" placeholder="Not filled yet">
    </div>
  `).join('') || '<p class="muted">No form chosen yet</p>';

  $$('#detailFields input').forEach(input => {
    input.addEventListener('change', async () => {
      const fieldKey = input.getAttribute('data-field-key');
      const data = await apiPostJson(`/api/session/${encodeURIComponent(session.id)}/field`, {
        field_key: fieldKey, value: input.value,
      });
      if(data.success){
        showToast('Field updated', 'success');
        await refreshSessions();
      }
    });
  });

  // Conversation history
  $('#detailHistory').innerHTML = (session.history || []).slice(-30).map(h => `
    <div class="history-msg ${h.role === 'user' ? 'user' : 'bot'}">${escapeHtml(h.text)}</div>
  `).join('') || '<p class="muted">No conversation yet</p>';

  // Completion stub
  $('#stubSection').classList.toggle('hidden', session.state !== 'COMPLETE');
}

$('#resetSessionBtn').addEventListener('click', async () => {
  if(!openSessionId) return;
  if(!confirm('Reset this session? Collected documents and fields will be cleared.')) return;
  const data = await apiPostJson(`/api/session/${encodeURIComponent(openSessionId)}/reset`, {});
  if(data.success){
    showToast('Session reset', 'info');
    await refreshSessions();
  }
});

// Delete from detail panel
$('#deleteSessionBtn').addEventListener('click', async () => {
  if(!openSessionId) return;
  if(!confirm(`Delete session ${openSessionId}? This cannot be undone.`)) return;
  try {
    const res = await fetch(apiUrl(`/api/session/${encodeURIComponent(openSessionId)}/delete`), { method: 'POST' });
    const data = await res.json();
    if(data.success){
      showToast('Session deleted', 'success');
      closeDetail();
      await refreshSessions();
    } else {
      showToast('Delete failed: ' + (data.error || 'unknown'), 'error');
    }
  } catch(err){
    showToast('Delete failed: ' + err.message, 'error');
  }
});

$('#printStubBtn').addEventListener('click', () => {
  const session = currentSessions.find(s => s.id === openSessionId);
  if(!session) return;
  const rows = (session.field_rows || [])
    .filter(f => f.value)
    .map(f => `<tr><td>${f.label}</td><td>${escapeHtml(f.value)}</td></tr>`)
    .join('');
  const win = window.open('', '_blank');
  win.document.write(`
    <html><head><title>${session.form_name} — Summary</title>
    <style>
      body{ font-family: 'Inter', system-ui, sans-serif; padding: 40px; color: #0f172a; }
      h1{ font-size: 20px; border-bottom: 2px solid #0d9488; padding-bottom: 10px; }
      table{ width: 100%; border-collapse: collapse; margin-top: 20px; }
      td{ padding: 8px 6px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
      td:first-child{ font-weight: 600; width: 45%; }
      .meta{ font-size: 12px; color: #94a3b8; }
    </style></head>
    <body>
      <h1>${session.form_name}</h1>
      <p class="meta">Session ${session.id} · generated ${new Date().toLocaleString()}</p>
      <table>${rows}</table>
    </body></html>
  `);
  win.document.close();
  win.print();
});

function escapeHtml(str){
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/* ── WhatsApp simulator widget ──────────────────────────────────── */
const SIM_PHONE = 'whatsapp:+910000000000';
$('#waPhoneLabel').textContent = SIM_PHONE;

$('#waToggleBtn').addEventListener('click', () => {
  $('#waWidget').classList.add('open');
  $('#waWidget').classList.remove('collapsed');
});

$('#waCloseBtn').addEventListener('click', () => {
  $('#waWidget').classList.remove('open');
  $('#waWidget').classList.add('collapsed');
});

function addWaMessage(text, direction){
  const el = document.createElement('div');
  el.className = `wa-msg ${direction}`;
  el.textContent = text;
  $('#waMessages').appendChild(el);
  $('#waMessages').scrollTop = $('#waMessages').scrollHeight;
}

$('#waForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = $('#waTextInput');
  const text = input.value.trim();
  const fileInput = $('#waFileInput');
  const file = fileInput.files[0];
  if(!text && !file) return;

  addWaMessage(text || `📎 ${file.name}`, 'out');
  input.value = '';

  const fd = new FormData();
  fd.append('phone', SIM_PHONE);
  fd.append('text', text);
  if(file) fd.append('file', file);
  fileInput.value = '';

  try {
    const data = await apiPostForm('/api/whatsapp/simulate', fd);
    if(data.success){
      addWaMessage(data.reply, 'in');
      await refreshSessions();
    } else {
      addWaMessage('⚠️ ' + (data.error || 'Something went wrong'), 'in');
    }
  } catch(err){
    addWaMessage('⚠️ Could not reach backend', 'in');
  }
});

$('#waAttachBtn').addEventListener('click', () => $('#waFileInput').click());
$('#waFileInput').addEventListener('change', () => {
  if($('#waFileInput').files[0]) $('#waForm').requestSubmit();
});

/* ── API base override ──────────────────────────────────────────── */
$('#apiBaseInput').value = API_BASE;
$('#apiBaseInput').addEventListener('change', (e) => {
  API_BASE = e.target.value.trim() || 'http://localhost:5000';
  localStorage.setItem('sahayak_api_base', API_BASE);
  showToast('API base updated', 'info');
  bootstrap();
});

/* ── Boot ────────────────────────────────────────────────────────── */
async function bootstrap(){
  await checkBackend();
  await loadForms();
  await refreshSessions();
  if(pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(() => { checkBackend(); refreshSessions(); }, POLL_MS);
}

bootstrap();
