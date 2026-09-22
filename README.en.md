# Letter Dispatcher — Sync edition

Address book + ready-made letters + one-click sending via Gmail or Outlook — the same core app as [Letter Dispatcher (LIGHT)](https://skymaverick171.github.io/letter-dispatcher/), plus a **Sync** tab that pulls your Contacts and Letters straight from a Google Sheet.

**Live app:** this page, once GitHub Pages is enabled for this repo (see below) — `https://<your-username>.github.io/letter-dispatcher-sync/`

## What's different from LIGHT

Everything LIGHT does, plus a **Sync** tab:

- Sign in with your own Google account (no server involved — sign-in and syncing happen entirely in your browser).
- One click pulls both your Contacts and Letters sheets into the app.
- **One-way only for now**: the sheet updates the app; the app never writes back to the sheet. Two-way sync is planned for a later version.
- Nothing is uploaded anywhere else. Your Google sign-in token stays in the browser tab's memory only and is never saved — closing the tab signs you out.

## First-time setup (one person, once)

1. **Create a Google Cloud project** and an **OAuth 2.0 Client ID** (type "Web application") in [Google Cloud Console](https://console.cloud.google.com/). Add this site's exact URL as an **Authorized JavaScript origin** (e.g. `https://<your-username>.github.io`).
2. Open the **Sync** tab in the app, paste in that **Client ID**, your Google Sheet's **Spreadsheet ID** (the long string in the sheet's URL, between `/d/` and `/edit`), and the sheet/range for Contacts (e.g. `Contacts!A:D`) and Letters (e.g. `Letters!A:E`).
3. Click **Save settings**, then **Sign in with Google**, then **Sync now**.

Sheet column layout is identical to LIGHT's existing paste/CSV import: Contacts = Name, Email, Office, Group; Letters = Subject, Body, Cc, Bcc, Personalize (yes/no).

## Repo layout

```
index.html   — the app (this is what GitHub Pages serves)
sw.js        — offline support / PWA install eligibility
docs/        — guides (added as they're written)
```

## Deploying an update

This repo has no build step — `index.html` is the whole app. To update it: replace `index.html` at the repo root with the new version and commit. GitHub Pages picks it up automatically within a minute or two.

---
See also: [Letter Dispatcher (LIGHT)](https://github.com/skymaverick171/letter-dispatcher) — the base edition this one is forked from.
