/**
 * SkillForge — Main Client Application (Pure JS)
 * Reactive State Management, API Integration, and UI Router.
 */

// Global App State
const state = {
  currentPage: 'create-skill',
  skillName: null,
  skillContent: '',
  taskDesc: '',
  category: 'Software Development',
  constraints: '',
  outputStyle: 'Balanced',
  includeChecklist: true,
  hasGenerated: false,
  validationResult: null,
  testResult: null,
  lastUpdated: null,
  exportFolderName: '',
  skillsHistory: [],
  projectFiles: {},
  codeEditMode: false,
  llmEvalMode: false,
  ollama: {
    endpoint: 'http://localhost:11434',
    activeModel: 'qwen2.5:7b',
    selectedModel: 'qwen2.5:7b',
    models: ['qwen2.5:7b', 'qwen2.5:3b', 'llama3.2:3b', 'deepseek-r1:7b', 'mistral:7b'],
    connected: false,
    useLocalModel: true,
    statusMessage: ''
  }
};

// --- Toast System ---
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `sf-toast toast-${type}`;
  toast.innerHTML = `
    <div style="flex: 1;">${message}</div>
    <span style="cursor: pointer; opacity: 0.7; font-weight: bold;" onclick="this.parentElement.remove()">&times;</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function applyTheme(theme) {
  const isLight = theme === 'light';
  document.documentElement.dataset.theme = isLight ? 'light' : 'dark';
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(isLight));
    toggle.setAttribute('aria-label', `Switch to ${isLight ? 'dark' : 'light'} mode`);
    toggle.querySelector('.theme-toggle-label').textContent = `${isLight ? 'Dark' : 'Light'} mode`;
  }
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
  applyTheme(nextTheme);
  try {
    localStorage.setItem('skillforge-theme', nextTheme);
  } catch (err) {
    console.warn('Could not save the theme preference:', err);
  }
}

// --- Navigation & Router ---
function navigateTo(pageId) {
  state.currentPage = pageId;

  // Update nav menu items
  document.querySelectorAll('.sf-nav-item').forEach(el => {
    if (el.dataset.page === pageId) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });

  // Switch visible page view
  document.querySelectorAll('.page-view').forEach(view => {
    if (view.id === `page-${pageId}`) {
      view.classList.add('active');
    } else {
      view.classList.remove('active');
    }
  });

  // Refresh page-specific content
  if (pageId === 'my-skills') {
    renderMySkillsPage();
  } else if (pageId === 'testing-lab') {
    renderTestingLabPage();
  }
}

// Reset workspace for "+ New Skill"
function resetNewSkill() {
  state.skillName = null;
  state.skillContent = '';
  state.taskDesc = '';
  state.constraints = '';
  state.hasGenerated = false;
  state.validationResult = null;
  state.testResult = null;
  state.lastUpdated = null;
  state.exportFolderName = '';
  state.codeEditMode = false;

  // Reset inputs in DOM
  const descEl = document.getElementById('input-task-desc');
  if (descEl) descEl.value = '';
  const constrEl = document.getElementById('input-constraints');
  if (constrEl) constrEl.value = '';
  updateCharCounts();

  navigateTo('create-skill');
  updateWorkspaceState();
  showToast('Ready for a new skill specification!', 'info');
}

// --- Stepper Calculation ---
function updateStepper() {
  let step = 1;
  if (state.hasGenerated) step = 2;
  if (state.validationResult !== null) step = 3;
  if (state.testResult !== null) step = 4;
  if (state.validationResult && state.validationResult.is_valid && state.testResult) step = 5;

  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step-node-${i}`);
    if (!el) continue;
    el.classList.remove('active', 'completed');
    if (i < step) {
      el.classList.add('completed');
      el.querySelector('.sf-step-circle').innerHTML = '✓';
    } else if (i === step) {
      el.classList.add('active');
      el.querySelector('.sf-step-circle').innerHTML = `${i}`;
    } else {
      el.querySelector('.sf-step-circle').innerHTML = `${i}`;
    }
  }
}

// --- Quick Presets ---
const PRESETS = {
  python: {
    desc: 'Review Python code for bugs, security vulnerabilities, and code smells, and suggest verified fixes without modifying files.',
    category: 'Software Development',
    constraints: 'Never modify files in place.\nAdhere to PEP 8 standards.\nInclude line numbers for all issues found.'
  },
  k8s: {
    desc: 'Audit Kubernetes Helm charts and manifest YAMLs for security misconfigurations, privilege escalation, and resource quota leaks.',
    category: 'Software Development',
    constraints: 'Flag runAsRoot permissions.\nCheck CPU and Memory limits.'
  },
  openapi: {
    desc: 'Generate comprehensive OpenAPI 3.1 specification documentation from FastAPI endpoint code including schema definitions.',
    category: 'Writing & Documentation',
    constraints: 'Include detailed error response codes (400, 401, 404, 500).\nInclude realistic example JSON payloads.'
  }
};

