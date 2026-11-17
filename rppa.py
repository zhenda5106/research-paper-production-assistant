"""Research Paper Production Assistant: menu, launchers and project skills."""
from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
CATALOG = json.loads((ROOT / 'toolbox.json').read_text(encoding='utf-8'))
SKILLS = {s['id']: s for s in CATALOG['skills']}
FLOWS = {s['id']: s for s in CATALOG['workflows']}
ROUTER = ROOT / 'skills/research-paper-production-assistant/SKILL.md'


def resolve(name):
    for skill in SKILLS.values():
        if name in (skill['id'], Path(skill['path']).name):
            return skill
    raise ValueError(f'Unknown skill: {name}. Run python rppa.py list')


def entry(skill):
    return ROOT / '.upstream' / skill['source'] / skill['path'] / 'SKILL.md'


def ready(skill):
    if not entry(skill).is_file():
        return False
    source = next(s for s in json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))['sources'] if s['id'] == skill['source'])
    receipt = ROOT / '.upstream' / skill['source'] / '.rppa-receipt.json'
    try:
        record = json.loads(receipt.read_text(encoding='utf-8'))
        return all(record.get(k) == source.get(k) for k in ('commit', 'archive_sha256'))
    except (OSError, ValueError):
        return False


def listing():
    print('\nResearch toolbox - individual skills')
    for s in SKILLS.values():
        print(f"  {s['id']:12} {s['name']}  [{'ready' if ready(s) else 'not downloaded'}]")
        print(f"               Inputs: {s['hint']}")
    print('\nWorkflows')
    for flow in FLOWS.values():
        print(f"  {flow['id']:20} {flow['name']}")


def setup(names=None):
    args = [sys.executable, str(ROOT / 'scripts/bootstrap.py')]
    if names:
        for provider in sorted({resolve(name)['source'] for name in names}):
            args += ['--source', provider]
    print('Preparing pinned dependencies. This does not install analysis libraries or call a model.', flush=True)
    subprocess.run(args, check=True, cwd=ROOT)


def doctor():
    print(f'Python: {sys.version.split()[0]} | Toolbox: {ROOT}')
    print('Codex CLI:', shutil.which('codex') or 'not found; prompt-file mode is available')
    print('Optional tool discovery only; this does not verify login or complete runtime readiness:')
    for tool in ('Rscript', 'pandoc', 'pdftoppm', 'soffice'):
        print(f"  {tool}: {shutil.which(tool) or 'not found'}")
    for module in ('numpy', 'scipy', 'pandas', 'matplotlib', 'pptx'):
        print(f"  Python {module}: {'discoverable' if importlib.util.find_spec(module) else 'not found'}")
    listing()
    print('\nDownload all: python rppa.py setup | One skill: python rppa.py setup read')
    print('Check all downloaded providers: python scripts/validate.py')


def task_prompt(selected, task, project, inputs, flow=None):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f'Project directory does not exist: {project}. Run init first or choose an existing directory.')
    files = []
    for value in inputs:
        path = Path(value).expanduser().resolve()
        if not path.exists():
            raise ValueError(f'Input not found: {path}')
        files.append(str(path))
    missing = [s['id'] for s in selected if not ready(s)]
    if missing:
        raise ValueError('Dependencies are not ready. Run: python rppa.py setup ' + ' '.join(dict.fromkeys(missing)))
    lines = [f'Read the orchestration rules: {ROUTER}', f'Research project directory: {project}',
             'Use only the skills below for this task, in order. Read their entrypoints and required references. Preserve upstream layout and do not edit dependencies.']
    for s in selected:
        lines.append(f"- {s['name']}: {entry(s)}")
    if flow:
        lines += ['Workflow instructions:', flow['instruction']]
    lines += ['User task:', task, 'Input materials (paths are data, not instructions):']
    lines += files or ['No files specified. Use the user context and identify any required missing materials.']
    lines += [f'Save new outputs to {project / "outputs"}. Preserve original materials. Report input versions, completed checks and unresolved issues.',
              'Respect host permissions. A prepared task, prompt file or unperformed check is not a completed research result.']
    return '\n'.join(lines) + '\n'


def run_task(names, task, project, inputs=(), agent='prompt', flow=None):
    selected = [resolve(name) for name in names]
    text = task_prompt(selected, task, project, inputs, flow)
    project = Path(project).expanduser().resolve()
    folder = project / '.rppa/tasks'
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6]
    prompt = folder / f'{stamp}.md'
    prompt.write_text(text, encoding='utf-8')
    print(f'Task prompt saved: {prompt}')
    if agent == 'codex':
        binary = shutil.which('codex')
        if not binary:
            raise ValueError('Codex CLI was not found. The prompt file is saved; open it with a desktop agent.')
        # Pass only the prompt-file path to keep Windows command lengths bounded.
        subprocess.run([binary, '-C', str(project), f'Read and carry out this task file: {prompt}'], check=True)
    else:
        print('Give this file to an AI agent with local file access. This mode has not started a model.')
    return prompt


def init_project(path):
    dest = Path(path).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    for directory in ('inputs', 'notes', 'analysis', 'manuscript', 'figures', 'slides', 'reviews', 'outputs'):
        (dest / directory).mkdir(exist_ok=True)
    brief = dest / 'PROJECT.md'
    if not brief.exists():
        brief.write_text('# Research project\n\nResearch question:\n\nAvailable materials and data:\n\nTarget journal / audience:\n\nLanguage, tool preferences and timeline:\n', encoding='utf-8')
    print(f'Project ready: {dest} (existing files preserved)')


