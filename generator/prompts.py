"""
SkillForge — Prompts for Skill Generation, Improvement, and Behavioral Evaluation
Includes support for grounding skill synthesis in user-imported project files.
"""

from typing import Dict, Any, Optional

MAX_PROJECT_CONTEXT_CHARS = 60000

SYSTEM_PROMPT = """You are SkillForge, an expert AI agent architect.
Your job is to generate production-ready, standardized agent skill specifications.
Every skill must adhere strictly to the Agent Skills open standard:
1. It must begin immediately with YAML frontmatter bounded by '---'.
2. Frontmatter must contain 'name' (lowercase kebab-case, only lowercase letters, numbers, and hyphens) and 'description' (clear summary of capability).
3. The body must contain clear markdown sections:
   # <Title>
   ## Purpose
   ## When to Use This Skill
   ## Key Capabilities
   ## Workflow (numbered steps with actionable substeps)
   ## Rules & Constraints
   ## Expected Output Format
   ## Quality & Verification Checklist
4. Ground all instructions, constraints, and recommendations directly in any supplied project reference files.
5. The closing '---' must appear on its own line immediately after the YAML metadata and before the first Markdown heading.
6. Do NOT output conversational filler (e.g. "Here is your skill:"). Output ONLY the valid markdown starting with '---'.
"""

def build_generation_prompt(
    task_desc: str,
    category: str,
    constraints: str,
    output_style: str,
    include_checklist: bool,
    project_files: Optional[Dict[str, str]] = None
) -> str:
    checklist_instruction = "Include a detailed '## Quality & Verification Checklist' section with checkboxes at the end." if include_checklist else ""
    
    files_context = ""
    if project_files:
        files_blocks = []
        remaining_chars = MAX_PROJECT_CONTEXT_CHARS
        for fname, fcontent in project_files.items():
            if remaining_chars <= 0:
                break
            file_header = f"--- File: {fname} ---\n"
            content_limit = min(4000, max(0, remaining_chars - len(file_header)))
            if content_limit == 0:
                break
            file_content = fcontent[:content_limit]
            files_blocks.append(f"{file_header}{file_content}\n")
            remaining_chars -= len(file_header) + len(file_content) + 1

        included_files = len(files_blocks)
        omitted_files = len(project_files) - included_files
        context_note = (
            f"\nNote: Context is limited to the first {included_files} files that fit; "
            f"{omitted_files} additional file(s) were not included.\n"
            if omitted_files else ""
        )
        
        files_context = f"""
=== IMPORTED PROJECT REFERENCE FILES ===
The user has provided the following project files for reference. Tailor the skill specifically to these files, their schemas, parameters, and architecture:

{context_note}{''.join(files_blocks)}
"""

    return f"""Create a comprehensive Agent Skill specification for the following request:

Task Description:
{task_desc}

If the request describes a reported issue, preserve its symptoms, expected versus observed behavior, and reproduction steps in the skill. Do not claim an unverified cause or fix.

Category:
{category}

User Rules & Constraints:
{constraints if constraints else "None specified. Enforce sandboxed safety and deterministic actions."}

Output Style:
{output_style} (Keep instructions structured, actionable, and aligned with this verbosity style).
{files_context}
{checklist_instruction}

Return ONLY a complete SKILL.md document. Start with '---', put 'name' and a one-line quoted
'description' in the YAML frontmatter, and close the frontmatter with a separate '---' line
before the first Markdown heading. Then include all required Markdown sections.
"""

def build_improvement_prompt(current_skill: str, failure_report: str) -> str:
    return f"""The following Agent Skill was tested and encountered behavioral or validation failures:

=== CURRENT SKILL.md ===
{current_skill}

=== FAILURE REPORT ===
{failure_report}

Revise and improve the SKILL.md file so that it resolves all the identified failures.
Preserve the kebab-case 'name' in the frontmatter. Ensure all rules and steps prevent these issues.
Return ONLY the updated SKILL.md markdown starting with '---'.
"""
