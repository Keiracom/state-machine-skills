"""
Phase 2: Core Implementation

Skill file for main build tasks.
Demonstrates more complex task structures with live tests and API calls.
"""

TASKS = {
    "2.1": {
        "title": "Implement User Authentication",
        "description": "Set up user authentication flow including login, logout, and session management.",
        "estimated_time": "30 minutes",
        "checks": [
            {
                "id": "2.1.1",
                "action": "Verify auth endpoint exists",
                "validation": "POST /api/auth/login returns 200 with valid credentials",
                "type": "http",
                "live_test": {
                    "method": "POST",
                    "url": "{{API_URL}}/api/auth/login",
                    "body": {"email": "{{TEST_EMAIL}}", "password": "{{TEST_PASSWORD}}"},
                    "expect": {"status": 200, "body_contains": ["token"]}
                }
            },
            {
                "id": "2.1.2",
                "action": "Test invalid credentials rejection",
                "validation": "POST /api/auth/login returns 401 with invalid credentials",
                "type": "http",
                "live_test": {
                    "method": "POST",
                    "url": "{{API_URL}}/api/auth/login",
                    "body": {"email": "wrong@test.com", "password": "wrongpass"},
                    "expect": {"status": 401}
                }
            },
            {
                "id": "2.1.3",
                "action": "Verify JWT token structure",
                "validation": "Token should be valid JWT with user ID claim",
                "type": "code_review",
                "key_files": ["src/auth/jwt.ts", "src/middleware/auth.ts"]
            }
        ],
        "dependencies": ["1.3"]
    },
    
    "2.2": {
        "title": "Build Data Models",
        "description": "Create database models and migrations for core entities.",
        "estimated_time": "20 minutes",
        "checks": [
            {
                "id": "2.2.1",
                "action": "Review model definitions",
                "validation": "Models should have proper types and relationships",
                "type": "code_review",
                "key_files": ["src/models/", "prisma/schema.prisma"]
            },
            {
                "id": "2.2.2",
                "action": "Run database migrations",
                "validation": "Migrations apply without errors",
                "type": "command",
                "command": "npx prisma migrate dev"
            },
            {
                "id": "2.2.3",
                "action": "Verify seed data loads",
                "validation": "Seed script creates test data successfully",
                "type": "command",
                "command": "npx prisma db seed"
            }
        ],
        "dependencies": ["1.2", "1.3"]
    },
    
    "2.3": {
        "title": "Implement API Endpoints",
        "description": "Create REST API endpoints for CRUD operations.",
        "estimated_time": "45 minutes",
        "checks": [
            {
                "id": "2.3.1",
                "action": "GET /api/items returns list",
                "validation": "Returns 200 with array of items",
                "type": "http",
                "live_test": {
                    "method": "GET",
                    "url": "{{API_URL}}/api/items",
                    "headers": {"Authorization": "Bearer {{AUTH_TOKEN}}"},
                    "expect": {"status": 200, "body_type": "array"}
                }
            },
            {
                "id": "2.3.2",
                "action": "POST /api/items creates item",
                "validation": "Returns 201 with created item",
                "type": "http",
                "live_test": {
                    "method": "POST",
                    "url": "{{API_URL}}/api/items",
                    "headers": {"Authorization": "Bearer {{AUTH_TOKEN}}"},
                    "body": {"name": "Test Item", "description": "Created by E2E test"},
                    "expect": {"status": 201, "body_contains": ["id", "name"]}
                }
            },
            {
                "id": "2.3.3",
                "action": "Unauthorized requests rejected",
                "validation": "Returns 401 without auth header",
                "type": "http",
                "live_test": {
                    "method": "GET",
                    "url": "{{API_URL}}/api/items",
                    "expect": {"status": 401}
                }
            }
        ],
        "dependencies": ["2.1", "2.2"]
    },
    
    "2.4": {
        "title": "Frontend Integration",
        "description": "Connect frontend to API and verify UI renders correctly.",
        "estimated_time": "30 minutes",
        "checks": [
            {
                "id": "2.4.1",
                "action": "Homepage loads without errors",
                "validation": "GET / returns 200, no console errors",
                "type": "http",
                "live_test": {
                    "method": "GET",
                    "url": "{{FRONTEND_URL}}/",
                    "expect": {"status": 200}
                }
            },
            {
                "id": "2.4.2",
                "action": "Login form submits successfully",
                "validation": "User can log in via UI",
                "type": "ui",
                "steps": [
                    "Navigate to /login",
                    "Enter test credentials",
                    "Click submit",
                    "Verify redirect to dashboard"
                ]
            },
            {
                "id": "2.4.3",
                "action": "API calls work from frontend",
                "validation": "Network tab shows successful API requests",
                "type": "ui",
                "steps": [
                    "Open browser dev tools",
                    "Navigate to items page",
                    "Verify /api/items call succeeds"
                ]
            }
        ],
        "dependencies": ["2.3"]
    }
}


def get_instructions(task_id: str) -> str:
    """Generate markdown instructions for a task on-demand."""
    task = TASKS.get(task_id)
    if not task:
        return f"❌ Task {task_id} not found in phase_2_build.py"
    
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
        
        if check.get('key_files'):
            lines.append(f"- **Key Files:** {', '.join(check['key_files'])}")
        
        if check.get('live_test'):
            lt = check['live_test']
            lines.append(f"- **Live Test:**")
            lines.append(f"  - Method: {lt.get('method', 'GET')}")
            lines.append(f"  - URL: `{lt.get('url')}`")
            if lt.get('body'):
                lines.append(f"  - Body: `{lt.get('body')}`")
            if lt.get('expect'):
                lines.append(f"  - Expect: {lt.get('expect')}")
        
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
