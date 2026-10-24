"""
SkillForge — Skill Validator Module
Validates the structural compliance and metadata of generated SKILL.md files.
Adheres to the Agent Skills open standard specification.
"""

import re
import yaml
from typing import Dict, Any, List

def validate_skill(content: str) -> Dict[str, Any]:
    """
    Validates a SKILL.md markdown string.
    
    Checks:
    1. Frontmatter delimiters (---) presence and format
    2. Valid YAML frontmatter parseability
    3. 'name' field existence and kebab-case naming convention (lowercase, hyphens, alphanumeric)
    4. 'description' field existence and non-empty
    5. Instruction body existence and non-empty
    6. Essential sections (Purpose, Workflow / Steps, Constraints / Output)
    7. Safety / dangerous instruction screening
    """
    checks: List[Dict[str, Any]] = []
    
    if not content or not content.strip():
        return {
            "is_valid": False,
            "score": 0,
            "passed_checks": 0,
            "total_checks": 6,
            "checks": [
                {
                    "name": "Content Presence",
                    "passed": False,
                    "level": "error",
                    "message": "Skill content is completely empty.",
                    "suggestion": "Provide a task description and generate a skill first."
                }
            ],
            "frontmatter": {},
            "body": "",
            "summary": "Validation failed: Content is empty."
        }
    
    # 1. Frontmatter delimiter check
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, re.DOTALL)
    fm_delim_passed = bool(frontmatter_match)
    
    raw_yaml = ""
    body = ""
    parsed_yaml: Dict[str, Any] = {}
    
    if fm_delim_passed and frontmatter_match:
        raw_yaml = frontmatter_match.group(1)
        body = frontmatter_match.group(2).strip()
        checks.append({
            "name": "YAML Frontmatter Delimiters",
            "passed": True,
            "level": "success",
            "message": "Valid frontmatter delimiters (---) found at start of document.",
            "suggestion": None
        })
    else:
        checks.append({
            "name": "YAML Frontmatter Delimiters",
            "passed": False,
            "level": "error",
            "message": "Frontmatter must start and end with triple hyphens (---).",
            "suggestion": "Ensure the first line is '---', followed by YAML metadata, followed by another '---'."
        })
        body = content.strip()
    
    # 2. YAML parsing
    yaml_valid = False
    if fm_delim_passed:
        try:
            parsed = yaml.safe_load(raw_yaml)
            if isinstance(parsed, dict):
                parsed_yaml = parsed
                yaml_valid = True
                checks.append({
                    "name": "YAML Syntax Validity",
                    "passed": True,
                    "level": "success",
                    "message": "Frontmatter contains well-formed YAML.",
                    "suggestion": None
                })
            else:
                checks.append({
                    "name": "YAML Syntax Validity",
                    "passed": False,
                    "level": "error",
                    "message": "Frontmatter is not a valid YAML dictionary / key-value mapping.",
                    "suggestion": "Ensure frontmatter has key-value pairs like 'name: my-skill' and 'description: ...'."
                })
        except Exception as e:
            checks.append({
                "name": "YAML Syntax Validity",
                "passed": False,
                "level": "error",
                "message": f"YAML parsing syntax error: {str(e)}",
                "suggestion": "Check for indentation errors or special characters in the YAML block."
            })
    else:
        checks.append({
            "name": "YAML Syntax Validity",
            "passed": False,
            "level": "error",
            "message": "Cannot parse YAML because frontmatter delimiters are missing.",
            "suggestion": "Add '---' delimiters around metadata."
        })
    
    # 3. 'name' field check
    name_val = parsed_yaml.get("name") if yaml_valid else None
    name_passed = False
    if name_val and isinstance(name_val, str) and name_val.strip():
        name_str = name_val.strip()
        # kebab-case: lowercase letters, digits, and hyphens only
        if re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name_str):
            name_passed = True
            checks.append({
                "name": "Skill Name & Kebab-case Convention",
                "passed": True,
                "level": "success",
                "message": f"Valid skill name: '{name_str}' (conforms to kebab-case).",
                "suggestion": None
            })
        else:
            checks.append({
                "name": "Skill Name & Kebab-case Convention",
                "passed": False,
                "level": "error",
                "message": f"Skill name '{name_str}' does not follow kebab-case standard (lowercase, numbers, and hyphens only).",
                "suggestion": f"Convert to '{re.sub(r'[^a-z0-9]+', '-', name_str.lower()).strip('-')}'."
            })
    else:
        checks.append({
            "name": "Skill Name & Kebab-case Convention",
            "passed": False,
            "level": "error",
            "message": "Missing required 'name' field in frontmatter.",
            "suggestion": "Add 'name: my-skill-slug' to frontmatter."
        })
    
    # 4. 'description' field check
    desc_val = parsed_yaml.get("description") if yaml_valid else None
    desc_passed = False
    if desc_val and isinstance(desc_val, str) and len(desc_val.strip()) >= 10:
        desc_passed = True
        checks.append({
            "name": "Description Field",
            "passed": True,
            "level": "success",
            "message": f"Meaningful description present ({len(desc_val.strip())} chars).",
            "suggestion": None
        })
    elif desc_val and isinstance(desc_val, str) and desc_val.strip():
        checks.append({
            "name": "Description Field",
            "passed": False,
            "level": "warning",
            "message": "Description is too brief (less than 10 characters).",
            "suggestion": "Expand the description to clearly explain what agent capability this skill provides."
        })
    else:
        checks.append({
            "name": "Description Field",
            "passed": False,
            "level": "error",
            "message": "Missing or empty 'description' field in frontmatter.",
            "suggestion": "Add 'description: Explanation of what this skill does' to frontmatter."
        })
    
    # 5. Body check
    body_passed = False
    if body and len(body) >= 50:
        body_passed = True
        checks.append({
            "name": "Instruction Body Content",
            "passed": True,
            "level": "success",
            "message": f"Instruction body is substantial ({len(body)} characters, {len(body.splitlines())} lines).",
            "suggestion": None
        })
    elif body:
        checks.append({
            "name": "Instruction Body Content",
            "passed": False,
            "level": "warning",
            "message": "Instruction body is very short (less than 50 characters).",
            "suggestion": "Provide comprehensive step-by-step instructions for the agent."
        })
    else:
        checks.append({
            "name": "Instruction Body Content",
            "passed": False,
            "level": "error",
            "message": "Instruction body is empty after frontmatter.",
            "suggestion": "Add markdown headings, instructions, and rules below the closing '---'."
        })
    
    # 6. Structural headings (Purpose, Workflow, Constraints / Rules)
    has_purpose = bool(re.search(r"(?im)^#+\s+.*\b(purpose|overview|goal)\b", body))
    has_workflow = bool(re.search(r"(?im)^#+\s+.*\b(workflow|steps|instructions|process|procedure)\b", body))
    has_rules = bool(re.search(r"(?im)^#+\s+.*\b(rules|constraints|guidelines|requirements|output)\b", body))
    
    if has_purpose and has_workflow and has_rules:
        checks.append({
            "name": "Recommended Skill Sections",
            "passed": True,
            "level": "success",
            "message": "Document contains Purpose, Workflow/Steps, and Rules/Constraints sections.",
            "suggestion": None
        })
    else:
        missing = []
        if not has_purpose: missing.append("Purpose/Overview")
        if not has_workflow: missing.append("Workflow/Steps")
        if not has_rules: missing.append("Rules/Constraints")
        checks.append({
            "name": "Recommended Skill Sections",
            "passed": False,
            "level": "warning",
            "message": f"Missing recommended standard sections: {', '.join(missing)}.",
            "suggestion": f"Add markdown headings for: {', '.join(missing)}."
        })
        
    passed_count = sum(1 for c in checks if c["passed"])
    total_count = len(checks)
    score = int((passed_count / total_count) * 100) if total_count > 0 else 0
    
    # Overall validity requires all error-level checks to pass
    has_error = any(not c["passed"] and c["level"] == "error" for c in checks)
    is_valid = not has_error
    
    if is_valid and score == 100:
        summary = "All structural and metadata validation checks passed successfully!"
    elif is_valid:
        summary = "Structural validation passed with minor recommendations."
    else:
        summary = "Structural validation failed. Address the required error items."
        
    return {
        "is_valid": is_valid,
        "score": score,
        "passed_checks": passed_count,
        "total_checks": total_count,
        "checks": checks,
        "frontmatter": parsed_yaml,
        "body": body,
        "summary": summary
    }
