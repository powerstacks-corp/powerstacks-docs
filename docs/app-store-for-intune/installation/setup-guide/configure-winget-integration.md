---
title: "Configure WinGet integration"
description: "Add a GitHub personal access token so the App Catalog gets higher API rate limits and live search, and optionally point at a custom WinGet repository."
---

# Configure WinGet integration

The App Catalog pulls package manifests from Microsoft's WinGet repository on GitHub. These settings live in **Admin** > **Settings** > **WinGet Integration**. Adding a GitHub token is optional but strongly recommended.

## GitHub personal access token (recommended)

Without a token, the catalog uses GitHub's anonymous API limit, which slows the initial cache sync and disables live search. With a token, syncs are faster and the "Show More Results" live search works.

| | Without a token | With a token |
| --- | --- | --- |
| API requests | 60 per hour | 5,000 per hour |
| Initial cache sync | 2 to 3 hours | 30 to 60 minutes |
| "Show More Results" live search | Not available (only cached results and exact package-ID lookups like `Google.Chrome` work) | Full live search across the WinGet repository in real time |

The live search needs a token because GitHub's code search API requires authentication.

To create and add the token:

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens).
2. Select **Generate new token** > **Generate new token (classic)**.
3. Give it a descriptive name, for example "App Store for Intune WinGet".
4. Select the **`public_repo`** scope.
5. Select **Generate token** and copy the value (it starts with `ghp_`).
6. In the portal, go to **Admin** > **Settings** > **WinGet Integration**, paste the value into **GitHub Personal Access Token**, and select **Save**.

The token is stored in Azure Key Vault and is never shown in logs or the UI.

## WinGet repository URL (advanced)

By default the catalog uses Microsoft's official repository, `https://github.com/microsoft/winget-pkgs`. Organizations that maintain an internal mirror can point this at their own repository (format: `https://github.com/owner/repo` or `owner/repo`).

!!! warning
    Changing the repository URL clears the entire package cache, so the catalog re-syncs from the new source.
