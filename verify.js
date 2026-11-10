// Certificate lookup. Reads the ElevateX certificate registry (a Google Sheet shared as
// "anyone with the link can view") straight from Google every time the page loads, so any
// change to the sheet shows up here immediately. Not connected to the Volunteer Hub.
(function () {
  const SHEET = '1Y9_ZSJSbBYdHdLUxm2c-4R0Zm3UsfUSlPfkcIKJ3O04';
  const form = document.getElementById('verifyForm');
  if (!form) return;
  const status = document.getElementById('verifyStatus');
  const out = document.getElementById('verifyResults');
  let headers = [];
  let rows = [];
  let ready = false;

  const norm = (s) => String(s ?? '').toLowerCase().replace(/\s+/g, ' ').trim();
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Google's chart-data endpoint supports JSONP, which works from any website without extra setup.
  window.exRegistry = function (resp) {
    try {
      if (resp.status === 'error') throw new Error('sheet');
      const t = resp.table;
      headers = t.cols.map((c, i) => (c.label || '').trim() || `Column ${i + 1}`);
      rows = t.rows.map((r) => (r.c || []).map((cell) => (cell == null ? '' : cell.f != null ? cell.f : cell.v != null ? cell.v : '')));
      // If the sheet's first row wasn't recognised as headers, use it.
      if (t.cols.every((c) => !c.label) && rows.length) { headers = rows[0].map((h, i) => String(h).trim() || `Column ${i + 1}`); rows = rows.slice(1); }
      rows = rows.filter((r) => r.some((v) => String(v).trim() !== ''));
      ready = true;
      status.textContent = `${rows.length} certificate${rows.length === 1 ? '' : 's'} in the registry. Search by ID or name.`;
      const q = new URLSearchParams(location.search).get('q');
      if (q) { document.getElementById('verifyQ').value = q; search(q); }
    } catch (_) { fail(); }
  };
  function fail() {
    status.innerHTML = 'We couldn\'t load the registry right now. You can <a href="https://docs.google.com/spreadsheets/d/' + SHEET + '" target="_blank" rel="noopener">open it directly</a>.';
  }
  const s = document.createElement('script');
  s.src = `https://docs.google.com/spreadsheets/d/${SHEET}/gviz/tq?tqx=responseHandler:exRegistry&headers=1&_=${Date.now()}`;
  s.onerror = fail;
  document.body.appendChild(s);
  setTimeout(() => { if (!ready) fail(); }, 12000);

  function search(raw) {
    const q = norm(raw);
    if (q.length < 3) { out.innerHTML = ''; status.textContent = 'Type at least 3 characters.'; return; }
    // Exact match on any cell (an ID) first; otherwise names containing what was typed.
    let hits = rows.filter((r) => r.some((v) => norm(v) === q));
    if (!hits.length) hits = rows.filter((r) => r.some((v) => norm(v).includes(q)));
    if (!hits.length) {
      out.innerHTML = '<div class="verify-card none"><b>No certificate found</b><p>Check the spelling or the ID. If you believe this is a real ElevateX certificate, write to us.</p></div>';
      status.textContent = '';
      return;
    }
    status.textContent = `${hits.length} matching record${hits.length === 1 ? '' : 's'}.`;
    out.innerHTML = hits.slice(0, 20).map((r) => '<div class="verify-card"><span class="ok">✓ Listed in the ElevateX registry</span><dl>' +
      headers.map((h, i) => (String(r[i] ?? '').trim() ? `<dt>${esc(h)}</dt><dd>${esc(r[i])}</dd>` : '')).join('') + '</dl></div>').join('');
  }
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = document.getElementById('verifyQ').value;
    if (!ready) { status.textContent = 'Still loading the registry, try again in a moment.'; return; }
    search(q);
    history.replaceState(null, '', `?q=${encodeURIComponent(q)}`);
  });
})();
