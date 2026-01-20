"""
Phase 1: Setup & Configuration

Skill file containing task definitions for the setup phase.
Each task has structured metadata and a get_instructions() function
for on-demand markdown generation.
"""

TASKS = {
    "1.1": {
        "title": "Initialize Project Structure",
        "description": "Create the basic project structure and verify all required directories exist.",
        "estimated_time": "5 minutes",
        "checks": [
            {
                "id": "1.1.1",
                "action": "Verify project root directory exists",
                "validation": "Directory should be accessible and writable",
                "type": "filesystem"
            },
            {
                "id": "1.1.2", 
                "action": "Check for package.json or equivalent config",
                "validation": "File should contain name, version, and dependencies",
                "type": "filesystem"
            },
            {
                "id": "1.1.3",
                "action": "Verify .gitignore is configured",
                "validation": "Should exclude node_modules, .env, and build artifacts",
                "type": "filesystem"
            }
        ],
        "on_failure": "Create missing files/directories as needed",
        "dependencies": []
    },
    
    "1.2": {
        "title": "Configure Environment Variables",
        "description": "Set up environment configuration for development and testing.",
        "estimated_time": "10 minutes",
        "checks": [
            {
                "id": "1.2.1",
                "action": "Create .env.example with all required variables",
                "validation": "Should list all env vars with placeholder values",
                "type": "filesystem"
            },
            {
                "id": "1.2.2",
                "action": "Verify .env is in .gitignore",
                "validation": ".env should never be committed",
                "type": "filesystem"
            },
            {
                "id": "1.2.3",
                "action": "Test environment variable loading",
                "validation": "Application should start without missing env errors",
                "type": "runtime"
            }
        ],
        "on_failure": "Document which variables are missing",
        "dependencies": ["1.1"]
    },
    
    "1.3": {
        "title": "Validate Dependencies",
        "description": "Ensure all project dependencies are installed and compatible.",
        "estimated_time": "5 minutes",
        "checks": [
            {
                "id": "1.3.1",
                "action": "Run dependency installation",
                "validation": "No errors during npm install / pip install",
                "type": "command",
                "command": "npm install"
            },
            {
                "id": "1.3.2",
                "action": "Check for security vulnerabilities",
                "validation": "No high/critical vulnerabilities",
                "type": "command",
                "command": "npm audit"
            },
            {
                "id": "1.3.3",
                "action": "Verify lock file is committed",
                "validation": "package-lock.json or equivalent exists in git",
                "type": "filesystem"
            }
        ],
        "on_failure": "Fix vulnerabilities or document exceptions",
        "dependencies": ["1.1"]
    }
}


def get_instructions(task_id: str) -> str:
    """
    Generate markdown instructions for a task on-demand.
    This keeps token usage minimal by only generating what's needed.
    """
    task = TASKS.get(task_id)
    if not task:
        return f"❌ Task {task_id} not found in phase_1_setup.py"
    
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
    
    if task.get('dependencies'):
        lines.append("")
        lines.append("## Dependencies")
        lines.append(f"Complete these first: {', '.join(task['dependencies'])}")
    
    if task.get('on_failure'):
        lines.append("")
        lines.append("## On Failure")
        lines.append(task['on_failure'])
    
    return "\n".join(lines)


def get_task_ids() -> list:
    """Return all task IDs in this skill file."""
    return list(TASKS.keys())


def get_task_summary(task_id: str) -> str:
    """Return a one-line summary for a task."""
    task = TASKS.get(task_id)
    if not task:
        return f"Task {task_id} not found"
    return f"{task_id}: {task['title']}"
