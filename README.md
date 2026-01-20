# State-Machine Skills for Claude Code

A token-efficient alternative to native SKILL.md files that achieves ~90% context reduction through deterministic CLI routing.

## The Problem

Native Claude Skills load ~100 tokens per skill just for metadata scanning. With 140 skills, that's 14,000 tokens before you start working.

## The Solution

- **JSON state files** track progress (no LLM memory needed)
- **Python skill files** with structured dicts (not markdown)
- **CLI router** that outputs only the current task
- **On-demand instruction generation** via `get_instructions()`

## Token Comparison

| Approach | Baseline | Per Task | Total |
|----------|----------|----------|-------|
| Native Skills (140) | ~14,000 | ~3,000 | ~17,000 |
| This System | ~200 | ~1,500 | ~1,700 |

## How It Works

1. `CLAUDE.md` points to CLI entry point (~200 tokens)
2. User says "continue" → Claude runs `python tools/workflow.py next`
3. CLI reads `state/process.json`, outputs current task only
4. Claude reads relevant skill file, executes checks
5. Claude runs `python tools/workflow.py complete TASK_ID -s "summary"`
6. State updates, ready for next session

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/state-machine-skills.git
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

## When to Use This

- Complex multi-phase workflows (E2E testing, migrations, audits)
- 50+ tasks with state persistence needs
- Approval gates between phases
- Session history logging requirements

## When NOT to Use This

- Simple, stateless skills
- Auto-invocation based on natural language matching
- Cross-platform portability (Claude.ai, API)

## Trade-offs vs Native Skills

| Feature | Native Skills | State-Machine |
|---------|--------------|---------------|
| Auto-invocation | ✅ | ❌ |
| Token efficiency | ❌ | ✅ |
| State persistence | ❌ | ✅ |
| Approval gates | ❌ | ✅ |
| Session history | ❌ | ✅ |
| Portable to claude.ai | ✅ | ❌ |

## License

MIT - Use it however you want.

## Contributing

PRs welcome. Keep it simple and generic.
