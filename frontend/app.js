const state = {
  sessionId: null,
  recorder: new window.WavRecorder(),
  recording: false,
  timerHandle: null,
  startedAt: null,
  audioUploaded: false,
};

const el = (id) => document.getElementById(id);

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed: ${response.status}`);
  return data;
}

function setStatus(message, kind = '') {
  el('status').textContent = message;
  el('status').className = `status ${kind}`;
}

async function ensureSession() {
  if (state.sessionId) return state.sessionId;
  const payload = await request('/api/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: el('title').value || 'Learning Session' }),
  });
  state.sessionId = payload.id;
  el('sessionId').textContent = payload.id;
  return state.sessionId;
}

async function uploadMaterials() {
  const files = [...el('materials').files];
  if (!files.length) return;
  const id = await ensureSession();
  const body = new FormData();
  files.forEach((file) => body.append('files', file));
  setStatus('Uploading reference material...');
  const result = await request(`/api/sessions/${id}/materials`, { method: 'POST', body });
  el('materialList').innerHTML = result.materials.map((name) => `<span class="chip">${escapeHtml(name)}</span>`).join('');
  setStatus('Reference material saved locally.', 'ok');
}

function updateTimer() {
  const seconds = Math.floor((Date.now() - state.startedAt) / 1000);
  const mm = String(Math.floor(seconds / 60)).padStart(2, '0');
  const ss = String(seconds % 60).padStart(2, '0');
  el('timer').textContent = `${mm}:${ss}`;
}

async function startRecording() {
  await ensureSession();
  await state.recorder.start();
  state.recording = true;
  state.audioUploaded = false;
  state.startedAt = Date.now();
  state.timerHandle = setInterval(updateTimer, 250);
  el('recordButton').classList.add('active');
  el('recordLabel').textContent = 'STOP TRACE';
  el('recordStatus').textContent = 'Recording locally in this browser tab.';
}

async function stopRecording() {
  const result = await state.recorder.stop();
  state.recording = false;
  clearInterval(state.timerHandle);
  el('recordButton').classList.remove('active');
  el('recordLabel').textContent = 'START TRACE';
  el('recordStatus').textContent = 'Recording stopped. Saving WAV locally...';
  if (!result) return;

  const body = new FormData();
  body.append('audio', result.blob, 'learning-trace.wav');
  body.append('duration_seconds', String(result.duration));
  await request(`/api/sessions/${state.sessionId}/audio`, { method: 'POST', body });
  state.audioUploaded = true;
  el('recordStatus').textContent = `Audio saved locally (${Math.round(result.duration)}s).`;
}

async function finishSession() {
  try {
    const id = await ensureSession();
    if (state.recording) await stopRecording();

    const manual = el('manualTranscript').value.trim();
    if (manual) {
      setStatus('Saving manual transcript...');
      await request(`/api/sessions/${id}/transcript/manual`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: manual }),
      });
    }

    setStatus('Running Cognitive Engine and Concept Engine...');
    const result = await request(`/api/sessions/${id}/finish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asr_provider: el('asrProvider').value }),
    });
    renderResults(result);
    setStatus('Diagnosis complete.', 'ok');
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

function renderResults(result) {
  el('results').classList.remove('hidden');
  const primary = result.cognitive.primary_bottleneck || {};
  el('bottleneck').textContent = primary.label || 'Insufficient evidence';
  el('observation').textContent = primary.hypothesis || primary.observation || '';
  const conf = Number(primary.confidence || 0);
  el('confidence').textContent = `${Math.round(conf * 100)}%`;
  el('evidence').innerHTML = (primary.evidence || []).map((q) => `<blockquote>${escapeHtml(q)}</blockquote>`).join('') || '<p class="muted">No strong evidence extracted.</p>';
  el('intervention').innerHTML = (primary.intervention || []).map((x) => `<li>${escapeHtml(x)}</li>`).join('');

  el('conceptOverview').textContent = result.concepts.overview || '';
  const concepts = result.concepts.concepts || [];
  el('concepts').innerHTML = concepts.length
    ? concepts.map((item) => `
      <div class="concept-item">
        <div class="row between"><strong>${escapeHtml(item.concept || '')}</strong><span class="badge ${escapeHtml(item.status || '')}">${escapeHtml(item.status || '')}</span></div>
        <p>${escapeHtml(item.student_understanding || '')}</p>
        <small>${escapeHtml(item.correction || '')}</small>
      </div>`).join('')
    : '<p class="muted">No grounded concept evaluation available.</p>';

  el('report').textContent = result.report_markdown || '';
  el('downloadReport').href = `/api/sessions/${state.sessionId}/report.md`;
  el('results').scrollIntoView({ behavior: 'smooth' });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

el('createSession').addEventListener('click', async () => {
  try {
    state.sessionId = null;
    await ensureSession();
    setStatus('New local session created.', 'ok');
  } catch (error) {
    setStatus(error.message, 'error');
  }
});

el('materials').addEventListener('change', () => uploadMaterials().catch((error) => setStatus(error.message, 'error')));
el('recordButton').addEventListener('click', () => {
  const action = state.recording ? stopRecording() : startRecording();
  action.catch((error) => {
    el('recordStatus').textContent = error.message;
    setStatus(error.message, 'error');
  });
});
el('finish').addEventListener('click', finishSession);

request('/api/health')
  .then((health) => {
    if ([...el('asrProvider').options].some((option) => option.value === health.default_asr)) {
      el('asrProvider').value = health.default_asr;
    }
    el('health').textContent = health.llm_configured ? 'Local service ready - semantic analysis on' : 'Local service ready - heuristic mode';
  })
  .catch(() => { el('health').textContent = 'Local service unavailable'; });
