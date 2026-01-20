# Comparison: Native Skills vs State-Machine Skills

## Feature Matrix

| Feature | Native SKILL.md | State-Machine |
|---------|----------------|---------------|
| **Token efficiency** | ❌ Poor (~14k+ baseline) | ✅ Excellent (~200 baseline) |
| **Auto-invocation** | ✅ Yes | ❌ No (explicit "continue") |
| **State persistence** | ❌ No | ✅ Yes (JSON file) |
| **Session history** | ❌ No | ✅ Yes (logged) |
| **Approval gates** | ❌ No | ✅ Yes (phase transitions) |
| **Multi-session** | ❌ Loses context | ✅ Full continuity |
| **Portable** | ✅ claude.ai, API | ❌ Claude Code only |
| **Discoverable** | ✅ Claude can browse | ❌ Must follow CLI |

## When to Use Native Skills

- Simple, stateless utilities
- Auto-invocation based on natural language
- Cross-platform deployment needs
- Fewer than 10 skills total
- No state persistence required

## When to Use State-Machine

- Complex multi-phase workflows
- 50+ sequential tasks
- State must persist across sessions
- Approval gates between phases
- Audit trail requirements
- Token budget is constrained

## Hybrid Approach

You can use both:
1. Native Skills for simple utilities (formatting, searching)
2. State-Machine for complex workflows (E2E testing, migrations)

Just keep them separate:
- `.claude/skills/` for native SKILL.md files
- `.claude-workflow/` for state-machine system
