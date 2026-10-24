"""
SkillForge — Prompts for Skill Generation, Improvement, and Behavioral Evaluation
"""

SYSTEM_PROMPT = """You are SkillForge, an expert AI agent architect.
Your job is to generate production-ready, standardized agent skill specifications.
Every skill must adhere to the Agent Skills open standard:
1. It must begin with YAML frontmatter bounded strictly by '---'.
2. Frontmatter must contain 'name' (lowercase kebab-case, only lowercase letters, numbers, and hyphens) and 'description' (clear summary of capability).
3. The body must contain clear markdown sections:
   # Overview / Purpose
   # Workflow & Step-by-Step Instructions
   # Rules & Constraints
   # Expected Output Format
   # Error Handling & Edge Cases
"""

def build_generation_prompt(task_desc: str, category: str, constraints: str, output_style: str, include_checklist: bool) -> str:
    checklist_instruction = "Include a detailed '## Quality & Verification Checklist' section at the end." if include_checklist else ""
    return f"""Create a comprehensive Agent Skill specification for the following request:

Task Description:
{task_desc}

Category:
{category}

User Rules & Constraints:
{constraints if constraints else "None specified."}

Output Style:
{output_style} (Keep instructions structured, actionable, and aligned with this verbosity style).

{checklist_instruction}

Generate ONLY the valid markdown content starting with '---' YAML frontmatter.
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
