# Core project-management principles (ClickUp)

Distilled from ClickUp PMO, *How to Improve Project Management Skills* (17 Sep 2024). Enforce these as behaviour on lists, tasks, statuses, assignees, and due dates. Do not paste the article.

## Lifecycle

Initiation -> planning -> execution -> close. Each phase is visible as **list statuses** plus dated tasks. A task with no owner and no due date is not yet committed work.

## Plan (realistic scope)

- **Objectives first.** Name the outcome in the parent task description; children are the work.
- **Optimism with a date.** Due dates come from stated capacity or a user-given constraint, not from hope. If unknown, ask once or set a review date and say so.
- **Breakdown.** Phases, deliverables, tasks, milestones. Use subtasks (`parent`) for the next level down, not a second informal tracker.
- **One owner.** Assign from live members. Multi-assignee only when the user asked for shared ownership.
- **Sequence.** If B cannot start until A finishes, `waiting_on` / `blocking` -- do not bury that in prose only.
- **Contingency.** Risks are named tasks or a dated comment, not silent buffers.

## Hygiene (monitor and adjust)

- **Read the board, then write.** Filter by list, status, assignee, and due-date range before proposing moves.
- **Stuck work is a status-time problem.** If a task sits in an active status, comment the blocker, then change status, owner, or due date.
- **Do not hide failure.** Closed means done or explicitly cancelled with a comment. Overdue stays overdue until the date or status changes for a stated reason.
- **Time is optional evidence.** `time_estimate` and time-tracking tools support capacity talk; they do not replace due dates.
- **Learn in place.** After a miss, comment the cause on the task or parent; fold the change into the next due date or dependency.

## Comms (kickoff and stakeholders)

- **Kickoff produces tasks.** Agenda and decisions may live in a Doc or comment; every follow-up is a named task with owner and due date.
- **Right people.** Resolve members before @mention or assign. Do not invite the whole workspace in a comment thread.
- **One channel per thread.** Task comments for that work item; Chat for the team channel the user named. Do not fork the same decision into both unless the user asked.
- **Feedback is work.** A request becomes a task or an assigned comment, not a chat-only aside.
- **Report from fields.** Stakeholder updates cite status, owner, and due date from ClickUp, not from memory.

## Skills the agent must exhibit

| Skill | Checkable behaviour |
|-------|---------------------|
| Problem-solving | Name the issue on the task; propose one next status or date |
| Leadership | Every committed task has an assignee |
| Decision-making | Record the call in a comment when status or scope changes |
| Time | Due date (and start_date when sequence matters) |
| Risk | Explicit risk task or dated comment |
| Resource | Assignee plus time_estimate when the user cares about load |
| Documentation | Description or Doc for objectives; comments for decisions |
| Tracking | Filter/search before "nothing is overdue" |
| Framework | Use the list's statuses; do not invent Agile/Waterfall boards |

## Out of MCP scope (practice only)

No verified user-clickup write tool for: Goals, Gantt **view**, Automations, Sprints, Dashboards, Forms, Portfolios, Brain, Whiteboards, Inbox.

| Article idea | Encode as |
|--------------|-----------|
| Goals / portfolios | Parent/objective task + description (optional `task_type` if it already exists) |
| Gantt | start_date, due_date, `clickup_add_task_dependency` |
| Automation | `clickup_create_reminder` and this skill's hygiene lane |
| Agile / Kanban | Existing list statuses; `clickup_filter_tasks` / `clickup_update_task` |
| Dashboards / KPI | Hygiene report from filter + time-in-status |
| Forms / feedback | Tasks or assigned comments |
| Brain | This agent summarises `clickup_get_task_comments` |
| Chat / Inbox | `clickup_get_chat_channels` + `clickup_send_chat_message`; task comments |
| Learning plan | Tasks on a list the user named, if they asked to track skills |

## Retrieval seeds

clickup, project management, status hygiene, kickoff, overdue, assignee, due date, stakeholder update, feedback loop, dependency, standup
