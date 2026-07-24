# New skill specification

**Skill name**  
(hyphen-case folder name)

**Primary pattern**  
(tool-wrapper | generator | reviewer | inversion | pipeline | generic)

**Target path**  
(e.g. `.cursor/skills/<skill-name>/` under the workspace root, or another `<pack-root>/<skill-name>/` the user chose)

**Rationale**  
- (bullet tied to first principles)
- (bullet)

**File tree**  
```
<skill-name>/
├── SKILL.md
└── ...
```

**SKILL.md**  
(full content)

**Other files**  
(For each path: `path` then content block.)

**Post-create notes**  
- (optional: register in reasoning-strategy-selector if routable)  
- (optional: skill.fish / skillfish — `add` / `submit` / `bundle`+`install`; see skillfish skill in repo; no fabricated repo URLs)

**Selector update snippets** (only if requested)  
- retrieval-corpus.md: (bullet line + optional seed line)  
- core-strategy-principles.md: (human summary line if needed)  
- related_skills.txt: (one new id line) then `python tools/sync_related_skills_from_txt.py`  
- downstream-skills-index.md: (id + hint row)  
- selector-output-template.md: (skill name in examples if needed)
