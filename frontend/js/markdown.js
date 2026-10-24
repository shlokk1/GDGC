/**
 * SkillForge — Fast Lightweight Markdown Parser & Formatter
 * Self-contained zero-dependency renderer for SKILL.md specs.
 */

window.MarkdownRenderer = {
  escapeHtml: function(text) {
    if (!text) return '';
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  render: function(md) {
    if (!md) return '<div style="color: #64748b; font-style: italic;">No content available.</div>';

    let html = '';
    let content = md;

    // 1. Parse Frontmatter if present (--- ... ---)
    if (content.startsWith('---')) {
      const secondIdx = content.indexOf('---', 3);
      if (secondIdx !== -1) {
        const fmRaw = content.substring(3, secondIdx).trim();
        content = content.substring(secondIdx + 3).trim();

        // Render frontmatter card
        const fmLines = fmRaw.split('\n');
        let fmMeta = {};
        fmLines.forEach(l => {
          const sep = l.indexOf(':');
          if (sep !== -1) {
            const k = l.substring(0, sep).trim();
            const v = l.substring(sep + 1).trim().replace(/^['"]|['"]$/g, '');
            fmMeta[k] = v;
          }
        });

        html += `
          <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-size: 0.74rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.04em;">Agent Skill Specification</span>
              <span class="sf-pill sf-pill-indigo">YAML v1.0</span>
            </div>
            <div style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
              ${this.escapeHtml(fmMeta.name || 'unnamed-skill')}
            </div>
            ${fmMeta.description ? `<p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">${this.escapeHtml(fmMeta.description)}</p>` : ''}
          </div>
        `;
      }
    }

    // 2. Parse Markdown body
    const lines = content.split('\n');
    let inCodeBlock = false;
    let codeBuffer = [];
    let codeLang = '';
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];

      // Code blocks
      if (line.trim().startsWith('```')) {
        if (!inCodeBlock) {
          if (inList) { html += '</ul>'; inList = false; }
          inCodeBlock = true;
          codeLang = line.trim().substring(3).trim();
          codeBuffer = [];
          continue;
        } else {
          inCodeBlock = false;
          html += `<pre><code class="language-${this.escapeHtml(codeLang)}">${this.escapeHtml(codeBuffer.join('\n'))}</code></pre>`;
          codeBuffer = [];
          continue;
        }
      }

      if (inCodeBlock) {
        codeBuffer.push(line);
        continue;
      }

      // Headers
      if (line.startsWith('# ')) {
        if (inList) { html += '</ul>'; inList = false; }
        html += `<h1>${this.inlineFormat(line.substring(2))}</h1>`;
        continue;
      }
      if (line.startsWith('## ')) {
        if (inList) { html += '</ul>'; inList = false; }
        html += `<h2>${this.inlineFormat(line.substring(3))}</h2>`;
        continue;
      }
      if (line.startsWith('### ')) {
        if (inList) { html += '</ul>'; inList = false; }
        html += `<h3>${this.inlineFormat(line.substring(4))}</h3>`;
        continue;
      }

      // Checklists [ ] or [x]
      if (line.trim().startsWith('- [ ]') || line.trim().startsWith('- [x]')) {
        if (inList) { html += '</ul>'; inList = false; }
        const isChecked = line.trim().startsWith('- [x]');
        const checkText = line.trim().substring(5).trim();
        html += `
          <div style="display: flex; align-items: center; gap: 8px; margin: 6px 0; font-size: 0.88rem; color: #cbd5e1;">
            <input type="checkbox" ${isChecked ? 'checked' : ''} disabled style="accent-color: #10b981;">
            <span>${this.inlineFormat(checkText)}</span>
          </div>
        `;
        continue;
      }

      // Unordered list
      if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        if (!inList) {
          html += '<ul>';
          inList = true;
        }
        html += `<li>${this.inlineFormat(line.trim().substring(2))}</li>`;
        continue;
      }

      // Ordered list
      const numMatch = line.trim().match(/^(\d+)\.\s+(.*)$/);
      if (numMatch) {
        if (inList) { html += '</ul>'; inList = false; }
        html += `<div style="margin: 4px 0 4px 14px; font-size: 0.9rem;"><strong>${numMatch[1]}.</strong> ${this.inlineFormat(numMatch[2])}</div>`;
        continue;
      }

      if (inList) {
        html += '</ul>';
        inList = false;
      }

      // Blank line
      if (!line.trim()) {
        html += '<div style="height: 8px;"></div>';
        continue;
      }

      // Regular paragraph
      html += `<p style="margin-bottom: 8px;">${this.inlineFormat(line)}</p>`;
    }

    if (inList) html += '</ul>';
    if (inCodeBlock) {
      html += `<pre><code>${this.escapeHtml(codeBuffer.join('\n'))}</code></pre>`;
    }

    return html;
  },

  inlineFormat: function(text) {
    if (!text) return '';
    let s = this.escapeHtml(text);

    // Bold **text**
    s = s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic *text*
    s = s.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Inline code `code`
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');

    return s;
  }
};
