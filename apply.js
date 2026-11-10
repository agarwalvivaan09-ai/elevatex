// Sends the application form straight to the ElevateX Volunteer Hub (Firestore), where HR reviews it.
// The Firebase web key is public by design; the database rules only allow creating a well-formed application.
(function () {
  const PROJECT = window.EX_FIRESTORE_PROJECT || 'elevate-x-volunteer-dash';
  const KEY = 'AIzaSyDLcanekJNrDYdg6WEpWQmNOvyYXrFG-bM';
  const ENDPOINT = window.EX_FIRESTORE_BASE || 'https://firestore.googleapis.com/v1';
  const form = document.getElementById('applyForm');
  if (!form) return;
  const err = document.getElementById('applyError');
  const btn = document.getElementById('applyBtn');
  const showError = (msg) => { err.textContent = msg; err.hidden = false; err.scrollIntoView({ block: 'center', behavior: 'smooth' }); };
  const str = (v) => (v ? { stringValue: v } : { nullValue: null });

  form.addEventListener('input', () => { err.hidden = true; });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    err.hidden = true;
    const d = new FormData(form);
    const val = (k) => String(d.get(k) || '').trim();
    if (val('website')) { done(); return; } // filled by a bot
    if (val('name').length < 2) return showError('Please add your full name.');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val('email'))) return showError('Please check your email address.');
    if (!val('school')) return showError('Please tell us your school.');
    if (val('why').length < 10) return showError('Please write a line or two about why you want to join.');
    if (!d.get('consent')) return showError('Please tick the box at the bottom to agree.');
    try {
      const last = Number(localStorage.getItem('ex-applied') || 0);
      if (Date.now() - last < 60000) { done(); return; }
    } catch (_) { /* storage unavailable */ }

    btn.disabled = true;
    btn.textContent = 'Sending…';
    const id = Array.from(crypto.getRandomValues(new Uint8Array(10)), (b) => b.toString(16).padStart(2, '0')).join('');
    const name = `projects/${PROJECT}/databases/(default)/documents/applications/${id}`;
    const fields = {
      name: str(val('name')),
      email: str(val('email').toLowerCase()),
      phone: str(val('phone')),
      school: str(val('school')),
      grade: str(val('grade')),
      city: str(val('city')),
      departments: { arrayValue: { values: d.getAll('departments').map((x) => ({ stringValue: String(x) })) } },
      why: str(val('why')),
      heard: str(val('heard')),
      availability: str(val('availability')),
      consent: { booleanValue: true },
      status: { stringValue: 'new' },
    };
    try {
      const res = await fetch(`${ENDPOINT}/projects/${PROJECT}/databases/(default)/documents:commit?key=${KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          writes: [{
            update: { name, fields },
            currentDocument: { exists: false },
            updateTransforms: [{ fieldPath: 'createdAt', setToServerValue: 'REQUEST_TIME' }],
          }],
        }),
      });
      if (!res.ok) throw new Error(String(res.status));
      try { localStorage.setItem('ex-applied', String(Date.now())); } catch (_) { /* ignore */ }
      done();
    } catch (_) {
      btn.disabled = false;
      btn.textContent = 'Send application';
      showError("Sorry, that didn't go through. Check your connection and try again, or email elevate.x.20.25.ad@gmail.com.");
    }
  });

  function done() {
    form.hidden = true;
    const ok = document.getElementById('applyDone');
    ok.hidden = false;
    ok.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }
})();
