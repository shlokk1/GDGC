# ⚡ SkillForge — Local-First AI Agent Skill Studio

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![Agent Skills Standard](https://img.shields.io/badge/Agent_Skills-v1.0-purple.svg)](https://github.com/agent-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**SkillForge** is an open-source, local-first developer studio for architecting, validating, testing, and exporting production-ready AI agent skills (`SKILL.md`). Built with a high-performance **UI & UX Pro Max** design system, SkillForge empowers developers to build safe, deterministic, and modular agent skills without cloud dependencies.

---

## 🌟 Key Features

- **🎨 UI & UX Pro Max Design**: Modern obsidian glassmorphism theme, dynamic glowing status badges, step-by-step interactive workflow progress bar, and real-time feedback.
- **⚡ Instant Presets**: 1-click prompt presets for Python Code Review, Kubernetes Manifest Auditing, and OpenAPI Documentation generation.
- **📝 Live Skill Editor & Markdown Preview**: Edit synthesized `SKILL.md` in real-time with syntax-highlighted preview and automatic state synchronization.
- **🔍 Structural Linter**: Deterministic validation engine checking YAML delimiters, kebab-case naming standard, description criteria, instruction body depth, and required sections.
- **🧪 Behavioral Testing Lab**: Run simulated scenario tests for instruction clarity, safety guardrails, and output consistency, with 1-click **Self-Improvement** to automatically patch test observations.
- **📦 In-Memory ZIP Bundler**: Export complete, standard-compliant skill packages on the fly with live ASCII folder tree preview and zero temporary disk residue.
- **🔒 Local & Private**: 100% private. Ready for Phase 2 zero-cost local LLM inference via Ollama (`qwen2.5:7b`).

---

## 🚀 Quick Start

### 1. Clone & Set Up
```bash
git clone https://github.com/shlokk1/GDGC.git
cd GDGC

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch SkillForge
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Run Tests
```bash
python3 -c "import tests.test_skillforge as t; t.test_slugify(); t.test_generate_mock_skill(); t.test_validate_skill_success(); t.test_validate_skill_errors(); t.test_behavioral_evaluator(); t.test_zip_exporter(); print('All tests passed!')"
```

---

## 🏗️ Architecture

```
GDGC/
├── app.py                      # Main Streamlit application & router
├── requirements.txt            # Dependencies
├── Frontend_Implementation.md  # Detailed frontend implementation docs
├── PRD_Frontend.md             # Product Requirements Document
├── PS.md                       # Problem Statement & Hackathon track
├── PS_summarized.md            # Problem summary
├── README.md                   # Project overview & guide
├── frontend/
│   ├── components.py           # Reusable widgets (Sidebar, Stepper, Cards, Badges)
│   └── styles.py               # UI/UX Pro Max CSS design system
├── generator/
│   ├── prompts.py              # Generation and improvement prompts
│   ├── skill_generator.py      # Deterministic Agent Skills generator
│   └── ollama_client.py        # Local Ollama client (Phase 2 integration)
├── validator/
│   └── skill_validator.py      # Structural & metadata validation engine
├── evaluator/
│   └── test_runner.py          # Behavioral test runner & self-improvement engine
├── exporter/
│   └── zip_exporter.py         # In-memory ZIP archive builder
└── tests/
    └── test_skillforge.py      # Test suite
```

---

## 📄 License
MIT License. Open source and built for the developer community.
