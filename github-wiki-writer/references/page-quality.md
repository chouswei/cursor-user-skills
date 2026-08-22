# Wiki page quality

Apply after drafting; max one revision.

## Pass

- [ ] More than one topic page besides Home
- [ ] `_Sidebar.md` lists every page with `[[WikiLinks]]`
- [ ] Home has no concatenated runbooks
- [ ] Each topic body is usable if Sources links 404
- [ ] Concrete facts match the project SSOT (model if present)
- [ ] No secrets
- [ ] ASCII filenames; wiki-root paths only in the publish clone
- [ ] British English unless the existing wiki uses another locale
- [ ] See also uses WikiLinks, not `#anchors` on Home as fake pages

## Fail (rewrite)

- Single `Home.md` dump
- Pages that only say "open the model"
- Invented topology or port maps
- Nested directories in `.wiki.git`
- Declared publish while wiki git still unprovisioned
- Treating https://github.com/skills as this workflow
