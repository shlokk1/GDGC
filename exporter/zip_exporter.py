"""
SkillForge — ZIP Exporter Module
Packages skill instructions and optional auxiliary project assets into a portable ZIP archive.
Created purely in-memory via io.BytesIO and zipfile without touching disk.
"""

import io
import re
import zipfile
from typing import Dict, Any, Optional, List

def sanitize_folder_name(name: str) -> str:
    """Sanitizes user input into a safe kebab-case folder name."""
    if not name or not name.strip():
        return "my-skill"
    cleaned = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[-\s]+", "-", cleaned).strip("-")
    return slug or "my-skill"

def create_skill_zip(
    folder_name: str,
    skill_content: str,
    include_metadata_manifest: bool = True,
    project_files: Optional[Dict[str, str]] = None,
    extra_files: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Creates an in-memory ZIP archive conforming to the standard skill bundle layout:
    
    <folder_name>.zip
    └── <folder_name>/
        ├── SKILL.md
        ├── MANIFEST.txt
        └── references/
            ├── file1.yaml
            └── file2.py
    """
    safe_slug = sanitize_folder_name(folder_name)
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Main SKILL.md
        zf.writestr(f"{safe_slug}/SKILL.md", skill_content)
        
        # 2. Package manifest
        if include_metadata_manifest:
            ref_list = "\n".join(f"- references/{f}" for f in (project_files or {}).keys()) or "None"
            manifest = f"""# SkillForge Package Manifest
Package: {safe_slug}
Format: Agent Skills Open Standard v1.0
Generator: SkillForge AI Studio
Target Specification: SKILL.md
Referenced Files:
{ref_list}
"""
            zf.writestr(f"{safe_slug}/MANIFEST.txt", manifest)

        # 3. Project reference files
        if project_files:
            for fname, fcontent in project_files.items():
                clean_name = fname.lstrip("/\\")
                zf.writestr(f"{safe_slug}/references/{clean_name}", fcontent)

        # 4. Any extra auxiliary files
        if extra_files:
            for filepath, filecontent in extra_files.items():
                clean_path = filepath.lstrip("/\\")
                zf.writestr(f"{safe_slug}/{clean_path}", filecontent)

    buffer.seek(0)
    return buffer.getvalue()

def generate_file_tree_view(folder_name: str, project_files: Optional[Dict[str, str]] = None) -> str:
    """Returns an ASCII directory tree of the exported ZIP bundle."""
    safe_slug = sanitize_folder_name(folder_name)
    tree_lines = [
        f"📦 {safe_slug}.zip",
        f"└── 📁 {safe_slug}/",
        f"    ├── 📄 SKILL.md",
        f"    └── 📄 MANIFEST.txt"
    ]
    if project_files:
        tree_lines.append(f"    └── 📁 references/")
        items = list(project_files.keys())
        for idx, fname in enumerate(items):
            prefix = "        └──" if idx == len(items) - 1 else "        ├──"
            tree_lines.append(f"{prefix} 📄 {fname}")

    return "\n".join(tree_lines)
