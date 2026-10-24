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

        # Project Context Status in Sidebar
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Project Files</span>
        </div>
        """, unsafe_allow_html=True)

        num_files = len(st.session_state.get("project_files", {}))
        folder_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'
        file_status_label = f"{num_files} File(s) Attached" if num_files > 0 else "No Files Attached"
        st.markdown(f"""
        <div class="sf-proj-item active">
            {folder_svg}
            <span>{file_status_label}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # Recent Skills (Real session history, zero mock data)
        search_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Session Skills</span>
            <span style="color: #94a3b8; cursor: pointer; display: flex; align-items: center;">{search_svg}</span>
        </div>
        """, unsafe_allow_html=True)

        skills_list = st.session_state.get("skills_history", [])
        doc_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>'
        
        if skills_list:
            for s_item in reversed(skills_list[-5:]):
                s_slug = s_item["name"]
                s_date = s_item.get("created_at", "Just now")
                is_active = (s_slug == st.session_state.get("skill_name"))
                cls = "sf-recent-card active" if is_active else "sf-recent-card"
                st.markdown(f"""
                <div class="{cls}">
                    <div style="color: #818cf8; margin-top: 2px; display: flex; align-items: center;">{doc_svg}</div>
                    <div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #ffffff;">{s_slug}</div>
                        <div style="font-size: 0.72rem; color: #64748b;">{s_date}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size: 0.78rem; color: #64748b; margin-left: 4px;'>No skills generated yet</p>", unsafe_allow_html=True)

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
    Completely dynamic parser with zero mock data.
    Extracts sections, step workflows, capabilities, and rules directly from markdown.
    """
    import re
    import html as html_escape

    if not skill_content or not skill_content.strip():
        return f"""
        <div class="sf-preview-window" style="text-align: center; padding: 48px 24px;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); display: inline-flex; align-items: center; justify-content: center; margin-bottom: 16px;">
                {icon_cube(24, "#818cf8")}
            </div>
            <h3 style="color: #f8fafc; font-size: 1.1rem; font-weight: 600; margin-bottom: 8px;">No Skill Content Generated Yet</h3>
            <p style="color: #64748b; font-size: 0.88rem; max-width: 420px; margin: 0 auto; line-height: 1.5;">
                Enter a task description on the left or attach project files and click <strong>Generate Agent Skill</strong> to synthesize your specification with local AI.
            </p>
        </div>
        """

    # 1. Parse Frontmatter if present
    body = skill_content.strip()
    fm_name = ""
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", body, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2).strip()
        name_search = re.search(r"^name:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE)
        if name_search:
            fm_name = name_search.group(1).strip()

    # 2. Extract Title
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    elif fm_name:
        title = fm_name.replace("-", " ").title()
    else:
        title = "Agent Skill Specification"

    # Remove the top # Title from the body to avoid duplicating it
    body_without_title = re.sub(r"^#\s+.+$", "", body, count=1, flags=re.MULTILINE).strip()

    # 3. Parse all ## Sections
    section_splits = re.split(r"(?m)^##\s+(.+)$", body_without_title)
    
    sections = []
    # If there is content before the first ##, treat it as Overview/Purpose
    if section_splits and section_splits[0].strip():
        intro_content = section_splits[0].strip()
        sections.append(("Purpose", intro_content))

    idx = 1
    while idx < len(section_splits):
        sec_title = section_splits[idx].strip()
        sec_body = section_splits[idx + 1].strip() if idx + 1 < len(section_splits) else ""
        sections.append((sec_title, sec_body))
        idx += 2

    # Map section titles to vector SVG icons
    def get_section_icon(title_str: str) -> str:
        low = title_str.lower()
        if any(w in low for w in ["purpose", "overview", "description", "about", "intent"]):
            return icon_shield_check(16, "#94a3b8")
        elif any(w in low for w in ["when", "trigger", "prerequisite", "condition", "scenario", "use"]):
            return icon_target(16, "#94a3b8")
        elif any(w in low for w in ["capabilit", "feature", "action", "tool", "scope"]):
            return icon_cpu(16, "#94a3b8")
        elif any(w in low for w in ["workflow", "step", "procedure", "process", "execution"]):
            return icon_workflow(16, "#94a3b8")
        elif any(w in low for w in ["rule", "constraint", "guardrail", "limit", "security"]):
            return icon_alert_triangle(16, "#94a3b8")
        else:
            return icon_file_code(16, "#94a3b8")

    rendered_sections_html = []

    for s_title, s_content in sections:
        sec_icon = get_section_icon(s_title)
        
        # Check if content has numbered steps (e.g. "1. **Title**\n - bullet")
        step_blocks = re.findall(r"(?ms)(?:^|\n)(\d+)\.\s*(?:\*\*(.*?)\*\*|(.*?))(?:\n|$)(.*?)(?=(?:\n\d+\.|\Z))", s_content)
        
        # Check if content is primarily a list of bullets
        bullets = [
            line.strip().lstrip("-*•").strip() 
            for line in s_content.splitlines() 
            if line.strip().startswith(("-", "*", "•")) and line.strip().lstrip("-*•").strip()
        ]

        if "workflow" in s_title.lower() or "step" in s_title.lower() or (step_blocks and len(step_blocks) >= 2):
            # Render as workflow step cards
            cards_html = []
            for num, b_title, alt_title, block_body in step_blocks:
                header = (b_title or alt_title or "Step").strip()
                sub_bullets = [
                    l.strip().lstrip("-*•").strip() 
                    for l in block_body.splitlines() 
                    if l.strip().startswith(("-", "*", "•")) and l.strip().lstrip("-*•").strip()
                ]
                other_text = [
                    l.strip() 
                    for l in block_body.splitlines() 
                    if l.strip() and not l.strip().startswith(("-", "*", "•"))
                ]
                
                content_inner = ""
                if sub_bullets:
                    b_items = "".join(f"<li>{html_escape.escape(b)}</li>" for b in sub_bullets)
                    content_inner += f'<ul class="sf-preview-bullets sf-nested-bullets">{b_items}</ul>'
                elif other_text:
                    p_items = " ".join(html_escape.escape(t) for t in other_text)
                    content_inner += f'<div style="font-size: 0.84rem; color: #94a3b8; margin-top: 6px; line-height: 1.45;">{p_items}</div>'

                cards_html.append(f"""
                <div class="sf-workflow-box">
                    <div class="sf-workflow-box-header">
                        <span class="sf-num-badge">{num}</span>
                        <span class="sf-workflow-box-title">{html_escape.escape(header)}</span>
                    </div>
                    {content_inner}
                </div>
                """)
            
            rendered_sections_html.append(f"""
            <div class="sf-preview-sec">
                <div class="sf-sec-header">
                    <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                        {sec_icon}
                    </div>
                    <h3 class="sf-sec-title">{html_escape.escape(s_title)}</h3>
                </div>
                {"".join(cards_html)}
            </div>
            """)

        elif ("capabilit" in s_title.lower() or "features" in s_title.lower()) and bullets:
            # Render as Capabilities Badged List
            cap_items = "".join(
                f'<div class="sf-cap-item"><span class="sf-num-badge">{i+1}</span><span class="sf-cap-text">{html_escape.escape(b)}</span></div>'
                for i, b in enumerate(bullets)
            )
            rendered_sections_html.append(f"""
            <div class="sf-preview-sec">
                <div class="sf-sec-header">
                    <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                        {sec_icon}
                    </div>
                    <h3 class="sf-sec-title">{html_escape.escape(s_title)}</h3>
                </div>
                <div class="sf-cap-list">
                    {cap_items}
                </div>
            </div>
            """)

        elif bullets and len(bullets) >= 2 and not any(k in s_title.lower() for k in ["purpose", "overview", "description"]):
            # Render as Bulleted List
            bullet_items = "".join(f"<li>{html_escape.escape(b)}</li>" for b in bullets)
            rendered_sections_html.append(f"""
            <div class="sf-preview-sec">
                <div class="sf-sec-header">
                    <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                        {sec_icon}
                    </div>
                    <h3 class="sf-sec-title">{html_escape.escape(s_title)}</h3>
                </div>
                <ul class="sf-preview-bullets">
                    {bullet_items}
                </ul>
            </div>
            """)

        else:
            # Render as Clean Prose Block
            clean_text = html_escape.escape(s_content)
            # Support basic formatting like inline backticks
            clean_text = re.sub(r"`([^`]+)`", r'<code style="background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; font-size: 0.82rem; color: #a5b4fc;">\1</code>', clean_text)
            clean_text = clean_text.replace("\n\n", "</p><p class='sf-sec-text'>").replace("\n", "<br/>")

            rendered_sections_html.append(f"""
            <div class="sf-preview-sec">
                <div class="sf-sec-header">
                    <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: center;">
                        {sec_icon}
                    </div>
                    <h3 class="sf-sec-title">{html_escape.escape(s_title)}</h3>
                </div>
                <p class="sf-sec-text">{clean_text}</p>
            </div>
            """)

    return f"""
    <div class="sf-preview-window">
        <h2 class="sf-preview-h1">{html_escape.escape(title)}</h2>
        {"".join(rendered_sections_html)}
    </div>
    """
