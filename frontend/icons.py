"""
SkillForge — Vector SVG Icon Library
Clean, standard, pixel-perfect developer icons (Lucide / Feather style).
Replaces all informal emojis and AI-style artifacts with standard engineering SVGs.
"""

def icon_svg(inner_svg: str, size: int = 16, color: str = "currentColor", extra_style: str = "") -> str:
    """Wraps inner SVG elements in standard SVG tag with crisp 24x24 viewport."""
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'style="display: inline-block; vertical-align: middle; {extra_style}">'
        f'{inner_svg}'
        f'</svg>'
    )

# --- Standard Developer Tool Icons ---

def icon_cube(size: int = 20, color: str = "currentColor") -> str:
    """Isometric geometric cube logo."""
    inner = (
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>'
        '<line x1="12" y1="22.08" x2="12" y2="12"></line>'
    )
    return icon_svg(inner, size, color)

def icon_layers(size: int = 24, color: str = "currentColor") -> str:
    """Stacked architectural layers."""
    inner = (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>'
        '<polyline points="2 17 12 22 22 17"></polyline>'
        '<polyline points="2 12 12 17 22 12"></polyline>'
    )
    return icon_svg(inner, size, color)

def icon_folder(size: int = 16, color: str = "currentColor") -> str:
    inner = '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>'
    return icon_svg(inner, size, color)

def icon_file_code(size: int = 16, color: str = "currentColor") -> str:
    inner = (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<polyline points="10 13 8 15 10 17"></polyline>'
        '<polyline points="14 13 16 15 14 17"></polyline>'
    )
    return icon_svg(inner, size, color)

def icon_book_open(size: int = 24, color: str = "currentColor") -> str:
    inner = (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>'
    )
    return icon_svg(inner, size, color)

def icon_flask(size: int = 24, color: str = "currentColor") -> str:
    inner = (
        '<path d="M10 2v7.31L4.69 19.3A2 2 0 0 0 6.42 22h11.16a2 2 0 0 0 1.73-2.7L14 9.31V2"></path>'
        '<line x1="8.5" y1="2" x2="15.5" y2="2"></line>'
        '<line x1="6.5" y1="16" x2="17.5" y2="16"></line>'
    )
    return icon_svg(inner, size, color)

def icon_check(size: int = 14, color: str = "#10b981") -> str:
    inner = '<polyline points="20 6 9 17 4 12"></polyline>'
    return icon_svg(inner, size, color, "margin-right: 4px;")

def icon_x(size: int = 14, color: str = "#f43f5e") -> str:
    inner = (
        '<line x1="18" y1="6" x2="6" y2="18"></line>'
        '<line x1="6" y1="6" x2="18" y2="18"></line>'
    )
    return icon_svg(inner, size, color, "margin-right: 4px;")

def icon_alert_triangle(size: int = 14, color: str = "#f59e0b") -> str:
    inner = (
        '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>'
        '<line x1="12" y1="9" x2="12" y2="13"></line>'
        '<line x1="12" y1="17" x2="12.01" y2="17"></line>'
    )
    return icon_svg(inner, size, color, "margin-right: 4px;")

def icon_lightbulb(size: int = 14, color: str = "#818cf8") -> str:
    inner = (
        '<line x1="9" y1="18" x2="15" y2="18"></line>'
        '<line x1="10" y1="22" x2="14" y2="22"></line>'
        '<path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5h6.18z"></path>'
    )
    return icon_svg(inner, size, color, "margin-right: 6px;")

def icon_info(size: int = 14, color: str = "#38bdf8") -> str:
    inner = (
        '<circle cx="12" cy="12" r="10"></circle>'
        '<line x1="12" y1="16" x2="12" y2="12"></line>'
        '<line x1="12" y1="8" x2="12.01" y2="8"></line>'
    )
    return icon_svg(inner, size, color, "margin-right: 4px;")

def icon_shield_check(size: int = 16, color: str = "#94a3b8") -> str:
    inner = (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>'
        '<polyline points="9 12 11 14 15 10"></polyline>'
    )
    return icon_svg(inner, size, color)

def icon_target(size: int = 16, color: str = "#94a3b8") -> str:
    inner = (
        '<circle cx="12" cy="12" r="10"></circle>'
        '<circle cx="12" cy="12" r="6"></circle>'
        '<circle cx="12" cy="12" r="2"></circle>'
    )
    return icon_svg(inner, size, color)

def icon_cpu(size: int = 16, color: str = "#94a3b8") -> str:
    inner = (
        '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>'
        '<rect x="9" y="9" width="6" height="6"></rect>'
        '<line x1="9" y1="1" x2="9" y2="4"></line>'
        '<line x1="15" y1="1" x2="15" y2="4"></line>'
        '<line x1="9" y1="20" x2="9" y2="23"></line>'
        '<line x1="15" y1="20" x2="15" y2="23"></line>'
        '<line x1="20" y1="9" x2="23" y2="9"></line>'
        '<line x1="20" y1="14" x2="23" y2="14"></line>'
        '<line x1="1" y1="9" x2="4" y2="9"></line>'
        '<line x1="1" y1="14" x2="4" y2="14"></line>'
    )
    return icon_svg(inner, size, color)

def icon_workflow(size: int = 16, color: str = "#94a3b8") -> str:
    inner = (
        '<line x1="6" y1="3" x2="6" y2="15"></line>'
        '<circle cx="18" cy="6" r="3"></circle>'
        '<circle cx="6" cy="18" r="3"></circle>'
        '<path d="M18 9a9 9 0 0 1-9 9"></path>'
    )
    return icon_svg(inner, size, color)

def icon_server(size: int = 16, color: str = "currentColor") -> str:
    inner = (
        '<rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>'
        '<rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>'
        '<line x1="6" y1="6" x2="6.01" y2="6"></line>'
        '<line x1="6" y1="18" x2="6.01" y2="18"></line>'
    )
    return icon_svg(inner, size, color)

def icon_download(size: int = 16, color: str = "currentColor") -> str:
    inner = (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>'
        '<polyline points="7 10 12 15 17 10"></polyline>'
        '<line x1="12" y1="15" x2="12" y2="3"></line>'
    )
    return icon_svg(inner, size, color)
