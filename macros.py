"""
PowerStacks Docs — MkDocs macros.

Provides two page-level macros:
  - storylane(url, title=None)            — embed a Storylane demo
  - release_archive(product, show='latest', count=6)
                                          — render the Latest or Archive release list

Invoked via mkdocs-macros-plugin (configured in mkdocs.yml).
"""
import os
import re
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────────────────────────
# Macro: storylane(url, title=None)
# ──────────────────────────────────────────────────────────────────

def _storylane(url, title=None):
    """
    Render a click-to-open card for a Storylane demo.

    Shows a branded card with a play button. Clicking opens the demo
    in a lightbox modal overlay (or new tab as fallback). No iframe
    on the page itself — avoids Storylane's embed wrapper issues.
    """
    if not url:
        return ""

    display_title = title or "Interactive Demo"

    return (
        f'<div class="ps-storylane">'
        f'  <a href="{url}" class="ps-storylane__card" target="_blank" rel="noopener" '
        f'     data-storylane-url="{url}" onclick="return psOpenStorylaneLightbox(this)">'
        f'    <span class="ps-storylane__play">'
        f'      <svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>'
        f'    </span>'
        f'    <span class="ps-storylane__info">'
        f'      <span class="ps-storylane__label">INTERACTIVE WALKTHROUGH</span>'
        f'      <span class="ps-storylane__title">{display_title}</span>'
        f'      <span class="ps-storylane__cta">Click to start demo</span>'
        f'    </span>'
        f'  </a>'
        f'</div>'
    )


# ──────────────────────────────────────────────────────────────────
# Macro: release_archive(product, show='latest', count=6)
# ──────────────────────────────────────────────────────────────────

_VERSION_FILE_RE = re.compile(r'^versions?-.+\.md$', re.IGNORECASE)


def _read_frontmatter(path):
    """Read frontmatter from a markdown file. Returns a dict."""
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return {}
    if not text.startswith('---'):
        return {}
    end = text.find('\n---', 3)
    if end < 0:
        return {}
    fm_text = text[3:end].strip()
    result = {}
    for line in fm_text.split('\n'):
        line = line.strip()
        if ':' in line:
            k, _, v = line.partition(':')
            v = v.strip().strip('"').strip("'")
            result[k.strip()] = v
    return result


