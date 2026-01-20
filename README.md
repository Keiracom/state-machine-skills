# State-Machine Skills for Claude Code

An experimental alternative to native SKILL.md files that uses deterministic CLI routing for complex workflows.

## The Theory

Native Claude Skills scan all SKILL.md files for metadata. With many skills, this *might* consume significant context. This approach loads only the current task on-demand.

**Caveat:** Token savings are theoretical and not formally measured. Your mileage may vary.

## What This Actually Solves

Regardless of token efficiency, this pattern provides features native Skills don't have:

- **Approval gates** - Pause between phases, require explicit confirmation
- **State persistence** - Track progress across sessions in JSON
- **Session history** - Log what was completed and when
- **Deterministic ordering** - Tasks execute in defined sequence, not LLM choice

## How It Works

1. `CLAUDE.md` points to CLI entry point
2. User says "continue" → Claude runs `python tools/workflow.py next`
3. CLI reads `state/process.json`, outputs current task only
4. Claude reads relevant skill file, executes checks
5. Claude runs `python tools/workflow.py complete TASK_ID -s "summary"`
6. State updates, ready for next session

## Why Approval Gates Matter

Native Skills have no concept of "wait for confirmation before proceeding." This is problematic for:

- Destructive operations (database migrations, file deletions)
- Multi-phase deployments requiring human verification
- Workflows where a mistake in phase 1 corrupts phase 2

With state-machine skills, phases can require explicit approval:
```json
{
  "id": "deployment",
  "name": "Production Deployment",
  "requires_approval": true
}
```

## Enforcing the Pattern

Claude might forget to check the CLI. Add strict instructions to your `CLAUDE.md`:

```markdown
## CRITICAL: Workflow Rules

**BEFORE doing any work, ALWAYS run:**
python .claude-workflow/tools/workflow.py next

**DO NOT:**
- Start working without checking current task
- Skip tasks or work out of order
- Mark tasks complete without running checks

**ALWAYS:**
- Run `workflow.py next` when user says "continue"
- Follow the instructions output by the CLI
- Mark complete with summary when done
```

**Note:** This isn't bulletproof. Claude may still ignore instructions in long contexts. This is an experiment, not a production-hardened system.

## Quick Start

```bash
git clone https://github.com/Keiracom/state-machine-skills.git
cd state-machine-skills

# Copy example to your project
cp -r example/ your-project/.claude-workflow/

# Add to your CLAUDE.md
cat example/CLAUDE.md >> your-project/CLAUDE.md
```

## Directory Structure

```
your-project/
├── CLAUDE.md                    # Points to workflow CLI
└── .claude-workflow/
    ├── state/
    │   ├── process.json         # Task state tracker
    │   └── config.json          # Workflow config
    ├── tools/
    │   └── workflow.py          # CLI router
    └── library/
        ├── setup_environment.py # Example skill
        └── run_tests.py         # Example skill
```

## When This Might Help

- Complex multi-phase workflows (E2E testing, migrations, audits)
- 50+ tasks with state persistence needs
- Approval gates between phases
- Session history logging requirements

## When to Just Use Native Skills

- Simple, stateless utilities
- You want auto-invocation based on natural language
- You need cross-platform portability (Claude.ai, API)
- You have fewer than ~20 skills

## Trade-offs

| Feature | Native Skills | State-Machine |
|---------|--------------|---------------|
| Auto-invocation | ✅ | ❌ |
| Token efficiency | Unknown | Unknown (theoretical) |
| State persistence | ❌ | ✅ |
| Approval gates | ❌ | ✅ |
| Session history | ❌ | ✅ |
| Portable to claude.ai | ✅ | ❌ |
| Reliability | Platform-managed | Depends on Claude following instructions |

## Known Limitations

- **No measurements:** Token savings are assumed, not proven
- **Claude may ignore instructions:** Especially in long contexts
- **State corruption risk:** If Claude hallucinates a completion, your JSON is wrong
- **Platform-dependent:** Will break if Anthropic changes how CLAUDE.md works
- **Overengineered for simple cases:** If you have <20 tasks, this is overkill

## Why Not Just Use X?

- **Git for history?** Fair point. This is more granular but git works.
- **Prefect/Airflow?** If you need real orchestration, use those. This is for Claude-in-the-loop workflows.
- **Markdown checklist?** Simpler. Try that first honestly.

## What If Anthropic Fixes This?

If native Skills add state persistence and approval gates, this becomes unnecessary. That's fine. The workflow logic lives in your skill files either way.

## License

MIT - Use it however you want.

## Contributing

PRs welcome. This is an experiment - feedback on whether the approach even makes sense is appreciated.
