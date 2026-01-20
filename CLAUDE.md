# State-Machine Skills

## Entry Point

All workflow operations go through the CLI. Do not improvise task order or skip the router.

```bash
python tools/workflow.py status    # Current position
python tools/workflow.py next      # Get current task
python tools/workflow.py complete TASK_ID -s "summary"  # Mark done
```

## Workflow

When asked to "continue", "next task", or similar:

1. Run `python tools/workflow.py next`
2. Read the skill file shown in output (if needed for detail)
3. Execute the checks listed
4. Report results
5. Run `python tools/workflow.py complete TASK_ID -s "brief summary"`

## State Files (reference only)

- `state/process.json` — Current phase, task, completed items
- `state/config.json` — Project configuration
- `state/history.json` — Session audit log

## Do NOT

- Load all skill files at once
- Guess the next task without checking process.json
- Skip the CLI entry point
- Modify state files directly (use the CLI)
