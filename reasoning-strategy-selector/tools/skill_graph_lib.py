"""
Shared skill-graph wire parse, scan, rank, and view generation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


SKILL_ROOT = Path(__file__).resolve().parent.parent
USER_PACK = SKILL_ROOT.parent
SEED_PATH = SKILL_ROOT / "references" / "skill-graph-seed.wire"

TYPED_RELATIONS = {
    "precedes",
    "complements",
    "default_stack",
    "specializes",
    "requires",
    "conflicts_with",
    "led_to_success",
}

EDGE_WEIGHTS = {
    "triggers": 1.0,
    "precedes": 0.8,
    "default_stack": 0.7,
    "complements": 0.5,
    "specializes": 0.4,
    "shares_domain": 0.2,
    "led_to_success": 0.6,
    "requires": 0.6,
}

FEATURE_MAP: Dict[str, Tuple[str, str, str, str, str, str]] = {
    "scientific-method-first-principles": ("P", "user", "high", "high", "measured", "medium"),
    "empirical-paradox-synthesis": ("P", "user", "high", "high", "measured", "high"),
    "control-theory-planner": ("P", "user", "high", "high", "conceptual", "low"),
    "mcdm-decider": ("P", "user", "high", "high", "measured", "medium"),
    "optimization-planner": ("P", "user", "high", "high", "measured", "low"),
    "project-planner": ("G", "user", "medium", "high", "structural", "low"),
    "risk-assessor": ("R", "user", "medium", "high", "measured", "low"),
    "launch-readiness-assessor": ("R", "user", "medium", "high", "structural", "low"),
    "decision-inverter": ("R", "user", "high", "high", "conceptual", "high"),
    "code-reviewer": ("R", "user", "medium", "medium", "structural", "low"),
    "pr-reviewer": ("R", "user", "medium", "medium", "structural", "low"),
    "architecture-reviewer": ("R", "user", "high", "high", "structural", "medium"),
    "security-reviewer": ("R", "user", "high", "high", "structural", "low"),
    "incentive-alignment-reviewer": ("R", "user", "high", "high", "conceptual", "high"),
    "skill-creator": ("G", "meta", "high", "low", "structural", "low"),
    "skill-reviewer": ("R", "meta", "high", "low", "structural", "low"),
    "skillfish": ("T", "meta", "low", "low", "structural", "low"),
    "academic-report-generator": ("G", "doc", "medium", "low", "structural", "low"),
    "tech-report-generator": ("G", "doc", "medium", "low", "structural", "low"),
    "tech-report-reviewer": ("R", "doc", "medium", "low", "structural", "low"),
    "rfc-generator": ("G", "doc", "medium", "low", "structural", "low"),
    "adr-generator": ("G", "doc", "low", "low", "structural", "low"),
    "commit-message-generator": ("G", "doc", "low", "low", "structural", "low"),
    "meeting-notes-generator": ("G", "doc", "low", "low", "structural", "low"),
    "toon-prompt-format": ("T", "doc", "medium", "low", "structural", "low"),
    "tron-format": ("T", "doc", "medium", "low", "structural", "low"),
    "pandas-expert": ("T", "user", "medium", "low", "structural", "low"),
    "mdtohtml": ("T", "doc", "low", "low", "structural", "low"),
    "engineering-practices-learner": ("P", "user", "high", "low", "structural", "low"),
    "sysml-modeling-workflow": ("P", "sysml", "high", "medium", "structural", "low"),
    "sysml-modeling-session-checklist": ("P", "sysml", "medium", "medium", "structural", "low"),
    "sysml-view-doc-sync": ("R", "sysml", "medium", "medium", "structural", "low"),
    "mcp-sysml-v2": ("T", "sysml-tool", "medium", "low", "structural", "low"),
    "mcp-sysmledgraph": ("T", "sysml-tool", "high", "low", "structural", "low"),
    "sysml-refactorer": ("P", "sysml", "high", "high", "structural", "low"),
    "sysml-new-project": ("G", "sysml", "medium", "medium", "structural", "low"),
    "sysml-memnet-documentation": ("P", "sysml", "high", "medium", "structural", "low"),
    "hardware-custom-pcba-workflow": ("P", "pcba", "high", "high", "structural", "low"),
    "pcba-netlist-reader": ("T", "pcba", "medium", "low", "structural", "low"),
    "pcba-design-reviewer": ("R", "pcba", "high", "high", "structural", "low"),
    "mermaid": ("G", "doc", "medium", "low", "structural", "low"),
    "mmdc": ("T", "doc", "low", "low", "structural", "low"),
    "md-to-tex": ("P", "doc", "medium", "low", "structural", "low"),
    "reasoning-strategy-selector": ("P", "meta", "medium", "low", "structural", "low"),
}

DOMAIN_HUBS = {
    "sysml": "sysml-modeling-workflow",
    "sysml-tool": "mcp-sysml-v2",
    "user": "scientific-method-first-principles",
    "doc": "tech-report-generator",
    "meta": "skill-creator",
    "pcba": "pcba-design-reviewer",
    "coding": "code-reviewer",
}

MANUAL_PRECEDES = [
    ("sysml-modeling-session-checklist", "sysml-modeling-workflow"),
    ("sysml-modeling-workflow", "sysml-memnet-documentation"),
    ("sysml-memnet-documentation", "sysml-view-doc-sync"),
    ("sysml-memnet-documentation", "mermaid"),
    ("sysml-new-project", "sysml-modeling-workflow"),
    ("decision-inverter", "risk-assessor"),
    ("scientific-method-first-principles", "empirical-paradox-synthesis"),
    ("tech-report-generator", "tech-report-reviewer"),
    ("rfc-generator", "adr-generator"),
]

MANUAL_COMPLEMENTS = [
    ("decision-inverter", "risk-assessor"),
    ("decision-inverter", "launch-readiness-assessor"),
    ("mcdm-decider", "optimization-planner"),
    ("scientific-method-first-principles", "empirical-paradox-synthesis"),
    ("pcba-netlist-reader", "pcba-design-reviewer"),
    ("code-reviewer", "pr-reviewer"),
    ("sysml-refactorer", "sysml-modeling-workflow"),
    ("skill-creator", "skill-reviewer"),
    ("mermaid", "sysml-memnet-documentation"),
    ("mermaid", "sysml-view-doc-sync"),
    ("tron-format", "mermaid"),
    ("sysml-view-doc-sync", "mermaid"),
]

# SKG_global default_stack targets (hub entry per domain)
SKG_DEFAULT_STACKS = [
    "sysml-modeling-workflow",
    "scientific-method-first-principles",
    "skill-creator",
    "pcba-design-reviewer",
    "mermaid",
    "mcp-sysml-v2",
    "sysml-memnet-documentation",
    "tech-report-generator",
    "mcdm-decider",
]

MANUAL_REQUIRES = [
    ("sysml-view-doc-sync", "sysml-modeling-workflow"),
    ("sysml-refactorer", "sysml-modeling-workflow"),
]

PATTERN_MAP = {
    "generator": "G",
    "reviewer": "R",
    "pipeline": "P",
    "tool-wrapper": "T",
    "tool": "T",
}


@dataclass
class SkillNode:
    id: str
    pack: str
    pattern: str
    dir: str
    domain: str
    cx: str
    stakes: str
    ev: str
    tension: str
    path: str
    recycle: str = "persistent"


@dataclass
class TriggerNode:
    id: str
    phrase: str
    recycle: str = "persistent"


@dataclass
class Edge:
    id: str
    src: str
    relation: str
    dst: str
    note: str
    recycle: str = "persistent"


@dataclass
class SkillGraph:
    version: str = "1"
    skills: Dict[str, SkillNode] = field(default_factory=dict)
    triggers: Dict[str, TriggerNode] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    trigger_to_skill: Dict[str, str] = field(default_factory=dict)
    adjacency: Dict[str, List[Tuple[str, str, int]]] = field(default_factory=dict)

    def rebuild_adjacency(self) -> None:
        self.adjacency.clear()
        for e in self.edges:
            self.adjacency.setdefault(e.src, []).append((e.dst, e.relation, 1))
            if e.relation in ("complements", "shares_domain"):
                self.adjacency.setdefault(e.dst, []).append((e.src, e.relation, 1))


def _parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    data: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip()
    return data


def _extract_triggers(description: str) -> List[str]:
    if not description:
        return []
    m = re.search(r"Triggers:\s*(.+?)(?:\.\s*Skip:|$)", description, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    chunk = m.group(1).replace("\n", " ")
    parts = re.split(r"[,;]\s*", chunk)
    out = []
    for p in parts:
        p = p.strip().strip(".")
        if len(p) >= 3:
            out.append(p[:80])
    return out[:6]


def _infer_domain(skill_id: str, domain_meta: str) -> str:
    if domain_meta:
        d = domain_meta.split(",")[0].strip()
        if d in ("sysml", "pcba", "doc", "meta", "user", "coding"):
            return d
    if skill_id.startswith("sysml-"):
        return "sysml"
    if skill_id.startswith("mcp-sysml") or skill_id == "sysml-v2-syntax-reference":
        return "sysml-tool"
    if skill_id.startswith("pcba-") or "pcba" in skill_id:
        return "pcba"
    if skill_id.startswith("mcp-") or skill_id in ("mmdc", "mdtohtml", "memnet-format"):
        return "doc" if "mermaid" in skill_id or skill_id in ("mmdc", "mdtohtml") else "meta"
    if skill_id.endswith("-generator") or skill_id.endswith("-reviewer"):
        return "doc" if "report" in skill_id or skill_id in ("rfc-generator", "adr-generator") else "user"
    return "user"


def _infer_pattern(skill_id: str, pattern_meta: str) -> str:
    if pattern_meta:
        p = PATTERN_MAP.get(pattern_meta.lower(), pattern_meta.upper()[:1])
        if p in "GRPT":
            return p
    if skill_id.startswith("mcp-") or skill_id in ("mmdc", "mdtohtml", "skillfish"):
        return "T"
    if "workflow" in skill_id or skill_id.endswith("-learner") or "selector" in skill_id:
        return "P"
    if skill_id.endswith("-reviewer") or skill_id.endswith("-reviewer"):
        return "R"
    if skill_id.endswith("-generator") or skill_id.startswith("sysml-") and "generator" in skill_id:
        return "G"
    if skill_id.endswith("-reviewer"):
        return "R"
    if "reviewer" in skill_id or skill_id.endswith("-audit"):
        return "R"
    if "generator" in skill_id:
        return "G"
    return "G"


def scan_skill_folder(skill_id: str, skill_path: Path, pack: str) -> Tuple[SkillNode, List[str]]:
    text = skill_path.read_text(encoding="utf-8", errors="replace")
    fm = _parse_frontmatter(text)
    desc = fm.get("description", "").strip("'\"")
    pattern_meta = ""
    domain_meta = ""
    meta_block = re.search(r"metadata:\s*\n((?:  .+\n)+)", text)
    if meta_block:
        for line in meta_block.group(1).splitlines():
            if "pattern:" in line:
                pattern_meta = line.split(":", 1)[1].strip()
            if "domain:" in line:
                domain_meta = line.split(":", 1)[1].strip()

    feats = FEATURE_MAP.get(skill_id)
    if feats:
        dir_, domain, cx, stakes, ev, tension = feats
        pattern = dir_
    else:
        pattern = _infer_pattern(skill_id, pattern_meta)
        domain = _infer_domain(skill_id, domain_meta)
        cx, stakes, ev, tension = "medium", "medium", "structural", "low"
        dir_ = pattern

    node = SkillNode(
        id=skill_id,
        pack=pack,
        pattern=pattern,
        dir=dir_,
        domain=domain,
        cx=cx,
        stakes=stakes,
        ev=ev,
        tension=tension,
        path=str(skill_path.parent).replace("\\", "/"),
    )
    triggers = _extract_triggers(desc)
    if not triggers:
        triggers = [skill_id.replace("-", " "), skill_id.split("-")[0]]
    return node, triggers


def discover_skills(extra_repo_paths: Optional[List[Path]] = None) -> Dict[str, Tuple[SkillNode, List[str]]]:
    found: Dict[str, Tuple[SkillNode, List[str]]] = {}
    skip = {"reasoning-strategy-selector"}  # router not in routable graph

    for child in sorted(USER_PACK.iterdir()):
        if not child.is_dir():
            continue
        sid = child.name
        skill_md = child / "SKILL.md"
        if not skill_md.is_file() or sid in skip:
            continue
        found[sid] = scan_skill_folder(sid, skill_md, "user")

    if extra_repo_paths:
        for repo_skills in extra_repo_paths:
            if not repo_skills.is_dir():
                continue
            for child in sorted(repo_skills.iterdir()):
                if not child.is_dir() or child.name in found or child.name in skip:
                    continue
                skill_md = child / "SKILL.md"
                if skill_md.is_file():
                    found[child.name] = scan_skill_folder(child.name, skill_md, "repo")
    return found


def build_seed_wire(discovered: Dict[str, Tuple[SkillNode, List[str]]]) -> SkillGraph:
    g = SkillGraph(version="1")
    lines_edges: List[Edge] = []
    edge_n = 0

    for sid, (node, triggers) in discovered.items():
        g.skills[sid] = node
        seen_phrases: Set[str] = set()
        trg_ids: List[str] = []
        for i, phrase in enumerate(triggers[:4]):
            key = phrase.lower()
            if key in seen_phrases:
                continue
            seen_phrases.add(key)
            tid = f"TRG_{sid}_{i}"
            g.triggers[tid] = TriggerNode(id=tid, phrase=phrase)
            g.trigger_to_skill[tid] = sid
            trg_ids.append(tid)
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", tid, "triggers", sid, phrase[:40]))

        # Pad to ≥2 triggers
        while len(trg_ids) < 2:
            tid = f"TRG_{sid}_pad{len(trg_ids)}"
            phrase = f"{sid.replace('-', ' ')} skill"
            g.triggers[tid] = TriggerNode(id=tid, phrase=phrase)
            g.trigger_to_skill[tid] = sid
            trg_ids.append(tid)
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", tid, "triggers", sid, "pad"))

    # SKG + default stacks
    for hub in SKG_DEFAULT_STACKS:
        if hub in g.skills:
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", "SKG_global", "default_stack", hub, "domain hub"))

    for a, b in MANUAL_PRECEDES:
        if a in g.skills and b in g.skills:
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", a, "precedes", b, "manual"))
    for a, b in MANUAL_COMPLEMENTS:
        if a in g.skills and b in g.skills:
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", a, "complements", b, "manual"))
    for a, b in MANUAL_REQUIRES:
        if a in g.skills and b in g.skills:
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", a, "requires", b, "manual"))

    # Domain specializes from hub
    for sid, node in g.skills.items():
        hub = DOMAIN_HUBS.get(node.domain)
        if hub and hub in g.skills and sid != hub:
            edge_n += 1
            lines_edges.append(Edge(f"E{edge_n:04d}", hub, "specializes", sid, node.domain))

    g.edges = lines_edges
    g.rebuild_adjacency()
    return g


def graph_to_wire_lines(g: SkillGraph) -> List[str]:
    out = [
        "# skill-graph-seed.wire — single source (D2). Regenerate via scan_skills_to_wire.py",
        f"@SKG: SKG_global|{g.version}|user_pack|persistent",
    ]
    for sid in sorted(g.skills):
        n = g.skills[sid]
        out.append(
            f"@SKL: {n.id}|{n.pack}|{n.pattern}|{n.dir}|{n.domain}|{n.cx}|{n.stakes}|{n.ev}|{n.tension}|{n.path}|{n.recycle}"
        )
    for tid in sorted(g.triggers):
        t = g.triggers[tid]
        out.append(f"@TRG: {t.id}|{t.phrase}|{t.recycle}")
    for e in g.edges:
        out.append(f"@EDG: {e.id}|{e.src}|{e.relation}|{e.dst}|{e.note}|{e.recycle}")
    return out


def parse_wire_file(path: Path) -> SkillGraph:
    g = SkillGraph()
    if not path.is_file():
        return g
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@SKG:"):
            parts = line.split(":", 1)[1].strip().split("|")
            if len(parts) >= 2:
                g.version = parts[1]
        elif line.startswith("@SKL:"):
            p = line.split(":", 1)[1].strip().split("|")
            if len(p) >= 10:
                g.skills[p[0]] = SkillNode(*p[:10], p[10] if len(p) > 10 else "persistent")
        elif line.startswith("@TRG:"):
            p = line.split(":", 1)[1].strip().split("|")
            if len(p) >= 2:
                g.triggers[p[0]] = TriggerNode(p[0], p[1], p[2] if len(p) > 2 else "persistent")
        elif line.startswith("@EDG:"):
            p = line.split(":", 1)[1].strip().split("|")
            if len(p) >= 5:
                e = Edge(p[0], p[1], p[2], p[3], p[4], p[5] if len(p) > 5 else "persistent")
                g.edges.append(e)
                if e.relation == "triggers":
                    g.trigger_to_skill[e.src] = e.dst
    g.rebuild_adjacency()
    return g


def extract_query_features(intent: str) -> dict:
    il = intent.lower()
    domain = "user"
    if any(k in il for k in ("sysml", "model", "deploy", "requirement", "part", "port", "behaviour")):
        domain = "sysml"
    elif any(k in il for k in ("pcba", "netlist", "eagle", "kicad", "circuit", "board")):
        domain = "pcba"
    elif any(k in il for k in ("mermaid", "latex", "report", "markdown", "rfc", "adr", "doc")):
        domain = "doc"
    elif any(k in il for k in ("skill", "routing", "meta", "mcp")):
        domain = "meta"

    direction = "G"
    if any(k in il for k in ("review", "audit", "check", "verify", "critique", "assess")):
        direction = "R"
    elif any(k in il for k in ("workflow", "refactor", "pipeline", "orchestrat", "multi-step")):
        direction = "P"
    elif any(k in il for k in ("mcp", "cli", "parse", "render", "tool")):
        direction = "T"

    return {
        "dir": direction,
        "domain": domain,
        "cx": "high" if any(k in il for k in ("complex", "cross-file", "refactor")) else "medium",
        "stakes": "high" if any(k in il for k in ("critical", "must", "safety", "mission")) else "medium",
        "ev": "measured" if any(k in il for k in ("data", "empirical", "test")) else "structural",
        "tension": "high" if any(k in il for k in ("paradox", "tension", "conflict", "ambiguous")) else "low",
    }


KEYWORD_DIRECT: List[Tuple[List[str], str, float]] = [
    (["cross-file", "refactor"], "sysml-refactorer", 2.0),
    (["sysml", "refactor"], "sysml-refactorer", 1.8),
    (["new", "sysml", "project"], "sysml-new-project", 2.0),
    (["scaffold", "sysml"], "sysml-new-project", 1.5),
    (["requirements", "audit"], "sysml-requirements-audit", 2.0),
    (["mermaid", "diagram"], "mermaid", 2.0),
    (["mermaid", "placement"], "mermaid", 2.0),
    (["interconnection", "mermaid"], "mermaid", 1.9),
    (["interconnection", "mermaid", "placement"], "sysml-interconnection-mermaid", 2.3),
    (["interconnection", "mermaid"], "sysml-interconnection-mermaid", 1.9),
    (["interconnection", "view"], "sysml-interconnection-mermaid", 2.0),
    (["memnet", "placement"], "sysml-memnet-documentation", 1.9),
    (["TSK", "diagram"], "sysml-memnet-documentation", 1.8),
    (["DiagramPlan"], "sysml-interconnection-mermaid", 2.0),
    (["block diagram"], "mermaid", 1.8),
    (["validate", "sysml"], "mcp-sysml-v2", 2.0),
    (["parse", "diagnostic"], "mcp-sysml-v2", 1.5),
    (["memnet", "query"], "sysml-memnet-documentation", 2.0),
    (["memnet", "warm"], "sysml-memnet-documentation", 2.0),
    (["goldfish", "loop"], "sysml-memnet-documentation", 1.8),
    (["design", "memory"], "sysml-memnet-documentation", 1.5),
    (["memnet"], "mcp-memnet", 1.0),
    (["technical report"], "tech-report-generator", 2.0),
    (["white paper"], "tech-report-generator", 1.8),
    (["rfc"], "rfc-generator", 2.0),
    (["adr"], "adr-generator", 1.5),
    (["skill", "skill.md"], "skill-creator", 1.8),
    (["premortem", "blind spot"], "decision-inverter", 1.8),
    (["scientific method", "hypothesis"], "scientific-method-first-principles", 1.5),
    (["empirical paradox", "measured tradeoff"], "empirical-paradox-synthesis", 1.5),
    (["eagle", "netlist"], "pcba-netlist-reader", 1.8),
    (["pcba", "review"], "pcba-design-reviewer", 2.0),
]


def match_triggers(intent: str, g: SkillGraph) -> List[Tuple[str, float]]:
    il = intent.lower()
    best: Dict[str, float] = {}

    for tid, t in g.triggers.items():
        phrase = t.phrase.lower()
        sid = g.trigger_to_skill.get(tid, "")
        if not sid:
            continue
        score = 0.0
        if phrase in il:
            score = 1.2
        else:
            tokens = [tok for tok in re.findall(r"[a-z0-9][a-z0-9_-]{2,}", phrase) if len(tok) > 3]
            if tokens and sum(1 for tok in tokens if tok in il) >= max(1, len(tokens) // 2):
                score = 0.9
        if score:
            best[sid] = max(best.get(sid, 0), score)

    for keywords, sid, boost in KEYWORD_DIRECT:
        if sid in g.skills and all(k in il for k in keywords):
            best[sid] = max(best.get(sid, 0), boost)

    return sorted(best.items(), key=lambda x: -x[1])


def traverse_candidates(seed_ids: List[Tuple[str, float]], g: SkillGraph, max_hops: int = 2) -> Dict[str, Tuple[float, List[str]]]:
    """Traverse from seeds; neighbours score from edges only (not full trigger boost)."""
    scores: Dict[str, Tuple[float, List[str]]] = {}
    for sid, trig_score in seed_ids:
        if sid in g.skills:
            scores[sid] = (max(scores.get(sid, (0, []))[0], trig_score), [sid])
        queue = [(sid, 0, [sid])]
        while queue:
            cur, hop, path = queue.pop(0)
            if hop >= max_hops:
                continue
            for nxt, rel, _ in g.adjacency.get(cur, []):
                if nxt not in g.skills:
                    continue
                w = EDGE_WEIGHTS.get(rel, 0.1)
                penalty = 0.15 * (hop + 1)
                nxt_score = w - penalty
                prev, pth = scores.get(nxt, (0, []))
                if nxt_score > prev:
                    scores[nxt] = (nxt_score, path + [nxt])
                queue.append((nxt, hop + 1, path + [nxt]))
    return scores


DIRECT_PIN_THRESHOLD = 1.5


def route_graph(intent: str, g: SkillGraph, threshold: float = 0.55, top_n: int = 3) -> Tuple[List[str], List[str], Dict[str, float]]:
    qf = extract_query_features(intent)
    triggers = match_triggers(intent, g)
    if triggers:
        seed = triggers
    else:
        hub = DOMAIN_HUBS.get(qf["domain"], "scientific-method-first-principles")
        seed = [(hub, 0.7)]

    raw = traverse_candidates(seed, g)
    ranked: List[Tuple[str, float, List[str]]] = []
    for sid, (sc, path) in raw.items():
        if sid not in g.skills or sid == "reasoning-strategy-selector":
            continue
        ranked.append((sid, sc, path))
    ranked.sort(key=lambda x: -x[1])

    # Empirical boost from led_to_success edges (Phase 4)
    empirical: Dict[str, float] = {}
    for e in g.edges:
        if e.relation == "led_to_success" and e.dst in g.skills:
            empirical[e.dst] = empirical.get(e.dst, 0) + EDGE_WEIGHTS["led_to_success"]

    ranked = [(sid, sc + empirical.get(sid, 0), path) for sid, sc, path in ranked]
    ranked.sort(key=lambda x: -x[1])

    order: List[str] = []
    if triggers and triggers[0][1] >= DIRECT_PIN_THRESHOLD:
        order.append(triggers[0][0])
    for sid, sc, _ in ranked:
        if sid not in order and sc >= threshold:
            order.append(sid)
    order = order[:top_n]

    rationale_path = ranked[0][2] if ranked else []
    if triggers and triggers[0][0] in g.skills:
        rationale_path = [triggers[0][0]] + [s for s in rationale_path if s != triggers[0][0]]
    feature_scores = {sid: round(sc, 3) for sid, sc, _ in ranked[:5]}
    if triggers:
        feature_scores[triggers[0][0]] = round(triggers[0][1], 3)
    return order, rationale_path, feature_scores


def validate_density(g: SkillGraph) -> List[str]:
    errors: List[str] = []
    typed_by_dst: Dict[str, Set[str]] = {sid: set() for sid in g.skills}
    trg_count: Dict[str, int] = {sid: 0 for sid in g.skills}

    for e in g.edges:
        if e.relation == "triggers" and e.dst in trg_count:
            trg_count[e.dst] += 1
        if e.relation in TYPED_RELATIONS and e.dst in typed_by_dst:
            typed_by_dst[e.dst].add(e.relation)
        if e.relation in TYPED_RELATIONS and e.src in g.skills and e.relation != "led_to_success":
            typed_by_dst.setdefault(e.src, set()).add(e.relation)

    for sid in g.skills:
        if trg_count.get(sid, 0) < 2:
            errors.append(f"{sid}: fewer than 2 triggers ({trg_count.get(sid, 0)})")
        if not typed_by_dst.get(sid):
            errors.append(f"{sid}: no typed edge (precedes/complements/default_stack/specializes/requires)")
    return errors
