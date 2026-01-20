# Contributing to State-Machine Skills

Thanks for your interest in contributing! This project aims to provide a token-efficient alternative to native Claude Code Skills.

## Ways to Contribute

### 1. Report Issues
- Bugs in the CLI router
- Documentation improvements
- Feature requests

### 2. Submit Examples
- New skill file templates for specific use cases
- Integration examples (CI/CD, specific frameworks)
- Real-world workflow configurations

### 3. Improve Core Functionality
- CLI enhancements
- State management improvements
- Performance optimizations

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/state-machine-skills.git
cd state-machine-skills

# Test the CLI
python tools/workflow.py status
python tools/workflow.py next
```

## Code Style

- Python: Follow PEP 8
- JSON: 2-space indentation
- Markdown: Use ATX-style headers (`#`)

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test locally with example workflow
5. Submit PR with clear description

## Skill File Guidelines

When creating new skill templates:

1. Use the `skills/TEMPLATE.md` as reference
2. Include `get_instructions()` function
3. Include `get_task_ids()` function
4. Use consistent check types (`manual`, `command`, `http`, etc.)
5. Document any variable placeholders used

## Questions?

Open an issue with the "question" label.
