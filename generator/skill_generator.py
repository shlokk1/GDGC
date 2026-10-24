"""
SkillForge — Skill Generator Module
Generates standardized Agent Skill specifications.
Supports:
1. Live local AI inference via Ollama (qwen2.5:7b).
2. Grounding in user-imported project files.
3. Deterministic template generation (offline fallback).
"""

import re
import yaml
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
    """
    Cleans raw LLM response.
    Extracts the document starting from the first frontmatter delimiter '---'.
    Removes extraneous markdown fences and preamble.
    """
    text = raw_text.strip()
    
    # Strip markdown block wrappers like ```markdown ... ```
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # If the model included commentary before '---', locate the frontmatter
    fm_idx = text.find("---")
    if fm_idx != -1:
        text = text[fm_idx:].strip()

    # If trailing closing code block exists, strip it
    if text.endswith("```"):
        text = text[:-3].strip()

    return text

def normalize_llm_skill(raw_text: str, task_desc: str) -> str:
    """Normalize model output to a complete, parseable SKILL.md frontmatter block."""
    text = clean_llm_markdown(raw_text)
    heading = re.search(r"(?m)^#{1,6}\s+.+$", text)
    if not heading:
        raise ValueError("The local model response did not include a Markdown skill body.")

    metadata_text = text[:heading.start()].strip()
    body = text[heading.start():].strip()
    if metadata_text.startswith("---"):
        metadata_text = metadata_text[3:].strip()
    if metadata_text.endswith("---"):
        metadata_text = metadata_text[:-3].strip()

    metadata: Dict[str, Any] = {}
    try:
        parsed = yaml.safe_load(metadata_text)
        if isinstance(parsed, dict):
            metadata = parsed
    except yaml.YAMLError:
        pass

    def metadata_value(key: str) -> Optional[str]:
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        match = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.*?)\s*$", metadata_text)
        if not match:
            return None
        raw_value = match.group(1).strip()
        try:
            parsed_value = yaml.safe_load(raw_value)
        except yaml.YAMLError:
            parsed_value = raw_value.strip("\"'")
        return parsed_value.strip() if isinstance(parsed_value, str) and parsed_value.strip() else None

    name = slugify(metadata_value("name") or task_desc)
    description = metadata_value("description") or (
        f"Provides instructions for {task_desc.strip().rstrip('.')}"
    )
    safe_description = yaml.safe_dump(
        description,
        allow_unicode=True,
        default_style='"'
    ).strip()
    return f"---\nname: {name}\ndescription: {safe_description}\n---\n\n{body}"

def generate_mock_skill(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True,
    project_files: Optional[Dict[str, str]] = None
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

    ref_files_section = ""
    if project_files:
        file_bullets = "\n".join(f"- `{fname}`: project reference artifact" for fname in project_files.keys())
        ref_files_section = f"""
## Reference Project Files
This skill is tailored to the following project artifacts:
{file_bullets}
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

## When to Use This Skill
- Performing automated review and auditing for `{category}` workflows.
- Identifying security misconfigurations, bugs, or syntax errors.
- Enforcing structured, reproducible quality standards across the project.

## Key Capabilities
1. Ingests and inspects input code, schema, and environment specifications.
2. Identifies security misconfigurations, bugs, and edge cases.
3. Formulates prioritized remediation steps with clear rationale.
4. Strictly respects execution constraints and sandboxed environments.

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
{ref_files_section}
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
    model: str = "qwen2.5:7b",
    project_files: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Generates an Agent Skill using the local Ollama LLM model."""
    client = OllamaClient(endpoint=endpoint, default_model=model)
    prompt = build_generation_prompt(
        task_desc=task_desc,
        category=category,
        constraints=constraints,
        output_style=output_style,
        include_checklist=include_checklist,
        project_files=project_files
    )
    
    resp = client.generate(prompt=prompt, system=SYSTEM_PROMPT, model=model, temperature=0.2)
    if resp.get("success") and resp.get("response"):
        try:
            cleaned = normalize_llm_skill(resp["response"], task_desc)
        except ValueError as exc:
            retry_prompt = (
                "Your previous response could not be used because "
                f"{exc}\nRegenerate the complete skill. Put a closing --- line after the YAML "
                "frontmatter and include a Markdown heading and body. Return only SKILL.md.\n\n"
                f"Original task:\n{prompt}\n\nPrevious response:\n{resp['response']}"
            )
            retry_resp = client.generate(
                prompt=retry_prompt,
                system=SYSTEM_PROMPT,
                model=model,
                temperature=0.1
            )
            if not retry_resp.get("success") or not retry_resp.get("response"):
                mock_res = generate_mock_skill(
                    task_desc, category, constraints, output_style, include_checklist, project_files
                )
                mock_res["error"] = retry_resp.get(
                    "error",
                    "The local model returned an incomplete skill document and the retry failed."
                )
                return mock_res
            try:
                cleaned = normalize_llm_skill(retry_resp["response"], task_desc)
            except ValueError as retry_error:
                mock_res = generate_mock_skill(
                    task_desc, category, constraints, output_style, include_checklist, project_files
                )
                mock_res["error"] = f"The local model returned an incomplete skill document: {retry_error}"
                return mock_res

        name_match = re.match(r"^---\s*\nname:\s*([^\n\r]+)", cleaned)
        slug = name_match.group(1).strip() if name_match else slugify(task_desc)
                
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
        mock_res = generate_mock_skill(task_desc, category, constraints, output_style, include_checklist, project_files)
        mock_res["error"] = resp.get("error", "Local Ollama generation failed, fell back to template.")
        return mock_res

def generate_skill_with_ollama(
    task_desc: str,
    category: str = "Software Development",
    constraints: str = "",
    output_style: str = "Balanced",
    include_checklist: bool = True,
    endpoint: str = "http://localhost:11434",
    model: str = "qwen2.5:7b",
    project_files: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Generates a skill via Ollama or raises RuntimeError if model inference fails."""
    res = generate_ai_skill(
        task_desc,
        category,
        constraints,
        output_style,
        include_checklist,
        endpoint,
        model,
        project_files=project_files
    )
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
    resp = client.generate(prompt=prompt, system=SYSTEM_PROMPT, model=model, temperature=0.2)
    if resp.get("success") and resp.get("response"):
        return clean_llm_markdown(resp["response"])
    return current_content
