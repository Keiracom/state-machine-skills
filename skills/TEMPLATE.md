# Skill File Template

Use this template to create new skill files for additional phases.

```python
"""
Phase X: [Phase Name]

Brief description of what this phase covers.
"""

TASKS = {
    "X.1": {
        "title": "Task Title",
        "description": "What this task accomplishes.",
        "estimated_time": "10 minutes",
        "checks": [
            {
                "id": "X.1.1",
                "action": "What to do",
                "validation": "How to verify success",
                "type": "manual|command|http|code_review|ui",
                
                # Optional fields based on type:
                "command": "shell command to run",  # for type: command
                "key_files": ["path/to/file.ts"],   # for type: code_review
                "live_test": {                       # for type: http
                    "method": "GET|POST|PUT|DELETE",
                    "url": "{{API_URL}}/endpoint",
                    "headers": {"Authorization": "Bearer {{TOKEN}}"},
                    "body": {"key": "value"},
                    "expect": {"status": 200, "body_contains": ["field"]}
                },
                "steps": [                           # for type: ui or manual
                    "Step 1",
                    "Step 2"
                ]
            }
        ],
        "on_failure": "What to do if this fails",
        "dependencies": ["previous.task.id"]
    }
}


def get_instructions(task_id: str) -> str:
    """Generate markdown instructions for a task on-demand."""
    task = TASKS.get(task_id)
    if not task:
        return f"❌ Task {task_id} not found"
    
    # Build markdown from task dict
    lines = [f"# {task['title']}", "", task['description'], "", "## Checks"]
    
    for check in task.get('checks', []):
        lines.append(f"### [{check['id']}] {check['action']}")
        lines.append(f"- Validation: {check['validation']}")
        # Add more fields as needed
    
    return "\n".join(lines)


def get_task_ids() -> list:
    """Return all task IDs in this skill file."""
    return list(TASKS.keys())
```

## Naming Convention

- File: `phase_N_description.py` (e.g., `phase_4_deploy.py`)
- Task IDs: `N.X` where N is phase number (e.g., `4.1`, `4.2`)
- Check IDs: `N.X.Y` (e.g., `4.1.1`, `4.1.2`)

## Check Types

| Type | Use For | Key Fields |
|------|---------|------------|
| `manual` | Human verification | `steps` |
| `command` | Shell commands | `command` |
| `http` | API testing | `live_test` |
| `code_review` | File inspection | `key_files` |
| `ui` | Browser testing | `steps` |
| `filesystem` | File/dir checks | - |

## Variable Substitution

Use `{{VARIABLE}}` syntax in URLs, commands, etc. These are replaced at runtime from `config.json`:

- `{{API_URL}}` → `config.endpoints.api`
- `{{FRONTEND_URL}}` → `config.endpoints.frontend`
- `{{TEST_EMAIL}}` → `config.credentials.test_user.email`
- `{{AUTH_TOKEN}}` → Retrieved from auth flow
