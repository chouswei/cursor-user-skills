# reasoning-strategy-selector

```
reasoning-strategy-selector/          # canonical: user-pack only (D1)
├── SKILL.md
├── Folder_Structure.md
├── assets/
│   └── selector-output-template.md
├── references/
│   ├── skill-graph.md                # schema, anchors, weights (source doc)
│   ├── skill-graph-seed.wire         # SINGLE SOURCE (D2) — @SKG/@SKL/@TRG/@EDG
│   ├── core-strategy-principles.md   # GENERATED audit view (not routing)
│   ├── routing-golden-set.toon       # labelled intents for score_routing.py
│   ├── routing-baseline.txt          # graph golden-set benchmark
│   ├── phase4-learning-loop.md       # deferred led_to_success protocol
│   ├── retrieval-corpus.md           # legacy retriever bullets
│   ├── related_skills.txt            # router subset ids
│   └── downstream-skills-index.md
└── tools/
    ├── skill_graph_lib.py            # parse, rank, validate
    ├── scan_skills_to_wire.py        # rebuild seed from SKILL.md scan
    ├── bootstrap_skill_graph.py      # sync views, MemNet emit
    ├── score_routing.py              # golden-set benchmark
    ├── strategy-retriever.py         # graph trigger helper (route_graph)
    ├── record_routing_success.py     # Phase 4 led_to_success edge formatter
    ├── sync_related_skills_from_txt.py
    └── validate_selector_pack.py
```

Repo `.cursor/skills/reasoning-strategy-selector/SKILL.md` is a **pointer** to this folder.
