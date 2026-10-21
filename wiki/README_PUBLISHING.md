# Publishing this folder to the GitHub Wiki

This folder (`wiki/`) is the source of truth for the project's **GitHub Wiki**
(not an Obsidian vault — that approach was dropped). Everything in here is
plain markdown generated or hand-curated for GitHub's wiki renderer, including
`_Sidebar.md` and `_Footer.md`.

## Why publishing is a separate step

GitHub's wiki has no REST or GraphQL API. The only way to update it
programmatically is a `git push` to the wiki's own git repository, at
`https://github.com/<owner>/<repo>.wiki.git` — a different git repo from the
main one, even though it's tied to the same GitHub repository.

## One-time setup (do this once, in the browser)

The wiki repo doesn't exist until it has a first page. On GitHub:

1. Open the repository → **Wiki** tab (if you don't see one, enable it under
   **Settings → Features → Wikis** first).
2. Click **Create the first page**, type anything, and **Save Page**.

After that, `https://github.com/<owner>/<repo>.wiki.git` is a real,
clonable/pushable git repository.

## Publishing after that

Run `scripts/publish_wiki.sh` from the repo root (needs git push access to
the repo, e.g. via `gh auth login`):

```bash
./scripts/publish_wiki.sh
```

It clones the wiki repo, mirrors the contents of `wiki/` into it, and pushes.
Re-run it any time `wiki/` changes — it's idempotent and only commits if
something actually changed.
