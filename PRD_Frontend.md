Product Requirements Document (PRD)
SkillForge — Frontend Implementation

Version: 1.0
Phase: Phase 1 — Frontend Development
Product Type: Local AI Skill Builder
Frontend Technology: Python + Streamlit
Target AI Model: Qwen2.5 7B Instruct via Ollama (integrated in a later phase)

1. Product Overview

SkillForge is a local-first application that helps users create, inspect, validate, test, and export reusable AI agent skills.

Users describe a task in plain English. The application provides a workspace to generate a SKILL.md file, review its content, check its structure, test its behavior, improve it, and download it as a ZIP package.

The frontend will be developed first, independently of the AI backend. During Phase 1, generation and testing may use mock data, but the architecture must allow these functions to be replaced with real backend services without redesigning the UI.

2. Problem Statement

Creating reliable AI agent skills requires users to write structured instructions, follow a consistent file format, test expected behavior, and fix errors manually.

This process can be difficult for users who do not understand skill-file conventions or prompt engineering.

SkillForge simplifies this workflow by providing a single interface for skill creation, editing, validation, testing, and export.

3. Product Goals
Provide a clean and intuitive interface for creating AI skills.
Allow users to describe tasks using natural language.
Display skill content in an editable Markdown editor.
Provide structural validation feedback.
Display test cases and their results in an organized dashboard.
Allow users to download skills as ZIP files containing SKILL.md.
Prepare the frontend for future integration with a local Ollama model.
Keep the application modular and easy to extend.
4. Target Users
Primary Users
Students participating in AI hackathons.
Developers building AI agents and reusable workflows.
AI enthusiasts experimenting with local language models.
Developers who want to create structured skill instructions without writing everything manually.
User Skill Level

The interface should be usable by beginners while providing enough information and control for experienced developers.

5. Scope of Phase 1
In Scope
Frontend layout and navigation.
Skill creation form.
Task description and constraint inputs.
Skill category selection.
Generation preference controls.
Template-based demo generation.
Editable SKILL.md content.
Rendered Markdown preview.
Basic structural validation.
Mock behavioral test results.
Export as a ZIP archive.
Session-based skill state.
Settings page with planned Ollama configuration.
User feedback, validation messages, and empty states.
Out of Scope
Real LLM inference.
Direct Ollama API integration.
Real behavioral evaluation of generated skills.
Automatic AI-powered skill improvement.
Persistent database storage.
User authentication and accounts.
Cloud deployment.
Team collaboration.
GitHub integration.
Advanced security analysis.

These features may be implemented in subsequent phases.

6. Technology Stack
Language: Python 3.10 or newer.
Frontend framework: Streamlit.
Styling: Custom CSS injected through Streamlit.
Session state: st.session_state.
Markdown rendering: Streamlit Markdown components.
Export: Python io and zipfile modules.
Configuration: Constants initially; environment variables when backend integration is added.
Version control: Git.
Dependencies

Create a requirements.txt file:

streamlit>=1.40.0


Use only the dependencies required for the frontend phase. Add AI, validation, and testing dependencies when those features are implemented.

7. Application Structure

The application must contain the following navigation sections:

Create Skill
My Skills
Testing Lab
Settings

The sidebar should display:

SkillForge logo or text branding.
Application subtitle.
Navigation menu.
Local model status.
Current development phase or integration status.

The main content area should update according to the selected navigation item.

8. UI Design Requirements
8.1 Visual Style

Use a modern developer-tool aesthetic.

Dark background.
Dark sidebar separated by a subtle border.
Blue or violet accent color.
Rounded cards and input containers.
Clear typography and readable spacing.
Consistent button styles.
Visible success, warning, and error states.
Monospaced styling for code and skill-file content where appropriate.

The design must prioritize usability over decorative effects.

8.2 Layout
Use Streamlit's wide layout.
Keep navigation visible in the sidebar.
Use responsive columns for forms and workspace panels.
Stack columns naturally on narrow screens when possible.
Keep primary actions easy to locate.
Avoid excessive scrolling and unnecessary nested containers.
8.3 Accessibility
Every input must have a meaningful label.
Statuses must include text, not color alone.
Maintain readable text contrast.
Buttons must have clear action labels.
Error messages must explain how users can recover.
9. Functional Requirements
9.1 Create Skill Page

This is the primary page.

It must include:

A. Hero Section

Display:

Product name or workspace title.
Short explanation of SkillForge.
Brief description of the creation and testing workflow.
B. Skill Creation Form

Fields:

Task Description
Multiline text area.
Required field.
Accepts a natural-language description of the desired skill.
Displays a placeholder example.
Skill Category
Dropdown selector.
Options:
Software Development
Research & Analysis
Writing & Documentation
Data Processing
Productivity
Other
Rules and Constraints
Optional multiline text area.
Used to specify restrictions and expected behavior.
Output Style
Dropdown selector.
Options:
Detailed
Balanced
Concise
Include Quality Checklist
Checkbox.
Controls whether the generated demo template includes a quality checklist.
Generate Skill
Primary action button.
Must validate that the task description is not empty.
Must show an error or warning when required input is missing.
In Phase 1, generate a deterministic sample skill from a template.
Must clearly indicate that generation is simulated and does not use an LLM.
C. Workspace Progress

