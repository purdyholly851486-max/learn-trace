const I18N = {
  en: {
    'hero.eyebrow': 'LOCAL-FIRST LEARNING DIAGNOSIS',
    'hero.subtitle': 'Capture a study session, ground it in your materials, and diagnose learning process plus concept precision.',
    'health.checking': 'Checking local service...',
    'health.on': 'Local service ready - semantic analysis on',
    'health.heuristic': 'Local service ready - heuristic mode',
    'health.off': 'Local service unavailable',
    'settings.title': 'Storage settings',
    'settings.desc': 'Choose where sessions, reference materials, transcripts and reports are saved. Point it at an Obsidian vault folder to open reports as notes.',
    'settings.dataDirLabel': 'Save location (absolute path recommended)',
    'settings.save': 'Save path',
    'settings.reset': 'Reset to default',
    'settings.saved': 'Save location updated.',
    'settings.resetDone': 'Save location reset to default.',
    'settings.defaultNote': 'Default folder inside the project.',
    'settings.customNote': 'Custom location active.',
    'setup.title': 'Session setup',
    'setup.desc': 'Create a local session and add reference material.',
    'setup.titleLabel': 'Session title',
    'setup.create': 'Create session',
    'setup.noSession': 'No session yet',
    'setup.created': 'New local session created.',
    'setup.dropzone': 'Upload PDF / Markdown / TXT',
    'setup.uploading': 'Uploading reference material...',
    'setup.materialSaved': 'Reference material saved locally.',
    'trace.title': 'Capture your learning trace',
    'trace.desc': 'Record your own explanations, questions, corrections, and uncertainty.',
    'trace.start': 'START TRACE',
    'trace.stop': 'STOP TRACE',
    'trace.off': 'Microphone is off.',
    'trace.recording': 'Recording locally in this browser tab.',
    'trace.stopping': 'Recording stopped. Saving WAV locally...',
    'trace.savedPrefix': 'Audio saved locally (',
    'trace.savedSuffix': 's).',
    'trace.asrLabel': 'ASR after stop',
    'trace.asrManual': 'Manual transcript / no ASR model',
    'trace.asrLocal': 'Qwen3-ASR local',
    'trace.asrServer': 'Qwen3-ASR server',
    'trace.manualLabel': 'Optional manual transcript',
    'trace.manualPlaceholder': 'Paste a transcript here to test the diagnosis pipeline without installing Qwen3-ASR.',
    'diagnose.title': 'Generate diagnosis',
    'diagnose.desc': 'Cognitive analysis and concept grounding run as separate engines.',
    'diagnose.button': 'END SESSION AND DIAGNOSE',
    'diagnose.ready': 'Ready.',
    'diagnose.savingManual': 'Saving manual transcript...',
    'diagnose.running': 'Running Cognitive Engine and Concept Engine...',
    'diagnose.done': 'Diagnosis complete.',
    'results.cognitive': 'COGNITIVE ENGINE',
    'results.concept': 'CONCEPT ENGINE',
    'results.output': 'OUTPUT',
    'results.reportTitle': 'Learning diagnosis report',
    'results.download': 'Download Markdown',
    'results.sessionConfidence': 'Session confidence',
    'results.evidence': 'Evidence',
    'results.intervention': 'Intervention',
    'results.conceptTitle': 'Concept precision',
    'results.noEvidence': 'No strong evidence extracted.',
    'results.noConcepts': 'No grounded concept evaluation available.',
    'results.insufficient': 'Insufficient evidence',
    'status.correct': 'correct',
    'status.partial': 'partial',
    'status.incorrect': 'incorrect',
    'status.unclear': 'unclear',
    'status.not_observed': 'not observed',
  },
  zh: {
    'hero.eyebrow': '本地优先的学习诊断',
    'hero.subtitle': '录制你的学习过程，对照你的课程材料，诊断学习状态与概念掌握程度。',
    'health.checking': '正在检查本地服务...',
    'health.on': '本地服务就绪 - 语义分析已开启',
    'health.heuristic': '本地服务就绪 - 启发式模式',
    'health.off': '本地服务不可用',
    'settings.title': '存储设置',
    'settings.desc': '选择会话、语料、转写和报告的保存位置。指向你的 Obsidian 库文件夹，报告即可作为笔记打开。',
    'settings.dataDirLabel': '保存位置（建议使用绝对路径）',
    'settings.save': '保存路径',
    'settings.reset': '恢复默认',
    'settings.saved': '保存位置已更新。',
    'settings.resetDone': '保存位置已恢复默认。',
    'settings.defaultNote': '当前为项目内默认文件夹。',
    'settings.customNote': '当前使用自定义保存位置。',
    'setup.title': '会话设置',
    'setup.desc': '创建本地会话并上传参考材料。',
    'setup.titleLabel': '会话标题',
    'setup.create': '创建会话',
    'setup.noSession': '尚未创建会话',
    'setup.created': '已创建新的本地会话。',
    'setup.dropzone': '上传 PDF / Markdown / TXT',
    'setup.uploading': '正在上传参考材料...',
    'setup.materialSaved': '参考材料已保存到本地。',
    'trace.title': '录制你的学习轨迹',
    'trace.desc': '录下你自己的解释、提问、纠正和不确定的地方。',
    'trace.start': '开始录制',
    'trace.stop': '停止录制',
    'trace.off': '麦克风已关闭。',
    'trace.recording': '正在浏览器本地录制。',
    'trace.stopping': '录制已停止，正在本地保存 WAV...',
    'trace.savedPrefix': '音频已保存到本地（',
    'trace.savedSuffix': ' 秒）。',
    'trace.asrLabel': '停止后的语音转写方式',
    'trace.asrManual': '手动粘贴转写 / 不使用 ASR 模型',
    'trace.asrLocal': 'Qwen3-ASR 本地模型',
    'trace.asrServer': 'Qwen3-ASR 服务端',
    'trace.manualLabel': '可选：手动粘贴转写文本',
    'trace.manualPlaceholder': '在此粘贴转写文本，无需安装 Qwen3-ASR 即可测试诊断流程。',
    'diagnose.title': '生成诊断',
    'diagnose.desc': '认知分析与概念核查由两个独立引擎完成。',
    'diagnose.button': '结束会话并诊断',
    'diagnose.ready': '准备就绪。',
    'diagnose.savingManual': '正在保存手动转写...',
    'diagnose.running': '正在运行认知引擎与概念引擎...',
    'diagnose.done': '诊断完成。',
    'results.cognitive': '认知引擎',
    'results.concept': '概念引擎',
    'results.output': '输出',
    'results.reportTitle': '学习诊断报告',
    'results.download': '下载 Markdown',
    'results.sessionConfidence': '会话置信度',
    'results.evidence': '证据',
    'results.intervention': '建议行动',
    'results.conceptTitle': '概念掌握评估',
    'results.noEvidence': '未提取到有力证据。',
    'results.noConcepts': '暂无基于材料的概念评估。',
    'results.insufficient': '证据不足',
    'status.correct': '正确',
    'status.partial': '部分正确',
    'status.incorrect': '错误',
    'status.unclear': '不明确',
    'status.not_observed': '未观察到',
  },
};

