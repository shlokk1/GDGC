
# SkillForge — Problems & Implementation Plan

## 1. Project Overview

SkillForge is a local AI tool that creates, validates, tests, and improves AI agent skills.

## 2. Problems We Are Solving

| Problem | Solution |
|---|---|
| Users don't know how to write effective AI agent instructions. | Generate skills from plain-English descriptions. |
| AI-generated instructions may have incorrect formatting or missing fields. | Automatically validate skill structure and metadata. |
| A skill may look correct but perform poorly. | Test it using sample tasks and predefined criteria. |
| Users don't know how to fix failed skills. | Use the local LLM to revise instructions based on test failures. |
| Skills are difficult to reuse and share. | Export portable skills as downloadable ZIP files. |

## 3. How the Project Works

1. **User describes a task:** For example, create a Python code-review skill.
2. **AI generates the skill:** A local LLM creates the `SKILL.md` file.
3. **Validate the skill:** Check YAML, metadata, structure, and required files.
4. **Test the skill:** Run three sample tasks and evaluate the results.
5. **Improve the skill:** Revise instructions based on failed tests.
6. **Export the skill:** Preview and download the final skill as a ZIP.

## 4. Implementation Plan (6 Hours)

| Time | Task |
|---|---|
| Hour 1 | Set up the project, Ollama, local model, and Streamlit UI. |
| Hour 2 | Implement AI skill generation. |
| Hour 3 | Build the skill format and metadata validator. |
| Hour 4 | Implement three sample tests and display test results. |
| Hour 5 | Add automatic improvement and ZIP download. |
| Hour 6 | Integrate components, fix bugs, write the README, publish to GitHub, and prepare the demo. |

## 5. Technology Stack

- **Python:** Core application logic.
- **Streamlit:** Web interface.
- **Ollama:** Runs the AI model locally.
- **Qwen or another suitable open-weight model:** Generates and improves skills.
- **PyYAML:** Validates YAML metadata.
- **pytest / custom test runner:** Tests application logic and skill behavior.
- **GitHub:** Public source code and documentation.

## 6. MVP Features

Prioritize these features for the six-hour hackathon:

1. Generate a valid `SKILL.md`.
2. Automatically validate its structure.
3. Test the skill against three example tasks.
4. Display test results and allow one improvement attempt.
5. Download the final skill as a ZIP.

Safety checks and automated GitHub publishing are optional if time permits.

## 7. Main Technical Challenge

The biggest challenge is not generating a skill; it is reliably evaluating whether the skill behaves as intended.

We will address this using deterministic format checks and a small set of predefined behavioral tests. Model-based evaluations will be treated as estimates rather than guarantees.

## 8. Final Goal

Build a working end-to-end MVP that allows users to describe a task, generate an AI agent skill locally, validate its structure, test its behavior, improve it, and download the final result.

Focus on completing the core workflow before adding advanced features.
```