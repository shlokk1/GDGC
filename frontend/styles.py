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

/* Compact sidebar top spacing without hiding any navigation elements */
[data-testid="stSidebarHeader"] {
    padding-top: 0.25rem !important;
    padding-bottom: 0.25rem !important;
    height: auto !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 2rem !important;
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

.sf-pill-purple-outline {
    background: rgba(99, 102, 241, 0.08);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 9999px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Sidebar Custom Elements */
.sf-proj-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
}

.sf-proj-item:hover {
    background: rgba(255, 255, 255, 0.04);
    color: #cbd5e1;
}

.sf-proj-item.active {
    background: rgba(99, 102, 241, 0.15);
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.sf-recent-card {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
}

.sf-recent-card:hover {
    background: rgba(255, 255, 255, 0.04);
}

.sf-recent-card.active {
    background: rgba(99, 102, 241, 0.18);
    border: 1px solid rgba(99, 102, 241, 0.35);
}

/* Bottom Stepper (Image 1) */
.sf-stepper-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-top: 26px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.sf-step-item-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 82px;
}

.sf-step-circle-badge {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.sf-step-circle-badge.active {
    background: #6366f1;
    color: #ffffff;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
}

.sf-step-circle-badge.inactive {
    background: rgba(255, 255, 255, 0.08);
    color: #64748b;
}

.sf-step-header-text {
    font-size: 0.8rem;
    font-weight: 700;
    color: #f1f5f9;
}

.sf-step-desc-text {
    font-size: 0.68rem;
    color: #64748b;
    margin-top: 2px;
    line-height: 1.3;
}

.sf-step-divider-line {
    flex-grow: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.12);
    margin-top: 13px;
    min-width: 12px;
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

/* Streamlit Tabs Customization — Segmented Dark Bar (Pro Max with Vector SVG Icons) */
div[data-testid="stTabs"] {
    background: transparent !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background-color: #0b1120 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 5px 6px !important;
    gap: 6px !important;
    display: inline-flex !important;
    width: 100% !important;
    border-bottom: none !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    color: #94a3b8 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    height: auto !important;
    display: inline-flex !important;
    align-items: center !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
    color: #f1f5f9 !important;
    background: rgba(255, 255, 255, 0.04) !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(79, 70, 229, 0.45) !important;
}

/* Tab 1: Preview — Eye SVG */
div[data-testid="stTabs"] button[data-baseweb="tab"]:nth-child(1)::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E") no-repeat center / contain;
}

/* Tab 2: Code — Code SVG */
div[data-testid="stTabs"] button[data-baseweb="tab"]:nth-child(2)::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='16 18 22 12 16 6'/%3E%3Cpolyline points='8 6 2 12 8 18'/%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='16 18 22 12 16 6'/%3E%3Cpolyline points='8 6 2 12 8 18'/%3E%3C/svg%3E") no-repeat center / contain;
}

/* Tab 3: Validation — Green Checkmark SVG */
div[data-testid="stTabs"] button[data-baseweb="tab"]:nth-child(3)::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-color: #10b981;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E") no-repeat center / contain;
}

/* Tab 4: Tests — Flask SVG */
div[data-testid="stTabs"] button[data-baseweb="tab"]:nth-child(4)::before {
    content: '';
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 7px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.69 19.3A2 2 0 0 0 6.42 22h11.16a2 2 0 0 0 1.73-2.7L14 9.31V2'/%3E%3Cline x1='8.5' y1='2' x2='15.5' y2='2'/%3E%3Cline x1='6.5' y1='16' x2='17.5' y2='16'/%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.69 19.3A2 2 0 0 0 6.42 22h11.16a2 2 0 0 0 1.73-2.7L14 9.31V2'/%3E%3Cline x1='8.5' y1='2' x2='15.5' y2='2'/%3E%3Cline x1='6.5' y1='16' x2='17.5' y2='16'/%3E%3C/svg%3E") no-repeat center / contain;
}

/* Sidebar Nav Buttons with SVG icons */
section[data-testid="stSidebar"] div.stButton:nth-of-type(1) button p::before {
    content: '';
    display: inline-block;
    width: 14px;
    height: 14px;
    margin-right: 6px;
    vertical-align: -1px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='5' x2='12' y2='19'%3E%3C/line%3E%3Cline x1='5' y1='12' x2='19' y2='12'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='5' x2='12' y2='19'%3E%3C/line%3E%3Cline x1='5' y1='12' x2='19' y2='12'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
}

