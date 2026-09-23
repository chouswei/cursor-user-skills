# Model-to-ClickUp projection

ClickUp is used as a **progress projection** of the system model. The model (`.sysml`) remains the Single Source of Truth (SSOT) for architecture, identity, and allocation.

## Fundamental principles

1. **Identity inheritance**: The model owns the existence and identity of system components (parts, requirements, functions). ClickUp tasks are derived from these model elements.
2. **Progress sovereignty**: ClickUp owns the **progress** state (status, due dates, assignees, comments).
3. **No back-projection**: MUST NOT write progress data (statuses, ClickUp URLs, task IDs) back into `.sysml` files.
4. **Diff-before-write**: ALWAYS read the current task state using `clickup_get_task` or `clickup_filter_tasks` before sending an update. If the ClickUp state already matches the intended projection, skip the write.
5. **Write-class priority**: If multiple fields need updating, prioritise `status` updates before `description` updates.
6. **Description safety**: Description rewrites are **OFF** by default. Do not overwrite an existing task description unless explicitly requested or when creating a new task.
7. **Status vocabulary**: Use only the live statuses configured on the ClickUp list. MUST NOT invent status names.

## Mapping

| Model Element | ClickUp Projection | Projection Owner | Progress Owner |
|---------------|-------------------|------------------|----------------|
| Requirement   | Task              | Model            | ClickUp        |
| Part / Block  | Task or List      | Model            | ClickUp        |
| Task (SysML)  | Task              | Model            | ClickUp        |

## Standing facts

For project-specific facts (e.g. workspace IDs, default lists, sprint schedules), refer to the project-level `AGENTS.md`. This skill contains the **practice** of projection, not the project data.
