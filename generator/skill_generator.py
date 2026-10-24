"""
SkillForge — Skill Generator Module
Generates standardized Agent Skill specifications.
Supports deterministic template generation (Phase 1) and seamless Ollama LLM integration (Phase 2).
"""

import re
from typing import Dict, Any, Optional

def slugify(text: str) -> str:
    """Converts a phrase into a clean kebab-case identifier."""
    # Clean non-alphanumeric
    cleaned = re.sub(r"[^\w\s-]", "", text.lower())
    # Replace whitespace and repeated dashes with single dash
    slug = re.sub(r"[-\s]+", "-", cleaned).strip("-")
    # Take first 4-5 words or 35 chars max to keep slug neat
    parts = slug.split("-")
    if len(parts) > 5:
        slug = "-".join(parts[:5])
    return slug or "custom-agent-skill"

def generate_mock_skill(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True
) -> Dict[str, Any]:
    """
    Generates a deterministic, standards-compliant SKILL.md template based on inputs.
    Follows Agent Skills standard specification.
    """
    skill_slug = slugify(task_desc)
    
    # Capitalized readable title
    words = task_desc.strip().split()
    title_words = words[:6] if len(words) > 6 else words
    readable_title = " ".join(w.capitalize() for w in title_words)
    if not readable_title:
        readable_title = "Agent Task Execution Skill"

    # User constraints formatting
    if constraints and constraints.strip():
        user_constraints_md = "\n".join(f"- {line.strip()}" for line in constraints.strip().splitlines() if line.strip())
    else:
        user_constraints_md = "- Adhere strictly to user security requirements and sandboxed execution boundaries.\n- Never perform destructive actions or overwrite files without explicit authorization.\n- Return deterministic and verified answers."

    # Style tone adjustment
    if output_style == "Concise":
        verbosity_note = "Provide minimal, high-density outputs. Focus on bullet points and immediate code diffs without conversational filler."
    elif output_style == "Detailed":
        verbosity_note = "Provide thorough explanations, rationale for each recommendation, architecture context, and comprehensive code walk-throughs."
    else:
        verbosity_note = "Provide balanced responses with concise summaries backed by focused code examples and clear explanations."

    checklist_section = ""
    if include_checklist:
        checklist_section = f"""
## Quality & Verification Checklist
Before completing the task, verify:
- [ ] Task objectives from original request are 100% satisfied.
- [ ] All specified user constraints and safety boundaries were upheld.
- [ ] Output formatting complies with `{output_style}` standard.
- [ ] Syntax is verified and free from parsing errors.
- [ ] No extraneous file system or network side-effects occurred.
"""

    content = f"""---
name: {skill_slug}
description: Automatically {task_desc.strip()[:120].lower()} with standardized verification and safety guards.
category: {category}
version: 1.0.0
author: SkillForge AI
tags:
  - {slugify(category)}
  - agent-skills
  - automation
---

# {readable_title}

## Purpose & Overview
This skill instructs an AI agent to execute: **{task_desc.strip()}**.
It establishes a structured procedure, handles boundary conditions, enforces constraints, and guarantees predictable, high-fidelity results.

## Operational Workflow
Follow these sequential phases when executing this skill:

1. **Context & Requirement Analysis**
   - Ingest user input and inspect target artifacts.
   - Parse all boundary constraints and environment prerequisites.
   - Clarify any ambiguous instructions before executing actions.

2. **Plan & Validation**
   - Formulate a stepwise execution plan.
   - Verify that all referenced paths, APIs, or schema exist and are accessible.

3. **Execution & Synthesis**
   - Perform primary computation or transformation matching the category: `{category}`.
   - Maintain safety invariants and avoid unauthorized side effects.

4. **Review & Output Formatting**
   - Format output according to the specified **{output_style}** style guideline.
   - Cross-check against the Quality & Verification Checklist.

## Strict Rules & Constraints
{user_constraints_md}
- **Style Enforcement**: {verbosity_note}
- **Fail-Safe Principle**: If a critical error or unhandled edge case arises, halt and surface a clean diagnostic message instead of guessing.

## Expected Output Format
The final response delivered to the user must include:
- **Summary**: A concise description of actions taken.
- **Artifacts / Findings**: Structured deliverables, code snippets, or analytical points.
- **Verification Status**: Explicit statement confirming all constraints were satisfied.
{checklist_section}"""

    return {
        "name": skill_slug,
        "content": content.strip(),
        "is_mock": True,
        "model": "SkillForge Deterministic Engine v1.0",
        "category": category,
        "task_desc": task_desc
    }