section[data-testid="stSidebar"] div.stButton:nth-of-type(2) button p::before {
    content: '';
    display: inline-block;
    width: 14px;
    height: 14px;
    margin-right: 8px;
    vertical-align: -1px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'%3E%3C/path%3E%3Cpolyline points='14 2 14 8 20 8'%3E%3C/polyline%3E%3Cline x1='16' y1='13' x2='8' y2='13'%3E%3C/line%3E%3Cline x1='16' y1='17' x2='8' y2='17'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'%3E%3C/path%3E%3Cpolyline points='14 2 14 8 20 8'%3E%3C/polyline%3E%3Cline x1='16' y1='13' x2='8' y2='13'%3E%3C/line%3E%3Cline x1='16' y1='17' x2='8' y2='17'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
}

section[data-testid="stSidebar"] div.stButton:nth-of-type(3) button p::before {
    content: '';
    display: inline-block;
    width: 14px;
    height: 14px;
    margin-right: 8px;
    vertical-align: -1px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.69 19.3A2 2 0 0 0 6.42 22h11.16a2 2 0 0 0 1.73-2.7L14 9.31V2'%3E%3C/path%3E%3Cline x1='8.5' y1='2' x2='15.5' y2='2'%3E%3C/line%3E%3Cline x1='6.5' y1='16' x2='17.5' y2='16'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.69 19.3A2 2 0 0 0 6.42 22h11.16a2 2 0 0 0 1.73-2.7L14 9.31V2'%3E%3C/path%3E%3Cline x1='8.5' y1='2' x2='15.5' y2='2'%3E%3C/line%3E%3Cline x1='6.5' y1='16' x2='17.5' y2='16'%3E%3C/line%3E%3C/svg%3E") no-repeat center / contain;
}

section[data-testid="stSidebar"] div.stButton:nth-of-type(4) button p::before {
    content: '';
    display: inline-block;
    width: 14px;
    height: 14px;
    margin-right: 8px;
    vertical-align: -1px;
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'%3E%3C/circle%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z'%3E%3C/path%3E%3C/svg%3E") no-repeat center / contain;
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'%3E%3C/circle%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z'%3E%3C/path%3E%3C/svg%3E") no-repeat center / contain;
}

/* Rendered Preview Window (Pro Max Design) */
.sf-preview-window {
    background: #0b1120;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 26px 28px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.36);
    margin-top: 14px;
}

.sf-preview-h1 {
    font-size: 1.55rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0 0 24px 0;
    line-height: 1.3;
}

.sf-preview-sec {
    margin-bottom: 24px;
}

.sf-sec-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.sf-sec-icon-circle {
    width: 28px;
    height: 28px;
    min-width: 28px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.sf-sec-icon-blue {
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
}

.sf-sec-icon-pink {
    background: rgba(236, 72, 153, 0.2);
    border: 1px solid rgba(236, 72, 153, 0.4);
    box-shadow: 0 0 10px rgba(236, 72, 153, 0.2);
}

.sf-sec-icon-cyan {
    background: rgba(6, 182, 212, 0.2);
    border: 1px solid rgba(6, 182, 212, 0.4);
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
}

.sf-sec-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
}

.sf-sec-text {
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.65;
    margin: 0;
}

.sf-preview-bullets {
    list-style: none;
    padding-left: 6px;
    margin: 0;
}

.sf-preview-bullets li {
    position: relative;
    padding-left: 20px;
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 6px;
}

.sf-preview-bullets li::before {
    content: "•";
    position: absolute;
    left: 4px;
    color: #94a3b8;
    font-size: 1.1rem;
}

.sf-cap-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 6px;
}

.sf-cap-item {
    display: flex;
    align-items: center;
    gap: 12px;
}

.sf-num-badge {
    width: 24px;
    height: 24px;
    min-width: 24px;
    border-radius: 50%;
    background: #6366f1;
    color: #ffffff;
    font-size: 0.8rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 8px rgba(99, 102, 241, 0.4);
}

.sf-cap-text {
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.5;
}

.sf-workflow-box {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 10px;
    margin-bottom: 12px;
}

.sf-workflow-box-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.sf-workflow-box-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: #ffffff;
}

.sf-nested-bullets {
    padding-left: 36px;
    margin: 0;
}

.sf-nested-bullets li {
    margin-bottom: 4px;
    line-height: 1.55;
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
