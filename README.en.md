# Letter Dispatcher — Sync edition

Address book + ready-made letters + one-click sending via Gmail or Outlook — the same core app as [Letter Dispatcher (LIGHT)](https://skymaverick171.github.io/letter-dispatcher/), plus a **Sync** tab that pulls your Contacts and Letters straight from a Google Sheet.

**Live app:** this page, once GitHub Pages is enabled for this repo (see below) — `https://<your-username>.github.io/letter-dispatcher-sync/`

## What's different from LIGHT

Everything LIGHT does, plus a **Sync** tab:

- Sign in with your own Google account (no server involved — sign-in and syncing happen entirely in your browser).
- One click pulls both your Contacts and Letters sheets into the app.
- **Two-way for admins, one-way for everyone else.** Whether "Sync now" also pushes local changes back to the sheet, or only pulls (like Stage 1), depends on whether the signed-in Google account is on the sheet's admins list — see below.
- Address book entries can carry a phone number, with a 📞 Call button next to any contact that has one — it opens your device's phone/calling app when one is available.
- Nothing is uploaded anywhere else. Your Google sign-in token stays in the browser tab's memory only and is never saved — closing the tab signs you out.

## First-time setup (one person, once)

1. **Create a Google Cloud project** and an **OAuth 2.0 Client ID** (type "Web application") in [Google Cloud Console](https://console.cloud.google.com/). Add this site's exact URL as an **Authorized JavaScript origin** (e.g. `https://<your-username>.github.io`).
2. In your Google Sheet, add a hidden **ID column** at the end of each data sheet — column **F** on both Contacts and Letters (already included if you start from the provided templates). Leave it blank for existing rows; the app fills it in the first time each row is synced. Don't type into it by hand.
3. Optional, for two-way sync: add a sheet/tab named **Admins** with one Google account email per row (column A). Any account NOT on this list gets one-way (read-only) sync, no matter what — this is a convenience switch, not real security, since this is a static site with no server to enforce it.
4. Open the **Sync** tab in the app, paste in that **Client ID**, your Google Sheet's **Spreadsheet ID** (the long string in the sheet's URL, between `/d/` and `/edit`), the sheet/range for Contacts (e.g. `Contacts!A:F`) and Letters (e.g. `Letters!A:F`), and — if you set one up — the Admins sheet/range (e.g. `Admins!A:A`).
5. Click **Save settings**, then **Sign in with Google** (accounts already granted access under Stage 1's narrower permissions will be asked to re-approve — two-way sync needs write access, not just read), then **Sync now**.

Sheet column layout: Contacts = Name, Email, Office, Group, Phone, ID; Letters = Subject, Body, Cc, Bcc, Personalize (yes/no), ID.

### If you already set up Contacts sync before this update

The Contacts sheet gained a **Phone** column, inserted right before the existing ID column — so the ID column moved from **E** to **F**. In Google Sheets, right-click the header of your current ID column and choose **Insert 1 column left**; that opens a blank column E for Phone and slides your existing ID values into F untouched (nothing is renumbered or lost). Then update the Contacts range in the app's Sync tab from `…!A:E` to `…!A:F`. Letters are unaffected.

### How two-way sync decides what to do

Since Google Sheets has no per-row "last edited" timestamp, the app keeps its own record (in this browser only) of what it last saw for each contact/letter. On every "Sync now" it compares that record against the current app data and the current sheet data:

- Changed only here → pushed to the sheet.
- Changed only in the sheet → pulled into the app.
- Changed in both, to different values → you're asked which version to keep, one at a time.
- Deleted here, or deleted in the sheet → **never propagated either way** — the app doesn't delete the sheet row, and the sheet doesn't delete the app record. This keeps a mistaken delete on either side from cascading, but it does mean an intentional deletion needs to be repeated on the other side by hand.

Because this bookkeeping lives in the browser's local storage, it's per-device — the same "worked on my computer, not on my phone until I signed in there too" behavior as Stage 1's settings.

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
