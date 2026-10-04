#!/usr/bin/env python3
"""Portable, standard-library-only research workspace starter."""
import argparse
import os
from datetime import datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent

def safe_name(value):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', value):
        raise ValueError('name must be 1-64 lowercase ASCII letters, digits, _ or -')
    return value

def task_path(value):
    p = Path(value).resolve()
    if p.parent != (BASE / 'test').resolve() or not (p / 'BRIEF.md').is_file():
        raise ValueError('use an exact active task directory under this workspace/test')
    return p

def refresh(p):
    text = '# Active context\n\nGenerated view; source files remain authoritative.\n\n'
    for name in ('BRIEF.md', 'WORKING_NOTE.md'):
        text += (p / name).read_text(encoding='utf-8') + '\n'
    (p / 'ACTIVE_CONTEXT.md').write_text(text, encoding='utf-8')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('init'); a.add_argument('destination')
    a = sp.add_parser('new'); a.add_argument('name'); a.add_argument('--objective', required=True)
    a = sp.add_parser('refresh'); a.add_argument('task')
    a = sp.add_parser('close'); a.add_argument('task'); a.add_argument('--summary', required=True)
    sp.add_parser('self-test')
    args = ap.parse_args()
    if args.cmd == 'init':
        dest = Path(args.destination).resolve()
        dest.mkdir(parents=True, exist_ok=False)
        for name in ('starter.py', 'AGENTS.md', 'START_HERE.md', 'WORKFLOW.md', 'LICENSE', '.gitignore'):
            shutil.copy2(BASE / name, dest / name)
        shutil.copytree(BASE / 'templates', dest / 'templates')
        for name in ('test', 'wiki', 'History'):
            (dest / name).mkdir()
        (dest / 'CONTEXT.md').write_text('# Project context\n\nObjective: fill this in.\nScope: fill this in.\nDefault: human-governed. Start from one exact task.\n', encoding='utf-8')
        print(dest)
    elif args.cmd == 'new':
        if not (BASE / 'CONTEXT.md').is_file():
            raise ValueError('run init first, then use the generated workspace starter.py')
        name = datetime.now().strftime('%Y-%m-%d_') + safe_name(args.name)
        p = BASE / 'test' / name
        p.mkdir(exist_ok=False)
        brief = (BASE / 'templates/BRIEF.md').read_text(encoding='utf-8').replace('{objective}', args.objective)
        (p / 'BRIEF.md').write_text(brief, encoding='utf-8')
        shutil.copy2(BASE / 'templates/WORKING_NOTE.md', p / 'WORKING_NOTE.md')
        refresh(p); print(p)
    elif args.cmd == 'refresh':
        p = task_path(args.task); refresh(p); print(p / 'ACTIVE_CONTEXT.md')
    elif args.cmd == 'close':
        p = task_path(args.task)
        summary = Path(args.summary).read_text(encoding='utf-8')
        if not summary.strip():
            raise ValueError('summary must not be empty')
        target = BASE / 'History' / p.name
        page = BASE / 'wiki' / (p.name + '.md')
        if target.exists() or page.exists():
            raise ValueError('refusing to overwrite existing history/wiki')
        with page.open('x', encoding='utf-8') as f:
            f.write(summary.rstrip() + '\n')
        try:
            shutil.move(str(p), str(target))
        except Exception:
            page.unlink(); raise
        print(target)
    elif args.cmd == 'self-test':
        with tempfile.TemporaryDirectory(prefix='attention-test-') as d:
            work = Path(d) / 'unicode-Δ demo'
            def run(base, *cmd, ok=True):
                result = subprocess.run([sys.executable, str(base / 'starter.py'), *map(str, cmd)], capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
                assert (result.returncode == 0) == ok, result.stderr
                return result.stdout.strip()
            run(BASE, 'init', work)
            run(BASE, 'init', work, ok=False)
            p = Path(run(work, 'new', 'demo', '--objective', 'finite evidence ≠ proof'))
            run(work, 'new', 'demo', '--objective', 'duplicate', ok=False)
            run(work, 'new', '../escape', '--objective', 'bad', ok=False)
            with (p / 'WORKING_NOTE.md').open('a', encoding='utf-8') as f: f.write('\nEvidence: refuted\n')
            run(work, 'refresh', p)
            assert 'refuted' in (p / 'ACTIVE_CONTEXT.md').read_text(encoding='utf-8')
            run(work, 'refresh', work, ok=False)
            summary = Path(d) / 'summary.md'
            summary.write_text('', encoding='utf-8')
            run(work, 'close', p, '--summary', summary, ok=False)
            assert p.exists()
            summary.write_text('Negative result; evidence retained.\n', encoding='utf-8')
            collision = work / 'History' / p.name
            collision.mkdir()
            run(work, 'close', p, '--summary', summary, ok=False)
            assert p.exists()
            collision.rmdir()
            run(work, 'close', p, '--summary', summary)
            assert (work / 'LICENSE').is_file()
            assert not p.exists()
            assert (work / 'History' / p.name / 'WORKING_NOTE.md').is_file()
            assert (work / 'wiki' / (p.name + '.md')).read_text(encoding='utf-8') == summary.read_text(encoding='utf-8')
        print('PASS: init/new/refresh/close, collision refusal, path boundary, Unicode/spaces, preserved failure')

if __name__ == '__main__':
    try: main()
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
