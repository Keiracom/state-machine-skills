# Architecture

## Overview

State-Machine Skills replaces the native SKILL.md pattern with a deterministic CLI-driven approach.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  CLAUDE.md  │────▶│  workflow.py │────▶│ process.json│
│  (~200 tok) │     │  (CLI router)│     │   (state)   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ library/*.py│
                    │  (skills)   │
                    └─────────────┘
```

## Components

### 1. CLAUDE.md (~200 tokens)
Minimal bootstrap that tells Claude how to use the workflow CLI.
No skill metadata, no task lists - just the commands.

### 2. workflow.py (CLI Router)
Python script that:
- Reads state from `process.json`
- Outputs ONLY the current task
- Loads skill instructions on-demand
- Updates state on completion

### 3. process.json (State)
JSON file tracking:
- Task list with statuses
- Current phase
- Session history
- Completion summaries

### 4. library/*.py (Skills)
Python files containing:
- `SKILL` dict with metadata
- `get_instructions(task_id)` for dynamic content
- No markdown parsing overhead

## Token Flow

### Native Skills (expensive)
```
1. Claude loads CLAUDE.md               ~500 tokens
2. Claude scans all SKILL.md files      ~100 tokens × N skills
3. Claude decides which skill to use    ~500 tokens
4. Claude loads full skill content      ~3000 tokens
                                        ─────────────
                                        ~4000+ tokens minimum
```

### State-Machine Skills (efficient)
```
1. Claude loads CLAUDE.md               ~200 tokens
2. User says "continue"                 
3. Claude runs `workflow.py next`       ~0 tokens (CLI output)
4. CLI outputs current task only        ~500 tokens
5. Claude reads one skill file          ~1000 tokens
                                        ─────────────
                                        ~1700 tokens total
```

## State Transitions

```
pending ──▶ completed (with summary)
   │
   └──────▶ skipped
```

Phases can require approval before transitioning:
```
setup ──[approval]──▶ execution ──▶ validation
```

## Session History

Every completion is logged:
```json
{
  "session_history": [
    {
      "task_id": "SETUP-001",
      "action": "completed", 
      "summary": "Python 3.11 verified, all env vars present",
      "timestamp": "2025-01-20T10:30:00Z"
    }
  ]
}
```

This enables:
- Multi-session continuity
- Audit trails
- Progress recovery
