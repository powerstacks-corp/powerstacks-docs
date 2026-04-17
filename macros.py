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
    Embed a Storylane demo in a responsive, branded wrapper.

    Accepts either a share URL (https://powerstacks.storylane.io/share/XXXX)
    or an already-finalized embed URL. If the URL has no ?embed=inline query
    parameter, we append it so Storylane renders the inline embed variant.
    """
    if not url:
        return ""

    embed_url = url
    if "embed=" not in embed_url:
        sep = "&" if "?" in embed_url else "?"
        embed_url = f"{embed_url}{sep}embed=inline"

    title_html = (
        f'<div class="ps-storylane__title">{title}</div>' if title else ""
    )

    return (
        f'<div class="ps-storylane">'
        f'  {title_html}'
        f'  <div class="ps-storylane__embed">'
        f'    <iframe src="{embed_url}" loading="lazy" allow="fullscreen" allowfullscreen '
        f'            referrerpolicy="no-referrer-when-downgrade" title="Storylane demo"></iframe>'
        f'  </div>'
        f'  <p class="ps-storylane__fallback">'
        f'    Having trouble with the embed? <a href="{url}" target="_blank" rel="noopener">Open the demo in a new tab</a>.'
        f'  </p>'
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
    out = ['<ul class="ps-release-list">']
    for e in entries:
        date_str = e['date'].strftime('%B %d, %Y') if e['date'] else ''
        date_html = f' <span class="ps-release-list__date">— {date_str}</span>' if date_str else ''
        out.append(
            f'  <li><a href="{e["url"]}"><strong>{e["title"]}</strong></a>{date_html}</li>'
        )
    out.append('</ul>')
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
