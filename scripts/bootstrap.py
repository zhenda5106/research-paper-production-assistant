"""Fetch pinned public skill repositories without executing their contents."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'sources.lock.json'


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={'User-Agent': 'research-paper-production-assistant'})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record-hashes', action='store_true', help='Maintainer: record archive hashes on first acquisition')
    parser.add_argument('--source', action='append', choices=['nature', 'ideas', 'scientific', 'academic'], help='Fetch only this provider; repeat for multiple providers')
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text(encoding='utf-8'))
    for source in lock['sources']:
        if args.source and source['id'] not in args.source:
            continue
        target = ROOT / '.upstream' / source['id']
        receipt = target / '.rppa-receipt.json'
        if target.exists():
            if receipt.exists() and json.loads(receipt.read_text(encoding='utf-8')).get('commit') == source['commit']:
                print(f"Already present: {source['id']}")
                continue
            raise SystemExit(f'Refusing to overwrite an existing directory: {target}')
        expected = source.get('archive_sha256')
        if not expected and not args.record_hashes:
            raise SystemExit(f"No approved archive hash: {source['id']}")
        url = f"https://codeload.github.com/{source['repository']}/zip/{source['commit']}"
        payload = fetch(url)
        digest = hashlib.sha256(payload).hexdigest()
        if expected and digest != expected:
            raise SystemExit(f"Archive hash mismatch: {source['id']}; nothing extracted")
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = []
            for info in archive.infolist():
                parts = PurePosixPath(info.filename).parts
                if len(parts) < 2 or info.is_dir():
                    continue
                relative = PurePosixPath(*parts[1:])
                if any(str(relative).startswith(prefix) for prefix in source.get('excluded_prefixes', [])):
                    continue
                if relative.is_absolute() or any(p in ('..', '.') or ':' in p or '\\' in p for p in relative.parts):
                    raise SystemExit(f'Unsafe archive path: {info.filename}')
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise SystemExit(f'Symlink not accepted: {info.filename}')
                destination = target.joinpath(*relative.parts).resolve()
                if not destination.is_relative_to(target.resolve()):
                    raise SystemExit(f'Path escapes destination: {info.filename}')
                members.append((info, destination))
            for info, destination in members:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(info))
        source['archive_sha256'] = digest
        receipt.write_text(json.dumps({'commit': source['commit'], 'archive_sha256': digest}, indent=2) + '\n', encoding='utf-8')
        if args.record_hashes:
            LOCK.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"Fetched {source['id']}: {len(members)} files; SHA256 {digest}")


if __name__ == '__main__':
    main()
