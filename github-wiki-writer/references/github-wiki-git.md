# GitHub wiki git (publish)

Wiki content is a **separate git repo**: `https://github.com/OWNER/REPO.wiki.git` (SSH: `git@github.com:OWNER/REPO.wiki.git`).

## Unprovisioned wiki (hard)

The wiki git is **unprovisioned** until someone **saves the first page in the browser**.

1. Repo **Settings -> Features -> Wikis** must be on.
2. Open `https://github.com/OWNER/REPO/wiki/_new`, write any title (often `Home`), save once.
3. REST and GraphQL **often cannot** create that first page. Do not loop on `gh api` / GraphQL `create` as the provisioner.
4. Then `git clone` the `.wiki.git` URL.

If clone fails with not-found **before** that browser save, the wiki git does not exist yet -- **MUST** provision in the browser, not invent a workaround.

## Private repos

Logged-out `https://github.com/OWNER/REPO/wiki` often **404**. That is **not** proof the wiki is empty or missing.

**MUST** verify with an **authenticated** clone or:

```text
git ls-remote https://github.com/OWNER/REPO.wiki.git
git clone https://github.com/OWNER/REPO.wiki.git
git ls-tree -r HEAD --name-only
```

Use the same credentials as for the private project repo (`gh auth`, Git Credential Manager, or SSH).

## Layout on disk

All pages live at the **wiki clone root** (Gollum). **MUSTNOT** nest `docs/wiki/` folders inside `.wiki.git`.

Required:

- `Home.md` -- hub
- `_Sidebar.md` -- navigation; `[[WikiLinks]]` to every page
- One `Topic.md` per topic

Optional: `_Footer.md`.

Copy from the versioned mirror:

```text
# after wiki git exists
git clone https://github.com/OWNER/REPO.wiki.git
# copy *.md from project docs/wiki/ to the clone root (overwrite)
git -C REPO.wiki add -A
git -C REPO.wiki status
git -C REPO.wiki commit -m "Publish wiki pages from docs/wiki mirror."
git -C REPO.wiki push
```

**MUSTNOT** force-push the wiki unless the user explicitly asks.

## Sidebar

`_Sidebar.md` is not a normal article. Keep it a list of `[[Page-Name]]` groups. Every published page **MUST** appear here or readers will not find it.

## Checks after push

- Authenticated `git ls-tree` shows `Home.md`, `_Sidebar.md`, and each topic file at **root**.
- Browser (logged in if private): Home is a hub; each sidebar link opens a **distinct** URL.
- **MUSTNOT** declare success from an anonymous 404.