function applyPreset(presetKey) {
  const p = PRESETS[presetKey];
  if (!p) return;

  state.taskDesc = p.desc;
  state.category = p.category;
  state.constraints = p.constraints;

  document.getElementById('input-task-desc').value = p.desc;
  document.getElementById('select-category').value = p.category;
  document.getElementById('input-constraints').value = p.constraints;

  updateCharCounts();
  showToast(`Applied preset: ${presetKey.toUpperCase()}`, 'info');
}

// --- Char Counters ---
function updateCharCounts() {
  const descEl = document.getElementById('input-task-desc');
  const constrEl = document.getElementById('input-constraints');
  if (descEl) {
    document.getElementById('desc-char-count').innerText = `${descEl.value.length}/2000`;
  }
  if (constrEl) {
    document.getElementById('constraints-char-count').innerText = `${constrEl.value.length}/1000`;
  }
}

// --- Project Files Handling ---
const PROJECT_FILE_EXTENSIONS = new Set([
  '.py', '.yaml', '.yml', '.json', '.md', '.txt', '.sh', '.sql', '.toml',
  '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.go', '.rs',
  '.java', '.kt', '.swift', '.c', '.h', '.cpp', '.cs', '.rb', '.php',
  '.vue', '.svelte', '.xml', '.ini', '.cfg', '.properties', '.gradle'
]);
const IGNORED_PROJECT_DIRECTORIES = new Set([
  '.git', 'node_modules', '.venv', 'venv', 'env', '__pycache__',
  'dist', 'build', 'coverage', '.next', '.nuxt', 'vendor'
]);
const MAX_PROJECT_FILES = 100;
const MAX_PROJECT_FILE_BYTES = 256 * 1024;
const MAX_PROJECT_TOTAL_BYTES = 5 * 1024 * 1024;

function handleFileDrop(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (!files || !files.length) return;
  processUploadedFiles(files);
}

function readProjectFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error || new Error(`Could not read ${file.name}`));
    reader.readAsText(file);
  });
}

async function processUploadedFiles(files) {
  const selectedFiles = Array.from(files);
  const currentBytes = Object.values(state.projectFiles)
    .reduce((total, content) => total + new Blob([content]).size, 0);
  let totalBytes = currentBytes;
  let skipped = 0;
  const acceptedFiles = [];

  for (const file of selectedFiles) {
    const relativePath = file.webkitRelativePath || file.name;
    const pathParts = relativePath.split('/');
    const fileName = pathParts[pathParts.length - 1];
    const extension = fileName.includes('.') ? fileName.slice(fileName.lastIndexOf('.')).toLowerCase() : '';
    const isSupportedName = ['dockerfile', 'makefile', 'procfile'].includes(fileName.toLowerCase());
    const isIgnoredPath = pathParts.some(part => IGNORED_PROJECT_DIRECTORIES.has(part.toLowerCase()));
    const isSkillFile = fileName.toLowerCase() === 'skill.md';

    if (isIgnoredPath || (!isSkillFile && !isSupportedName && !PROJECT_FILE_EXTENSIONS.has(extension)) ||
        file.size > MAX_PROJECT_FILE_BYTES || totalBytes + file.size > MAX_PROJECT_TOTAL_BYTES) {
      skipped += 1;
      continue;
    }
    if (!Object.prototype.hasOwnProperty.call(state.projectFiles, relativePath) &&
        Object.keys(state.projectFiles).length + acceptedFiles.length >= MAX_PROJECT_FILES) {
      skipped += 1;
      continue;
    }

    totalBytes += file.size;
    acceptedFiles.push({ file, relativePath, fileName });
  }

  try {
    const results = await Promise.all(acceptedFiles.map(async ({ file, relativePath, fileName }) => ({
      relativePath,
      fileName,
      text: await readProjectFile(file)
    })));

    for (const { relativePath, fileName, text } of results) {
      state.projectFiles[relativePath] = text;
      if (fileName.toLowerCase() === 'skill.md') {
        showToast(`Detected skill file '${relativePath}'. Auto-loading into editor...`, 'success');
        state.skillContent = text;
        state.skillName = fileName.replace(/\.md$/i, '').toLowerCase().replace(/[^a-z0-9_-]/g, '-');
        state.hasGenerated = true;
        updateWorkspaceState();
        runValidation();
      }
    }
    renderProjectFilesList();
    if (results.length) {
      showToast(`Imported ${results.length} project file(s)${skipped ? `; skipped ${skipped} unsupported or oversized file(s)` : ''}.`, 'success');
    } else if (skipped) {
      showToast(`No supported project files were imported; skipped ${skipped} file(s).`, 'error');
    }
  } catch (err) {
    showToast(`Project file import failed: ${err.message}`, 'error');
  }
}

