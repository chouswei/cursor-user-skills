# Roles

Roles are duties. Model families live only in User Rules **Model by role**. Resolve the newest listed slug for that family and tier; if the preferred tier is missing, use the newest family slug on the session allowlist and name the gap.

MUST NOT pin a nickname (`Opus`, `Luna`) as a role. MUST NOT use Cursor `subagent_type` values (`explore`, `bugbot`) as house roles.

| Role | Does | MUST NOT | Who runs it |
|------|------|----------|-------------|
| Architect | Thin root plan: purpose, constraints, approach, path/qname pointers. Complex root plan or complex diagnosis only. | Emit atoms, waves, patches, file bodies, skill stacks, `.sysml` bodies. | Worker. Parent sends pointers only. |
| Bind | Catch Architect (or write a normal plan). Fill detail. Emit atom cards with `wave`, `order`, `role`, disjoint scopes, proof. | Implement, deploy, or spawn Task itself. | Grok parent, else one Bind worker that returns cards and stops. |
| Diagnose | Name cause and a checkable proof. | Implement or emit execute atoms. | Worker unless parent is Grok and the diagnosis is small. Then Bind. |
| Implement | Change one bound atom. Run that atom's proof command. | Plan, diagnose, deploy, edit outside `scope.paths` / `scope.qnames`. | One worker per atom. |
| Deploy | Ship a committed change to the live host, verify, state rollback. | Author the change. Treat local tests as deploy proof. | Own wave/atom after Implement proof. |
| Web | Live web or library docs for one question. | Edit the repo. | Worker when Bind tagged Web. |
| Visual | Visual review of named artefacts. | Implement. | Worker when needed. |
| Prose | Author named prose. | Redesign architecture. | Worker when needed. |
| Unclear | Bound question or route when two scans fail. | Invent a specialist. | Parent or Grok worker. |

Architect input: problem, constraints, path/qname pointers. Architect output: purpose, constraints, approach, path/qname pointers.

Review roles (Visual, Web, Prose, Unclear) only when Bind tags them or the user asks.

## Parent vs worker

- Parent coordinates even when Bind is on parent.
- MUST NOT bundle Bind + Implement in one worker or one Task prompt.
- MUST NOT give Implement a root plan, a diagnosis, a bundled sequential job, live deploy, visual review, or web search.
- Fallback when a role's family is off the allowlist: name the gap, pick the next live listed slug, continue. MUST NOT stall.
