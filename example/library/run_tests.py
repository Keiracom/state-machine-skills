"""
Example Skill: Run Tests

Demonstrates a skill for execution-phase tasks.
"""

SKILL = {
    "name": "Run Tests",
    "description": "Execute test suite and collect results",
    "steps": [
        "1. Ensure test environment is configured",
        "2. Run the test command",
        "3. Capture output and exit codes",
        "4. Parse results into structured format"
    ],
    "checks": [
        "Test command executed without errors",
        "Output captured and logged",
        "Results parsed successfully",
        "Summary generated"
    ]
}

def get_instructions(task_id: str) -> str:
    """Generate task-specific instructions."""
    instructions = {
        "EXEC-001": """
Run Primary Task:
- Execute the main workflow command
- Monitor for errors or warnings
- Capture all output for later analysis
""",
        "EXEC-002": """
Process Results:
- Parse the output from the primary task
- Extract key metrics or data points
- Format results for the validation phase
"""
    }
    return instructions.get(task_id, "Execute the task as described.")
