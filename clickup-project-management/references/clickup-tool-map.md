# ClickUp tool map (user-clickup)

Verified against namespace `user-clickup` at authoring time. Re-inspect schemas before write. Prefer dedicated `clickup_*` tools over `clickup_execute_operator`.

## Discover

| Need | Tool |
|------|------|
| Workspace tree | `clickup_get_workspace_hierarchy` (structure only) |
| List id, statuses | `clickup_get_list` |
| Members | `clickup_get_workspace_members`, `clickup_find_member_by_name`, `clickup_resolve_assignees` |
| Field filter | `clickup_filter_tasks` (status, list, assignee, due range, tags, custom fields) |
| Keyword search | `clickup_search` (paginate on `next_cursor`) |
| One task | `clickup_get_task` (`include` as needed; `expand_statuses=true` before status change) |
| Custom field ids | `clickup_get_custom_fields` then set via `clickup_update_task` `custom_fields` |

## Plan lane

| Practice | Tool |
|----------|------|
| New list (user asked) | `clickup_create_list` or `clickup_create_list_in_folder` (`clickup_get_folder` first) |
| New task | `clickup_create_task` (`name` + `list_id`; optional description, status, priority, dates, parent, tags, assignees, time_estimate, task_type) |
| Edit fields | `clickup_update_task` |
| Subtask | `clickup_create_task` with `parent` |
| Sequence | `clickup_add_task_dependency` (`waiting_on` \| `blocking`); remove with `clickup_remove_task_dependency` |
| Related not blocking | `clickup_add_task_link` |
| Tags (must already exist) | `clickup_create_task` `tags` or `clickup_add_tag_to_task` |
| Move list | `clickup_move_task` |

## Hygiene lane

| Practice | Tool |
|----------|------|
| Overdue / by status | `clickup_filter_tasks` (`due_date_to`, `statuses`, `assignees`, `include_closed`) |
| Time stuck | `clickup_get_task_time_in_status` (ClickApp "Total time in Status") |
| Bulk time in status | `clickup_get_bulk_tasks_time_in_status` |
| Clock | `clickup_start_time_tracking`, `clickup_stop_time_tracking`, `clickup_add_time_entry`, `clickup_get_current_time_entry` |
| Follow-up | `clickup_create_reminder` (title + due_date) |

`clickup_filter_tasks`: page while `has_more`; `assignees` are numeric ids.

## Comms lane

| Practice | Tool |
|----------|------|
| Comment / assigned comment | `clickup_create_comment` (`entity_type` + `entity_id`; `reply_to_id` for thread) |
| Read comments | `clickup_get_task_comments`; replies: `clickup_get_threaded_comments` |
| Edit/delete comment | `clickup_update_comment`, `clickup_delete_comment` |
| Chat | `clickup_get_chat_channels`, `clickup_send_chat_message`, `clickup_get_chat_channel_messages`, `clickup_get_chat_message_replies` |
| Doc record | `clickup_create_document`, `clickup_create_document_page`, `clickup_update_document_page`, `clickup_list_document_pages`, `clickup_get_document_pages` |
| File on task | `clickup_attach_task_file` / `clickup_request_attachment_upload` (user asked) |

Deprecated: `clickup_create_task_comment` -> `clickup_create_comment`.

## Artifact lane

| Practice | Tool |
|----------|------|
| PRD / brief record | `clickup_create_document`, `clickup_create_document_page`, `clickup_update_document_page` |
| Parent + child work | `clickup_create_task` (`parent` for children); Doc URL in description |
| Weekly rollup read | `clickup_filter_tasks` (paginate `has_more`); `clickup_get_task` as needed |
| Weekly rollup write | `clickup_create_comment` or Doc page or `clickup_send_chat_message` (one place) |
| Retro notes already in ClickUp | `clickup_get_task_comments` / `clickup_get_document_pages` |
| Retro actions | `clickup_create_task` with assignee + due_date |
| Review date on the artifact | `clickup_update_task` due_date + assignees on parent or reminder |

## Do not call for these article features

No write tool in this namespace for Goals, Gantt view, Automations, Sprints, Dashboards, Forms, Portfolios, Brain, Super Agents, Whiteboards, or Inbox. `clickup_search` may **find** docs, whiteboards, dashboards, chats, or forms; finding is not operating those surfaces.