function removeProjectFile(fname) {
  delete state.projectFiles[fname];
  renderProjectFilesList();
  showToast(`Removed ${fname}`, 'info');
}

function clearAllProjectFiles() {
  state.projectFiles = {};
  renderProjectFilesList();
  showToast('Cleared all attached files', 'info');
}

function viewProjectFile(fname) {
  const content = state.projectFiles[fname];
  document.getElementById('modal-title').innerText = `Viewing: ${fname}`;
  document.getElementById('modal-content').innerHTML = `
    <pre style="background: #080c14; padding: 14px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.82rem; color: #e2e8f0; overflow-x: auto;"><code>${window.MarkdownRenderer.escapeHtml(content)}</code></pre>
  `;
  document.getElementById('sf-modal-overlay').classList.add('open');
}

function closeModal() {
  document.getElementById('sf-modal-overlay').classList.remove('open');
}

function renderProjectFilesList() {
  const container = document.getElementById('attached-files-container');
  const countSpan = document.getElementById('attached-files-count');
  const filenames = Object.keys(state.projectFiles);

  if (countSpan) countSpan.innerText = `(${filenames.length} attached)`;

  if (!container) return;
  if (!filenames.length) {
    container.innerHTML = '';
    return;
  }

  const list = document.createElement('div');
  list.className = 'attached-files-list';
  filenames.forEach(fn => {
    const size = state.projectFiles[fn].length;
    const item = document.createElement('div');
    item.className = 'attached-file-item';
    const info = document.createElement('div');
    info.className = 'attached-file-info';
    const icon = document.createElement('span');
    icon.textContent = '📄';
    const name = document.createElement('span');
    name.textContent = fn;
    const sizeLabel = document.createElement('span');
    sizeLabel.style.cssText = 'color: #64748b; font-size: 0.74rem;';
    sizeLabel.textContent = `(${size} chars)`;
    info.append(icon, name, sizeLabel);

    const actions = document.createElement('div');
    actions.className = 'attached-file-actions';
    const viewButton = document.createElement('button');
    viewButton.className = 'btn-secondary';
    viewButton.style.cssText = 'padding: 3px 8px; font-size: 0.75rem;';
    viewButton.textContent = 'View';
    viewButton.addEventListener('click', () => viewProjectFile(fn));
    const removeButton = document.createElement('button');
    removeButton.className = 'btn-danger';
    removeButton.style.cssText = 'padding: 3px 8px; font-size: 0.75rem;';
    removeButton.textContent = '×';
    removeButton.addEventListener('click', () => removeProjectFile(fn));
    actions.append(viewButton, removeButton);
    item.append(info, actions);
    list.appendChild(item);
  });

  const footer = document.createElement('div');
  footer.style.cssText = 'margin-top: 8px; text-align: right;';
  const clearButton = document.createElement('button');
  clearButton.className = 'btn-secondary';
  clearButton.style.cssText = 'padding: 4px 10px; font-size: 0.76rem;';
  clearButton.textContent = 'Clear All';
  clearButton.addEventListener('click', clearAllProjectFiles);
  footer.appendChild(clearButton);
  list.appendChild(footer);
  container.replaceChildren(list);
}

// --- Workspace State & Render ---
function updateWorkspaceState() {
  // Breadcrumb
  const nameDisplay = state.skillName || 'New Skill';
  document.getElementById('breadcrumb-skill-name').innerText = nameDisplay;

  // Stepper
  updateStepper();

  const emptyState = document.getElementById('workspace-empty-state');
  const activeTabs = document.getElementById('workspace-active-tabs');

  if (!state.hasGenerated) {
    emptyState.style.display = 'block';
    activeTabs.style.display = 'none';
  } else {
    emptyState.style.display = 'none';
    activeTabs.style.display = 'block';

    // Update Code & Preview Tab contents
    renderPreviewTab();
    renderCodeTab();
    updateAsciiTree();
  }
}

