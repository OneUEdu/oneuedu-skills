#!/usr/bin/env python3
"""Validate skill discovery, bundled references and existing MCP dependencies offline."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://mcp.oneuedu.com/mcp'


def validate(root=ROOT):
    skills = root / 'skills'
    if skills.is_symlink() or not skills.is_dir():
        raise ValueError('A real skills directory is required')
    names = []
    for skill in sorted(skills.iterdir()):
        if skill.is_symlink() or not skill.is_dir() or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', skill.name):
            raise ValueError('Invalid skill directory')
        entry = skill / 'SKILL.md'
        if not entry.is_file():
            raise ValueError('Missing SKILL.md: ' + skill.name)
        text = entry.read_text()
        header = text.split('\n---\n', 1)[0]
        if not header.startswith('---\nname: ' + skill.name + '\n') or not re.search(r'^description: \S.+$', header, re.M):
            raise ValueError('Missing skill name/description: ' + skill.name)
        dependency = skill / 'agents/openai.yaml'
        if not dependency.is_file() or ENDPOINT not in dependency.read_text():
            raise ValueError('Missing official MCP dependency: ' + skill.name)
        for path in skill.rglob('*'):
            if path.is_symlink():
                raise ValueError('Symlinks are not distributable')
            if not path.is_file():
                continue
            if path.suffix not in ('.md', '.yaml', '.yml'):
                raise ValueError('Unreviewed skill file: ' + path.name)
            if path.suffix != '.md':
                continue
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                resolved = (path.parent / target.split('#')[0]).resolve()
                if not resolved.is_relative_to(skill.resolve()) or not resolved.is_file():
                    raise ValueError('Broken or external relative reference: ' + target)
        names.append(skill.name)
    if not names:
        raise ValueError('No skills found')
    return names


if __name__ == '__main__':
    print('Validated: ' + ', '.join(validate()))
