# SkillForge — Detailed Implementation Plan

The goal is to build a working application in six hours that can generate an AI agent skill, validate it, test it, improve it, and export it using a locally running AI model.

The most important principle is to build the complete basic workflow first. Don't start with advanced agents or complex architectures.

## 1. Understand the final application

A user opens the website and enters:

> Create an AI skill that reviews Python code, finds bugs and security issues, and suggests fixes without modifying files.

SkillForge then:

1. Sends the task to a local AI model.
2. Generates a standard-compatible `SKILL.md` file.
3. Checks the file structure and metadata.
4. Tests the skill against three sample tasks.
5. Shows which tests passed and failed.
6. Uses the failed results to improve the instructions.
7. Lets the user download the final skill as a ZIP file.

User Input

Task description and constraints

Skill Generator

Python + Ollama + local LLM

Validator

Metadata, YAML, naming, and file checks

Test Runner

Three test cases and evaluation results

Improve & Export

Revise instructions and download ZIP

## 2. Technology setup

Use a small, straightforward stack so you can finish within the hackathon.

| Component | Technology | Purpose |
| --- | --- | --- |
| Frontend | Streamlit | Input form, results, skill preview |
| Backend | Python | Connect all components |
| Local AI runtime | Ollama | Run the model on your computer |
| AI model | Qwen2.5 3B Instruct or another compatible model | Generate and revise skills |
| Metadata parsing | PyYAML | Read and validate YAML |
| Testing | pytest and custom evaluation code | Verify logic and sample outputs |
| Export | Python `zipfile` | Package the skill |
| Repository | GitHub | Publish the source code |

A local model avoids requiring a paid cloud inference API. However, actual inference speed depends on your computer's memory and hardware, so download and test the model before the hackathon timer starts if possible.

## 3. Hour 1 — Set up the project and local model

### Step 1: Install the requirements

Install Python 3.11 or newer, Git, and Ollama.

