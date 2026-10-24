"""
SkillForge — Local-First AI Agent Skill Generator
Phase 1: Full-Featured Frontend Implementation with Pro Max UI/UX Design
Conforms to PRD_Frontend.md and the Agent Skills Open Standard.
"""

import sys
import os
import datetime
import streamlit as st

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from validator.skill_validator import validate_skill
from generator.skill_generator import generate_mock_skill, slugify
from generator.ollama_client import OllamaClient
from evaluator.test_runner import run_skill_tests, improve_skill_content
from exporter.zip_exporter import create_skill_zip, sanitize_folder_name, generate_file_tree_view
from frontend.styles import CUSTOM_CSS
from frontend.components import (
    render_sidebar,
    render_hero,
    render_stepper,
    render_stat_box,
    render_check_item,
    render_test_item,
)

# Page configuration
st.set_page_config(
    page_title="SkillForge — AI Agent Skill Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject UI/UX Pro Max CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Management
# -----------------------------------------------------------------------------
def init_session_state():
    defaults = {
        "current_page": "Create Skill",
        "skill_name": None,
        "skill_content": "",
        "task_desc_input": "",
        "original_task_desc": "",
        "category_input": "Software Development",
        "constraints_input": "",
        "output_style_input": "Balanced",
        "checklist_input": True,
        "has_generated": False,
        "validation_result": None,
        "test_result": None,
        "last_updated": None,
        "export_folder_name": "",
        "skills_history": [],
        "ollama_endpoint": "http://localhost:11434",
        "active_model": "qwen2.5:7b (Target)",
        "ollama_connected": False,
        "execution_mode": "Deterministic Engine (Phase 1)"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# Render Navigation Sidebar
render_sidebar()

# -----------------------------------------------------------------------------
# PAGE 1: CREATE SKILL (Primary Workspace)
# -----------------------------------------------------------------------------
def page_create_skill():
    render_hero()

    # Step progress derivation
    step = 1
    if st.session_state.has_generated:
        step = 2
    if st.session_state.validation_result is not None:
        step = 3
    if st.session_state.test_result is not None:
        step = 4
    if st.session_state.validation_result and st.session_state.validation_result.get("is_valid") and st.session_state.test_result:
        step = 5

    render_stepper(step)

    # Main split layout: Left form (40%), Right workspace (60%) if generated, or centered card
    left_col, right_col = st.columns([5, 7] if st.session_state.has_generated else [7, 5], gap="large")

    with left_col:
        st.markdown("""
        <div class="sf-card">
            <div class="sf-card-header">
                <h3 class="sf-card-title">1. Define Skill Requirements</h3>
                <span class="sf-pill sf-pill-indigo">Step 1</span>
            </div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px;">
                Specify the exact capability you want to instill in an autonomous AI agent.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Quick preset selector
        st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #a5b4fc; margin-bottom: 6px;'>💡 Quick Presets (Click to load):</p>", unsafe_allow_html=True)
        preset_cols = st.columns(3)
        with preset_cols[0]:
            if st.button("🐍 Python Code Review", use_container_width=True):
                st.session_state.task_desc_input = "Review Python code for bugs, security vulnerabilities, and code smells, and suggest verified fixes without modifying files."
                st.session_state.category_input = "Software Development"
                st.session_state.constraints_input = "Never modify files in place.\nAdhere to PEP 8 standards.\nInclude line numbers for all issues found."
                st.rerun()
        with preset_cols[1]:
            if st.button("☸️ K8s Helm Auditor", use_container_width=True):
                st.session_state.task_desc_input = "Audit Kubernetes Helm charts and manifest YAMLs for security misconfigurations, privilege escalation, and resource quota leaks."
                st.session_state.category_input = "Software Development"
                st.session_state.constraints_input = "Flag runAsRoot permissions.\nCheck CPU and Memory limits.\nFollow CIS benchmark recommendations."
                st.rerun()
        with preset_cols[2]:
            if st.button("📝 OpenAPI Doc Writer", use_container_width=True):
                st.session_state.task_desc_input = "Generate comprehensive OpenAPI 3.1 specification documentation from FastAPI endpoint code including schema definitions."
                st.session_state.category_input = "Writing & Documentation"
                st.session_state.constraints_input = "Include detailed error response codes (400, 401, 404, 500).\nInclude realistic example JSON payloads."
                st.rerun()

        # Skill Creation Form
        task_desc = st.text_area(
            "Task Description *",
            value=st.session_state.task_desc_input,
            placeholder="e.g., Create an AI skill that reviews Python code, finds bugs and security issues, and suggests fixes without modifying files...",
            height=130,
            help="Describe the exact agent task in natural language."
        )
        st.session_state.task_desc_input = task_desc

        category_options = [
            "Software Development",
            "Research & Analysis",
            "Writing & Documentation",
            "Data Processing",
            "Productivity",
            "Other"
        ]
        cat_idx = category_options.index(st.session_state.category_input) if st.session_state.category_input in category_options else 0
        category = st.selectbox("Skill Category", options=category_options, index=cat_idx)
        st.session_state.category_input = category

        constraints = st.text_area(
            "Rules and Constraints (Optional)",
            value=st.session_state.constraints_input,
            placeholder="e.g., Never modify user files directly\nOnly return read-only unified diffs\nProvide deterministic explanations",
            height=90,
            help="Explicit boundary conditions, security rules, or execution restrictions."
        )
        st.session_state.constraints_input = constraints

        style_cols = st.columns(2)
        with style_cols[0]:
            output_style = st.selectbox(
                "Output Style",
                options=["Balanced", "Detailed", "Concise"],
                index=["Balanced", "Detailed", "Concise"].index(st.session_state.output_style_input)
            )
            st.session_state.output_style_input = output_style
        with style_cols[1]:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            include_checklist = st.checkbox(
                "Include Quality Checklist",
                value=st.session_state.checklist_input
            )
            st.session_state.checklist_input = include_checklist

        # Generation CTA
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button("✨ Generate Agent Skill", type="primary", use_container_width=True):
            if not task_desc or not task_desc.strip():
                st.error("⚠️ Task Description is required. Please provide a description of the skill.")
            else:
                with st.spinner("Synthesizing standard SKILL.md specification..."):
                    # Deterministic mock generation as per Phase 1 PRD
                    result = generate_mock_skill(
                        task_desc=task_desc,
                        category=category,
                        constraints=constraints,
                        output_style=output_style,
                        include_checklist=include_checklist
                    )
                    st.session_state.skill_name = result["name"]
                    st.session_state.skill_content = result["content"]
                    st.session_state.original_task_desc = task_desc
                    st.session_state.has_generated = True
                    st.session_state.export_folder_name = result["name"]
                    
                    # Rule 10: Generation resets previous validation and test results
                    st.session_state.validation_result = None
                    st.session_state.test_result = None
                    st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S")

                    # Add to session history if not already present
                    exists = any(item["name"] == result["name"] for item in st.session_state.skills_history)
                    if not exists:
                        st.session_state.skills_history.append({
                            "name": result["name"],
                            "category": category,
                            "content": result["content"],
                            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    st.success(f"Skill `{result['name']}` generated successfully!")
                    st.rerun()

        # Phase 1 notice badge
        st.markdown("""
        <div style="margin-top: 16px; padding: 10px 14px; background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 8px;">
            <p style="font-size: 0.76rem; color: #38bdf8; margin: 0; line-height: 1.4;">
                ℹ️ <strong>Phase 1 Notice:</strong> Generation uses a deterministic Agent Skills template engine. No external LLM or cloud API is invoked.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Right column: Results Workspace or Empty State Guide
    with right_col:
        if not st.session_state.has_generated:
            st.markdown("""
            <div class="sf-card" style="text-align: center; padding: 48px 24px;">
                <div style="font-size: 3.5rem; margin-bottom: 12px;">⚡</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; color: #f8fafc; margin-bottom: 8px;">Agent Workspace Idle</h3>
                <p style="font-size: 0.88rem; color: #94a3b8; max-width: 420px; margin: 0 auto 20px;">
                    Enter a task description on the left or click one of the quick presets to synthesize your first standardized AI agent skill package.
                </p>
                <div style="display: inline-flex; gap: 12px; justify-content: center;">
                    <span class="sf-pill sf-pill-indigo">YAML Frontmatter</span>
                    <span class="sf-pill sf-pill-cyan">Deterministic Linter</span>
                    <span class="sf-pill sf-pill-emerald">ZIP Bundler</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Workspace Tabs (PRD Section 9.3)
            tabs = st.tabs([
                "📝 Skill Editor",
                "🔍 Validation",
                "🧪 Testing Lab",
                "📦 Export ZIP"
            ])

            # TAB 1: SKILL EDITOR
            with tabs[0]:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <span style="font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;">Active File:</span>
                        <span style="font-family: monospace; font-size: 0.95rem; font-weight: 700; color: #ffffff;">{st.session_state.skill_name}/SKILL.md</span>
                    </div>
                    <span class="sf-pill sf-pill-indigo">Last Saved: {st.session_state.last_updated or 'Just now'}</span>
                </div>
                """, unsafe_allow_html=True)

                # Editable Text Area
                edited_content = st.text_area(
                    "SKILL.md Content",
                    value=st.session_state.skill_content,
                    height=380,
                    label_visibility="collapsed",
                    key="editor_textarea"
                )

                # Actions bar
                act_cols = st.columns([3, 3, 3])
                with act_cols[0]:
                    if st.button("💾 Save Edits", type="primary", use_container_width=True):
                        st.session_state.skill_content = edited_content
                        # Rule 10: Saving edits invalidates previous validation and test results
                        st.session_state.validation_result = None
                        st.session_state.test_result = None
                        st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S")
                        st.toast("Edits saved! Validation and test caches reset.", icon="✅")
                        st.rerun()
                with act_cols[1]:
                    if st.button("🔍 Run Validation", use_container_width=True):
                        st.session_state.skill_content = edited_content
                        st.session_state.validation_result = validate_skill(edited_content)
                        st.toast("Validation complete!", icon="🔍")
                        st.rerun()
                with act_cols[2]:
                    if st.button("🧪 Run Behavioral Tests", use_container_width=True):
                        st.session_state.skill_content = edited_content
                        st.session_state.test_result = run_skill_tests(edited_content, st.session_state.task_desc_input)
                        st.toast("Behavioral tests complete!", icon="🧪")
                        st.rerun()

                # Rendered Markdown Preview
                with st.expander("👁️ Rendered Markdown Preview", expanded=False):
                    st.markdown(st.session_state.skill_content)

            # TAB 2: VALIDATION
            with tabs[1]:
                # Automatically run validation if not yet run
                if st.session_state.validation_result is None:
                    st.session_state.validation_result = validate_skill(st.session_state.skill_content)

                val = st.session_state.validation_result
                is_valid = val.get("is_valid", False)
                score = val.get("score", 0)
                passed_cnt = val.get("passed_checks", 0)
                total_cnt = val.get("total_checks", 0)

                # Stat row
                st.markdown("<div class='sf-stat-grid'>", unsafe_allow_html=True)
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    status_badge = "PASSED" if is_valid else "FAILED"
                    status_col = "#10b981" if is_valid else "#f43f5e"
                    st.markdown(render_stat_box("Validation Status", status_badge, status_col), unsafe_allow_html=True)
                with stat_col2:
                    st.markdown(render_stat_box("Compliance Score", f"{score}%", "#6366f1"), unsafe_allow_html=True)
                with stat_col3:
                    st.markdown(render_stat_box("Passed Checks", f"{passed_cnt}/{total_cnt}", "#38bdf8"), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"<p style='font-size: 0.88rem; color: #cbd5e1; margin-bottom: 14px;'><strong>Summary:</strong> {val.get('summary', '')}</p>", unsafe_allow_html=True)

                # List of checks
                st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;'>Detailed Structural Checks:</p>", unsafe_allow_html=True)
                for check in val.get("checks", []):
                    st.markdown(render_check_item(check), unsafe_allow_html=True)

                if st.button("🔄 Re-Validate Current Content", use_container_width=True):
                    st.session_state.validation_result = validate_skill(st.session_state.skill_content)
                    st.rerun()

            # TAB 3: TESTING LAB
            with tabs[2]:
                if st.session_state.test_result is None:
                    st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)

                test_res = st.session_state.test_result
                tot = test_res.get("total_tests", 0)
                pas = test_res.get("passed_tests", 0)
                rev = test_res.get("review_tests", 0)
                rate = test_res.get("pass_rate", 0)

                st.markdown("<div class='sf-stat-grid'>", unsafe_allow_html=True)
                tcol1, tcol2, tcol3 = st.columns(3)
                with tcol1:
                    st.markdown(render_stat_box("Total Scenarios", tot, "#ffffff"), unsafe_allow_html=True)
                with tcol2:
                    st.markdown(render_stat_box("Passed Scenarios", pas, "#10b981"), unsafe_allow_html=True)
                with tcol3:
                    st.markdown(render_stat_box("Pass Rate", f"{rate}%", "#6366f1" if rate >= 80 else "#f59e0b"), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""
                <div style="padding: 8px 12px; background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; margin-bottom: 14px;">
                    <span style="font-size: 0.78rem; color: #a5b4fc;">
                        ℹ️ <strong>Demo Test Suite:</strong> These are illustrative behavioral evaluation scenarios. No external LLM was charged or executed.
                    </span>
                </div>
                """, unsafe_allow_html=True)

                for t in test_res.get("tests", []):
                    st.markdown(render_test_item(t), unsafe_allow_html=True)

                # Self improvement CTA
                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                t_act_cols = st.columns(2)
                with t_act_cols[0]:
                    if st.button("⚡ Self-Improve Skill", type="primary", use_container_width=True, help="Automatically address test observations and upgrade SKILL.md"):
                        improved = improve_skill_content(st.session_state.skill_content, [t for t in test_res.get("tests", []) if t["status"] != "PASSED"])
                        st.session_state.skill_content = improved
                        st.session_state.validation_result = validate_skill(improved)
                        st.session_state.test_result = run_skill_tests(improved, st.session_state.task_desc_input)
                        st.toast("Skill improved and re-tested!", icon="🚀")
                        st.rerun()
                with t_act_cols[1]:
                    if st.button("🔄 Re-run All Tests", use_container_width=True):
                        st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)
                        st.rerun()

            # TAB 4: EXPORT ZIP
            with tabs[3]:
                st.markdown("""
                <div class="sf-card">
                    <div class="sf-card-header">
                        <h4 class="sf-card-title">Package &amp; Export Skill Bundle</h4>
                        <span class="sf-pill sf-pill-cyan">Standard Bundle</span>
                    </div>
                    <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">
                        Generates an in-memory ZIP package containing standard-compliant <code>SKILL.md</code> and package manifest.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                folder_input = st.text_input(
                    "Folder / Package Name",
                    value=st.session_state.export_folder_name or (st.session_state.skill_name or "my-agent-skill"),
                    help="Customizable slug for folder and ZIP archive."
                )
                safe_folder = sanitize_folder_name(folder_input)
                st.session_state.export_folder_name = safe_folder

                # Validation warning if invalid
                if st.session_state.validation_result and not st.session_state.validation_result.get("is_valid", True):
                    st.warning("⚠️ Warning: The current skill has failing structural validation checks. You may still download, but address errors before deploying to agents.")

                # Package Tree Preview
                st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;'>Archive Structure Preview:</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='sf-tree-box'>{generate_file_tree_view(safe_folder, True)}</div>", unsafe_allow_html=True)

                # ZIP generation in memory
                zip_bytes = create_skill_zip(
                    folder_name=safe_folder,
                    skill_content=st.session_state.skill_content,
                    include_metadata_manifest=True
                )

                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                st.download_button(
                    label=f"⬇️ Download {safe_folder}.zip ({len(zip_bytes)} bytes)",
                    data=zip_bytes,
                    file_name=f"{safe_folder}.zip",
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )


# -----------------------------------------------------------------------------
# PAGE 2: MY SKILLS (Session Library)
# -----------------------------------------------------------------------------
def page_my_skills():
    st.markdown("""
    <div class="sf-hero-card">
        <h1 class="sf-hero-title">Session Skills Library</h1>
        <p class="sf-hero-desc">
            Manage and inspect all skills generated in your current interactive session.
        </p>
        <span class="sf-pill sf-pill-indigo">Session Memory Only (Phase 1)</span>
    </div>
    """, unsafe_allow_html=True)

    skills = st.session_state.skills_history
    if not skills and not st.session_state.skill_name:
        st.markdown("""
        <div class="sf-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 3rem; margin-bottom: 8px;">📚</div>
            <h3 style="color: #f8fafc; font-size: 1.2rem;">No Skills Created Yet</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 400px; margin: 0 auto 16px;">
                You haven't generated any agent skills in this session yet. Head over to Create Skill to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Go to Create Skill", type="primary"):
            st.session_state.current_page = "Create Skill"
            st.rerun()
        return

    # List session skills
    st.markdown(f"<p style='font-size: 0.88rem; color: #94a3b8;'>Found <strong>{len(skills)}</strong> skill(s) created in this session:</p>", unsafe_allow_html=True)

    for idx, item in enumerate(skills):
        is_active = (item["name"] == st.session_state.skill_name)
        active_badge = '<span class="sf-pill sf-pill-emerald">● ACTIVE</span>' if is_active else ''
        
        st.markdown(f"""
        <div class="sf-card">
            <div class="sf-card-header">
                <div>
                    <span style="font-family: monospace; font-size: 1.05rem; font-weight: 700; color: #ffffff;">{item['name']}</span>
                    <span class="sf-pill sf-pill-cyan" style="margin-left: 8px;">{item.get('category', 'General')}</span>
                </div>
                {active_badge}
            </div>
            <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 12px;">Created: {item.get('created_at', 'Today')}</p>
        </div>
        """, unsafe_allow_html=True)

        scol1, scol2, scol3 = st.columns([3, 3, 6])
        with scol1:
            if st.button(f"📂 Open in Workspace", key=f"open_{idx}", use_container_width=True):
                st.session_state.skill_name = item["name"]
                st.session_state.skill_content = item["content"]
                st.session_state.has_generated = True
                st.session_state.validation_result = validate_skill(item["content"])
                st.session_state.test_result = run_skill_tests(item["content"])
                st.session_state.current_page = "Create Skill"
                st.rerun()
        with scol2:
            zip_data = create_skill_zip(item["name"], item["content"])
            st.download_button(
                label="⬇️ Download ZIP",
                data=zip_data,
                file_name=f"{item['name']}.zip",
                mime="application/zip",
                key=f"dl_{idx}",
                use_container_width=True
            )


# -----------------------------------------------------------------------------
# PAGE 3: TESTING LAB (Dedicated Dashboard)
# -----------------------------------------------------------------------------
def page_testing_lab():
    st.markdown("""
    <div class="sf-hero-card">
        <h1 class="sf-hero-title">Testing &amp; Quality Lab</h1>
        <p class="sf-hero-desc">
            Deep diagnostic evaluation suite. Validates structural syntax and simulates behavioral execution against standard test scenarios.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.has_generated or not st.session_state.skill_name:
        st.markdown("""
        <div class="sf-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 3rem; margin-bottom: 8px;">🧪</div>
            <h3 style="color: #f8fafc; font-size: 1.2rem;">No Active Skill Selected</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 400px; margin: 0 auto 16px;">
                Please create or load a skill to run the behavioral evaluation suite.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Create a Skill First", type="primary"):
            st.session_state.current_page = "Create Skill"
            st.rerun()
        return

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
        <div>
            <span style="font-size: 0.85rem; color: #94a3b8;">Testing Skill:</span>
            <span style="font-family: monospace; font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-left: 8px;">{st.session_state.skill_name}</span>
        </div>
        <span class="sf-pill sf-pill-indigo">Agent Skills Standard v1.0</span>
    </div>
    """, unsafe_allow_html=True)

    # Compute or retrieve validation and tests
    if st.session_state.validation_result is None:
        st.session_state.validation_result = validate_skill(st.session_state.skill_content)
    if st.session_state.test_result is None:
        st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)

    val = st.session_state.validation_result
    test_res = st.session_state.test_result

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(render_stat_box("Structural Status", "PASSED" if val.get("is_valid") else "FAILED", "#10b981" if val.get("is_valid") else "#f43f5e"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_stat_box("Validation Score", f"{val.get('score', 0)}%", "#6366f1"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_stat_box("Behavioral Tests", f"{test_res.get('passed_tests', 0)}/{test_res.get('total_tests', 0)}", "#38bdf8"), unsafe_allow_html=True)
    with m4:
        st.markdown(render_stat_box("Test Pass Rate", f"{test_res.get('pass_rate', 0)}%", "#10b981" if test_res.get('pass_rate', 0) >= 80 else "#f59e0b"), unsafe_allow_html=True)

    col_val, col_test = st.columns(2, gap="medium")
    with col_val:
        st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-bottom: 10px;'>Structural Linter Checks</h4>", unsafe_allow_html=True)
        for check in val.get("checks", []):
            st.markdown(render_check_item(check), unsafe_allow_html=True)

    with col_test:
        st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-bottom: 10px;'>Behavioral Scenario Results</h4>", unsafe_allow_html=True)
        for t in test_res.get("tests", []):
            st.markdown(render_test_item(t), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    cta_cols = st.columns([4, 4, 4])
    with cta_cols[0]:
        if st.button("⬅️ Return to Workspace", use_container_width=True):
            st.session_state.current_page = "Create Skill"
            st.rerun()
    with cta_cols[1]:
        if st.button("🔄 Re-evaluate All", use_container_width=True):
            st.session_state.validation_result = validate_skill(st.session_state.skill_content)
            st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)
            st.toast("Evaluations refreshed!", icon="✅")
            st.rerun()
    with cta_cols[2]:
        if st.button("⚡ Self-Improve Skill", type="primary", use_container_width=True):
            improved = improve_skill_content(st.session_state.skill_content, [t for t in test_res.get("tests", []) if t["status"] != "PASSED"])
            st.session_state.skill_content = improved
            st.session_state.validation_result = validate_skill(improved)
            st.session_state.test_result = run_skill_tests(improved, st.session_state.task_desc_input)
            st.toast("Skill improved and verified!", icon="🚀")
            st.rerun()


# -----------------------------------------------------------------------------
# PAGE 4: SETTINGS (Local Model & Architecture)
# -----------------------------------------------------------------------------
def page_settings():
    st.markdown("""
    <div class="sf-hero-card">
        <h1 class="sf-hero-title">Engine Configuration &amp; Settings</h1>
        <p class="sf-hero-desc">
            Configure local AI runtime connection and inspection parameters.
            SkillForge is built local-first for 100% data privacy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sf-card">
        <div class="sf-card-header">
            <h3 class="sf-card-title">Local Ollama Integration (Planned Phase 2)</h3>
            <span class="sf-pill sf-pill-cyan">Local AI Runtime</span>
        </div>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px;">
            In Phase 2, SkillForge connects directly to Ollama running on your machine to perform live LLM skill generation, autonomous test execution, and continuous revision loops.
        </p>
    </div>
    """, unsafe_allow_html=True)

    endpoint_input = st.text_input(
        "Ollama Daemon Endpoint",
        value=st.session_state.ollama_endpoint,
        help="Local HTTP endpoint for Ollama REST API."
    )
    st.session_state.ollama_endpoint = endpoint_input

    model_options = [
        "qwen2.5:7b",
        "qwen2.5:3b",
        "llama3.2:3b",
        "deepseek-r1:7b",
        "mistral:7b"
    ]
    model_choice = st.selectbox(
        "Target Open-Weight Model",
        options=model_options,
        index=0,
        help="Selected model for Phase 2 local inference."
    )
    st.session_state.active_model = f"{model_choice} (Target)"

    # Live connection test
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🔌 Test Connection to Ollama Daemon", use_container_width=True):
        client = OllamaClient(endpoint=endpoint_input, default_model=model_choice)
        res = client.check_connection()
        if res.get("connected"):
            st.session_state.ollama_connected = True
            st.success(f"✅ {res.get('message')}")
            if res.get("models"):
                st.info(f"Available installed models: {', '.join(res.get('models'))}")
        else:
            st.session_state.ollama_connected = False
            st.info(f"ℹ️ {res.get('message')}\n\nRunning in Phase 1 Deterministic Mode. To enable Phase 2, start Ollama locally (`ollama serve`).")

    # Architecture Reference Box
    st.markdown("""
    <div class="sf-card" style="margin-top: 24px;">
        <h4 style="color: #f8fafc; font-size: 1rem; margin-bottom: 10px;">Roadmap &amp; Architecture Roadmap</h4>
        <div style="font-size: 0.83rem; color: #94a3b8; line-height: 1.6;">
            <div><strong>Phase 1 (Current):</strong> Full Streamlit Pro Max UI/UX, deterministic generation engine, structural linter, illustrative test lab, and in-memory ZIP exporter.</div>
            <div><strong>Phase 2:</strong> Connect to local <code>qwen2.5:7b</code> via Ollama for zero-cost, private prompt generation.</div>
            <div><strong>Phase 3:</strong> Extended Agent Skills validator with AST-based parsing and safety scanning.</div>
            <div><strong>Phase 4:</strong> Behavioral sandboxed sandbox runner executing real agent tasks.</div>
            <div><strong>Phase 5:</strong> Multi-turn automated self-healing feedback loop.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Main Application Router
# -----------------------------------------------------------------------------
def main():
    page = st.session_state.current_page
    if page == "Create Skill":
        page_create_skill()
    elif page == "My Skills":
        page_my_skills()
    elif page == "Testing Lab":
        page_testing_lab()
    elif page == "Settings":
        page_settings()
    else:
        page_create_skill()

if __name__ == "__main__":
    main()
