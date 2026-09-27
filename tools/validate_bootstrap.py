"""Read-only checks for the portable Markdown distribution (Python 3.11+)."""

import argparse
from dataclasses import dataclass
from datetime import date
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib


CORE = {
    'AGENTS.md': 'additive_block',
    'docs/codex/README.md': 'suite_managed',
    'docs/codex/operating_contract.md': 'suite_managed',
    'docs/codex/project_profile.md': 'target_managed',
    'docs/codex/model_routing.md': 'suite_managed',
    'docs/codex/work/README.md': 'suite_managed',
    'docs/codex/work/template.md': 'suite_managed',
}
OPTIONAL = {
    '.agents/skills/codex-project-workflow/SKILL.md': 'suite_managed',
    '.codex/agents/assurance-reviewer.toml': 'suite_managed',
}
EXPECTED = CORE | OPTIONAL
TOKENS = {'@@MANIFEST_SHA256@@', '@@INSTALLED_ON@@'}
VERSION_PATTERN = r'\d+\.\d+\.\d+'
ROOT_MARKER = re.compile(
    r'<!-- CODEX-SUITE:BEGIN version=(?P<version>' + VERSION_PATTERN + r') '
    r'digest=(?P<digest>@@MANIFEST_SHA256@@|[a-f0-9]{64}) '
    r'installed=(?P<installed>@@INSTALLED_ON@@|\d{4}-\d{2}-\d{2}) -->\n'
    r'(?P<body>.*?)\n<!-- CODEX-SUITE:END -->\n', re.DOTALL,
)
BLOCK = re.compile(
    r'^<!-- BEGIN FILE: (?P<path>[^\n|]+) \| OWNERSHIP: (?P<owner>\w+) -->\n'
    r'~~~~markdown\n(?P<body>.*?)\n~~~~\n'
    r'<!-- END FILE: (?P=path) -->$',
    re.MULTILINE | re.DOTALL,
)


