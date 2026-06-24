# Docs replatform: MkDocs -> Astro Starlight (decisions captured)

Status: decided in principle, POC not built yet. This is the agreed spec to
build against when we pick it up.

## Why move

- One unified nav. Today the marketing site (Astro) and the docs (MkDocs) have
  two separate nav menus that must be kept in sync by hand. Biggest win: a single
  shared header across site + docs so there is only one nav to maintain.
- Layout. MkDocs wastes space in the left and right margins. We want the
  full-width feel Nerdio's docs have, using the whole screen.
- Left sidebar. The current MkDocs left menu is not great. We want a scoped
  accordion sidebar like Nerdio's.
- Scroll behavior. The current biggest annoyance: past a certain point the MkDocs
  left menu stops scrolling and you have to scroll the page body instead. The new
  layout must fix this (sticky, independently scrolling sidebar).

## Target design

- "Docs" appears in the top nav as a NON-clickable dropdown. Under it, each of the
  four products is a clickable link: BI for Intune, BI for SCCM, BI for Defender,
  App Store for Intune.
- Each product link goes to a per-product LANDING page. The landing page has:
  - Intro text (not a "promoted articles" section).
  - Tiles for the main sections: Install, Admin, User, What's New.
  - Look: a mix of our current style, Nerdio, and Intune. Tiles similar to what
    Nerdio and Intune use. Do NOT build custom icon tiles linking to top-level
    sections from a global docs home; the tiles live on the product landing pages.
- Article pages: an "In this article" right-hand table of contents, MS Learn
  style.
- Where MS Learn has "Ask Learn", we have an "Ask Pax" button.
- "Was this helpful?" thumbs on each page. This is the DOC-PAGE feedback and goes
  to Google Analytics as an event (per-page counts). It is separate from Pax's own
  answer thumbs, which land in the Pax Postgres DB.

## Hosting and repo

- Host the built docs on AWS S3, same model as the marketing site: push content,
  publish to the dev site, and when happy promote to prod (a dev -> prod gate).
- Once the docs are off GitHub Pages, make the docs source repo private (the
  marketing site already proves private-repo / public-site works on S3).

## SEO note

- Keep docs as a subdirectory (powerstacks.com/docs/...) rather than the
  docs.powerstacks.com subdomain. Subdirectory consolidates authority to the main
  domain, and the Starlight move gets us there while also unifying the nav.

## Open design question

- Same repo as powerstacks-website (shared components, one build) vs a separate
  repo that imports a shared nav/header component. Decide before the POC.

## Next step

- Build a Starlight POC of one product (likely App Store for Intune or BI for
  Intune) to validate the nav, landing page tiles, sidebar scroll, "In this
  article" TOC, and the Ask Pax + Was-this-helpful elements.
