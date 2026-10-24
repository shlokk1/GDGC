"""
SkillForge — UI Components Module
Provides polished, reusable UI widgets and renderers following the Pro Max design guidelines.
"""

import streamlit as st
from typing import Dict, Any, List, Optional

def render_sidebar():
    """Renders the dark glassmorphic navigation sidebar with brand and status."""
    with st.sidebar:
        st.markdown("""
        <div class="sf-brand-box">
            <div class="sf-brand-logo">⚡</div>
            <div>
                <p class="sf-brand-title">SkillForge</p>
                <p class="sf-brand-sub">Agent Skill Architect</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Menu
        nav_options = [
            "🛠️  Create Skill",
            "📚  My Skills",
            "🧪  Testing Lab",
            "⚙️  Settings"
        ]
        
        # Determine index from session state
        current_page = st.session_state.get("current_page", "Create Skill")
        page_idx = 0
        if current_page == "My Skills":
            page_idx = 1
        elif current_page == "Testing Lab":
            page_idx = 2
        elif current_page == "Settings":
            page_idx = 3

        selected_nav = st.radio(
            "Navigation",
            options=nav_options,
            index=page_idx,
            label_visibility="collapsed"
        )
        
        # Sync back to page key
        cleaned_page = selected_nav.split("  ")[1]
        if cleaned_page != current_page:
            st.session_state.current_page = cleaned_page
            st.rerun()

        st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0 16px;'>", unsafe_allow_html=True)
        
        # System & Model Status
        st.markdown("<p style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em; margin-bottom: 8px;'>System Status</p>", unsafe_allow_html=True)
        
        is_ollama_live = st.session_state.get("ollama_connected", False)
        status_color = "#10b981" if is_ollama_live else "#06b6d4"
        status_text = "Live Ollama Connected" if is_ollama_live else "Ollama Not Connected"
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 14px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background-color: {status_color}; display: inline-block; box-shadow: 0 0 8px {status_color};"></span>
                <span style="font-size: 0.82rem; font-weight: 600; color: #f1f5f9;">{status_text}</span>
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-family: monospace;">Model: {st.session_state.get('active_model', 'qwen2.5:7b (Target)')}</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-family: monospace;">Engine: {"Local Ollama" if st.session_state.get("use_local_model", True) else "Deterministic template"}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Active Skill Tracker
        current_skill_name = st.session_state.get("skill_name")
        if current_skill_name:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 10px; padding: 12px 14px; margin-bottom: 16px;">
                <div style="font-size: 0.72rem; text-transform: uppercase; color: #a5b4fc; font-weight: 700;">Active Session Skill</div>
                <div style="font-size: 0.86rem; font-weight: 700; color: #ffffff; margin-top: 2px; font-family: monospace; word-break: break-all;">{current_skill_name}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Reset Session", use_container_width=True):
            st.session_state.skill_name = None
            st.session_state.skill_content = ""
            st.session_state.task_desc = ""
            st.session_state.validation_result = None
            st.session_state.test_result = None
            st.session_state.has_generated = False
            st.rerun()

def render_hero():
    """Renders the top hero banner with developer-tool branding."""
    st.markdown("""
    <div class="sf-hero-card">
        <h1 class="sf-hero-title">SkillForge Studio</h1>
        <p class="sf-hero-desc">
            Architect, validate, test, and export production-ready AI agent skills.
            Transforms natural language task requirements into standard-compliant <code>SKILL.md</code> packages locally.
        </p>
        <div class="sf-badge-row">
            <span class="sf-pill sf-pill-indigo">✨ Agent Skills Open Standard</span>
            <span class="sf-pill sf-pill-cyan">🔒 Local &amp; Private</span>
            <span class="sf-pill sf-pill-emerald">⚡ Real-time Structural Linter</span>
            <span class="sf-pill sf-pill-amber">📦 In-Memory ZIP Bundler</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stepper(active_step: int = 1):
    """
    Renders an interactive step indicator:
    1: Task Definition
    2: Generated & Editable
    3: Validated
    4: Behavioral Tests
    5: Export Ready
    """
    steps = [
        (1, "Task Spec"),
        (2, "Skill Draft"),
        (3, "Validation"),
        (4, "Behavioral Tests"),
        (5, "ZIP Export")
    ]
    
    html = ['<div class="sf-stepper">']
    for idx, (num, label) in enumerate(steps):
        if num < active_step:
            cls = "completed"
            icon = "✓"
        elif num == active_step:
            cls = "active"
            icon = str(num)
        else:
            cls = ""
            icon = str(num)
            
        html.append(f"""
        <div class="sf-step-item {cls}">
            <div class="sf-step-num">{icon}</div>
            <span>{label}</span>
        </div>
        """)
        
        if idx < len(steps) - 1:
            div_cls = "completed" if num < active_step else ""
            html.append(f'<div class="sf-step-divider {div_cls}"></div>')
            
    html.append('</div>')
    st.markdown("".join(html), unsafe_allow_html=True)

def render_stat_box(label: str, value: Any, color: str = "#ffffff"):
    return f"""
    <div class="sf-stat-box">
        <span class="sf-stat-label">{label}</span>
        <span class="sf-stat-value" style="color: {color};">{value}</span>
    </div>
    """

def render_check_item(check: Dict[str, Any]):
    """Renders a single structural validation check card."""
    is_passed = check.get("passed", False)
    level = check.get("level", "info")
    name = check.get("name", "Check")
    msg = check.get("message", "")
    tip = check.get("suggestion")

    if is_passed:
        card_cls = "pass"
        badge = '<span class="sf-pill sf-pill-emerald">● PASSED</span>'
    elif level == "warning":
        card_cls = "warn"
        badge = '<span class="sf-pill sf-pill-amber">▲ WARNING</span>'
    else:
        card_cls = "fail"
        badge = '<span class="sf-pill sf-pill-rose">✕ FAILED</span>'

    tip_html = f'<div class="sf-check-tip">💡 <strong>Suggestion:</strong> {tip}</div>' if tip else ""

    return f"""
    <div class="sf-check-card {card_cls}">
        <div class="sf-check-row">
            <span class="sf-check-name">{name}</span>
            {badge}
        </div>
        <div class="sf-check-msg">{msg}</div>
        {tip_html}
    </div>
    """

def render_test_item(test: Dict[str, Any]):
    """Renders a single behavioral test case card."""
    status = test.get("status", "PENDING")
    tid = test.get("id", "TC-00")
    name = test.get("name", "Test Scenario")
    scenario = test.get("scenario", "")
    expected = test.get("expected", "")
    observed = test.get("observed", "")
    score = test.get("score", 0)

    if status == "PASSED":
        card_cls = "pass"
        badge = f'<span class="sf-pill sf-pill-emerald">● PASSED ({score}/100)</span>'
    elif status == "REQUIRES REVIEW":
        card_cls = "warn"
        badge = f'<span class="sf-pill sf-pill-amber">▲ REQUIRES REVIEW ({score}/100)</span>'
    else:
        card_cls = "fail"
        badge = f'<span class="sf-pill sf-pill-rose">✕ FAILED ({score}/100)</span>'

    return f"""
    <div class="sf-check-card {card_cls}">
        <div class="sf-check-row">
            <div>
                <span style="font-family: monospace; font-size: 0.78rem; color: #a5b4fc; margin-right: 6px;">{tid}</span>
                <span class="sf-check-name">{name}</span>
            </div>
            {badge}
        </div>
        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;"><strong>Scenario:</strong> {scenario}</div>
        <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 2px;"><strong>Expected:</strong> {expected}</div>
        <div style="font-size: 0.8rem; color: #38bdf8; margin-top: 2px;"><strong>Observed:</strong> {observed}</div>
    </div>
    """
