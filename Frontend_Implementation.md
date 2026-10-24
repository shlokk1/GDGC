# SkillForge — Frontend Implementation Architecture & Documentation

## Overview
SkillForge is a local-first AI agent skill creator, structural linter, behavioral test lab, and package bundler built with **Python & Streamlit** using a **UI & UX Pro Max** design system.

This implementation satisfies all requirements specified in [PRD_Frontend.md](PRD_Frontend.md) and aligns with the Agent Skills Open Standard.

---

## 🎨 UI & UX Pro Max Design System

SkillForge delivers a modern developer studio interface:
- **Obsidian & Glassmorphic Palette**: Deep dark background (`#07090e`), layered elevated panels with `backdrop-filter: blur(12px)`, and subtle translucent borders (`rgba(255, 255, 255, 0.08)`).
- **Vibrant Accent Indicators**:
  - Neon Indigo-Violet gradient (`#6366f1` to `#a855f7`) for primary actions and brand focus.
  - Emerald Green (`#10b981`) for passing statuses and verification.
  - Cyan (`#06b6d4`, `#38bdf8`) for live model badges and system architecture highlights.
  - Amber (`#f59e0b`) for diagnostic warnings and recommendations.
  - Rose (`#f43f5e`) for structural errors.
- **Micro-interactions & Hover States**: Elevation transforms on cards, glowing pills, and responsive layout.
- **Workflow Stepper**: Step-by-step breadcrumb progress bar dynamically derived from application state:
  `Task Spec` ➔ `Skill Draft` ➔ `Validation` ➔ `Behavioral Tests` ➔ `ZIP Export`.
- **One-Click Quick Presets**: Built-in prompt presets (*Python Code Review*, *K8s Helm Auditor*, *OpenAPI Doc Writer*) for rapid developer onboarding.

---

## 📂 Project Architecture

```
.
├── app.py                      # Main Streamlit application and page router
├── requirements.txt            # Python dependencies (streamlit, pyyaml, requests)
├── Frontend_Implementation.md  # Frontend architecture documentation
├── PRD_Frontend.md             # Product Requirements Document
├── PS.md                       # Problem Statement
├── PS_summarized.md            # Problem Summary & 6-Hour Plan
├── README.md                   # Getting Started & Setup Guide
├── frontend/
│   ├── __init__.py
│   ├── components.py           # Reusable UI widgets (sidebar, hero, stepper, stat cards, check items)
│   └── styles.py               # Pro Max custom CSS design system
├── generator/
│   ├── __init__.py
│   ├── prompts.py              # Prompts for LLM synthesis and revision
│   ├── skill_generator.py      # Deterministic Agent Skills template generator (Phase 1)
│   └── ollama_client.py        # Local Ollama client for model connectivity & Phase 2 inference
├── validator/
│   ├── __init__.py
│   └── skill_validator.py      # Deterministic structural linter & frontmatter validator
├── evaluator/
│   ├── __init__.py
│   └── test_runner.py          # Behavioral test runner and self-improvement engine
├── exporter/
│   ├── __init__.py
│   └── zip_exporter.py         # In-memory ZIP bundler & ASCII directory tree generator
└── tests/
    └── test_skillforge.py      # Unit tests for core functions
```

---

## 🛠️ Feature Walkthrough

### 1. Create Skill Page (`app.py`)
- **Hero & Stepper**: Explains the Agent Skills format and tracks current workspace progress.
- **Task Definition Form**:
  - Task description input with character counter and presets.
  - Skill category selector (Software Development, Writing, Research, Data Processing, Productivity, Other).
  - Explicit rules and constraints input.
  - Output style selector (`Balanced`, `Detailed`, `Concise`).
  - Optional quality checklist toggle.
- **Interactive Multi-Tab Workspace**:
  - **📝 Skill Editor**: Live editable editor for `SKILL.md` with instant save, rendered markdown preview expander, and automatic cache invalidation on edit.
  - **🔍 Validation**: Structural linter verifying frontmatter delimiters, kebab-case naming, description length, body content, and standard sections.
  - **🧪 Testing Lab**: Evaluates 3 behavioral test scenarios (Instruction Clarity, Safety Guardrails, and Output Specification). Includes single-click **Self-Improve Skill** to auto-patch missing guidelines!
  - **📦 Export ZIP**: In-memory ZIP package creation with real-time ASCII archive tree preview and direct download.

### 2. My Skills Page
- Session library displaying all skills generated during the interactive session.
- Cards showing skill name, category, creation timestamp, and quick actions to open back in workspace or download ZIP.

### 3. Dedicated Testing Lab Page
- Deep diagnostic dashboard displaying structural linter results, overall compliance score, test pass rate, and before/after self-improvement triggers.

### 4. Settings Page
- Local Ollama configuration panel (`http://localhost:11434`).
- Model selector (`qwen2.5:7b`, `qwen2.5:3b`, `llama3.2:3b`, etc.).
- Active live connection ping button to detect running local Ollama instances.
- Clear documentation of Phase 1 vs Phase 2 architecture.

---

## 🚀 Running the Application

1. **Activate Environment**:
   ```bash
   source .venv/bin/activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch Streamlit**:
   ```bash
   streamlit run app.py
   ```
4. **Run Unit Tests**:
   ```bash
   python3 -c "import tests.test_skillforge as t; t.test_slugify(); t.test_generate_mock_skill(); t.test_validate_skill_success(); t.test_validate_skill_errors(); t.test_behavioral_evaluator(); t.test_zip_exporter(); print('All passed!')"
   ```
