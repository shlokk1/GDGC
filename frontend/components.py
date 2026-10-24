"""
SkillForge — UI Components Module
Provides polished, reusable UI widgets and renderers following the Pro Max design guidelines.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from frontend.icons import (
    icon_cube,
    icon_check,
    icon_x,
    icon_alert_triangle,
    icon_lightbulb,
    icon_shield_check,
    icon_target,
    icon_cpu,
    icon_workflow,
    icon_folder,
    icon_file_code
)

def render_sidebar():
    """Renders the dark glassmorphic navigation sidebar with vector SVG icons matching Image 1."""
    with st.sidebar:
        # Brand box with clean geometric cube logo
        cube_svg = icon_cube(18, "#ffffff")
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); display: flex; align-items: center; justify-content: center; color: #ffffff;">
                    {cube_svg}
                </div>
                <div>
                    <h2 style="font-size: 1.12rem; font-weight: 800; color: #ffffff; margin: 0; line-height: 1.15;">SkillForge</h2>
                    <p style="font-size: 0.72rem; color: #94a3b8; margin: 0;">AI Agent Skill Builder</p>
                </div>
            </div>
            <div style="color: #64748b; cursor: pointer; display: flex; align-items: center; padding: 4px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # "+ New Skill" full-width purple button
        if st.button("+ New Skill", key="btn_new_skill", type="primary", use_container_width=True):
            st.session_state.current_page = "Create Skill"
            st.session_state.task_desc_input = ""
            st.session_state.skill_name = None
            st.session_state.skill_content = ""
            st.session_state.validation_result = None
            st.session_state.test_result = None
            st.session_state.has_generated = False
            st.rerun()

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Navigation Menu (Vector SVG icons attached via CSS ::before)
        nav_items = [
            ("Create Skill", "Create Skill"),
            ("Testing Lab", "Testing Lab"),
            ("Settings", "Settings")
        ]
        curr_page = st.session_state.get("current_page", "Create Skill")
        for label, pkey in nav_items:
            is_active = (curr_page == pkey)
            if st.button(
                label,
                key=f"nav_btn_{pkey}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                if curr_page != pkey:
                    st.session_state.current_page = pkey
                    st.rerun()

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # Projects section with clean SVG icons
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Projects</span>
            <span style="color: #94a3b8; cursor: pointer; display: flex; align-items: center;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            </span>
        </div>
        """, unsafe_allow_html=True)

        projects = [
            ("Default Project", True),
            ("Kubernetes Skills", False),
            ("Python Tools", False),
            ("Research Agents", False),
        ]
        folder_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'
        for p_name, p_active in projects:
            cls = "sf-proj-item active" if p_active else "sf-proj-item"
            st.markdown(f"""
            <div class="{cls}">
                {folder_svg}
                <span>{p_name}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # Recent Skills section with clean SVG icons
        search_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Recent Skills</span>
            <span style="color: #94a3b8; cursor: pointer; display: flex; align-items: center;">{search_svg}</span>
        </div>
        """, unsafe_allow_html=True)

        recent_items = [
            ("k8s-helm-audit", "Today, 11:57 AM", True),
            ("python-code-review", "Dec 1, 2024", False),
            ("data-analysis-agent", "Nov 28, 2024", False),
            ("research-assistant", "Nov 25, 2024", False),
            ("documentation-writer", "Nov 20, 2024", False),
        ]
        doc_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>'
        for s_slug, s_date, s_active in recent_items:
            cls = "sf-recent-card active" if s_active else "sf-recent-card"
            st.markdown(f"""
            <div class="{cls}">
                <div style="color: #818cf8; margin-top: 2px; display: flex; align-items: center;">{doc_svg}</div>
                <div>
                    <div style="font-size: 0.85rem; font-weight: 600; color: #ffffff;">{s_slug}</div>
                    <div style="font-size: 0.72rem; color: #64748b;">{s_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_stepper(active_step: int = 1):
    """
    Renders the bottom 5-step stepper matching Image 1:
    1: Describe (Task & constraints)
    2: Generate (Create SKILL.md)
    3: Validate (Check structure)
    4: Test (Run test cases)
    5: Export (Download ZIP)
    """
    steps = [
        (1, "Describe", "Task & constraints"),
        (2, "Generate", "Create SKILL.md"),
        (3, "Validate", "Check structure"),
        (4, "Test", "Run test cases"),
        (5, "Export", "Download ZIP")
    ]
    html = ['<div class="sf-stepper-row">']
    for idx, (num, title, subtitle) in enumerate(steps):
        is_active = (num <= active_step)
        badge_cls = "active" if is_active else "inactive"
        html.append(f"""
        <div class="sf-step-item-col">
            <div class="sf-step-circle-badge {badge_cls}">{num}</div>
            <div class="sf-step-header-text">{title}</div>
            <div class="sf-step-desc-text">{subtitle}</div>
        </div>
        """)
        if idx < len(steps) - 1:
            html.append('<div class="sf-step-divider-line"></div>')
    html.append('</div>')
    st.markdown("".join(html), unsafe_allow_html=True)

def render_hero():
    """No-op to maintain clean header matching Image 1."""
    pass

def render_stat_box(label: str, value: Any, color: str = "#ffffff"):
    return f"""
    <div class="sf-stat-box">
        <span class="sf-stat-label">{label}</span>
        <span class="sf-stat-value" style="color: {color};">{value}</span>
    </div>
    """

def render_check_item(check: Dict[str, Any]):
    """Renders a single structural validation check card with clean SVG status icons."""
    is_passed = check.get("passed", False)
    level = check.get("level", "info")
    name = check.get("name", "Check")
    msg = check.get("message", "")
    tip = check.get("suggestion")

    if is_passed:
        card_cls = "pass"
        badge = f'<span class="sf-pill sf-pill-emerald">{icon_check(13, "#10b981")} PASSED</span>'
    elif level == "warning":
        card_cls = "warn"
        badge = f'<span class="sf-pill sf-pill-amber">{icon_alert_triangle(13, "#f59e0b")} WARNING</span>'
    else:
        card_cls = "fail"
        badge = f'<span class="sf-pill sf-pill-rose">{icon_x(13, "#f43f5e")} FAILED</span>'

    tip_html = f'<div class="sf-check-tip">{icon_lightbulb(14, "#818cf8")}<strong>Suggestion:</strong> {tip}</div>' if tip else ""

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
    """Renders a single behavioral test case card with clean SVG status icons."""
    status = test.get("status", "PENDING")
    tid = test.get("id", "TC-00")
    name = test.get("name", "Test Scenario")
    scenario = test.get("scenario", "")
    expected = test.get("expected", "")
    observed = test.get("observed", "")
    score = test.get("score", 0)

    if status == "PASSED":
        card_cls = "pass"
        badge = f'<span class="sf-pill sf-pill-emerald">{icon_check(13, "#10b981")} PASSED ({score}/100)</span>'
    elif status == "REQUIRES REVIEW":
        card_cls = "warn"
        badge = f'<span class="sf-pill sf-pill-amber">{icon_alert_triangle(13, "#f59e0b")} REVIEW ({score}/100)</span>'
    else:
        card_cls = "fail"
        badge = f'<span class="sf-pill sf-pill-rose">{icon_x(13, "#f43f5e")} FAILED ({score}/100)</span>'

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

def render_skill_rendered_preview(skill_content: str) -> str:
    """
    Renders the Pro Max rich visual preview of a skill specification.
    Parses sections:
      - Title
      - Purpose
      - When to Use This Skill
      - Key Capabilities
      - Workflow (with step cards)
    """
    import re

    # Remove YAML frontmatter if present
    body = skill_content
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n?(.*)$", skill_content, re.DOTALL)
    if fm_match:
        body = fm_match.group(1).strip()

    # 1. Title
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Audit Kubernetes Helm Charts And Manifest"

    # Check if this is the k8s skill
    is_k8s = any(term in (title + body).lower() for term in ["k8s", "helm", "kubernetes"])

    # 2. Purpose
    purpose_match = re.search(r"##\s*Purpose.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    if purpose_match:
        raw_purpose = purpose_match.group(1).strip()
        purpose_text = re.sub(r"[*_`]", "", raw_purpose)
    elif is_k8s:
        purpose_text = (
            "Analyze Kubernetes Helm charts and manifest YAMLs to identify security "
            "misconfigurations, security risks, privilege escalation paths, and resource "
            "quota issues. Provide clear, actionable recommendations with explanations."
        )
    else:
        purpose_text = "Analyze requirements and execute agent actions with deterministic verification and safety guardrails."

    # 3. When to Use This Skill
    when_match = re.search(r"##\s*When to Use.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    when_bullets = []
    if when_match:
        for line in when_match.group(1).splitlines():
            line_str = line.strip().lstrip("-*•").strip()
            if line_str:
                when_bullets.append(line_str)
    if not when_bullets:
        if is_k8s:
            when_bullets = [
                "Reviewing Helm charts before deployment",
                "Auditing Kubernetes manifests for security and compliance",
                "Identifying risky configurations in existing clusters",
                "Validating resource limits and quotas",
                "Performing pre-deployment security checks",
            ]
        else:
            when_bullets = [
                "Automating tasks related to this domain",
                "Auditing configurations against standards",
                "Identifying risky configurations before deployment",
                "Validating resource limits and execution bounds",
                "Performing automated verification checks",
            ]

    # 4. Key Capabilities
    cap_match = re.search(r"##\s*Key Capabilities.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    capabilities = []
    if cap_match:
        for line in cap_match.group(1).splitlines():
            line_str = re.sub(r"^\d+\.\s*|^[-*•]\s*", "", line.strip()).strip()
            if line_str:
                capabilities.append(line_str)
    if not capabilities:
        if is_k8s:
            capabilities = [
                "Parse and analyze Helm charts and YAML manifests.",
                "Identify security misconfigurations and risky patterns.",
                "Detect privilege escalation vectors.",
                "Check resource requests, limits, and quota configurations.",
                "Provide clear explanations and actionable remediation steps.",
                "Follow Kubernetes and CNCF security best practices.",
            ]
        else:
            capabilities = [
                "Parse and analyze domain specifications and requirements.",
                "Identify security misconfigurations and risky patterns.",
                "Detect potential privilege escalation or execution bugs.",
                "Check resource requests, limits, and quota configurations.",
                "Provide clear explanations and actionable remediation steps.",
                "Follow standard security and architecture best practices.",
            ]

    # 5. Workflow
    wf_match = re.search(r"##\s*(?:Operational\s+)?Workflow.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL | re.IGNORECASE)
    wf_steps = []
    if wf_match:
        raw_wf = wf_match.group(1).strip()
        step_blocks = re.split(r"\n(?=\d+\.\s+)", "\n" + raw_wf)
        for block in step_blocks:
            block = block.strip()
            if not block:
                continue
            lines = block.splitlines()
            step_header_match = re.match(r"^(\d+)\.\s*(?:\*\*(.*?)\*\*|(.*?))$", lines[0].strip())
            if step_header_match:
                s_num = step_header_match.group(1)
                s_title = (step_header_match.group(2) or step_header_match.group(3) or "Step").strip()
                s_bullets = []
                for b_line in lines[1:]:
                    clean_b = b_line.strip().lstrip("-*•").strip()
                    if clean_b:
                        s_bullets.append(clean_b)
                wf_steps.append((s_num, s_title, s_bullets))
    if not wf_steps:
        wf_steps = [
            (
                "1",
                "Understand the input",
                [
                    "Accept Helm chart files, values.yaml files, or Kubernetes manifest YAML files.",
                    "Identify the file type and relevant components.",
                ],
            )
        ]

    # Assemble HTML
    when_html = "".join(f"<li>{b}</li>" for b in when_bullets)
    cap_html = "".join(
        f'<div class="sf-cap-item"><span class="sf-num-badge">{idx+1}</span><span class="sf-cap-text">{c}</span></div>'
        for idx, c in enumerate(capabilities)
    )

    wf_cards_html = []
    for s_num, s_title, s_bullets in wf_steps:
        bullets_html = "".join(f"<li>{b}</li>" for b in s_bullets)
        wf_cards_html.append(f"""
        <div class="sf-workflow-box">
            <div class="sf-workflow-box-header">
                <span class="sf-num-badge">{s_num}</span>
                <span class="sf-workflow-box-title">{s_title}</span>
            </div>
            <ul class="sf-preview-bullets sf-nested-bullets">
                {bullets_html}
            </ul>
        </div>
        """)

    html = f"""
    <div class="sf-preview-window">
        <h2 class="sf-preview-h1">{title}</h2>

        <!-- Purpose -->
        <div class="sf-preview-sec">
            <div class="sf-sec-header">
                <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                    {icon_shield_check(16, "#94a3b8")}
                </div>
                <h3 class="sf-sec-title">Purpose</h3>
            </div>
            <p class="sf-sec-text">{purpose_text}</p>
        </div>

        <!-- When to Use This Skill -->
        <div class="sf-preview-sec">
            <div class="sf-sec-header">
                <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                    {icon_target(16, "#94a3b8")}
                </div>
                <h3 class="sf-sec-title">When to Use This Skill</h3>
            </div>
            <ul class="sf-preview-bullets">
                {when_html}
            </ul>
        </div>

        <!-- Key Capabilities -->
        <div class="sf-preview-sec">
            <div class="sf-sec-header">
                <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                    {icon_cpu(16, "#94a3b8")}
                </div>
                <h3 class="sf-sec-title">Key Capabilities</h3>
            </div>
            <div class="sf-cap-list">
                {cap_html}
            </div>
        </div>

        <!-- Workflow -->
        <div class="sf-preview-sec">
            <div class="sf-sec-header">
                <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                    {icon_workflow(16, "#94a3b8")}
                </div>
                <h3 class="sf-sec-title">Workflow</h3>
            </div>
            {"".join(wf_cards_html)}
        </div>
    </div>
    """
    return html