// --- Tabs Switcher ---
function switchTab(tabId) {
  document.querySelectorAll('.sf-tab-btn').forEach(btn => {
    if (btn.dataset.tab === tabId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  document.querySelectorAll('.sf-tab-pane').forEach(pane => {
    if (pane.id === `tab-pane-${tabId}`) {
      pane.classList.add('active');
    } else {
      pane.classList.remove('active');
    }
  });

  if (tabId === 'preview') {
    renderPreviewTab();
  } else if (tabId === 'code') {
    renderCodeTab();
  } else if (tabId === 'validation') {
    if (!state.validationResult) {
      runValidation();
    } else {
      renderValidationTab();
    }
  } else if (tabId === 'tests') {
    if (!state.testResult) {
      runTests();
    } else {
      renderTestsTab();
    }
  }
}

// --- Skill Generation ---
async function generateSkill() {
  const descEl = document.getElementById('input-task-desc');
  const taskDesc = descEl.value.trim();

  if (!taskDesc) {
    showToast('Task Description is required. Please specify what the agent skill should do.', 'error');
    return;
  }

  state.taskDesc = taskDesc;
  state.category = document.getElementById('select-category').value;
  state.outputStyle = document.getElementById('select-output-style').value;
  state.constraints = document.getElementById('input-constraints').value;
  state.includeChecklist = document.getElementById('checkbox-checklist').checked;

  const btn = document.getElementById('btn-generate-skill');
  btn.disabled = true;
  btn.innerHTML = `<span style="display: inline-block; animation: spin 1s infinite linear;">↻</span> Generating Skill...`;

  try {
    const payload = {
      task_desc: state.taskDesc,
      category: state.category,
      constraints: state.constraints,
      output_style: state.outputStyle,
      include_checklist: state.includeChecklist,
      use_local_model: state.ollama.useLocalModel && state.ollama.connected,
      endpoint: state.ollama.endpoint,
      model: state.ollama.selectedModel,
      project_files: state.projectFiles
    };

    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Generation failed');
    }

    // Success
    const skill = data.skill;
    state.skillName = skill.name;
    state.skillContent = skill.content;
    state.hasGenerated = true;
    state.validationResult = data.validation || null;
    state.testResult = null;
    state.lastUpdated = new Date().toLocaleTimeString();
    state.exportFolderName = skill.name;

    // Add to history
    const exists = state.skillsHistory.some(s => s.name === skill.name);
    if (!exists) {
      state.skillsHistory.push({
        name: skill.name,
        category: state.category,
        content: skill.content,
        created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    }

    updateWorkspaceState();
    switchTab('preview');
    showToast(`Skill '${skill.name}' generated successfully!`, 'success');
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `Generate Skill →`;
  }
}

// --- Preview Tab ---
function renderPreviewTab() {
  const container = document.getElementById('preview-container');
  if (container) {
    container.innerHTML = window.MarkdownRenderer.render(state.skillContent);
  }
}

// --- Code & Edit Tab ---
function renderCodeTab() {
  document.getElementById('code-active-file').innerText = `${state.skillName || 'skill'}/SKILL.md`;
  document.getElementById('code-last-saved').innerText = `Last Saved: ${state.lastUpdated || 'Just now'}`;

  const viewMode = document.getElementById('code-view-container');
  const editMode = document.getElementById('code-edit-container');
  const toggle = document.getElementById('toggle-edit-mode');

  toggle.checked = state.codeEditMode;

  if (state.codeEditMode) {
    viewMode.style.display = 'none';
    editMode.style.display = 'block';
    document.getElementById('code-textarea').value = state.skillContent;
  } else {
    viewMode.style.display = 'block';
    editMode.style.display = 'none';
    document.getElementById('code-display').innerText = state.skillContent;
  }
}

function toggleEditMode() {
  state.codeEditMode = document.getElementById('toggle-edit-mode').checked;
  renderCodeTab();
}

function saveEdits() {
  const newContent = document.getElementById('code-textarea').value;
  state.skillContent = newContent;
  state.validationResult = null;
  state.testResult = null;
  state.lastUpdated = new Date().toLocaleTimeString();

  updateWorkspaceState();
  renderCodeTab();
  showToast('Edits saved! Validation and test caches reset.', 'success');
}

// --- Validation Tab ---
async function runValidation() {
  if (!state.skillContent) return;

  const btn = document.getElementById('btn-revalidate');
  if (btn) btn.disabled = true;

  try {
    const res = await fetch('/api/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_content: state.skillContent })
    });
    const data = await res.json();
    state.validationResult = data;
    renderValidationTab();
    updateStepper();
    showToast('Validation completed!', 'success');
  } catch (err) {
    showToast(`Validation error: ${err.message}`, 'error');
  } finally {
    if (btn) btn.disabled = false;
  }
}

function renderValidationTab() {
  const val = state.validationResult;
  if (!val) return;

  // Stat boxes
  const statusEl = document.getElementById('val-status-badge');
  const scoreEl = document.getElementById('val-score-text');
  const countEl = document.getElementById('val-checks-count');
  const summaryEl = document.getElementById('val-summary-text');
  const checksContainer = document.getElementById('val-checks-list');

  const isValid = val.is_valid;
  statusEl.innerText = isValid ? 'PASSED' : 'FAILED';
  statusEl.style.color = isValid ? '#10b981' : '#f43f5e';
  scoreEl.innerText = `${val.score}%`;
  countEl.innerText = `${val.passed_checks}/${val.total_checks}`;
  summaryEl.innerHTML = `<strong>Summary:</strong> ${val.summary}`;

  let checksHtml = '';
  (val.checks || []).forEach(chk => {
    let icon = '<span style="color: #10b981; font-weight: bold;">✓</span>';
    let pillClass = 'sf-pill-emerald';
    let statusText = 'PASSED';

    if (!chk.passed) {
      if (chk.level === 'error') {
        icon = '<span style="color: #f43f5e; font-weight: bold;">✕</span>';
        pillClass = 'sf-pill-rose';
        statusText = 'ERROR';
      } else {
        icon = '<span style="color: #f59e0b; font-weight: bold;">▲</span>';
        pillClass = 'sf-pill-amber';
        statusText = 'WARNING';
      }
    }

    checksHtml += `
      <div class="check-item">
        <div class="check-item-icon">${icon}</div>
        <div class="check-item-body">
          <div class="check-item-title">
            <span>${chk.name}</span>
            <span class="sf-pill ${pillClass}">${statusText}</span>
          </div>
          <div class="check-item-desc">${chk.message}</div>
          ${chk.suggestion ? `<div class="check-item-fix">💡 Suggestion: ${chk.suggestion}</div>` : ''}
        </div>
      </div>
    `;
  });
  checksContainer.innerHTML = checksHtml;
}

// --- Behavioral Testing Tab ---
async function runTests() {
  if (!state.skillContent) return;

  const btn = document.getElementById('btn-rerun-tests');
  if (btn) {
    btn.disabled = true;
    btn.innerText = 'Executing tests...';
  }

  try {
    const res = await fetch('/api/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        skill_content: state.skillContent,
        task_desc: state.taskDesc,
        use_local_llm: state.llmEvalMode && state.ollama.connected,
        endpoint: state.ollama.endpoint,
        model: state.ollama.selectedModel
      })
    });
    const data = await res.json();
    state.testResult = data;
    renderTestsTab();
    updateStepper();
    showToast('Behavioral test suite completed!', 'success');
  } catch (err) {
    showToast(`Test execution error: ${err.message}`, 'error');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerText = 'Re-run All Tests';
    }
  }
}

