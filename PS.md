SkillForge — Local-First AI Agent Skill Generator
1. Project Overview

SkillForge is an open-source AI developer tool that converts a user's task description into a reusable AI agent skill, validates its structure, tests its behavior, and improves it based on test failures.

Instead of merely generating a prompt or Markdown file, SkillForge aims to create reliable, portable agent skills through an automated Generate → Validate → Test → Improve → Export workflow.

Hackathon track: Best Open-Source AI Project.

2. Problem Statement

Creating effective AI agent skills requires writing structured instructions, following a standard format, handling edge cases, and testing whether the skill actually works.

Beginners often struggle to create reliable, reusable skills. AI-generated instructions may also contain invalid metadata, missing files, ambiguous rules, or unsafe instructions.

SkillForge automates skill creation and provides measurable validation and testing.

3. Core Features
A. AI Skill Generation
User describes a task, such as reviewing Python code or researching a topic.
User specifies constraints, expected behavior, and optional examples.
A locally running LLM generates a skill following the Agent Skills open standard.
The output includes a valid SKILL.md file with YAML frontmatter containing name and description.
Optional supporting scripts and reference files can be added if time permits.
B. Automatic Validation

Validate the generated skill using deterministic checks:

Required metadata and valid YAML.
Naming conventions and folder structure.
Required files and referenced paths.
Missing sections and malformed content.
Potentially unsafe instructions that require human review.
C. Automated Skill Testing
Generate three test scenarios based on the user's task.
Run the skill instructions against the test scenarios using the local LLM.
Evaluate outputs against predefined criteria, including task completion, required formatting, and adherence to user constraints.
Show passed and failed tests with explanations.
D. Self-Improvement
Identify failed tests.
Send the failure report and existing skill to the LLM.
Generate a revised version of the skill.
Rerun the tests and display before-and-after results.

Limit the revision loop to one or two attempts for the hackathon MVP.

E. Export
Display the generated skill in a readable Markdown preview.
Download the complete skill folder as a ZIP.
Allow users to publish it to GitHub manually; automated publishing is optional.
4. Technology Stack
Frontend: Streamlit.
Local model runtime: Ollama.
LLM: Qwen2.5 3B Instruct or another suitable small open-weight instruction model.
Backend: Python.
Validation: PyYAML and Python validation logic; use the official Agent Skills validator if practical.
Testing: pytest and a custom test runner.
Export: Python ZIP utilities.
Version control: Git and GitHub.

Model inference should happen locally without requiring a paid LLM API. Verify the chosen model's license and hardware requirements before development.

5. Application Workflow
The user opens the Streamlit application.
The user enters a task description and constraints.
The application sends the prompt to the local LLM through Ollama.
The LLM generates a skill and optional test scenarios.
The validator checks metadata, format, file structure, and basic safety indicators.
The test runner evaluates the skill against three test cases.
The application displays validation results, test scores, and failure explanations.
If tests fail, the user can request an improved version.
The application reruns validation and tests.
The user previews and downloads the final skill as a ZIP.
6. UI Design

Build a clean, modern developer dashboard with three main sections:

Create Skill

Task description text area.
Optional constraints and category.
Generate Skill button.

Validation & Testing

Validation checklist.
Test results with pass/fail indicators.
Explanations for failed checks.
Improve Skill button.
Before-and-after comparison.

Preview & Export

Generated folder structure.
Markdown preview of SKILL.md.
Download ZIP button.

Keep the interface simple and functional; avoid spending excessive time on animations or decorative elements.

7. Six-Hour Implementation Plan
Hour 1: Install Ollama and the model, initialize the repository, and create the Streamlit interface.
Hour 2: Implement local model integration and skill generation.
Hour 3: Implement metadata, YAML, and structural validation.
Hour 4: Implement three test scenarios and a basic evaluation runner.
Hour 5: Add the revision loop, results dashboard, and ZIP export.
Hour 6: Test the complete flow, fix bugs, write the README, add an open-source license, and prepare the demonstration.

Prioritize a working end-to-end MVP over advanced features.

8. Team Division

For a three-person team:

Person 1: Ollama integration, prompts, skill generation, and revision.
Person 2: Streamlit UI, skill preview, and ZIP export.
Person 3: Specification compliance, validation, test runner, and README.

Integrate components early rather than waiting until the end.

9. What Makes the Project Different?

SkillForge does not stop at generating AI instructions. It validates the resulting artifact, tests its behavior, identifies failures, and attempts to improve it.

Its differentiators are:

Local-first inference and privacy.
Standards-based portable skills.
Automated validation.
Behavioral testing with measurable results.
A self-improvement workflow.
10. Important Constraints
Use the Agent Skills open standard rather than inventing a proprietary skill format.
Do not claim a skill is reliable merely because it passes metadata validation.
Distinguish deterministic validation from LLM-based behavioral evaluation.
Never execute generated scripts automatically without appropriate isolation and explicit approval.
Do not commit API keys, secrets, or personal data.
Publish the project in a public GitHub repository with an appropriate open-source license.
11. Definition of Done

The MVP is complete when a user can describe a task, generate a skill using a local model, validate it, test it on three scenarios, view failures, attempt one improvement, and download the resulting skill.

The entire flow must work reliably on the team's available hardware.

Instructions for Implementation

First, inspect the available environment and determine whether Ollama and the chosen model are installed. Then build the smallest working end-to-end version.

Implement the application in modular files, keep the code easy to understand, and test each component. Do not introduce unnecessary frameworks or complex agent orchestration.

Prioritize a functioning demonstration within six hours. If time is limited, implement skill generation, deterministic validation, three basic tests, and ZIP export before adding self-improvement.