# PowerStacks Docs

Consolidated documentation site for PowerStacks BI products:

- **BI for Intune**
- **BI for SCCM**
- **BI for Defender**

Published at <https://docs.powerstacks.com/>.

## History

This repo consolidates the documentation from three predecessor repos:

- `powerstacks-corp/BI-for-Intune` (docs migrated here; `.pbix` files and product assets remain in original repo)
- `powerstacks-corp/BI-for-SCCM` (same)
- `powerstacks-corp/BI-for-Defender` (same)

Full git history from all three is preserved in this repo via `git filter-repo` + `git merge --allow-unrelated-histories`. Blame works across the migration (use `--follow` for files that moved).

## Local development

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000/> to view.

Override URLs for local testing:

```bash
MARKETING_URL=http://localhost:4321 ASSISTANT_URL=http://localhost:3000 mkdocs serve
```

## Repo layout

```text
docs/
├── index.md                  # site root (product picker)
├── assets/                   # logo, favicon, shared images
├── bi-for-intune/
│   ├── index.md              # product landing
│   ├── installation/
│   │   ├── getting-started/
│   │   ├── setup-guide/
│   │   ├── log-analytics/    # Intune-specific
│   │   └── custom-inventory/ # Intune-specific
│   ├── administration/
│   ├── user-guides/
│   ├── release-notes/
│   └── images/
├── bi-for-sccm/
├── bi-for-defender/
├── shared/                   # content used by multiple products (e.g. licensing)
├── stylesheets/              # site-wide CSS
└── scripts/                  # site-wide JS
macros.py                     # Storylane + release_archive macros
overrides/
  └── main.html               # global nav + assistant widget
.github/
  └── workflows/
      └── deploy.yml          # builds and deploys to GitHub Pages
```

## Deploy

Pushes to `main` trigger a GitHub Actions workflow that builds the site with MkDocs and deploys to GitHub Pages. Custom domain `docs.powerstacks.com` is configured in repo Settings → Pages.