async function applyManualFeedback() {
  if (!state.skillContent) {
    showToast('Generate or load a skill before applying feedback.', 'error');
    return;
  }

  const feedbackInput = document.getElementById('manual-feedback-input');
  const feedback = feedbackInput.value.trim();
  if (!feedback) {
    showToast('Enter feedback describing what you want improved.', 'error');
    feedbackInput.focus();
    return;
  }
  if (!state.ollama.connected) {
    showToast('Connect to Ollama in Settings before applying feedback.', 'error');
    return;
  }

  const btn = document.getElementById('btn-apply-feedback');
  btn.disabled = true;
  btn.innerText = 'Applying feedback...';
  try {
    const res = await fetch('/api/improve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        skill_content: state.skillContent,
        failed_tests: [],
        manual_feedback: feedback,
        use_local_llm: true,
        endpoint: state.ollama.endpoint,
        model: state.ollama.selectedModel
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success || !data.improved_content) {
      throw new Error(data.error || 'The model did not return an improved skill.');
    }

    state.skillContent = data.improved_content;
    state.validationResult = null;
    state.testResult = null;
    state.lastUpdated = new Date().toLocaleTimeString();
    feedbackInput.value = '';
    updateWorkspaceState();
    await runValidation();
    renderPreviewTab();
    switchTab('preview');
    showToast('Feedback applied. The revised skill passed through validation.', 'success');
  } catch (err) {
    showToast(`Could not apply feedback: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerText = 'Apply Feedback & Refine';
  }
}

function renderTestsTab() {
  const tr = state.testResult;
  if (!tr) return;

  document.getElementById('test-total-count').innerText = tr.total_tests;
  document.getElementById('test-passed-count').innerText = tr.passed_tests;
  document.getElementById('test-pass-rate').innerText = `${tr.pass_rate}%`;

  const engineLabel = (state.llmEvalMode && state.ollama.connected)
    ? `Live Local Ollama (${state.ollama.selectedModel})`
    : 'Fast Deterministic Engine';
  document.getElementById('test-engine-badge').innerText = engineLabel;

  const listContainer = document.getElementById('test-scenarios-list');
  let html = '';
  (tr.tests || []).forEach(t => {
    const isPassed = t.status === 'PASSED';
    const pillClass = isPassed ? 'sf-pill-emerald' : 'sf-pill-amber';

    html += `
      <div class="test-item">
        <div class="test-item-header">
          <span class="test-item-name">${t.name}</span>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="sf-pill sf-pill-indigo">${t.score}/100</span>
            <span class="sf-pill ${pillClass}">${t.status}</span>
          </div>
        </div>
        <div class="test-item-criteria"><strong>Criteria:</strong> ${t.criteria}</div>
        <div class="test-item-obs">${t.observation}</div>
      </div>
    `;
  });
  listContainer.innerHTML = html;
}

// Self-Improve Skill
async function selfImproveSkill() {
  if (!state.skillContent || !state.testResult) return;

  const btn = document.getElementById('btn-self-improve');
  btn.disabled = true;
  btn.innerText = 'Refining instructions...';

  try {
    const failedTests = (state.testResult.tests || []).filter(t => t.status !== 'PASSED');
    const res = await fetch('/api/improve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        skill_content: state.skillContent,
        failed_tests: failedTests,
        use_local_llm: state.llmEvalMode && state.ollama.connected,
        endpoint: state.ollama.endpoint,
        model: state.ollama.selectedModel
      })
    });
    const data = await res.json();
    if (data.improved_content) {
      state.skillContent = data.improved_content;
      state.lastUpdated = new Date().toLocaleTimeString();
      await runValidation();
      await runTests();
      updateWorkspaceState();
      showToast('Skill automatically improved and re-verified!', 'success');
    }
  } catch (err) {
    showToast(`Improvement error: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerText = '⚡ Self-Improve Skill';
  }
}

// --- Export & ASCII Tree ---
async function updateAsciiTree() {
  const folderInput = document.getElementById('export-folder-input');
  const folderName = folderInput ? folderInput.value.trim() : (state.skillName || 'my-skill');

  try {
    const res = await fetch('/api/tree', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folder_name: folderName,
        project_files: state.projectFiles
      })
    });
    const data = await res.json();
    const treeEl = document.getElementById('ascii-tree-preview');
    if (treeEl) treeEl.innerText = data.tree;
  } catch (err) {
    console.error('Tree error', err);
  }
}

