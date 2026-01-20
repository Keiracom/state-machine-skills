"""
Phase 3: Testing & Validation

Skill file for final testing phase.
Demonstrates integration tests and sign-off checks.
"""

TASKS = {
    "3.1": {
        "title": "Run Full Test Suite",
        "description": "Execute all automated tests and verify passing status.",
        "estimated_time": "15 minutes",
        "checks": [
            {
                "id": "3.1.1",
                "action": "Run unit tests",
                "validation": "All unit tests pass",
                "type": "command",
                "command": "npm run test:unit"
            },
            {
                "id": "3.1.2",
                "action": "Run integration tests",
                "validation": "All integration tests pass",
                "type": "command",
                "command": "npm run test:integration"
            },
            {
                "id": "3.1.3",
                "action": "Check test coverage",
                "validation": "Coverage meets minimum threshold (80%)",
                "type": "command",
                "command": "npm run test:coverage"
            }
        ],
        "dependencies": ["2.4"]
    },
    
    "3.2": {
        "title": "Final Validation & Sign-off",
        "description": "Complete final checks and document any known issues.",
        "estimated_time": "10 minutes",
        "checks": [
            {
                "id": "3.2.1",
                "action": "Verify production build succeeds",
                "validation": "Build completes without warnings",
                "type": "command",
                "command": "npm run build"
            },
            {
                "id": "3.2.2",
                "action": "Review all completed tasks",
                "validation": "All task summaries are documented",
                "type": "manual",
                "steps": [
                    "Run: python tools/workflow.py history",
                    "Verify all tasks have completion summaries",
                    "Note any issues or follow-ups needed"
                ]
            },
            {
                "id": "3.2.3",
                "action": "Document known issues",
                "validation": "KNOWN_ISSUES.md is up to date",
                "type": "manual",
                "steps": [
                    "Create/update KNOWN_ISSUES.md",
                    "List any bugs or limitations discovered",
                    "Add workarounds if available"
                ]
            }
        ],
        "dependencies": ["3.1"]
    }
}


def get_instructions(task_id: str) -> str:
    """Generate markdown instructions for a task on-demand."""
    task = TASKS.get(task_id)
    if not task:
        return f"❌ Task {task_id} not found in phase_3_test.py"
    
    lines = [
        f"# {task['title']}",
        "",
        f"**Task ID:** {task_id}",
        f"**Estimated Time:** {task.get('estimated_time', 'Unknown')}",
        "",
        "## Description",
        task['description'],
        "",
        "## Checks",
    ]
    
    for check in task.get('checks', []):
        lines.append(f"")
        lines.append(f"### [{check['id']}] {check['action']}")
        lines.append(f"- **Type:** {check.get('type', 'manual')}")
        lines.append(f"- **Validation:** {check['validation']}")
        
        if check.get('command'):
            lines.append(f"- **Command:** `{check['command']}`")
        
        if check.get('steps'):
            lines.append(f"- **Steps:**")
            for i, step in enumerate(check['steps'], 1):
                lines.append(f"  {i}. {step}")
    
    if task.get('dependencies'):
        lines.append("")
        lines.append("## Dependencies")
        lines.append(f"Complete these first: {', '.join(task['dependencies'])}")
    
    return "\n".join(lines)


def get_task_ids() -> list:
    """Return all task IDs in this skill file."""
    return list(TASKS.keys())