def _parse_date(s):
    """Parse various date formats used in frontmatter."""
    if not s:
        return None
    formats = [
        '%Y-%m-%d',
        '%B %d, %Y',
        '%b %d, %Y',
        '%b. %d, %Y',
        '%d %B %Y',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def _version_pages(product_slug, docs_dir):
    """Return list of (path, title, date, url) for each release-notes version."""
    rn_dir = Path(docs_dir) / product_slug / 'release-notes'
    if not rn_dir.exists():
        return []

    entries = []
    for md in rn_dir.iterdir():
        if not md.is_file():
            continue
        if md.name in ('index.md', 'archive.md'):
            continue
        if not md.name.endswith('.md'):
            continue

        fm = _read_frontmatter(md)
        title = fm.get('title', md.stem.replace('-', ' ').title())
        date = _parse_date(fm.get('date', ''))
        if not date:
            # Fallback: try to extract from filename, e.g. "version-65-0-feb-21-2026.md"
            m = re.search(r'([a-z]+)-(\d{1,2})-(\d{4})', md.name.lower())
            if m:
                try:
                    date = datetime.strptime(f"{m.group(1)} {m.group(2)}, {m.group(3)}", '%b %d, %Y')
                except ValueError:
                    try:
                        date = datetime.strptime(f"{m.group(1)} {m.group(2)}, {m.group(3)}", '%B %d, %Y')
                    except ValueError:
                        date = None

        # Generate the URL relative to the doc being rendered.
        # Since the release_archive is called from .../release-notes/index.md
        # or archive.md, we want "version-XX.../" as a relative link.
        url = md.stem + '/'

        entries.append({
            'path': md,
            'title': title,
            'date': date,
            'url': url,
        })

    # Sort by date descending (newest first); undated entries last
    entries.sort(key=lambda e: (e['date'] is None, -(e['date'].timestamp() if e['date'] else 0)))
    return entries


def _release_archive(product, show='latest', count=6, docs_dir=None):
    """
    Render release notes as an HTML list.

    Args:
        product: slug like 'bi-for-intune'
        show:    'latest' (first N entries) or 'archive' (past N, year-grouped)
        count:   how many to treat as "latest"
    """
    entries = _version_pages(product, docs_dir or 'docs')
    if not entries:
        return '<p><em>No release notes found.</em></p>'

    if show == 'latest':
        subset = entries[:count]
        return _render_flat_list(subset)
    elif show == 'archive':
        subset = entries[count:]
        if not subset:
            return '<p><em>No older releases to archive yet.</em></p>'
        return _render_year_grouped(subset)
    else:
        raise ValueError(f"Unknown show mode: {show!r} (use 'latest' or 'archive')")


def _render_flat_list(entries):
    """Render recent releases with expanded content (body text shown inline)."""
    out = []
    for e in entries:
        date_str = e['date'].strftime('%B %d, %Y') if e['date'] else ''

        # Read the markdown body (everything after frontmatter)
        body = ''
        try:
            text = e['path'].read_text(encoding='utf-8')
            # Strip frontmatter
            if text.startswith('---'):
                end = text.find('\n---', 3)
                if end > 0:
                    body = text[end + 4:].strip()
                else:
                    body = text
            else:
                body = text.strip()

            # Remove the H1 title (already shown in our heading)
            lines = body.split('\n')
            if lines and lines[0].startswith('# '):
                lines = lines[1:]
            body = '\n'.join(lines).strip()

            # Truncate very long notes — show first ~30 lines
            body_lines = body.split('\n')
            if len(body_lines) > 40:
                body = '\n'.join(body_lines[:40]) + '\n\n*[Read full release notes...](' + e['url'] + ')*'
        except Exception:
            body = ''

        out.append(f'<div class="ps-release-entry">')
        out.append(f'<h3><a href="{e["url"]}">{e["title"]}</a>')
        if date_str:
            out.append(f' <span class="ps-release-entry__date">— {date_str}</span>')
        out.append(f'</h3>')

        if body:
            # Convert markdown body to a raw block that MkDocs will render
            # We use HTML wrapper + the body as-is (macros plugin processes it)
            out.append(f'<div class="ps-release-entry__body" markdown>')
            out.append(body)
            out.append(f'</div>')
        out.append(f'</div>')
        out.append('')  # blank line between entries

    return '\n'.join(out)


def _render_year_grouped(entries):
    from collections import defaultdict
    by_year = defaultdict(list)
    for e in entries:
        # Use a string key so mixing dated + undated entries can still sort.
        year = str(e['date'].year) if e['date'] else '0000'
        by_year[year].append(e)

    out = []
    for year in sorted(by_year.keys(), reverse=True):
        header = 'Undated' if year == '0000' else f'{year} Releases'
        out.append(f'<h2>{header}</h2>')
        out.append('<ul class="ps-release-list">')
        for e in by_year[year]:
            date_str = e['date'].strftime('%B %d, %Y') if e['date'] else ''
            date_html = f' <span class="ps-release-list__date">— {date_str}</span>' if date_str else ''
            out.append(
                f'  <li><a href="{e["url"]}"><strong>{e["title"]}</strong></a>{date_html}</li>'
            )
        out.append('</ul>')
    return '\n'.join(out)


# ──────────────────────────────────────────────────────────────────
# Plugin entry point
# ──────────────────────────────────────────────────────────────────

def define_env(env):
    """Register macros with mkdocs-macros-plugin."""
    docs_dir = env.conf.get('docs_dir', 'docs')

    @env.macro
    def storylane(url, title=None):
        return _storylane(url, title)

    @env.macro
    def release_archive(product, show='latest', count=6):
        return _release_archive(product, show=show, count=count, docs_dir=docs_dir)
