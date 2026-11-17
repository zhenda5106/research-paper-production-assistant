"""Check the local integration without executing upstream code."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    lock = json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))
    errors = []
    count = 0
    for source in lock['sources']:
        base = ROOT / '.upstream' / source['id']
        receipt = base / '.rppa-receipt.json'
        if not re.fullmatch(r'[0-9a-f]{40}', source['commit']):
            errors.append(f"Invalid commit: {source['id']}")
        if not re.fullmatch(r'[0-9a-f]{64}', source.get('archive_sha256', '')):
            errors.append(f"Missing archive hash: {source['id']}")
        if not receipt.exists():
            errors.append(f"Missing snapshot: {source['id']}")
            continue
        actual = json.loads(receipt.read_text(encoding='utf-8'))
        for key in ('commit', 'archive_sha256'):
            if actual.get(key) != source.get(key):
                errors.append(f"Receipt mismatch: {source['id']} {key}")
        if not any((base / name).exists() for name in ('LICENSE', 'LICENSE.md')):
            errors.append(f"Missing license: {source['id']}")
        for excluded in source.get('excluded_prefixes', []):
            if (base / excluded).exists():
                errors.append(f'Excluded assets present: {excluded}')
        for skill in source['skills']:
            folder = base / skill
            entry = folder / 'SKILL.md'
            count += 1
            if not entry.exists():
                errors.append(f'Missing skill: {entry}')
                continue
            if not entry.read_text(encoding='utf-8').startswith('---'):
                errors.append(f'Missing frontmatter: {entry}')
            if source['id'] == 'nature':
                manifest = folder / 'manifest.yaml'
                if not manifest.exists():
                    errors.append(f'Missing manifest: {manifest}')
                    continue
                # Manifest resource paths use plain relative YAML scalars.
                for line in manifest.read_text(encoding='utf-8').splitlines():
                    match = re.match(r'^\s*(?:-\s+|[\w-]+:\s+)[\"\']?((?:\.\./nature-shared/|static/|references/|scripts/)[^\s#\"\']+\.(?:md|py|yaml|json|R))[\"\']?\s*(?:#.*)?$', line)
                    if match:
                        rel = match.group(1).strip('"\'')
                        if not (folder / rel).exists():
                            errors.append(f'Missing manifest resource: {skill}/{rel}')
    routing = (ROOT / 'skills/research-paper-production-assistant/references/routing.md').read_text(encoding='utf-8')
    for rel in re.findall(r'`(\.upstream/[^`]+/SKILL.md)`', routing):
        if not (ROOT / rel).exists():
            errors.append(f'Missing routing target: {rel}')
    for rel in ('shared', 'scripts'):
        if not (ROOT / '.upstream/academic' / rel).is_dir():
            errors.append(f'Missing academic shared dependency: {rel}')
    if count != 9:
        errors.append(f'Expected 9 selected skills; found {count}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {count} selected skills, 4 pinned snapshots, licenses, routing, Nature manifest resources and exclusions.')
    print('Structural validation only; no upstream scripts or scientific workflows executed.')


if __name__ == '__main__':
    main()
