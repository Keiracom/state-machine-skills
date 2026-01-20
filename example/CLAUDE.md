# Project Workflow

This project uses state-machine skills for workflow management.

## Workflow Commands

```bash
# Get current task
python .claude-workflow/tools/workflow.py next

# Check progress  
python .claude-workflow/tools/workflow.py status

# Mark task complete
python .claude-workflow/tools/workflow.py complete TASK_ID -s "summary"

# Skip a task
python .claude-workflow/tools/workflow.py skip TASK_ID

# Reset workflow
python .claude-workflow/tools/workflow.py reset
```

## How to Continue Work

When user says "continue" or "next task":
1. Run `python .claude-workflow/tools/workflow.py next`
2. Read the instructions output
3. Execute the task
4. Mark complete with summary

## Skill Files

Task instructions are in `.claude-workflow/library/`. 
Only read the skill file referenced by the current task.