async function downloadZip() {
  const folderInput = document.getElementById('export-folder-input');
  const folderName = folderInput ? folderInput.value.trim() : (state.skillName || 'my-skill');

  try {
    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folder_name: folderName,
        skill_content: state.skillContent,
        project_files: state.projectFiles
      })
    });

    if (!res.ok) throw new Error('Failed to generate archive');

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${folderName}.zip`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    showToast(`Downloaded ${folderName}.zip`, 'success');
  } catch (err) {
    showToast(`Download failed: ${err.message}`, 'error');
  }
}

// --- My Skills Page ---
function renderMySkillsPage() {
  const container = document.getElementById('my-skills-grid');
  const emptyState = document.getElementById('my-skills-empty');

  if (!state.skillsHistory.length) {
    emptyState.style.display = 'block';
    container.innerHTML = '';
    return;
  }

  emptyState.style.display = 'none';
  let html = '';
  state.skillsHistory.forEach((item, idx) => {
    const isActive = (item.name === state.skillName);
    const activeBadge = isActive ? '<span class="sf-pill sf-pill-emerald">● ACTIVE</span>' : '';

    html += `
      <div class="sf-card" style="margin-bottom: 14px;">
        <div class="sf-card-header">
          <div>
            <span style="font-family: var(--font-mono); font-size: 1.05rem; font-weight: 700; color: #ffffff;">${item.name}</span>
            <span class="sf-pill sf-pill-cyan" style="margin-left: 8px;">${item.category}</span>
          </div>
          ${activeBadge}
        </div>
        <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 12px;">Created: ${item.created_at}</p>
        <div style="display: flex; gap: 10px;">
          <button class="btn-primary" style="padding: 6px 14px; font-size: 0.82rem;" onclick="loadSkillFromHistory(${idx})">Open in Workspace</button>
          <button class="btn-secondary" style="padding: 6px 14px; font-size: 0.82rem;" onclick="downloadHistoryZip(${idx})">Download ZIP</button>
        </div>
      </div>
    `;
  });
  container.innerHTML = html;
}

function loadSkillFromHistory(idx) {
  const item = state.skillsHistory[idx];
  if (!item) return;

  state.skillName = item.name;
  state.skillContent = item.content;
  state.category = item.category;
  state.hasGenerated = true;
  state.exportFolderName = item.name;

  updateWorkspaceState();
  runValidation();
  runTests();
  navigateTo('create-skill');
  showToast(`Loaded skill '${item.name}' into workspace`, 'info');
}

async function downloadHistoryZip(idx) {
  const item = state.skillsHistory[idx];
  if (!item) return;

  try {
    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folder_name: item.name,
        skill_content: item.content
      })
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${item.name}.zip`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

