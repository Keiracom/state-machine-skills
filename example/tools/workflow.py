#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State-Machine Skills CLI Router

Token-efficient workflow management for Claude Code.
Outputs only the current task context to minimize token usage.

Usage:
    python workflow.py next              # Get next pending task
    python workflow.py status            # Show workflow progress  
    python workflow.py complete TASK_ID -s "summary"  # Mark task done
    python workflow.py reset             # Reset all tasks to pending
    python workflow.py skip TASK_ID      # Skip a task
"""

import json
import argparse
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STATE_FILE = Path(__file__).parent.parent / "state" / "process.json"
CONFIG_FILE = Path(__file__).parent.parent / "state" / "config.json"
LIBRARY_DIR = Path(__file__).parent.parent / "library"


def load_state():
    """Load current workflow state."""
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    """Save workflow state."""
    state['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def load_config():
    """Load workflow configuration."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def load_skill(skill_file):
    """Dynamically load a skill file and return its SKILL dict."""
    skill_path = LIBRARY_DIR / Path(skill_file).name
    if not skill_path.exists():
        return None
    spec = importlib.util.spec_from_file_location("skill", skill_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'SKILL', None)


def cmd_next():
    """Get the next pending task with minimal context."""
    state = load_state()
    config = load_config()
    
    # Find next pending task
    for i, task in enumerate(state['tasks']):
        if task['status'] == 'pending':
            # Check for phase transition requiring approval
            if i > 0:
                prev_task = state['tasks'][i-1]
                if prev_task['phase'] != task['phase']:
                    phase_info = next(
                        (p for p in config['phases'] if p['id'] == task['phase']), 
                        None
                    )
                    if phase_info and phase_info.get('requires_approval'):
                        print(f"⚠️  PHASE TRANSITION: {prev_task['phase']} → {task['phase']}")
                        print(f"   Phase '{phase_info['name']}' requires approval.")
                        print(f"   Run: python workflow.py approve-phase {task['phase']}")
                        return
            
            # Load skill and output task context
            skill = load_skill(task['skill_file'])
            print(f"📋 CURRENT TASK: {task['id']}")
            print(f"   Name: {task['name']}")
            print(f"   Phase: {task['phase']}")
            print(f"   Skill: {task['skill_file']}")
            print()
            if skill:
                print("📖 INSTRUCTIONS:")
                if 'get_instructions' in dir(importlib.util.module_from_spec(
                    importlib.util.spec_from_file_location("skill", LIBRARY_DIR / Path(task['skill_file']).name)
                )):
                    skill_path = LIBRARY_DIR / Path(task['skill_file']).name
                    spec = importlib.util.spec_from_file_location("skill", skill_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'get_instructions'):
                        print(module.get_instructions(task['id']))
                else:
                    for step in skill.get('steps', []):
                        print(f"   {step}")
                print()
                print("✅ COMPLETION CHECKS:")
                for check in skill.get('checks', []):
                    print(f"   [ ] {check}")
            print()
            print(f"When done: python workflow.py complete {task['id']} -s \"your summary\"")
            return
    
    print("🎉 All tasks completed!")


def cmd_status():
    """Show workflow progress summary."""
    state = load_state()
    total = len(state['tasks'])
    completed = sum(1 for t in state['tasks'] if t['status'] == 'completed')
    skipped = sum(1 for t in state['tasks'] if t['status'] == 'skipped')
    pending = total - completed - skipped
    
    print(f"📊 WORKFLOW STATUS: {state['workflow_id']}")
    print(f"   Progress: {completed}/{total} ({100*completed//total}%)")
    print(f"   Completed: {completed} | Skipped: {skipped} | Pending: {pending}")
    print(f"   Current Phase: {state['current_phase']}")
    print()
    
    current_phase = None
    for task in state['tasks']:
        if task['phase'] != current_phase:
            current_phase = task['phase']
            print(f"\n── {current_phase.upper()} ──")
        
        icon = {"completed": "✅", "skipped": "⏭️", "pending": "⬜"}.get(task['status'], "❓")
        summary = f" - {task['summary']}" if task.get('summary') else ""
        print(f"  {icon} {task['id']}: {task['name']}{summary}")


def cmd_complete(task_id, summary):
    """Mark a task as completed."""
    state = load_state()
    
    for task in state['tasks']:
        if task['id'] == task_id:
            task['status'] = 'completed'
            task['summary'] = summary
            task['completed_at'] = datetime.utcnow().isoformat() + 'Z'
            
            # Log to session history
            state['session_history'].append({
                'task_id': task_id,
                'action': 'completed',
                'summary': summary,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })
            
            save_state(state)
            print(f"✅ Task {task_id} marked complete.")
            return
    
    print(f"❌ Task {task_id} not found.")

def cmd_skip(task_id):
    """Skip a task."""
    state = load_state()
    
    for task in state['tasks']:
        if task['id'] == task_id:
            task['status'] = 'skipped'
            task['summary'] = 'Skipped'
            save_state(state)
            print(f"⏭️  Task {task_id} skipped.")
            return
    
    print(f"❌ Task {task_id} not found.")


def cmd_reset():
    """Reset all tasks to pending."""
    state = load_state()
    
    for task in state['tasks']:
        task['status'] = 'pending'
        task['summary'] = None
        task['completed_at'] = None
    
    state['current_task_index'] = 0
    state['session_history'] = []
    save_state(state)
    print("🔄 All tasks reset to pending.")

def main():
    parser = argparse.ArgumentParser(description='State-Machine Skills CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # next
    subparsers.add_parser('next', help='Get next pending task')
    
    # status
    subparsers.add_parser('status', help='Show workflow progress')
    
    # complete
    complete_parser = subparsers.add_parser('complete', help='Mark task complete')
    complete_parser.add_argument('task_id', help='Task ID to complete')
    complete_parser.add_argument('-s', '--summary', required=True, help='Completion summary')
    
    # skip
    skip_parser = subparsers.add_parser('skip', help='Skip a task')
    skip_parser.add_argument('task_id', help='Task ID to skip')
    
    # reset
    subparsers.add_parser('reset', help='Reset all tasks')
    
    args = parser.parse_args()
    
    if args.command == 'next':
        cmd_next()
    elif args.command == 'status':
        cmd_status()
    elif args.command == 'complete':
        cmd_complete(args.task_id, args.summary)
    elif args.command == 'skip':
        cmd_skip(args.task_id)
    elif args.command == 'reset':
        cmd_reset()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