- Ollama: [ollama.com/download](<https://ollama.com/download?utm_source=chatgpt.com>)
- Python: [python.org/downloads](<https://www.python.org/downloads/?utm_source=chatgpt.com>)
- Git: [git-scm.com](<https://git-scm.com/?utm_source=chatgpt.com>)

Download a model:

bash
```
ollama pull qwen2.5:3b
```

Check that the model works:

bash
```
ollama run qwen2.5:3b
```

Enter a test prompt, then exit the model session.

### Step 2: Create the project

bash
```
mkdir skillforge
cd skillforge

python -m venv .venv
```

Activate the environment.

Windows:

bash
```
.venv\Scripts\activate
```

macOS/Linux:

bash
```
source .venv/bin/activate
```

Install dependencies:

bash
```
pip install streamlit requests pyyaml pytest
```

### Step 3: Create the folder structure

text
```
skillforge/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── generator/
│   ├── __init__.py
│   ├── ollama_client.py
│   └── prompts.py
├── validator/
│   ├── __init__.py
│   └── skill_validator.py
├── evaluator/
│   ├── __init__.py
│   └── test_runner.py
├── exporter/
│   ├── __init__.py
│   └── zip_exporter.py
└── tests/
    └── test_validator.py
```

Each module has one responsibility. This makes it easier for team members to work independently.

### Step 4: Connect Python to Ollama

Create `generator/ollama_client.py`:

python
```
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"

def generate_text(system_prompt, user_prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()["message"]["content"]
```

What this code does: It sends instructions to your local model and returns its response as a Python string. All later features will use this function.

Test this connection before moving on. If Ollama is not running or the model is missing, show a helpful error in the interface instead of crashing.

## 4. Hour 2 — Build the skill generator

This is the main AI feature.

### Step 1: Design the generation prompt

Create `generator/prompts.py`:

python
```
SYSTEM_PROMPT = """
You are SkillForge, an expert at creating
portable AI agent skills.

Generate a skill that follows the Agent Skills
open standard.

Return only the contents of SKILL.md.

Requirements:
- Include YAML frontmatter.
- Include a valid name and description.
- Give clear, step-by-step instructions.
- Include relevant constraints and expected behavior.
- Avoid vague or contradictory instructions.
- Never instruct the agent to reveal secrets.
- Do not include explanatory text outside the skill.
"""

def build_skill_prompt(task, constraints):
    return f"""
Create an AI agent skill for this task:

{task}

User constraints:
{constraints}

Include:
- Skill name and description
- Clear workflow
- Expected output
- Important constraints
- Instructions for handling uncertainty
"""
```

The prompt tells the model what it needs to produce and how to format it.

### Step 2: Generate a skill

Create a function in `generator/` or a separate `skill_generator.py`:

python
```
from generator.ollama_client import generate_text
from generator.prompts import (
    SYSTEM_PROMPT,
    build_skill_prompt
)

def generate_skill(task, constraints=""):
    prompt = build_skill_prompt(task, constraints)

    return generate_text(
        SYSTEM_PROMPT,
        prompt
    )
```

### Step 3: Test the generator

Try the input:

text
```
Create a skill that reviews Python code for bugs,
security problems, and missing tests.

It must explain each issue and suggest fixes.
It must never modify files automatically.
```

Expected output: a Markdown file with YAML frontmatter and sections describing the workflow and constraints.

Important: The model may return malformed YAML or extra text. Don't assume the output is valid just because generation succeeded. The next step handles that.

## 5. Hour 3 — Implement the skill validator

This is where your project becomes more than a basic LLM wrapper.

### What should the validator check?

- Is the YAML frontmatter present and valid?
- Are `name` and `description` provided?
- Does the skill name follow the standard's naming rules?
- Is there meaningful instruction content?
- Are referenced files present if the skill uses them?

For the hackathon, start with `SKILL.md` only. Add supporting files later if time permits.

Create `validator/skill_validator.py`:

python
```
import re
import yaml

def validate_skill(content):
    errors = []

    if not content.startswith("---"):
        return {
            "valid": False,
            "errors": ["Missing YAML frontmatter"]
        }

    parts = content.split("---", 2)

    if len(parts) != 3:
        return {
            "valid": False,
            "errors": ["Malformed YAML frontmatter"]
        }

    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {
            "valid": False,
            "errors": ["Invalid YAML syntax"]
        }

    if not isinstance(metadata, dict):
        return {
            "valid": False,
            "errors": ["Frontmatter must be a YAML mapping"]
        }

    name = metadata.get("name")
    description = metadata.get("description")

    if not isinstance(name, str) or not name:
        errors.append("Missing skill name")

    elif (
        len(name) > 64
        or not re.fullmatch(
            r"[a-z0-9]+(-[a-z0-9]+)*",
            name
        )
    ):
        errors.append("Invalid skill name format")

    if not isinstance(description, str) or not description.strip():
        errors.append("Missing skill description")

    if not parts[2].strip():
        errors.append("Skill instructions are empty")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "metadata": metadata
    }
```

This is a basic validator, not a complete implementation of the Agent Skills specification. You should compare it with the current specification and official validator before publishing.

### How the validator helps

For example, if the model generates a skill without a description, the validator reports:

text
```
Validation failed

- Missing skill description
```

Your UI can then show the problem and offer the user an option to regenerate the skill.

### Step 4: Test the validator

Create `tests/test_validator.py`:

python
```
from validator.skill_validator import validate_skill

def test_valid_skill():
    content = """---
name: python-review
description: Review Python code for bugs.
---

# Workflow

1. Inspect the code.
2. Explain potential bugs.
"""

    result = validate_skill(content)

    assert result["valid"] is True

def test_missing_description():
    content = """---
name: python-review
---

# Workflow

Review the code.
"""

    result = validate_skill(content)

    assert result["valid"] is False
    assert "Missing skill description" in result["errors"]
```

Run:

bash
```
pytest -q
```

These are ordinary software tests that verify your validator works correctly. They are different from the behavioral tests that will evaluate a generated skill.

## 6. Hour 4 — Build the behavioral testing system

This is the most important feature after generation and validation.

The difference: structural validation checks whether the skill file is formatted correctly; behavioral testing checks whether the instructions help the AI perform the intended task.

### Step 1: Generate three test scenarios

For a Python code-review skill, use these scenarios:

| Test | Input | Expected behavior |
| --- | --- | --- |
| Bug detection | Code with a division-by-zero bug | Identify and explain the bug |
| Security review | Code containing unsafe SQL construction | Identify the potential SQL injection |
| Safe behavior | Code with no obvious issues | Avoid inventing problems and explain the result cautiously |

For your six-hour MVP, you can write these three test cases manually rather than asking the model to generate them. This makes results easier to compare and reduces the number of model calls.

### Step 2: Run the tests

For each scenario:

1. Send the generated skill instructions and test input to the local model.
2. Ask the model to perform the task while following the skill.
3. Capture its response.
4. Check whether the response meets predefined criteria.
5. Record the result and explanation.

For example, the SQL injection test can pass if the response identifies the unsafe query construction and recommends parameterized queries.

Avoid simply asking a second LLM, “Was this answer good?” Use specific criteria wherever possible.

### Step 3: Implement a basic evaluator

Create `evaluator/test_runner.py`:

python
```
from generator.ollama_client import generate_text

def run_test(skill, test_case):
    prompt = f"""
Follow these skill instructions:

{skill}

Perform the following task:
{test_case['input']}

Return your findings and recommendations.
"""

    output = generate_text(
        "Follow the supplied skill instructions carefully.",
        prompt
    )

    expected_terms = test_case["expected_terms"].lower()
    output_lower = output.lower()

    passed = all(
        term in output_lower
        for term in test_case["expected_terms_list"]
    )

    return {
        "name": test_case["name"],
        "passed": passed,
        "output": output,
        "expected_terms": expected_terms
    }
```

Use test cases such as:

python
```
TEST_CASES = [
    {
        "name": "Bug detection",
        "input": (
            "Review this code: "
            "x = 10 / 0"
        ),
        "expected_terms": "division by zero",
        "expected_terms_list": [
            "division by zero"
        ]
    },
    {
        "name": "Security review",
        "input": (
            "Review this query: "
            "query = 'SELECT * FROM users WHERE id=' + user_input"
        ),
        "expected_terms": "sql injection",
        "expected_terms_list": [
            "sql injection"
        ]
    },
    {
        "name": "Actionable fix",
        "input": (
            "Review this code: "
            "x = 10 / 0"
        ),
        "expected_terms": "division by zero",
        "expected_terms_list": [
            "division by zero"
        ]
    }
]
```

This is a starter example, not a robust evaluation framework. The first and third cases overlap intentionally to demonstrate the mechanics; make the final tests genuinely distinct, and account for valid alternative wording. A keyword-based test can incorrectly fail a good answer or pass a poor one.

### Step 4: Display a score

If two tests pass out of three, the pass rate is:

$$
\text{Pass rate}=\frac{2}{3}\times100=66.7\%
$$

Display the result alongside the actual outputs and explanations. Make it clear that this is a score on your selected tests, not a guarantee of overall skill quality.

## 7. Hour 5 — Implement self-improvement and ZIP export

### A. Self-improvement

When a test fails, send the existing skill and test report back to the local model.

The improvement prompt should ask the model to:

- Preserve the original goal and constraints.
- Identify why the current instructions may have failed.
- Make targeted changes.
- Return a complete revised `SKILL.md`.
- Avoid claiming the revised version works until it has been tested.

A simple function:

python
```
from generator.ollama_client import generate_text

def improve_skill(skill, failure_report):
    prompt = f"""
Revise this AI agent skill to address the
reported test failures.

CURRENT SKILL:
{skill}

TEST FAILURE REPORT:
{failure_report}

Preserve the original purpose and constraints.
Make only relevant improvements.
Return the complete revised SKILL.md.
"""

    return generate_text(
        "You improve AI agent skills based on test failures.",
        prompt
    )
```

After improvement, rerun both validation and behavioral tests. Never automatically declare the new version successful.

For the MVP, allow one improvement attempt and show a comparison of the original and revised results.

### B. ZIP export

Once a skill passes validation, let the user download it.

Create `exporter/zip_exporter.py`:

python
```
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

def create_skill_zip(skill_content, skill_name):
    buffer = BytesIO()

    with ZipFile(
        buffer,
        "w",
        compression=ZIP_DEFLATED
    ) as archive:
        archive.writestr(
            f"{skill_name}/SKILL.md",
            skill_content
        )

    buffer.seek(0)
    return buffer.getvalue()
```

This creates a downloadable ZIP in memory without writing temporary files to disk.

The exported skill should contain valid metadata and follow the Agent Skills specification. A ZIP download alone does not guarantee compatibility with every agent.

## 8. Hour 6 — Build the UI and connect everything

Use Streamlit to keep the frontend simple.

Create `app.py`:

python
```
import streamlit as st

from generator.skill_generator import generate_skill
from validator.skill_validator import validate_skill
from evaluator.test_runner import run_test, TEST_CASES
from exporter.zip_exporter import create_skill_zip

st.set_page_config(
    page_title="SkillForge",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ SkillForge")
st.caption(
    "Generate, validate, test, and improve AI agent skills locally."
)

task = st.text_area(
    "Describe the skill you want",
    placeholder=(
        "Create a skill that reviews Python code "
        "for bugs and security issues."
    )
)

constraints = st.text_area(
    "Constraints",
    placeholder="Never modify files automatically."
)

if st.button("Generate Skill", type="primary"):
    if not task.strip():
        st.warning("Please describe the skill first.")
    else:
        try:
            with st.spinner("Generating skill locally..."):
                skill = generate_skill(task, constraints)

            st.session_state["skill"] = skill

        except Exception as exc:
            st.error(
                "Could not generate the skill. "
                "Check that Ollama is running and "
                "the selected model is installed."
            )

if "skill" in st.session_state:
    skill = st.session_state["skill"]

    st.subheader("Generated Skill")
    st.markdown(skill)

    validation = validate_skill(skill)

    st.subheader("Validation")

    if validation["valid"]:
        st.success("Structural validation passed.")
    else:
        st.error("Validation failed.")

        for error in validation["errors"]:
            st.write(f"- {error}")

    if st.button(
        "Run Tests",
        disabled=not validation["valid"]
    ):
        results = []

        with st.spinner("Testing the generated skill..."):
            for case in TEST_CASES:
                results.append(run_test(skill, case))

        passed = sum(
            result["passed"] for result in results
        )

        st.metric(
            "Test pass rate",
            f"{passed}/{len(results)}"
        )

        for result in results:
            with st.expander(result["name"]):
                st.write(
                    "Passed" if result["passed"]
                    else "Failed"
                )
                st.write(result["output"])

        st.session_state["test_results"] = results

    if validation["valid"]:
        metadata = validation["metadata"]
        name = metadata["name"]

        zip_data = create_skill_zip(skill, name)

        st.download_button(
            "Download Skill ZIP",
            data=zip_data,
            file_name=f"{name}.zip",
            mime="application/zip"
        )
```

This is an integration skeleton. Before running it, you will need to implement `generate_skill` in `generator/skill_generator.py` and define `TEST_CASES` in the evaluator module using the earlier examples. Add the improvement button and comparison after the main flow works.

### Run the application

bash
```
streamlit run app.py
```

Your browser should open the SkillForge interface.

## 9. Test the complete workflow

Before the hackathon ends, verify these scenarios:

- [ ]The local model generates a skill from a plain-English description.
- [ ]Valid skills pass the structural validator.
- [ ]Invalid YAML or missing metadata is rejected.
- [ ]Three sample tests produce visible results.
- [ ]Failed tests can trigger one revision attempt.
- [ ]The revised skill is validated and tested again.
- [ ]The ZIP contains a correctly named `SKILL.md`.
- [ ]The application shows useful errors if Ollama is unavailable.
- [ ]The README explains installation, usage, limitations, and model requirements.
- [ ]The repository is public and includes an appropriate open-source license.

## 10. How to divide the work

If you have three team members, work in parallel:

- Member 1 — AI: Ollama integration, generation prompts, and improvement loop.
- Member 2 — Frontend: Streamlit interface, skill preview, results, and download.
- Member 3 — Validation: Specification checks, test cases, evaluator, and application tests.

Agree on the function interfaces early so that all three components can be integrated without waiting until the final hour.

## 11. What to do first

Your immediate next steps should be:

1. Install Ollama and verify that the model runs on your hardware.
2. Create the repository and folder structure.
3. Implement and test `generate_text()`.
4. Generate one valid `SKILL.md`.
5. Implement the validator and connect it to Streamlit.
6. Add testing, improvement, and export in that order.

Keep the scope under control: if time becomes tight, prioritize generation, structural validation, three tests, and ZIP export. Self-improvement is valuable, but a reliable end-to-end demo is more important than unfinished advanced features.