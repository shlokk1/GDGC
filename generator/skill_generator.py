"""
SkillForge — Skill Generator Module
Generates standardized Agent Skill specifications.
Supports:
1. Live local AI inference via Ollama (qwen2.5:7b).
2. Deterministic template generation (offline fallback).
"""

import re
from typing import Dict, Any, Optional, List
from generator.ollama_client import OllamaClient
from generator.prompts import SYSTEM_PROMPT, build_generation_prompt, build_improvement_prompt

def slugify(text: str) -> str:
    """Converts a phrase into a clean kebab-case identifier."""
    cleaned = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", cleaned).strip("-")
    parts = slug.split("-")
    if len(parts) > 5:
        slug = "-".join(parts[:5])
    return slug or "custom-agent-skill"

def clean_llm_markdown(raw_text: str) -> str:
    """Strips leading/trailing markdown code fences if the model wraps the output."""
    text = raw_text.strip()
    # Strip markdown block wrappers like ```markdown ... ``` or ```yaml ... ```
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

def generate_mock_skill(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True
) -> Dict[str, Any]:
    """Generates a deterministic standard-compliant SKILL.md template."""
    skill_slug = slugify(task_desc)
    words = task_desc.strip().split()
    title_words = words[:6] if len(words) > 6 else words
    readable_title = " ".join(w.capitalize() for w in title_words) or "Agent Task Execution Skill"

    if constraints and constraints.strip():
        user_constraints_md = "\n".join(f"- {line.strip()}" for line in constraints.strip().splitlines() if line.strip())
    else:
        user_constraints_md = "- Adhere strictly to user security requirements and sandboxed execution boundaries.\n- Never perform destructive actions or overwrite files without explicit authorization.\n- Return deterministic and verified answers."

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

def generate_ai_skill(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True,
    endpoint: str = "http://localhost:11434",
    model: str = "qwen2.5:7b"
) -> Dict[str, Any]:
    """Generates an Agent Skill using the local Ollama LLM model."""
    client = OllamaClient(endpoint=endpoint, default_model=model)
    prompt = build_generation_prompt(
        task_desc=task_desc,
        category=category,
        constraints=constraints,
        output_style=output_style,
        include_checklist=include_checklist
    )
    
    resp = client.generate(prompt=prompt, system=SYSTEM_PROMPT, model=model)
    if resp.get("success") and resp.get("response"):
        cleaned = clean_llm_markdown(resp["response"])
        # Extract slug from frontmatter or derive from task
        name_match = re.search(r"^name:\s*([^\n\r]+)", cleaned, re.MULTILINE)
        if name_match:
            slug = slugify(name_match.group(1))
        else:
            slug = slugify(task_desc)
            # Inject name if missing
            if cleaned.startswith("---"):
                cleaned = cleaned.replace("---", f"---\nname: {slug}", 1)
                
        return {
            "name": slug,
            "content": cleaned,
            "is_mock": False,
            "model": f"Ollama ({model})",
            "category": category,
            "task_desc": task_desc
        }
    else:
        # Fallback to mock if Ollama generation failed
        mock_res = generate_mock_skill(task_desc, category, constraints, output_style, include_checklist)
        mock_res["error"] = resp.get("error", "Local Ollama generation failed, fell back to template.")
        return mock_res

def generate_skill_with_ollama(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True,
    endpoint: str = "http://localhost:11434",
    model: str = "qwen2.5:7b"
) -> Dict[str, Any]:
    """Generates a skill via Ollama or raises RuntimeError if model inference fails."""
    res = generate_ai_skill(task_desc, category, constraints, output_style, include_checklist, endpoint, model)
    if res.get("is_mock") and "error" in res:
        raise RuntimeError(res["error"])
    return res

def improve_ai_skill(
    current_content: str,
    failure_report: str,
    endpoint: str = "http://localhost:11434",
    model: str = "qwen2.5:7b"
) -> str:
    """Uses the local LLM to refine and fix an existing skill."""
    client = OllamaClient(endpoint=endpoint, default_model=model)
    prompt = build_improvement_prompt(current_skill=current_content, failure_report=failure_report)
    resp = client.generate(prompt=prompt, system=SYSTEM_PROMPT, model=model)
    if resp.get("success") and resp.get("response"):
        return clean_llm_markdown(resp["response"])
    return current_content
