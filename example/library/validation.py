"""
Example Skill: Validation

Final phase skill for verifying outputs.
"""

SKILL = {
    "name": "Validation",
    "description": "Verify workflow outputs and cleanup",
    "steps": [
        "1. Review all task summaries",
        "2. Verify expected outputs exist",
        "3. Run any validation checks",
        "4. Generate final report"
    ],
    "checks": [
        "All expected outputs present",
        "Validation checks passed",
        "No critical errors in logs",
        "Final report generated"
    ]
}

def get_instructions(task_id: str) -> str:
    """Generate task-specific instructions."""
    return """
Verify Outputs:
- Check that all previous tasks completed successfully
- Verify expected files/data exist
- Run `python workflow.py status` to see full summary
- Document any issues found
"""
