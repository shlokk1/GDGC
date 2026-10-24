"""
SkillForge — Behavioral Test Runner Module
Evaluates skill behavior against standard execution test cases.
Provides deterministic mock evaluations for Phase 1 and hooks for model-based execution in Phase 2.
"""

from typing import Dict, Any, List

def run_skill_tests(skill_content: str, task_desc: str = "") -> Dict[str, Any]:
    """
    Executes behavioral test scenarios against the given skill instructions.
    In Phase 1, runs deterministic rule-based evaluation checks that simulate behavioral tests.
    """
    if not skill_content or not skill_content.strip():
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "review_tests": 0,
            "pass_rate": 0,
            "tests": [],
            "is_mock": True,
            "summary": "No skill content provided to evaluate."
        }

    lower_content = skill_content.lower()
    
    # Test 1: Instruction Clarity & Actionability
    clarity_passed = (
        "## operational workflow" in lower_content or "## workflow" in lower_content or "### step" in lower_content
    ) and len(skill_content.splitlines()) >= 20
    
    test_1 = {
        "id": "TC-01",
        "name": "Instruction Clarity & Operational Structure",
        "category": "Behavioral Flow",
        "status": "PASSED" if clarity_passed else "REQUIRES REVIEW",
        "score": 95 if clarity_passed else 65,
        "scenario": "Simulate agent ingest of prompt with multi-step goal requiring clear phased execution.",
        "expected": "Instructions clearly segment actions into discrete phases (Plan, Execute, Review).",
        "observed": (
            "Well-structured workflow with numbered phases and deterministic step progression."
            if clarity_passed else
            "Workflow lacks distinct operational phases or contains ambiguous action instructions."
        ),
        "notes": "Illustrative behavioral evaluation based on structural workflow analysis."
    }

    # Test 2: Constraint & Safety Boundaries Handling
    has_constraints = "## strict rules" in lower_content or "rules & constraints" in lower_content or "safety" in lower_content
    has_failsafe = "fail-safe" in lower_content or "halt" in lower_content or "never" in lower_content or "boundary" in lower_content
    constraint_passed = has_constraints and has_failsafe
    
    test_2 = {
        "id": "TC-02",
        "name": "Constraint & Safety Boundary Enforcement",
        "category": "Safety Guardrails",
        "status": "PASSED" if constraint_passed else "REQUIRES REVIEW",
        "score": 100 if constraint_passed else 70,
        "scenario": "Trigger an ambiguous or borderline edge-case request to test boundary obedience.",
        "expected": "Agent halts, warns the user, and adheres to strict execution restrictions.",
        "observed": (
            "Guardrails and fail-safe triggers present. Agent correctly restricts unauthorized actions."
            if constraint_passed else
            "Safety boundaries or fail-safe error instructions are underspecified."
        ),
        "notes": "Simulated safety check against edge-case inputs."
    }

    # Test 3: Output Specification & Deliverable Consistency
    has_output_spec = "## expected output format" in lower_content or "output format" in lower_content
    has_checklist = "checklist" in lower_content or "- [ ]" in lower_content or "- [x]" in lower_content
    output_passed = has_output_spec
    
    test_3 = {
        "id": "TC-03",
        "name": "Output Specification & Verification Criteria",
        "category": "Deliverables & Output",
        "status": "PASSED" if output_passed else "REQUIRES REVIEW",
        "score": 98 if (output_passed and has_checklist) else (85 if output_passed else 60),
        "scenario": "Verify that agent returns structured deliverables conforming to expected format specifications.",
        "expected": "Standardized sections for Summary, Findings/Artifacts, and Verification Status.",
        "observed": (
            "Output formatting requirements and verification criteria are clearly specified."
            if output_passed else
            "Expected output format is not clearly defined in the skill instructions."
        ),
        "notes": "Evaluates consistency of deliverable formatting."
    }

    tests = [test_1, test_2, test_3]
    passed_count = sum(1 for t in tests if t["status"] == "PASSED")
    review_count = sum(1 for t in tests if t["status"] == "REQUIRES REVIEW")
    failed_count = sum(1 for t in tests if t["status"] == "FAILED")
    total_count = len(tests)
    pass_rate = int((passed_count / total_count) * 100) if total_count > 0 else 0

    if pass_rate == 100:
        summary = "All 3 sample test scenarios passed with high confidence."
    elif pass_rate >= 66:
        summary = f"{passed_count} of {total_count} tests passed. Review suggested improvements."
    else:
        summary = "Multiple test cases require review. Improve the skill before deployment."

    return {
        "total_tests": total_count,
        "passed_tests": passed_count,
        "failed_tests": failed_count,
        "review_tests": review_count,
        "pass_rate": pass_rate,
        "tests": tests,
        "is_mock": True,
        "summary": summary
    }

def improve_skill_content(current_content: str, failed_tests: List[Dict[str, Any]]) -> str:
    """
    Deterministic self-improvement: enhances the skill content by addressing
    any missing workflow, safety constraints, or output checklist requirements.
    """
    improved = current_content
    
    # Ensure fail-safe rules
    if "fail-safe" not in improved.lower():
        improved += "\n\n## Automated Safety Improvements\n- **Strict Sandboxing**: Never execute destructive file operations.\n- **Fail-Safe Mechanism**: Immediately halt execution and report error if input violates schema.\n"
        
    # Ensure checklist
    if "- [ ]" not in improved:
        improved += "\n## Enhanced Verification Checklist\n- [ ] Input parameters thoroughly sanitized.\n- [ ] Edge cases handled gracefully without crashing.\n- [ ] Output conforms to schema and verbosity rules.\n"
        
    return improved
