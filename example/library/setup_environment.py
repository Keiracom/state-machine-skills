"""
Example Skill: Setup Environment

This demonstrates the skill file structure.
Skills are Python files with a SKILL dict containing metadata,
and optionally a get_instructions() function for dynamic content.
"""

SKILL = {
    "name": "Setup Environment",
    "description": "Initialize project environment and verify prerequisites",
    "steps": [
        "1. Check Python version >= 3.9",
        "2. Verify required environment variables are set",
        "3. Create necessary directories if missing",
        "4. Install dependencies from requirements.txt"
    ],
    "checks": [
        "Python version verified",
        "Environment variables present",
        "Directory structure exists",
        "Dependencies installed successfully"
    ]
}

def get_instructions(task_id: str) -> str:
    """
    Generate task-specific instructions.
    This allows dynamic content based on task context.
    """
    instructions = {
        "SETUP-001": """
Check Prerequisites:
- Run `python --version` and verify >= 3.9
- Check for required env vars: PROJECT_ROOT, CONFIG_PATH
- If missing, document what needs to be set
""",
        "SETUP-002": """
Initialize Configuration:
- Create config directory if not exists
- Copy template config files
- Set appropriate permissions
"""
    }
    return instructions.get(task_id, "No specific instructions for this task.")