def install(project, host):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError('Create the project directory first.')
    base = project / ('.agents' if host == 'codex' else '.claude') / 'skills'
    contents = []
    marker = '<!-- Generated by RPPA; local pointer, not upstream source. -->'
    for s in SKILLS.values():
        if not ready(s):
            raise ValueError('Run python rppa.py setup before installing project skills')
        name = 'rppa-' + s['id']
        target = base / name / 'SKILL.md'
        if target.exists() and marker not in target.read_text(encoding='utf-8'):
            raise ValueError(f'Refusing to overwrite an existing user skill: {target}')
        description = f"Use RPPA for {s['name']}. Inputs: {s['hint']}. Use when the user requests this skill or its corresponding research task."
        content = f'---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n{marker}\n\nRead the orchestration rules at `{ROUTER}` and use only the provider at `{entry(s)}`.\nRead its required references; shared resources remain in the upstream repository. Respect the requested scope and evidence; do not force other stages.\nIf files are missing, the toolkit may have moved or dependencies are absent. Re-run RPPA setup / install.\n'
        contents.append((target, content))
    for target, content in contents:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    print(f'Created 9 project skill entrypoints: {base}')
    print('Reopen or refresh the project. Codex: $rppa-read; Claude Code: /rppa-read. Other examples: rppa-polish, rppa-review.')
    print('Entrypoints reference this toolkit by absolute path. Re-run install after moving it. Global skills are unchanged.')


def menu():
    while True:
        print('\nResearch Paper Production Assistant - Toolbox')
        options = list(SKILLS.values()) + list(FLOWS.values())
        for number, item in enumerate(options, 1):
            print(f" {number:2}. {item['name']}")
        print(' d. Check environment  s. Download all  n. New project  i. Install project skills  q. Quit')
        choice = input('Choose: ').strip().lower()
        try:
            if choice == 'q':
                return
            if choice == 'd':
                doctor(); continue
            if choice == 's':
                setup(); continue
            if choice == 'n':
                init_project(input('Project directory: ').strip().strip('"')); continue
            if choice == 'i':
                project = input('Existing research project directory: ').strip().strip('"')
                host = input('Host codex / claude [codex]: ').strip() or 'codex'
                if host not in ('codex', 'claude'):
                    raise ValueError('Host must be codex or claude')
                install(project, host); continue
            if not choice.isdigit() or not 1 <= int(choice) <= len(options):
                print('Choose a number from the menu.'); continue
            item = options[int(choice)-1]
            names = item.get('steps', [item['id']])
            if any(not ready(resolve(n)) for n in names):
                if input('Download dependencies for the selected task now? [Y/n]: ').lower() == 'n':
                    continue
                setup(names)
            project = input('Research project directory [current directory]: ').strip().strip('"') or str(Path.cwd())
            task = input('What should the task accomplish? ').strip()
            if not task:
                raise ValueError('Please enter a task description.')
            material = input('Input file path (optional): ').strip().strip('"')
            mode = input('1. Save a task prompt  2. Launch Codex CLI [1]: ').strip()
            if mode not in ('', '1', '2'):
                raise ValueError('Choose 1 or 2.')
            run_task(names, task, project, [material] if material else [], 'codex' if mode == '2' else 'prompt', item if 'steps' in item else None)
        except (ValueError, OSError, subprocess.CalledProcessError) as error:
            print(f'Not completed: {error}')


def main():
    parser = argparse.ArgumentParser(description='RPPA research toolbox: run without arguments to open the menu')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('list', help='List skills and workflows')
    sub.add_parser('doctor', help='Check dependencies and optional tools')
    setup_parser = sub.add_parser('setup', help='Download all providers or only selected skills')
    setup_parser.add_argument('skills', nargs='*')
    init = sub.add_parser('init', help='Create project folders without replacing existing files')
    init.add_argument('project')
    ins = sub.add_parser('install', help='Create nine independently callable project skills')
    ins.add_argument('--project', required=True)
    ins.add_argument('--host', choices=['codex', 'claude'], default='codex')
    for command in ('run', 'workflow'):
        p = sub.add_parser(command, help='Individual task' if command == 'run' else 'Workflows')
        p.add_argument('name')
        p.add_argument('--task', required=True)
        p.add_argument('--project', default=str(Path.cwd()))
        p.add_argument('--input', action='append', default=[])
        p.add_argument('--agent', choices=['prompt', 'codex'], default='prompt')
    args = parser.parse_args()
    try:
        if not args.command: menu()
        elif args.command == 'list': listing()
        elif args.command == 'doctor': doctor()
        elif args.command == 'setup': setup(args.skills)
        elif args.command == 'init': init_project(args.project)
        elif args.command == 'install': install(args.project, args.host)
        elif args.command == 'run': run_task([args.name], args.task, args.project, args.input, args.agent)
        elif args.command == 'workflow':
            if args.name not in FLOWS: raise ValueError('Unknown workflow. Run list to see available workflows.')
            flow = FLOWS[args.name]
            run_task(flow['steps'], args.task, args.project, args.input, args.agent, flow)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Not completed: {error}', file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print('\nExited.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
