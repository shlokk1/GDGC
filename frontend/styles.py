"""
SkillForge — UI & UX Pro Max Design System
Custom CSS styles for a high-end developer studio aesthetic:
- Deep obsidian / dark navy palette with glassmorphism
- Neon violet / cyan / emerald accents
- Polished typography, cards, badges, and micro-interactions
"""

CUSTOM_CSS = """
<style>
/* ==========================================================================
   SkillForge Pro Max Design System — Dark Glassmorphic Theme
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #07090e;
    --bg-surface: #0f172a;
    --bg-surface-elevated: #1e293b;
    --bg-card: rgba(17, 24, 39, 0.72);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(99, 102, 241, 0.35);
    
    --accent-indigo: #6366f1;
    --accent-purple: #a855f7;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Global Font and Body */
html, body, [class*="css"] {
    font-family: var(--font-sans) !important;
}

/* Streamlit Main Container Padding */
.main .block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1280px !important;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
}

/* Top App Brand in Sidebar */
.sf-brand-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.08) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    margin-bottom: 24px;
}

.sf-brand-logo {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 1.25rem;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
}

.sf-brand-title {
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}

.sf-brand-sub {
    font-size: 0.72rem;
    color: var(--accent-cyan);
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin: 0;
}

/* Hero Section */
.sf-hero-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    position: relative;
    overflow: hidden;
}

.sf-hero-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #06b6d4);
}

.sf-hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 6px;
    background: linear-gradient(90deg, #ffffff 30%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sf-hero-desc {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 14px;
}

.sf-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.sf-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.sf-pill-indigo {
    background: rgba(99, 102, 241, 0.15);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.sf-pill-cyan {
    background: rgba(6, 182, 212, 0.15);
    color: #67e8f9;
    border: 1px solid rgba(6, 182, 212, 0.3);
}

.sf-pill-emerald {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.sf-pill-amber {
    background: rgba(245, 158, 11, 0.15);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.sf-pill-rose {
    background: rgba(244, 63, 94, 0.15);
    color: #fda4af;
    border: 1px solid rgba(244, 63, 94, 0.3);
}

/* Workflow Stepper */
.sf-stepper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 24px;
}

.sf-step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
}

.sf-step-item.active {
    color: #f8fafc;
}

.sf-step-item.completed {
    color: var(--accent-emerald);
}

.sf-step-num {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-muted);
}

.sf-step-item.active .sf-step-num {
    background: var(--accent-indigo);
    color: white;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
}

.sf-step-item.completed .sf-step-num {
    background: var(--accent-emerald);
    color: white;
}

.sf-step-divider {
    flex-grow: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.08);
    margin: 0 12px;
}

.sf-step-divider.completed {
    background: var(--accent-emerald);
}

/* Glass Card */
.sf-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
    transition: all 0.2s ease;
}

.sf-card:hover {
    border-color: rgba(255, 255, 255, 0.15);
}

.sf-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.sf-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
}

/* Metric / Stat Boxes */
.sf-stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
}

.sf-stat-box {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
}

.sf-stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}

.sf-stat-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.02em;
}

/* Checklist and Test Item Cards */
.sf-check-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.sf-check-card:hover {
    transform: translateY(-1px);
    border-color: rgba(255, 255, 255, 0.14);
}

.sf-check-card.pass {
    border-left: 3px solid var(--accent-emerald);
}

.sf-check-card.fail {
    border-left: 3px solid var(--accent-rose);
}

.sf-check-card.warn {
    border-left: 3px solid var(--accent-amber);
}

.sf-check-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sf-check-name {
    font-weight: 600;
    font-size: 0.92rem;
    color: #f1f5f9;
}

.sf-check-msg {
    font-size: 0.83rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

.sf-check-tip {
    font-size: 0.78rem;
    color: #a5b4fc;
    background: rgba(99, 102, 241, 0.08);
    padding: 6px 10px;
    border-radius: 6px;
    font-family: var(--font-mono);
}

/* Tree View Visualizer */
.sf-tree-box {
    background: #090d16;
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 16px 20px;
    font-family: var(--font-mono);
    font-size: 0.86rem;
    color: #38bdf8;
    white-space: pre-wrap;
    line-height: 1.6;
}

/* Streamlit Widget Polishing */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] select {
    background-color: #0b1120 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-indigo) !important;
    box-shadow: 0 0 0 1px var(--accent-indigo) !important;
}

/* Streamlit Tabs Customization */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: var(--text-muted) !important;
    padding: 10px 18px !important;
    border-radius: 8px 8px 0 0 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 2px solid var(--accent-indigo) !important;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-1px) !important;
}
</style>
"""
