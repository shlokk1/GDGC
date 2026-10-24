"""
SkillForge — ZIP Exporter Module
Packages skill instructions and optional auxiliary assets into a portable, standard-compliant ZIP archive.
Created purely in-memory via io.BytesIO and zipfile without touching disk.
"""

import io
import re
import zipfile
from typing import Dict, Any, Optional

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
    extra_files: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Creates an in-memory ZIP archive conforming to the standard skill bundle layout:
    
    <folder_name>.zip
    └── <folder_name>/
        ├── SKILL.md
        └── (optional extras)
    """
    safe_slug = sanitize_folder_name(folder_name)
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Main SKILL.md
        zf.writestr(f"{safe_slug}/SKILL.md", skill_content)
        
        # 2. Optional manifest / metadata file
        if include_metadata_manifest:
            manifest = f"""# SkillForge Package Manifest
Package: {safe_slug}
Format: Agent Skills Open Standard
Generator: SkillForge v1.0
Target File: SKILL.md
"""
            zf.writestr(f"{safe_slug}/MANIFEST.txt", manifest)

        # 3. Any extra auxiliary files
        if extra_files:
            for filepath, filecontent in extra_files.items():
                clean_path = filepath.lstrip("/\\")
                zf.writestr(f"{safe_slug}/{clean_path}", filecontent)

    buffer.seek(0)
    return buffer.getvalue()

def generate_file_tree_view(folder_name: str, has_extras: bool = False) -> str:
    """Returns an ASCII directory tree of the exported ZIP bundle."""
    safe_slug = sanitize_folder_name(folder_name)
    if has_extras:
        return f"""📦 {safe_slug}.zip
└── 📁 {safe_slug}/
    ├── 📄 SKILL.md
    └── 📄 MANIFEST.txt"""
    return f"""📦 {safe_slug}.zip
└── 📁 {safe_slug}/
    ├── 📄 SKILL.md
    └── 📄 MANIFEST.txt"""
