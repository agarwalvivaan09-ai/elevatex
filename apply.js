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
    const body = JSON.stringify({
      writes: [{
        update: { name, fields },
        currentDocument: { exists: false },
        updateTransforms: [{ fieldPath: 'createdAt', setToServerValue: 'REQUEST_TIME' }],
      }],
    });
    // Sent as text/plain so the browser doesn't need a separate permission check (CORS preflight) first.
    // Each try gives up after 15 seconds instead of waiting forever; a second try follows automatically.
    const attempt = async () => {
      const ctrl = typeof AbortController === 'function' ? new AbortController() : null;
      const timer = ctrl && setTimeout(() => ctrl.abort(), 15000);
      try {
        const res = await fetch(`${ENDPOINT}/projects/${PROJECT}/databases/(default)/documents:commit?key=${KEY}`, {
          method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body, signal: ctrl ? ctrl.signal : undefined,
        });
        if (res.ok) return true;
        // The first try reached the server but its reply got lost: the application is already saved.
        const text = await res.text().catch(() => '');
        if (/ALREADY_EXISTS|FAILED_PRECONDITION/.test(text)) return true;
        return false;
      } catch (_) {
        return false;
      } finally {
        if (timer) clearTimeout(timer);
      }
    };
    const slow = setTimeout(() => { btn.textContent = 'Still sending… slow connection'; }, 6000);
    let ok = await attempt();
    if (!ok) { btn.textContent = 'Trying again…'; ok = await attempt(); }
    clearTimeout(slow);
    if (ok) {
      try { localStorage.setItem('ex-applied', String(Date.now())); } catch (_) { /* ignore */ }
      done();
      return;
    }
    btn.disabled = false;
    btn.textContent = 'Send application';
    showError("Sorry, your application couldn't be sent from this connection. Try again on another network (for example mobile data or Wi-Fi), or use the button below to send it by email instead.");
    const mail = document.getElementById('applyMail');
    if (mail) {
      const lines = [['Name', val('name')], ['Email', val('email')], ['Phone', val('phone')], ['School', val('school')], ['Class', val('grade')], ['City', val('city')],
        ['Departments', d.getAll('departments').join(', ')], ['Why I want to join', val('why')], ['How I heard about ElevateX', val('heard')], ['Availability', val('availability')]];
      const text = lines.filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
      mail.href = `mailto:elevate.x.20.25.ad@gmail.com?subject=${encodeURIComponent('Application to join ElevateX: ' + val('name'))}&body=${encodeURIComponent(text)}`;
      mail.hidden = false;
    }
  });

  function done() {
    form.hidden = true;
    const ok = document.getElementById('applyDone');
    ok.hidden = false;
    ok.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }
})();