Display the following workflow steps:

Task description provided.
Skill created.
Validation completed.
Tests reviewed.

Show an appropriate incomplete or completed state for each step.

Progress must be derived from application state, not hardcoded.

9.2 Skill Generation Behavior

For Phase 1, the application must create a sample skill without calling an AI API.

The generated file must contain:

YAML frontmatter.
A skill name.
A short description.
A purpose section.
A step-by-step workflow.
A category.
User-defined constraints.
Expected output.
A quality checklist when enabled.

The skill name should be converted to a safe lowercase slug.

Example:

Review Python code for bugs

becomes:

review-python-code-bugs

The generated Markdown must remain editable.

Generation must reset any previous validation and testing results because they may no longer apply to the new content.

9.3 Skill Editor and Preview

After a skill is generated, display a results section containing four tabs:

Skill Editor
Validation
Testing Lab
Export
Skill Editor

Requirements:

Display the full SKILL.md content in an editable text area.
Allow users to edit the Markdown.
Provide a Save Edits action.
Store saved changes in session state.
Invalidate previous validation and test results when content changes.
Provide an expandable rendered Markdown preview.

The editor must preserve the user's content rather than regenerate it automatically.

9.4 Validation Tab

Provide a structural validation interface.

The Phase 1 validator should check:

YAML frontmatter delimiters are present.
A valid lowercase, hyphen-separated name field exists.
A non-empty description field exists.
The instruction body is not empty.

Display:

Overall validation status.
Individual checks.
Passed checks.
Failed checks.
Actionable error messages.

The validation status must be based on the actual results of the local validation function.

Do not describe this basic validator as a complete Agent Skills specification validator.

9.5 Testing Lab Tab

Display a basic test dashboard using mock test results.

Example test cases:

Instruction clarity.
Output expectations.
Constraint handling.

Each test result must include:

Test name.
Status.
Explanation or output.

Display summary metrics:

Total test cases.
Number passed.
Number requiring review.

Clearly label these as illustrative demo results.

The application must not imply that an LLM executed the generated skill or that the skill passed real behavioral tests.

9.6 Export Tab

Allow users to download the current skill as a ZIP archive.

Requirements:

Provide an editable folder-name field.
Sanitize the folder name into a safe slug.
Include the current edited content as SKILL.md.
Create the ZIP in memory using io.BytesIO and zipfile.
Provide a Streamlit download button.
Use the ZIP filename derived from the sanitized folder name.

Expected ZIP structure:

my-skill.zip
└── my-skill/
    └── SKILL.md


Export must use the latest saved skill content.

Display a warning if the most recent validation failed. Users may still download the file, but the interface must make the failed validation visible.

9.7 My Skills Page

Display the skill created during the current session.

Requirements:

Show the skill name.
Indicate that it belongs to the current session.
Provide an action to return to the current skill workspace.
Display an empty state if no skill has been created.

Persistent storage is not required in Phase 1.

Do not claim that skills are permanently saved.

9.8 Testing Lab Page

Provide a dedicated page for reviewing the current skill's validation and test status.

Requirements:

Show the current skill name.
Show validation status when available.
Show test results when available.
Display an appropriate message when checks have not been run.
Provide navigation back to the creation workspace.

The page should use the same session-state data as the main workspace instead of creating a separate, inconsistent copy of the results.

9.9 Settings Page

Display the planned local model configuration.

Fields:

Ollama endpoint: http://localhost:11434
Planned model: qwen2.5:7b

In Phase 1:

These values may be read-only.
Do not attempt to connect to Ollama.
Display a clear message that model integration is not yet implemented.

Future phases may make these settings configurable and add model connectivity checks.

10. State Management

Use Streamlit's st.session_state to manage the application.

Required state:

Current page.
Current skill content.
Current skill name.
Original task description.
Whether a skill has been generated.
Latest validation results.
Latest test results.
Last updated timestamp.

State rules:

A newly generated skill replaces the current workspace skill.
A newly generated skill clears old validation and test results.
Saving edited content clears validation and test results.
Validation results must correspond to the current skill content.
Test results must correspond to the current skill content.
Navigation between pages must preserve the current session's skill.
Clearing the current skill must reset all related state.

Avoid storing redundant state when a value can be derived from existing state.

11. Error Handling

The frontend must handle the following conditions:

Empty task description.
Missing or malformed skill frontmatter.
Missing skill name.
Missing description.
Empty instruction body.
Empty or invalid export folder name.
Attempting to open a skill before creating one.
Attempting to view results before running validation or tests.

Error messages must explain the problem and, when possible, how to fix it.

Avoid exposing raw stack traces to users for expected input errors.