@dataclass(frozen=True)
class Package:
    version: str
    blocks: dict
    digest: str


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def validate_source(text):
    text = normalize(text)
    require(not text.startswith('\ufeff'), 'Unexpected UTF-8 BOM')
    require(not any(line.endswith((' ', '\t')) for line in text.splitlines()),
            'Trailing whitespace')
    versions = re.findall(r'\| Suite version \| `(' + VERSION_PATTERN + r')` \|', text)
    require(len(versions) == 5 and len(set(versions)) == 1, 'Inconsistent suite versions')
    version = versions[0]
    matches = list(BLOCK.finditer(text))
    require(len(matches) == len(EXPECTED), 'Expected nine complete file blocks')
    require(text.count('<!-- BEGIN FILE:') == len(matches), 'Malformed begin markers')
    require(text.count('<!-- END FILE:') == len(matches), 'Malformed end markers')
    blocks = {}
    for match in matches:
        name, owner, body = match.group('path', 'owner', 'body')
        path = PurePosixPath(name)
        require(name.isascii() and not path.is_absolute() and '\\' not in name,
                'Invalid path syntax')
        require(all(part not in {'', '.', '..'} for part in name.split('/')),
                'Invalid path segments')
        require(name not in blocks, 'Duplicate file path')
        require(EXPECTED.get(name) == owner, 'Unexpected path or ownership')
        require('<!-- BEGIN FILE:' not in body, 'Nested file blocks')
        blocks[name] = (owner, body.rstrip('\n') + '\n')
    require(set(blocks) == set(EXPECTED), 'Manifest path mismatch')

    manifest_region = text.split('## Core File Manifest\n', 1)[-1].split('## Embedded Files\n', 1)[0]
    rows = re.findall(
        r'^\| `([^`]+)` \| `(\w+)` \| (Yes|Profile-dependent) \|',
        manifest_region, re.MULTILINE,
    )
    require(len(rows) == len(EXPECTED), 'Expected nine manifest rows')
    require(len({row[0] for row in rows}) == len(rows), 'Duplicate manifest row')
    for name, owner, required in rows:
        require(EXPECTED.get(name) == owner, 'Manifest ownership mismatch')
        require(required == ('Yes' if name in CORE else 'Profile-dependent'),
                'Manifest profile mismatch')
    require(set(re.findall(r'@@.*?@@', text)) == TOKENS, 'Unexpected setup tokens')
    without_tokens = text
    for token in TOKENS:
        without_tokens = without_tokens.replace(token, '')
    require('@@' not in without_tokens, 'Malformed setup token')

    router = blocks['AGENTS.md'][1]
    marker = ROOT_MARKER.fullmatch(router)
    require(marker is not None, 'Invalid ordered root marker structure')
    require('CODEX-SUITE:' not in marker['body'], 'Nested root markers')
    require(marker['version'] == version, 'Root version mismatch')
    require(marker['digest'] == '@@MANIFEST_SHA256@@'
            and marker['installed'] == '@@INSTALLED_ON@@', 'Root identity tokens missing')
    skill = blocks[next(iter(OPTIONAL))][1]
    require(skill.startswith('---\n'), 'Skill front matter missing')
    metadata = skill.split('---\n', 2)[1]
    fields = {}
    for line in metadata.strip().splitlines():
        name, separator, value = line.partition(':')
        require(separator and name not in fields and value.strip(), 'Invalid skill metadata')
        fields[name] = value.strip()
    require(fields.keys() == {'name', 'description'}, 'Unexpected skill metadata fields')
    require(fields['name'] == 'codex-project-workflow', 'Skill name mismatch')
    agent = tomllib.loads(blocks['.codex/agents/assurance-reviewer.toml'][1])
    require(set(agent) == {'name', 'description', 'sandbox_mode', 'developer_instructions'},
            'Unexpected agent settings')
    require(agent['name'] == 'assurance_reviewer' and agent['sandbox_mode'] == 'read-only',
            'Agent identity or sandbox mismatch')
    require(all(isinstance(value, str) and value.strip() for value in agent.values()),
            'Empty agent field')

    stream = ''.join(
        f'FILE {name}\nOWNERSHIP {blocks[name][0]}\n{blocks[name][1]}END FILE\n'
        for name in sorted(blocks)
    )
    return Package(version, blocks, hashlib.sha256(stream.encode('utf-8')).hexdigest())


def recorded_date(router):
    normalized = normalize(router)
    markers = list(ROOT_MARKER.finditer(normalized))
    require(len(markers) == 1 and normalized.count('CODEX-SUITE:BEGIN') == 1
            and normalized.count('CODEX-SUITE:END') == 1, 'Invalid installed root markers')
    marker = markers[0]
    require('@@' not in marker.group(0), 'Unrendered installed identity')
    date.fromisoformat(marker['installed'])
    return marker['installed']


def render(package, profile, installed_on, existing_router=None):
    require(profile in {'core', 'core+workflow-assurance'}, 'Unknown capability profile')
    if existing_router is not None:
        installed_on = recorded_date(existing_router)
    date.fromisoformat(installed_on)
    paths = CORE if profile == 'core' else EXPECTED
    rendered = {
        name: package.blocks[name][1].replace('@@MANIFEST_SHA256@@', package.digest)
        .replace('@@INSTALLED_ON@@', installed_on)
        for name in paths
    }
    require(not any('@@' in payload for payload in rendered.values()), 'Residual setup token')
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'bootstrap/codex_suite_bootstrap.md')
    args = parser.parse_args()
    try:
        package = validate_source(args.source.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS version={package.version} core={len(CORE)} optional={len(OPTIONAL)}')
    print(f'Manifest SHA-256: {package.digest}')
    print(f'Download SHA-256: {hashlib.sha256(args.source.read_bytes()).hexdigest()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