// --- Testing Lab Dedicated Page ---
function renderTestingLabPage() {
  const emptyState = document.getElementById('testing-lab-empty');
  const activeView = document.getElementById('testing-lab-content');

  if (!state.hasGenerated || !state.skillName) {
    emptyState.style.display = 'block';
    activeView.style.display = 'none';
    return;
  }

  emptyState.style.display = 'none';
  activeView.style.display = 'block';

  document.getElementById('tlab-skill-name').innerText = state.skillName;

  if (!state.validationResult) runValidation();
  if (!state.testResult) runTests();

  const val = state.validationResult || { is_valid: false, score: 0, checks: [] };
  const tr = state.testResult || { total_tests: 0, passed_tests: 0, pass_rate: 0, tests: [] };

  document.getElementById('tlab-struct-status').innerText = val.is_valid ? 'PASSED' : 'FAILED';
  document.getElementById('tlab-struct-status').style.color = val.is_valid ? '#10b981' : '#f43f5e';
  document.getElementById('tlab-val-score').innerText = `${val.score}%`;
  document.getElementById('tlab-tests-ratio').innerText = `${tr.passed_tests}/${tr.total_tests}`;
  document.getElementById('tlab-tests-rate').innerText = `${tr.pass_rate}%`;

  // Left col: checks
  const valContainer = document.getElementById('tlab-checks-list');
  let valHtml = '';
  (val.checks || []).forEach(chk => {
    let icon = chk.passed ? '<span style="color: #10b981;">✓</span>' : '<span style="color: #f43f5e;">✕</span>';
    valHtml += `
      <div class="check-item">
        <div class="check-item-icon">${icon}</div>
        <div class="check-item-body">
          <div class="check-item-title">${chk.name}</div>
          <div class="check-item-desc">${chk.message}</div>
        </div>
      </div>
    `;
  });
  valContainer.innerHTML = valHtml;

  // Right col: tests
  const testContainer = document.getElementById('tlab-tests-list');
  let testHtml = '';
  (tr.tests || []).forEach(t => {
    testHtml += `
      <div class="test-item">
        <div class="test-item-header">
          <span class="test-item-name">${t.name}</span>
          <span class="sf-pill ${t.status === 'PASSED' ? 'sf-pill-emerald' : 'sf-pill-amber'}">${t.status}</span>
        </div>
        <div class="test-item-obs">${t.observation}</div>
      </div>
    `;
  });
  testContainer.innerHTML = testHtml;
}