let lang = localStorage.getItem('learnTraceLang') || (navigator.language.toLowerCase().startsWith('zh') ? 'zh' : 'en');

function t(key) {
  return (I18N[lang] && I18N[lang][key]) || I18N.en[key] || key;
}

function applyLanguage() {
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-i18n]').forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });
  if (!state.sessionId) {
    el('sessionId').textContent = t('setup.noSession');
  }
  el('langEn').classList.toggle('active', lang === 'en');
  el('langZh').classList.toggle('active', lang === 'zh');
  refreshHealth();
  refreshSettingsNote();
}

function setLanguage(next) {
  lang = next;
  localStorage.setItem('learnTraceLang', next);
  applyLanguage();
}

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
  setStatus(t('setup.uploading'));
  const result = await request(`/api/sessions/${id}/materials`, { method: 'POST', body });
  el('materialList').innerHTML = result.materials.map((name) => `<span class="chip">${escapeHtml(name)}</span>`).join('');
  setStatus(t('setup.materialSaved'), 'ok');
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
  el('recordLabel').textContent = t('trace.stop');
  el('recordStatus').textContent = t('trace.recording');
}

async function stopRecording() {
  const result = await state.recorder.stop();
  state.recording = false;
  clearInterval(state.timerHandle);
  el('recordButton').classList.remove('active');
  el('recordLabel').textContent = t('trace.start');
  el('recordStatus').textContent = t('trace.stopping');
  if (!result) return;

  const body = new FormData();
  body.append('audio', result.blob, 'learning-trace.wav');
  body.append('duration_seconds', String(result.duration));
  await request(`/api/sessions/${state.sessionId}/audio`, { method: 'POST', body });
  state.audioUploaded = true;
  el('recordStatus').textContent = `${t('trace.savedPrefix')}${Math.round(result.duration)}${t('trace.savedSuffix')}`;
}