12. Non-Functional Requirements
Performance
The frontend should load quickly on a typical development computer.
Template generation and structural validation should execute locally without external API calls.
ZIP export should work without writing temporary files to disk.
Privacy
Phase 1 must not transmit user inputs to an external service.
User-provided task descriptions and constraints remain within the local application process.
No analytics or telemetry are required.
Maintainability
Use clearly named functions for generation, validation, test results, and export.
Keep UI rendering separate from reusable helper functions where practical.
Avoid placing all business logic inside individual UI callbacks.
Keep function interfaces stable so future Ollama integration can replace the mock generator.
Reliability
Avoid stale validation and test results after content changes.
Ensure exported content matches the current skill.
Sanitize generated folder names.
Handle missing session state safely.
13. Suggested Project Structure

Use the following structure for Phase 1:

skillforge/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore


Keep the first implementation simple. When the backend is introduced, refactor into modules such as:

skillforge/
├── app.py
├── requirements.txt
├── README.md
├── frontend/
│   └── components.py
├── generator/
│   └── skill_generator.py
├── validator/
│   └── skill_validator.py
├── evaluator/
│   └── test_runner.py
└── exporter/
    └── zip_exporter.py


Do not create unnecessary modules in Phase 1 unless they improve maintainability.

14. Acceptance Criteria

Phase 1 is complete when all of the following conditions are satisfied:

The application starts with streamlit run app.py.
The sidebar contains all four navigation sections.
The Create Skill page displays all required inputs.
Submitting an empty task displays a warning.
Submitting a valid task creates a sample SKILL.md.
The generated content contains frontmatter and instructions.
The skill content can be edited and saved.
Saving changes invalidates previous validation and testing results.
The rendered Markdown preview displays the current content.
The validator reports individual structural checks.
The testing dashboard displays clearly labeled mock results.
The export action downloads a valid ZIP containing SKILL.md.
My Skills displays the current session's skill or an empty state.
Testing Lab displays the current skill's status.
Settings displays the planned Ollama configuration.
Navigation does not unnecessarily lose the current skill.
No real LLM calls are made in Phase 1.
Mock generation and mock test results are clearly identified.
The interface is usable at common desktop and laptop resolutions.
15. Implementation Plan
Step 1: Project Initialization
Create the project directory.
Create and activate a virtual environment.
Add requirements.txt.
Install Streamlit.
Create the initial app.py.
Step 2: Design and Navigation
Configure the Streamlit page.
Implement the sidebar and navigation.
Add the custom CSS theme.
Build the shared layout and reusable visual elements.
Step 3: Skill Creation Form
Add task description, category, constraints, and preferences.
Add input validation.
Implement template-based demo generation.
Store the generated skill in session state.
Step 4: Editor and Preview
Add the Markdown editor.
Implement saving.
Add rendered Markdown preview.
Reset stale results after edits.
Step 5: Validation and Testing UI
Implement basic structural checks.
Add validation feedback.
Add illustrative test cases.
Display test summary metrics and individual results.
Step 6: Export
Implement ZIP generation in memory.
Sanitize folder names.
Add download functionality.
Ensure the ZIP contains the latest skill content.
Step 7: Secondary Pages
Implement My Skills.
Implement Testing Lab.
Implement Settings.
Ensure navigation uses shared session state.
Step 8: Testing and Cleanup
Test every acceptance criterion.
Fix state-management issues.
Check empty and invalid input scenarios.
Verify the ZIP archive.
Add setup and usage instructions to the README.
16. Future Integration Requirements

The frontend must be ready for later backend integration.

In Phase 2, replace the demo generator with an Ollama-backed implementation using the configured endpoint and model.

In Phase 3, improve validation to check the selected skill-file specification and metadata requirements.

In Phase 4, replace mock test results with real behavioral evaluations.

In Phase 5, add an improvement loop that uses test failures to revise the skill and rerun validation and tests.

In Phase 6, enhance export, error handling, and optional persistent storage.

The frontend should not require a complete redesign when these services are introduced.

17. Instructions for the Implementing Developer or AI

Implement the frontend according to this PRD.

Follow these rules:

Build a complete, runnable Streamlit application.
Use Python and Streamlit; do not introduce a separate React or Next.js frontend.
Keep the visual style consistent across all pages.
Implement real local form handling, session state, validation, and ZIP export.
Use mock data only for generation and behavioral testing.
Clearly identify every mocked capability.
Do not call Ollama or any external AI API in this phase.
Do not claim that a skill has passed real behavioral testing.
Keep the code readable and modular.
Avoid unnecessary dependencies.
Include the complete source code for every required file.
Provide installation and execution instructions.
Test the application's main workflows before considering the phase complete.
Do not leave core frontend actions as non-functional placeholder buttons.
18. Definition of Done

The frontend phase is complete when a user can launch SkillForge locally, enter a task description, create a sample skill, edit the resulting Markdown, run structural validation, view illustrative test results, navigate between all pages, and download the skill as a ZIP file.

The application must be stable, understandable, and ready for the next phase: integrating the local Ollama model.

End of PRD