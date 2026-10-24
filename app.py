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
from generator.skill_generator import generate_mock_skill, generate_skill_with_ollama, slugify
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
    render_skill_rendered_preview,
)
from frontend.icons import (
    icon_layers,
    icon_book_open,
    icon_flask,
    icon_check,
    icon_folder
)

# Page configuration
st.set_page_config(
    page_title="SkillForge — AI Agent Skill Studio",
    page_icon="❖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject UI/UX Pro Max CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Management
# -----------------------------------------------------------------------------
def init_session_state():
    default_task = "Audit Kubernetes Helm charts and manifest YAMLs for security misconfigurations, privilege escalation, and resource quota leaks."
    k8s_default = generate_mock_skill(
        task_desc=default_task,
        category="Software Development",
        constraints="Flag runAsRoot permissions.\nCheck CPU and Memory limits.",
        output_style="Detailed",
        include_checklist=True
    )
    defaults = {
        "current_page": "Create Skill",
        "skill_name": "k8s-helm-audit",
        "skill_content": k8s_default["content"],
        "task_desc_input": default_task,
        "original_task_desc": default_task,
        "category_input": "Software Development",
        "constraints_input": "Flag runAsRoot permissions.\nCheck CPU and Memory limits.",
        "output_style_input": "Detailed",
        "checklist_input": True,
        "has_generated": True,
        "validation_result": validate_skill(k8s_default["content"]),
        "test_result": run_skill_tests(k8s_default["content"], default_task),
        "last_updated": "11:57 AM",
        "export_folder_name": "k8s-helm-audit",
        "skills_history": [
            {
                "name": "k8s-helm-audit",
                "category": "Software Development",
                "content": k8s_default["content"],
                "created_at": "Today, 11:57 AM"
            }
        ],
        "ollama_endpoint": "http://localhost:11434",
        "active_model": "qwen2.5:7b",
        "selected_model": "qwen2.5:7b",
        "ollama_models": [],
        "ollama_connected": False,
        "use_local_model": True,
        "ollama_status_message": "",
        "ollama_checked": False,
        "code_edit_mode": False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    if not st.session_state.ollama_checked:
        st.session_state.ollama_checked = True
        try:
            client = OllamaClient(endpoint=st.session_state.ollama_endpoint)
            res = client.check_connection()
            if res.get("connected"):
                st.session_state.ollama_connected = True
                models = res.get("models", [])
                st.session_state.ollama_models = models
                st.session_state.use_local_model = True
                if "qwen2.5:7b" in models:
                    st.session_state.selected_model = "qwen2.5:7b"
                    st.session_state.active_model = "qwen2.5:7b"
                elif models:
                    st.session_state.selected_model = models[0]
                    st.session_state.active_model = models[0]
                st.session_state.ollama_status_message = res.get("message", "")
        except Exception:
            pass

init_session_state()

# Render Navigation Sidebar
render_sidebar()

# -----------------------------------------------------------------------------
# PAGE 1: CREATE SKILL (Primary Workspace)
# -----------------------------------------------------------------------------
def page_create_skill():
    folder_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'
    info_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
    more_svg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>'
    book_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'

    # Top breadcrumb and title matching Image 1
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; margin-top: -10px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.88rem; color: #94a3b8;">
            <span style="display: flex; align-items: center;">{folder_svg}</span>
            <span>Default Project</span>
            <span style="color: #64748b;">›</span>
            <span style="color: #f1f5f9; font-weight: 600;">{st.session_state.skill_name or 'k8s-helm-audit'}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span class="sf-pill sf-pill-purple-outline" style="display: inline-flex; align-items: center; gap: 6px;">
                <span style="display: flex; align-items: center;">{info_svg}</span>
                <span>Demo Mode</span>
            </span>
            <span style="color: #94a3b8; cursor: pointer; display: flex; align-items: center;">{more_svg}</span>
        </div>
    </div>
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 1.85rem; font-weight: 800; color: #ffffff; margin: 0 0 6px 0; letter-spacing: -0.02em;">Create Your AI Skill</h1>
        <p style="font-size: 0.9rem; color: #94a3b8; margin: 0;">Describe your idea and transform it into a structured, reusable AI agent skill.</p>
    </div>
    """, unsafe_allow_html=True)

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

    # Main split layout: Left form (48%), Right workspace (52%)
    left_col, right_col = st.columns([5, 6], gap="large")

    with left_col:
        # Template expander trigger
        with st.expander("Templates & Presets", expanded=False):
            p_cols = st.columns(3)
            with p_cols[0]:
                if st.button("Python Review", use_container_width=True):
                    st.session_state.task_desc_input = "Review Python code for bugs, security vulnerabilities, and code smells, and suggest verified fixes without modifying files."
                    st.session_state.category_input = "Software Development"
                    st.session_state.constraints_input = "Never modify files in place.\nAdhere to PEP 8 standards.\nInclude line numbers for all issues found."
                    st.rerun()
            with p_cols[1]:
                if st.button("K8s Helm Audit", use_container_width=True):
                    st.session_state.task_desc_input = "Audit Kubernetes Helm charts and manifest YAMLs for security misconfigurations, privilege escalation, and resource quota leaks."
                    st.session_state.category_input = "Software Development"
                    st.session_state.constraints_input = "Flag runAsRoot permissions.\nCheck CPU and Memory limits."
                    st.rerun()
            with p_cols[2]:
                if st.button("OpenAPI Spec", use_container_width=True):
                    st.session_state.task_desc_input = "Generate comprehensive OpenAPI 3.1 specification documentation from FastAPI endpoint code including schema definitions."
                    st.session_state.category_input = "Writing & Documentation"
                    st.session_state.constraints_input = "Include detailed error response codes (400, 401, 404, 500).\nInclude realistic example JSON payloads."
                    st.rerun()

        # Skill Requirements Card Header
        st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.72); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px 14px 0 0; padding: 18px 20px 10px; margin-bottom: -1px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 26px; height: 26px; border-radius: 50%; background: #6366f1; color: #ffffff; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; justify-content: center;">1</div>
                    <div>
                        <h3 style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 0;">Skill Requirements</h3>
                        <p style="font-size: 0.8rem; color: #94a3b8; margin: 2px 0 0 0;">Provide the details for your AI agent skill.</p>
                    </div>
                </div>
                <div style="color: #818cf8; font-size: 0.82rem; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                    <span style="display: flex; align-items: center;">{book_svg}</span>
                    <span>Use a template</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Skill Creation Form Container
        st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.72); border: 1px solid rgba(255, 255, 255, 0.08); border-top: none; border-radius: 0 0 14px 14px; padding: 12px 20px 20px; margin-bottom: 16px;">
        """, unsafe_allow_html=True)

        task_desc = st.text_area(
            "Task Description *",
            value=st.session_state.task_desc_input,
            placeholder="e.g., Audit Kubernetes Helm charts and manifest YAMLs for security misconfigurations...",
            height=125,
            help="Describe the exact agent task in natural language."
        )
        st.session_state.task_desc_input = task_desc
        st.markdown(f"<div style='text-align: right; font-size: 0.75rem; color: #64748b; margin-top: -8px; margin-bottom: 12px;'>{len(task_desc)}/2000</div>", unsafe_allow_html=True)

        category_options = [
            "Software Development",
            "Research & Analysis",
            "Writing & Documentation",
            "Data Processing",
            "Productivity",
            "Other"
        ]
        cat_idx = category_options.index(st.session_state.category_input) if st.session_state.category_input in category_options else 0

        style_cols = st.columns(2)
        with style_cols[0]:
            category = st.selectbox(
                "Skill Category",
                options=category_options,
                index=cat_idx,
                format_func=lambda x: f"</> {x}" if x == "Software Development" else x
            )
            st.session_state.category_input = category
        with style_cols[1]:
            output_style = st.selectbox(
                "Output Style",
                options=["Detailed", "Balanced", "Concise"],
                index=["Detailed", "Balanced", "Concise"].index(st.session_state.output_style_input) if st.session_state.output_style_input in ["Detailed", "Balanced", "Concise"] else 0,
                format_func=lambda x: x
            )
            st.session_state.output_style_input = output_style

        constraints = st.text_area(
            "Rules and Constraints (Optional)",
            value=st.session_state.constraints_input,
            placeholder="e.g., Flag runAsRoot permissions.\nCheck CPU and Memory limits.",
            height=90,
            help="Explicit boundary conditions, security rules, or execution restrictions."
        )
        st.session_state.constraints_input = constraints
        st.markdown(f"<div style='text-align: right; font-size: 0.75rem; color: #64748b; margin-top: -8px; margin-bottom: 12px;'>{len(constraints)}/1000</div>", unsafe_allow_html=True)

        include_checklist = st.checkbox(
            "Include Quality Checklist",
            value=st.session_state.checklist_input,
            help="Add a verification checklist to the generated skill."
        )
        st.markdown("<p style='font-size: 0.78rem; color: #64748b; margin-top: -12px; margin-left: 26px; margin-bottom: 16px;'>Add a verification checklist to the generated skill.</p>", unsafe_allow_html=True)
        st.session_state.checklist_input = include_checklist

        # Generation CTA Button (Clean normal icon, no AI sparkles)
        if st.button("Generate Skill →", type="primary", use_container_width=True):
            if not task_desc or not task_desc.strip():
                st.error("Task Description is required. Please provide a description of the skill.")
            else:
                with st.spinner("Synthesizing standard SKILL.md specification..."):
                    try:
                        if st.session_state.use_local_model:
                            result = generate_skill_with_ollama(
                                task_desc=task_desc,
                                category=category,
                                constraints=constraints,
                                output_style=output_style,
                                include_checklist=include_checklist,
                                endpoint=st.session_state.ollama_endpoint,
                                model=st.session_state.selected_model,
                            )
                            validation = validate_skill(result["content"])
                            if not validation.get("is_valid"):
                                failed_checks = [
                                    check["message"]
                                    for check in validation.get("checks", [])
                                    if not check.get("passed") and check.get("level") == "error"
                                ]
                                raise ValueError(
                                    "The model response did not pass skill validation: "
                                    + "; ".join(failed_checks)
                                )
                        else:
                            result = generate_mock_skill(
                                task_desc=task_desc,
                                category=category,
                                constraints=constraints,
                                output_style=output_style,
                                include_checklist=include_checklist
                            )
                    except (RuntimeError, ValueError) as exc:
                        st.error(f"Skill generation failed: {exc}")
                        return

                    st.session_state.ollama_connected = bool(st.session_state.use_local_model)
                    st.session_state.active_model = result["model"]
                    st.session_state.skill_name = result["name"]
                    st.session_state.skill_content = result["content"]
                    st.session_state.original_task_desc = task_desc
                    st.session_state.has_generated = True
                    st.session_state.export_folder_name = result["name"]
                    
                    st.session_state.validation_result = None
                    st.session_state.test_result = None
                    st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S")

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

        # Stepper rendered at the bottom of the card/column (Image 1)
        render_stepper(step)

        st.markdown("</div>", unsafe_allow_html=True)

    # Right column: Results Workspace or Empty State Guide
    with right_col:
        if not st.session_state.has_generated:
            layers_svg = icon_layers(44, "#6366f1")
            st.markdown(f"""
            <div class="sf-card" style="text-align: center; padding: 48px 24px;">
                <div style="display: flex; justify-content: center; margin-bottom: 16px;">{layers_svg}</div>
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
            # Workspace Tabs — Pro Max Redesign with Vector SVG Icons
            tabs = st.tabs([
                "Preview",
                "Code",
                "Validation",
                "Tests"
            ])

            # TAB 1: PREVIEW (Image 2 Pro Max Rendered View)
            with tabs[0]:
                with st.container(height=520, border=False):
                    st.markdown(render_skill_rendered_preview(st.session_state.skill_content), unsafe_allow_html=True)

            # TAB 2: CODE & EDIT
            with tabs[1]:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; margin-top: 6px;">
                    <div>
                        <span style="font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;">Active File:</span>
                        <span style="font-family: monospace; font-size: 0.95rem; font-weight: 700; color: #ffffff;">{st.session_state.skill_name}/SKILL.md</span>
                    </div>
                    <span class="sf-pill sf-pill-indigo">Last Saved: {st.session_state.last_updated or 'Just now'}</span>
                </div>
                """, unsafe_allow_html=True)

                col_top1, col_top2 = st.columns([6, 3])
                with col_top2:
                    edit_mode = st.toggle("Edit Mode", value=st.session_state.get("code_edit_mode", False), key="toggle_edit_mode")
                    st.session_state.code_edit_mode = edit_mode

                if edit_mode:
                    edited_content = st.text_area(
                        "SKILL.md Content",
                        value=st.session_state.skill_content,
                        height=420,
                        label_visibility="collapsed",
                        key="editor_textarea"
                    )

                    # Actions bar
                    act_cols = st.columns([3, 3, 3])
                    with act_cols[0]:
                        if st.button("Save Edits", type="primary", use_container_width=True):
                            st.session_state.skill_content = edited_content
                            st.session_state.validation_result = None
                            st.session_state.test_result = None
                            st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S")
                            st.toast("Edits saved! Validation and test caches reset.")
                            st.rerun()
                    with act_cols[1]:
                        if st.button("Run Validation", use_container_width=True):
                            st.session_state.skill_content = edited_content
                            st.session_state.validation_result = validate_skill(edited_content)
                            st.toast("Validation complete!")
                            st.rerun()
                    with act_cols[2]:
                        if st.button("Run Behavioral Tests", use_container_width=True):
                            st.session_state.skill_content = edited_content
                            st.session_state.test_result = run_skill_tests(edited_content, st.session_state.task_desc_input)
                            st.toast("Behavioral tests complete!")
                            st.rerun()
                else:
                    with st.container(height=520, border=False):
                        st.code(st.session_state.skill_content, language="markdown", line_numbers=True)

                # Export ZIP Bundle
                with st.expander("Export Skill ZIP Bundle", expanded=False):
                    folder_input = st.text_input(
                        "Folder / Package Name",
                        value=st.session_state.export_folder_name or (st.session_state.skill_name or "my-agent-skill"),
                        help="Customizable slug for folder and ZIP archive."
                    )
                    safe_folder = sanitize_folder_name(folder_input)
                    st.session_state.export_folder_name = safe_folder

                    if st.session_state.validation_result and not st.session_state.validation_result.get("is_valid", True):
                        st.warning("Warning: The current skill has failing structural validation checks. You may still download, but address errors before deploying to agents.")

                    st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase;'>Archive Structure Preview:</p>", unsafe_allow_html=True)
                    st.markdown(f"<div class='sf-tree-box'>{generate_file_tree_view(safe_folder, True)}</div>", unsafe_allow_html=True)

                    zip_bytes = create_skill_zip(
                        folder_name=safe_folder,
                        skill_content=st.session_state.skill_content,
                        include_metadata_manifest=True
                    )

                    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                    st.download_button(
                        label=f"Download {safe_folder}.zip ({len(zip_bytes)} bytes)",
                        data=zip_bytes,
                        file_name=f"{safe_folder}.zip",
                        mime="application/zip",
                        type="primary",
                        use_container_width=True
                    )

            # TAB 3: VALIDATION
            with tabs[2]:
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

                if st.button("Re-Validate Current Content", use_container_width=True):
                    st.session_state.validation_result = validate_skill(st.session_state.skill_content)
                    st.rerun()

            # TAB 4: TESTING LAB
            with tabs[3]:
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
                        <strong>Demo Test Suite:</strong> Standard behavioral evaluation scenarios executing deterministically.
                    </span>
                </div>
                """, unsafe_allow_html=True)

                for t in test_res.get("tests", []):
                    st.markdown(render_test_item(t), unsafe_allow_html=True)

                # Self improvement CTA
                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                t_act_cols = st.columns(2)
                with t_act_cols[0]:
                    if st.button("Self-Improve Skill", type="primary", use_container_width=True, help="Automatically address test observations and upgrade SKILL.md"):
                        improved = improve_skill_content(st.session_state.skill_content, [t for t in test_res.get("tests", []) if t["status"] != "PASSED"])
                        st.session_state.skill_content = improved
                        st.session_state.validation_result = validate_skill(improved)
                        st.session_state.test_result = run_skill_tests(improved, st.session_state.task_desc_input)
                        st.toast("Skill improved and re-tested!")
                        st.rerun()
                with t_act_cols[1]:
                    if st.button("Re-run All Tests", use_container_width=True):
                        st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)
                        st.rerun()


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
        book_svg = icon_book_open(40, "#6366f1")
        st.markdown(f"""
        <div class="sf-card" style="text-align: center; padding: 40px;">
            <div style="display: flex; justify-content: center; margin-bottom: 14px;">{book_svg}</div>
            <h3 style="color: #f8fafc; font-size: 1.2rem;">No Skills Created Yet</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 400px; margin: 0 auto 16px;">
                You haven't generated any agent skills in this session yet. Head over to Create Skill to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Skill", type="primary"):
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
            if st.button(f"Open in Workspace", key=f"open_{idx}", use_container_width=True):
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
                label="Download ZIP",
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
        flask_svg = icon_flask(40, "#6366f1")
        st.markdown(f"""
        <div class="sf-card" style="text-align: center; padding: 40px;">
            <div style="display: flex; justify-content: center; margin-bottom: 14px;">{flask_svg}</div>
            <h3 style="color: #f8fafc; font-size: 1.2rem;">No Active Skill Selected</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; max-width: 400px; margin: 0 auto 16px;">
                Please create or load a skill to run the behavioral evaluation suite.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Skill First", type="primary"):
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
        if st.button("Return to Workspace", use_container_width=True):
            st.session_state.current_page = "Create Skill"
            st.rerun()
    with cta_cols[1]:
        if st.button("Re-evaluate All", use_container_width=True):
            st.session_state.validation_result = validate_skill(st.session_state.skill_content)
            st.session_state.test_result = run_skill_tests(st.session_state.skill_content, st.session_state.task_desc_input)
            st.toast("Evaluations refreshed!")
            st.rerun()
    with cta_cols[2]:
        if st.button("Self-Improve Skill", type="primary", use_container_width=True):
            improved = improve_skill_content(st.session_state.skill_content, [t for t in test_res.get("tests", []) if t["status"] != "PASSED"])
            st.session_state.skill_content = improved
            st.session_state.validation_result = validate_skill(improved)
            st.session_state.test_result = run_skill_tests(improved, st.session_state.task_desc_input)
            st.toast("Skill improved and verified!")
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
            <h3 class="sf-card-title">Local Ollama Model</h3>
            <span class="sf-pill sf-pill-cyan">Private Inference</span>
        </div>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 16px;">
            Connect to Ollama on this machine. Skill generation runs locally, and generated skills are checked before being opened in the editor.
        </p>
    </div>
    """, unsafe_allow_html=True)

    endpoint_input = st.text_input(
        "Ollama Daemon Endpoint",
        value=st.session_state.ollama_endpoint,
        help="Local HTTP endpoint for Ollama REST API."
    )
    if endpoint_input != st.session_state.ollama_endpoint:
        st.session_state.ollama_connected = False
        st.session_state.ollama_status_message = ""
    st.session_state.ollama_endpoint = endpoint_input

    if st.button("Detect & Connect to Ollama", use_container_width=True):
        client = OllamaClient(endpoint=endpoint_input)
        result = client.check_connection()
        st.session_state.ollama_connected = result.get("connected", False)
        st.session_state.ollama_models = result.get("models", [])
        st.session_state.ollama_status_message = result.get("message", "Connection check failed.")
        if result.get("connected") and result.get("models"):
            if st.session_state.selected_model not in result["models"]:
                preferred_model = "qwen2.5:7b"
                st.session_state.selected_model = (
                    preferred_model if preferred_model in result["models"] else result["models"][0]
                )
        st.rerun()

    model_options = st.session_state.ollama_models or [
        "qwen2.5:7b",
        "qwen2.5:3b",
        "llama3.2:3b",
        "deepseek-r1:7b",
        "mistral:7b"
    ]
    if st.session_state.selected_model not in model_options:
        model_options = [st.session_state.selected_model] + model_options
    model_choice = st.selectbox(
        "Ollama Model",
        options=model_options,
        key="selected_model",
        help="Choose a model installed in your local Ollama instance."
    )
    st.session_state.active_model = model_choice

    st.checkbox(
        "Use this local model to generate skills",
        key="use_local_model",
        help="Disable this only if you want to use the deterministic template generator instead."
    )
    if st.session_state.ollama_status_message:
        if st.session_state.ollama_connected:
            st.success(st.session_state.ollama_status_message)
            if st.session_state.ollama_models:
                st.info(f"Installed local models: {', '.join(st.session_state.ollama_models)}")
        else:
            st.error(st.session_state.ollama_status_message)
    elif not st.session_state.ollama_connected:
        st.caption("Connect to Ollama above before generating. If needed, start it with `ollama serve` and install a model with `ollama pull qwen2.5:7b`.")

    # Architecture Reference Box
    st.markdown("""
    <div class="sf-card" style="margin-top: 24px;">
        <h4 style="color: #f8fafc; font-size: 1rem; margin-bottom: 10px;">Roadmap &amp; Architecture Roadmap</h4>
        <div style="font-size: 0.83rem; color: #94a3b8; line-height: 1.6;">
            <div><strong>Generation:</strong> Live local model inference through Ollama, followed by structural validation.</div>
            <div><strong>Evaluation:</strong> Deterministic structural linter and illustrative behavioral test scenarios.</div>
            <div><strong>Privacy:</strong> Prompts are sent only to the configured Ollama endpoint; no cloud model API is called.</div>
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