// --- Settings Page & Ollama ---
async function detectOllama() {
  const endpoint = document.getElementById('ollama-endpoint-input').value.trim();
  state.ollama.endpoint = endpoint;

  const btn = document.getElementById('btn-detect-ollama');
  btn.disabled = true;
  btn.innerText = 'Detecting...';

  try {
    const res = await fetch('/api/ollama/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ endpoint: endpoint })
    });
    const data = await res.json();
    state.ollama.connected = data.connected;
    state.ollama.models = data.models || [];
    state.ollama.statusMessage = data.message;

    renderSettingsPage();
    updateSidebarStatus();
    showToast(data.connected ? 'Connected to local Ollama!' : 'Could not connect to Ollama daemon', data.connected ? 'success' : 'error');
  } catch (err) {
    state.ollama.connected = false;
    state.ollama.statusMessage = `Connection check failed: ${err.message}`;
    renderSettingsPage();
    updateSidebarStatus();
    showToast(`Ollama detection error: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerText = 'Detect & Connect to Ollama';
  }
}

function renderSettingsPage() {
  document.getElementById('ollama-endpoint-input').value = state.ollama.endpoint;

  const select = document.getElementById('ollama-model-select');
  select.innerHTML = '';
  const models = state.ollama.models.length ? state.ollama.models : ['qwen2.5:7b', 'qwen2.5:3b', 'llama3.2:3b', 'deepseek-r1:7b', 'mistral:7b'];

  models.forEach(m => {
    const opt = document.createElement('option');
    opt.value = m;
    opt.innerText = m;
    if (m === state.ollama.selectedModel) opt.selected = true;
    select.appendChild(opt);
  });

  const msgBox = document.getElementById('ollama-status-banner');
  if (state.ollama.statusMessage) {
    msgBox.style.display = 'block';
    msgBox.className = state.ollama.connected ? 'sf-card' : 'sf-card';
    msgBox.style.borderColor = state.ollama.connected ? '#10b981' : '#f43f5e';
    msgBox.innerHTML = `
      <div style="color: ${state.ollama.connected ? '#6ee7b7' : '#fda4af'}; font-size: 0.88rem;">
        ${state.ollama.statusMessage}
      </div>
      ${state.ollama.models.length ? `<div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">Detected Models: ${state.ollama.models.join(', ')}</div>` : ''}
    `;
  } else {
    msgBox.style.display = 'none';
  }
}

function updateSidebarStatus() {
  const pill = document.getElementById('sidebar-model-status');
  if (!pill) return;

  if (state.ollama.connected) {
    pill.className = 'sf-pill sf-pill-emerald';
    pill.innerHTML = `<span class="status-dot status-dot-emerald"></span> ${state.ollama.selectedModel} Active`;
  } else {
    pill.className = 'sf-pill sf-pill-cyan';
    pill.innerHTML = `<span class="status-dot status-dot-cyan"></span> Offline Engine`;
  }
}

// --- App Initialization ---
document.addEventListener('DOMContentLoaded', async () => {
  let savedTheme = 'dark';
  try {
    savedTheme = localStorage.getItem('skillforge-theme') || 'dark';
  } catch (err) {
    console.warn('Could not read the saved theme preference:', err);
  }
  applyTheme(savedTheme);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

  // Setup char counters
  const descEl = document.getElementById('input-task-desc');
  const constrEl = document.getElementById('input-constraints');
  if (descEl) descEl.addEventListener('input', updateCharCounts);
  if (constrEl) constrEl.addEventListener('input', updateCharCounts);

  // Setup Presets Accordion
  const presetsToggle = document.getElementById('presets-toggle');
  if (presetsToggle) {
    presetsToggle.addEventListener('click', () => {
      document.getElementById('presets-content').classList.toggle('open');
    });
  }

  // Setup Dropzone
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-upload-input');
  const projectFolderInput = document.getElementById('project-folder-input');
  const browseProjectFiles = document.getElementById('browse-project-files');
  const browseProjectFolder = document.getElementById('browse-project-folder');
  if (dropzone && fileInput && projectFolderInput) {
    browseProjectFiles.addEventListener('click', () => fileInput.click());
    browseProjectFolder.addEventListener('click', () => projectFolderInput.click());
    fileInput.addEventListener('change', async (e) => {
      await processUploadedFiles(e.target.files);
      fileInput.value = '';
    });
    projectFolderInput.addEventListener('change', async (e) => {
      await processUploadedFiles(e.target.files);
      projectFolderInput.value = '';
    });
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', handleFileDrop);
  }

  // Load initial backend status
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    state.ollama.connected = data.ollama_connected;
    state.ollama.statusMessage = data.ollama_status_message || '';
    state.ollama.activeModel = data.active_model;
    state.ollama.selectedModel = data.selected_model;
    state.ollama.endpoint = data.ollama_endpoint;
    if (data.ollama_models && data.ollama_models.length) {
      state.ollama.models = data.ollama_models;
      if (!state.ollama.models.includes(state.ollama.selectedModel)) {
        state.ollama.selectedModel = state.ollama.models.includes('qwen2.5:7b')
          ? 'qwen2.5:7b'
          : state.ollama.models[0];
      }
    }
  } catch (err) {
    console.log('Running in local mode');
  }

  updateSidebarStatus();
  updateStepper();
  renderSettingsPage();
});
