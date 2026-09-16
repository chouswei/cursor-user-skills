---
name: clickup-project-management
description: >-
  Run project-management practice in ClickUp: plan work, keep status hygiene,
  run stakeholder communication, and emit recurring artifacts (PRD or feature
  brief, weekly status rollup, retrospective) on lists, tasks, Docs, and comments.
  Pairs with user-clickup MCP for API calls; does not wrap those tools.
  Triggers: ClickUp project management, plan this in ClickUp, ClickUp status
  hygiene, overdue ClickUp tasks, ClickUp kickoff, stakeholder update in ClickUp,
  ClickUp standup, assign and due-date work, ClickUp feedback loop, ClickUp PRD,
  feature brief in ClickUp, weekly status rollup, ClickUp retrospective.
metadata:
  pattern: pipeline
  domain: project-management
  version: 1.1-clickup-pm
  secondary: "hybrid: writes via user-clickup MCP; complements project-planner and meeting-notes-generator"
pattern: pipeline
version: 1.1-clickup-pm

pipeline_steps:
  1. Classify lane
     - plan | hygiene | comms | artifact | mixed. Name the lane (and artifact type) before any write.
  2. Resolve ClickUp objects
     - List, valid statuses, assignees. Ask which list if missing. Read before write.
  3. Load practice
     - references/core-pm-principles.md then references/clickup-tool-map.md for that lane.
     - Artifact: also references/pm-artifacts.md.
  4. Apply
     - Create or update lists/tasks/comments/chat/docs using named user-clickup tools only.
  5. Self-review
     - Check MUST / MUST NOT; max one revision of the write set.
  6. Report
     - Fill assets/pm-output.md. Mention tasks as [name](https://app.clickup.com/t/<id>).

system_instruction: |
  Concise British English. PM practice, not an MCP wrapper. Inspect user-clickup
  schemas before first write this turn. Intermediate steps stay short. Final
  user-visible report matches assets/pm-output.md.

token_guardrails: |
  - Load core-pm-principles.md once per run; load clickup-tool-map.md for the active lane only.
  - Load pm-artifacts.md only for the artifact lane (or mixed that includes an artifact).
  - Do not paste ClickUp blog copy. Do not dump MCP schemas into the report.
---

# ClickUp project management

**Role:** Enforce project-management practice on ClickUp lists, tasks, statuses, assignees, due dates, and recurring PM artifacts.

**Pairing:** This skill is the **procedure** (how). **user-clickup** is the **connection** (`clickup_*` read/write). Inspect schemas before the first write; do not restate them here. Standing facts (sprint length, default list) live in the project's AGENTS.md -- inherit, do not copy. If `mcp-clickup` exists in the pack, load it for API conventions; do not duplicate it here. Product-roadmap interview: [project-planner](../project-planner/SKILL.md) first. Kickoff or retro minutes: [meeting-notes-generator](../meeting-notes-generator/SKILL.md) then action-item tasks here. New Agent Skill folder: [skill-creator](../skill-creator/SKILL.md), not this skill.

Sources distilled (do not paste): [How to Improve Project Management Skills](https://clickup.com/blog/how-to-improve-project-management-skills/) (ClickUp PMO Team, 17 Sep 2024); [Claude Skills for Project Management](https://clickup.com/blog/claude-skills-project-management/) (Praburam Srinivasan, 9 Jul 2026).

## When to use

User wants work **run in ClickUp**: plan a project, set owners and dates, clean statuses, run a kickoff, post a stakeholder update, close a feedback loop, or produce a **PRD / feature brief**, **weekly status rollup**, or **retrospective**.

## When not to use

- Inventree / DigiKey / SysML architecture -- those skills own those domains.
- "Wrap ClickUp MCP" or "add clickup_* tools" -- not this skill.
- "Write a new Agent Skill" -- [skill-creator](../skill-creator/SKILL.md).
- Features with no verified user-clickup tool (Goals, Gantt view, Automations, Sprints, Dashboards, Forms, Portfolios, Brain, Super Agents, Whiteboards, Inbox). Encode the **practice** on lists/tasks/comments/docs/chat instead.

## MUST

1. **Inspect then call.** `GetDynamicTools` on namespace `user-clickup` (or the live `clickup_*` schemas) before the first write this turn.
2. **Ask which list** before `clickup_create_task`. Resolve with `clickup_get_list` (`list_id` or `list_name`). Create a list only when the user asked (`clickup_create_list` or `clickup_create_list_in_folder`).
3. **Use live statuses.** Read configured statuses from `clickup_get_list` or `clickup_get_task` with `expand_statuses=true`. Pass those names to `clickup_update_task` / `clickup_create_task`.
4. **Resolve people.** `clickup_resolve_assignees` for names, emails, or `"me"` when IDs are required (filters, comment @mentions).
5. **Owner + date on committed work.** Every task that is meant to move has an assignee and a due date (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM`), unless the user forbids assignment.
6. **Dependencies as blocking links.** Sequence with `clickup_add_task_dependency` (`waiting_on` or `blocking`). Do not claim a Gantt chart API.
7. **Record decisions on the task.** Status changes, scope calls, and risks go in `clickup_create_comment` (Markdown). @mention as `[@Name](#user_mention#<numeric_user_id>)`.
8. **Mention tasks as links.** In user-facing text: `[Task name](https://app.clickup.com/t/<id>)`. Never a bare URL.
9. **Paginate reads.** `clickup_filter_tasks`: repeat while `has_more`. `clickup_search`: repeat while `next_cursor` is present.
10. **Live fields for rollups.** Weekly status and hygiene snapshots come from `clickup_filter_tasks` / `clickup_get_task` on the named list. A paste is current only when the user said it is the source.
11. **One artifact type.** PRD, weekly status, or retro -- one per run unless the user asked mixed. Owner + review date on the Doc or parent task.

## MUST NOT

- Invent ClickUp product surfaces or MCP tools that were not in the live `user-clickup` listing.
- Duplicate `mcp-clickup` or paste full `clickup_*` schemas into this skill.
- Set a status string that is not configured on that list.
- Create tasks without a `list_id`.
- Close or delete tasks to hide a problem; name the issue in a comment and set a checkable next status or due date.
- Commit API tokens or echo secrets.
- Use `clickup_create_task_comment` (deprecated; use `clickup_create_comment`).
- Treat a chat thread URL (`/v/cn/<channel>/t/<id>` or `/chat/r/<channel>/t/<id>`) as a task id; that trailing id is a chat message.
- Treat a pasted export as live board state when user-clickup can read the list.
- Merge a PRD, weekly rollup, and retro into one undifferentiated write.

## Pipeline

### 1. Classify lane

| Lane | User intent |
|------|-------------|
| **plan** | New work, kickoff setup, owners, dates, breakdown, dependencies |
| **hygiene** | Overdue, stuck, standup from ClickUp, monitor, time in status |
| **comms** | Stakeholder update, kickoff meeting actions, feedback, chat |
| **artifact** | PRD / feature brief, weekly status rollup, retrospective |
| **mixed** | Plan or artifact first, then hygiene or comms on the same list |

If two scans still leave the list, lane, or artifact type open, ask one bounded question; otherwise pick the checkable default and state it.

### 2. Resolve objects

1. List: user-supplied id/name, else `clickup_get_list` / `clickup_search` (`asset_types: ["task"]`) / `clickup_get_workspace_hierarchy` only when structure is required.
2. Statuses: from that list (step MUST 3).
3. People: `clickup_resolve_assignees`.
4. Existing work: `clickup_filter_tasks` (fields) or `clickup_search` (keywords). Prefer filter for status, assignee, due-date range.

### 3-4. Apply the lane

Load [references/core-pm-principles.md](references/core-pm-principles.md) and the matching rows in [references/clickup-tool-map.md](references/clickup-tool-map.md).

**plan:** Break objectives into tasks and subtasks (`parent` on `clickup_create_task`). Set name, markdown description, assignees, priority (`urgent` | `high` | `normal` | `low`), start_date, due_date, time_estimate (minutes as a string). Link sequence with `clickup_add_task_dependency`. Optional `task_type` only if that type already exists in the workspace.

**hygiene:** `clickup_filter_tasks` for overdue (`due_date_to` = today), unassigned, or named statuses. For a stuck task, `clickup_get_task_time_in_status` (requires ClickApp "Total time in Status"; if the tool errors, fall back to comments + dates). Update status, assignee, or due date; comment the reason.

**comms:** Action items become tasks. Narrative goes to `clickup_create_comment` or `clickup_send_chat_message` after `clickup_get_chat_channels`. Longer record: `clickup_create_document` then `clickup_create_document_page` / `clickup_update_document_page`. Personal follow-up: `clickup_create_reminder` (title + due_date).

**artifact:** Load [references/pm-artifacts.md](references/pm-artifacts.md). Write one type: PRD/brief (Doc + parent task), weekly status (live filter then comment/Doc/chat), or retrospective (notes then Doc/comment + action tasks).

### 5-6. Review and report

Fill [assets/pm-output.md](assets/pm-output.md). Every created or changed task is an inline markdown link.

## Resources

- [references/core-pm-principles.md](references/core-pm-principles.md)
- [references/clickup-tool-map.md](references/clickup-tool-map.md)
- [references/pm-artifacts.md](references/pm-artifacts.md)
- [assets/pm-output.md](assets/pm-output.md)