async function finishSession() {
  try {
    const id = await ensureSession();
    if (state.recording) await stopRecording();

    const manual = el('manualTranscript').value.trim();
    if (manual) {
      setStatus(t('diagnose.savingManual'));
      await request(`/api/sessions/${id}/transcript/manual`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: manual }),
      });
    }

    setStatus(t('diagnose.running'));
    const result = await request(`/api/sessions/${id}/finish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asr_provider: el('asrProvider').value }),
    });
    renderResults(result);
    setStatus(t('diagnose.done'), 'ok');
  } catch (error) {
    setStatus(error.message, 'error');
  }
}

function renderResults(result) {
  el('results').classList.remove('hidden');
  const primary = result.cognitive.primary_bottleneck || {};
  el('bottleneck').textContent = primary.label || t('results.insufficient');
  el('observation').textContent = primary.hypothesis || primary.observation || '';
  const conf = Number(primary.confidence || 0);
  el('confidence').textContent = `${Math.round(conf * 100)}%`;
  el('evidence').innerHTML = (primary.evidence || []).map((q) => `<blockquote>${escapeHtml(q)}</blockquote>`).join('') || `<p class="muted">${t('results.noEvidence')}</p>`;
  el('intervention').innerHTML = (primary.intervention || []).map((x) => `<li>${escapeHtml(x)}</li>`).join('');

  el('conceptOverview').textContent = result.concepts.overview || '';
  const concepts = result.concepts.concepts || [];
  el('concepts').innerHTML = concepts.length
    ? concepts.map((item) => {
      const status = item.status || '';
      return `
      <div class="concept-item">
        <div class="row between"><strong>${escapeHtml(item.concept || '')}</strong><span class="badge ${escapeHtml(status)}">${escapeHtml(t(`status.${status}`))}</span></div>
        <p>${escapeHtml(item.student_understanding || '')}</p>
        <small>${escapeHtml(item.correction || '')}</small>
      </div>`;
    }).join('')
    : `<p class="muted">${t('results.noConcepts')}</p>`;

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

// --- Storage settings ---

let settingsState = { data_dir: '', is_custom: false };

function refreshSettingsNote() {
  const note = el('dataDirHint');
  if (!settingsState.data_dir) {
    note.textContent = '';
    return;
  }
  const label = settingsState.is_custom ? t('settings.customNote') : t('settings.defaultNote');
  note.textContent = `${label} ${settingsState.data_dir}`;
}

async function loadSettings() {
  try {
    settingsState = await request('/api/settings');
    el('dataDir').value = settingsState.data_dir || '';
    refreshSettingsNote();
  } catch {
    // settings unavailable; leave field empty
  }
}

async function saveDataDir(reset = false) {
  const statusEl = el('settingsStatus');
  try {
    const body = reset ? { data_dir: null } : { data_dir: el('dataDir').value };
    settingsState = await request('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    el('dataDir').value = settingsState.data_dir || '';
    refreshSettingsNote();
    statusEl.textContent = reset ? t('settings.resetDone') : t('settings.saved');
  } catch (error) {
    statusEl.textContent = error.message;
  }
}

// --- Health badge ---

let healthState = null;

function refreshHealth() {
  const badge = el('health');
  if (healthState === null) {
    badge.textContent = t('health.checking');
    return;
  }
  badge.textContent = healthState.llm_configured ? t('health.on') : t('health.heuristic');
}

el('createSession').addEventListener('click', async () => {
  try {
    state.sessionId = null;
    await ensureSession();
    setStatus(t('setup.created'), 'ok');
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
el('langEn').addEventListener('click', () => setLanguage('en'));
el('langZh').addEventListener('click', () => setLanguage('zh'));
el('saveDataDir').addEventListener('click', () => saveDataDir(false));
el('resetDataDir').addEventListener('click', () => saveDataDir(true));

request('/api/health')
  .then((health) => {
    healthState = health;
    if ([...el('asrProvider').options].some((option) => option.value === health.default_asr)) {
      el('asrProvider').value = health.default_asr;
    }
    refreshHealth();
  })
  .catch(() => {
    healthState = null;
    el('health').textContent = t('health.off');
  });

loadSettings();
applyLanguage();
