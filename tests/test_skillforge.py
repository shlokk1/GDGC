"""
Unit Tests for SkillForge Core Modules
Tests generator, validator, evaluator, and zip exporter.
"""

import os
import sys
import zipfile
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generator.skill_generator import generate_mock_skill, slugify
from validator.skill_validator import validate_skill
from evaluator.test_runner import run_skill_tests, improve_skill_content
from exporter.zip_exporter import create_skill_zip, sanitize_folder_name

def test_slugify():
    assert slugify("Review Python code for bugs") == "review-python-code-for-bugs"
    assert slugify("Custom   Task!!! With Symbols???") == "custom-task-with-symbols"

def test_generate_mock_skill():
    res = generate_mock_skill(
        task_desc="Review Python code for bugs and security vulnerabilities",
        category="Software Development",
        constraints="Never modify files in place",
        output_style="Balanced",
        include_checklist=True
    )
    assert res["name"] == "review-python-code-for-bugs"
    assert "---" in res["content"]
    assert "name: review-python-code-for-bugs" in res["content"]
    assert "## Quality & Verification Checklist" in res["content"]

def test_validate_skill_success():
    res = generate_mock_skill(
        task_desc="Audit Kubernetes manifests for security issues",
        category="Software Development"
    )
    val = validate_skill(res["content"])
    assert val["is_valid"] is True
    assert val["score"] >= 80
    assert val["passed_checks"] >= 5

def test_validate_skill_errors():
    # Empty content
    empty_val = validate_skill("")
    assert empty_val["is_valid"] is False

    # Bad frontmatter
    bad_fm = "No frontmatter at all here\nJust markdown."
    val_bad = validate_skill(bad_fm)
    assert val_bad["is_valid"] is False

def test_behavioral_evaluator():
    res = generate_mock_skill(
        task_desc="Review Python code for security issues",
        category="Software Development"
    )
    eval_res = run_skill_tests(res["content"])
    assert eval_res["total_tests"] == 3
    assert eval_res["passed_tests"] >= 2

def test_zip_exporter():
    content = "---\nname: test-skill\ndescription: Test description\n---\n# Test\n"
    zip_bytes = create_skill_zip("test-skill", content)
    assert len(zip_bytes) > 0

    # Read back zip in memory
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    file_list = zf.namelist()
    assert "test-skill/SKILL.md" in file_list
    assert "test-skill/MANIFEST.txt" in file_list
    extracted_skill = zf.read("test-skill/SKILL.md").decode("utf-8")
    assert extracted_skill == content
