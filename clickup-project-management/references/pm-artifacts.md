# Recurring PM artifacts (ClickUp)

Distilled from *Claude Skills for Project Management* (9 Jul 2026). Procedure only: same headings every cycle, live ClickUp fields, owner + review date. Do not paste the article. Load this file for the **artifact** lane.

This skill plus **user-clickup** is the pair: the skill is how; MCP fetches and writes. A procedure that never re-reads the list goes stale while still looking well-formed -- worse than no procedure.

## Shared gates

- **One type per run** unless the user asked mixed.
- **Owner + review date** on the Doc or parent task (`assignees` + `due_date`).
- **Examples set the bar.** If the user supplied past briefs, last week's rollup, or a prior retro, match that structure. Else use the template below and say the bar is the template only.
- **Re-read statuses** with `clickup_get_list` this run. Do not reuse last-run status names.
- **Action items are tasks**, not bullets that die in a Doc.

## PRD / feature brief

**Trigger:** new PRD, feature brief, or initiative spec in ClickUp.

**Input:** problem statement. Optional: two or three past briefs the user names as the bar.

**Write:** `clickup_create_document` + `clickup_create_document_page` (or update pages). Create a parent task on the named list; put the Doc link in the task description. Children are the work.

**Headings (this order):**

1. Problem
2. Users and context
3. Scope in
4. Scope out
5. Success measures
6. Risks
7. Open questions
8. Work in ClickUp (parent + child task links)

**Critical seam:** without user-supplied examples the output is structurally correct and generic. Do not invent metrics the user did not give; leave Success measures as open questions instead.

## Weekly status rollup

**Trigger:** weekly status, Friday update, executive rollup from ClickUp.

**Input:** live tasks from `clickup_filter_tasks` on the named list (due range, statuses, assignees as needed). Paginate while `has_more`.

**Write:** comment on the parent/programme task, a Doc page, or `clickup_send_chat_message` on the channel the user named -- one place, not all three.

**Headings (this order):**

1. Status (moved, blocked, done -- each a task link)
2. Risks
3. Next steps (owner + due date)

Tone: short enough for an executive reader. Cite `[name](https://app.clickup.com/t/<id>)`. Do not pad.

**Critical seam:** the rollup is only as current as the read. MUST NOT polish a stale paste as this week's status when the list is readable. If user-clickup cannot read, say so in Blocked and stop, or use a user-labelled export and mark the report **export-sourced**.

This is where a **procedure** stops and an unsupervised **agent** would start: pulling data without a named list, then sending the rollup on a clock. This skill reads and shapes once per request.

## Retrospective

**Trigger:** sprint retro, retrospective summary, "what shipped / what slipped".

**Input:** raw notes (paste or meeting-notes-generator output). Light labels upstream help; unlabelled notes are allowed.

**Write:** Doc or parent-task comment with four headings. Each action item is `clickup_create_task` with assignee and due date.

**Headings (this order):**

1. What shipped
2. What slipped
3. Action items (task links, owner, due date)
4. Carry-over (still open from last cycle)

**Critical seam:** missing owners. Extract candidate actions, resolve people, then create tasks. If an owner is unknown after one resolve pass, ask once or assign `"me"` only when the user said so.

Same four headings every cycle so later retros compare.

## Retrieval seeds

PRD, feature brief, weekly status, rollup, retrospective, shipped, slipped, action item, executive update
