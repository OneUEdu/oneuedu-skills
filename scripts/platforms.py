#!/usr/bin/env python3
"""Generate the root plugin manifests that let hosts install this repository directly, or check them."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://mcp.oneuedu.com/mcp'
NAME = 'one-u-education'
MARKETPLACE = 'oneuedu'
DISPLAY_NAME = 'One U Education'
# The course application's Forms and handoff cards only reach hosts the service has enrolled for secure UI
# (the reviewed ChatGPT plugin that oneuedu-plugin builds). Claude Code also carries it so users can save and
# review an application; other direct installs carry the remaining skills.
SKILLS = ('australian-immigration-planning', 'website-feedback')
SKILL_PATHS = ['./skills/' + name for name in SKILLS]
CLAUDE_SKILLS = ('australian-course-application',) + SKILLS
CLAUDE_SKILL_PATHS = ['./skills/' + name for name in CLAUDE_SKILLS]
DESCRIPTION = ('Australian study and migration help from One U Education: public course, school, occupation '
               'and visa data, personal migration planning and feedback through the official MCP server.')
AUTHOR = {'name': 'One U Education', 'url': 'https://www.oneuedu.com/'}
HOMEPAGE = 'https://www.oneuedu.com/'
DOCS = 'https://mcp.oneuedu.com/docs'
PRIVACY = 'https://mcp.oneuedu.com/privacy'
TERMS = 'https://www.oneuedu.com/en-US/data-terms'
REPOSITORY = 'https://github.com/OneUEdu/oneuedu-skills'
LICENSE = 'MIT'
KEYWORDS = ['australia', 'study', 'migration', 'visa', 'courses', 'mcp']
LOGO = './assets/logo.png'
GROK_KEYWORDS = ['one-u-education', 'one u education', 'oneuedu']
GROK_DOMAINS = ['oneuedu.com', 'mcp.oneuedu.com']
CATEGORY = 'Education & Research'
PROMPTS = [
    'Compare Melbourne carpentry courses for an onshore student by indicative fees, duration and entry requirements.',
    'Look up the carpenter occupation and show available skills assessment information and related courses.',
    'Help me compare ways to stay in Australia after my studies and save a planning dossier.',
]


def manifests():
    common = {'name': NAME, 'description': DESCRIPTION, 'author': AUTHOR, 'homepage': HOMEPAGE,
              'repository': REPOSITORY, 'keywords': KEYWORDS}
    return {
        '.mcp.json': {'mcpServers': {NAME: {'type': 'http', 'url': ENDPOINT}}},
        '.claude-plugin/plugin.json': {
            **common, 'license': LICENSE, 'displayName': DISPLAY_NAME, 'icon': LOGO, 'documentationUrl': DOCS,
            'supportUrl': DOCS, 'privacyPolicyUrl': PRIVACY, 'termsOfServiceUrl': TERMS},
        '.claude-plugin/marketplace.json': {
            'name': MARKETPLACE, 'owner': AUTHOR, 'description': DESCRIPTION,
            'plugins': [{'name': NAME, 'source': './', 'description': DESCRIPTION, 'skills': CLAUDE_SKILL_PATHS}]},
        '.codex-plugin/plugin.json': {
            **common, 'skills': SKILL_PATHS, 'mcpServers': './.mcp.json',
            'interface': {
                'displayName': DISPLAY_NAME, 'shortDescription': 'Australian courses & migration',
                'longDescription': (
                    'Search One U Education data on Australian CRICOS courses, schools and RTOs, ANZSCO '
                    'occupations, skills assessments, state nomination, SkillSelect invitation rounds and visa '
                    'fees, processing times and conditions. Public lookups need no account. With a connected One '
                    'U Education account, users can keep a personal migration-planning dossier, calculate '
                    'pathway options and read the results, and follow up on their own feedback. Information is '
                    'general, links to its source and does not establish personal eligibility.'),
                'developerName': AUTHOR['name'], 'category': CATEGORY, 'capabilities': ['Read', 'Write'],
                'websiteURL': HOMEPAGE, 'privacyPolicyURL': PRIVACY, 'termsOfServiceURL': TERMS,
                'defaultPrompt': PROMPTS, 'composerIcon': LOGO, 'logo': LOGO}},
        '.agents/plugins/marketplace.json': {
            'name': MARKETPLACE, 'interface': {'displayName': DISPLAY_NAME},
            'plugins': [{'name': NAME, 'source': {'source': 'local', 'path': './'},
                         'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'},
                         'category': CATEGORY}]},
        # Copilot reads this before .claude-plugin/ and ignores a marketplace entry's skill list.
        '.github/plugin/plugin.json': {**common, 'skills': SKILL_PATHS, 'mcpServers': './.mcp.json'},
        '.cursor-plugin/plugin.json': {
            **common, 'logo': LOGO, 'skills': SKILL_PATHS, 'mcpServers': './.mcp.json'},
        '.cursor-plugin/marketplace.json': {
            'name': MARKETPLACE, 'owner': {'name': AUTHOR['name']},
            'plugins': [{'name': NAME, 'source': './', 'description': DESCRIPTION}]},
        # Grok Build reads .grok-plugin/ before .claude-plugin/. The marketplace makes the repository a
        # self-contained source for `grok plugin install OneUEdu/oneuedu-skills`; keywords and domains stay
        # brand-scoped because Grok uses them to suggest the plugin.
        '.grok-plugin/plugin.json': {**common, 'skills': SKILL_PATHS, 'mcpServers': './.mcp.json'},
        '.grok-plugin/marketplace.json': {
            'name': MARKETPLACE, 'description': DESCRIPTION, 'owner': AUTHOR,
            'plugins': [{'name': NAME, 'source': './', 'description': DESCRIPTION, 'category': 'education',
                         'homepage': HOMEPAGE, 'keywords': GROK_KEYWORDS, 'domains': GROK_DOMAINS}]},
    }


def render(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def check(root=ROOT):
    """Require the generated manifests, their skill paths and logo to be committed as generated."""
    for path in CLAUDE_SKILL_PATHS:
        if not (root / path / 'SKILL.md').is_file():
            raise ValueError('Manifest skill is missing: ' + path)
    if not (root / LOGO).is_file() or (root / LOGO).is_symlink():
        raise ValueError('Missing plugin logo: ' + LOGO)
    stale = [name for name, data in manifests().items()
             if (root / name).is_symlink() or not (root / name).is_file() or (root / name).read_text() != render(data)]
    if stale:
        raise ValueError('Run python3 scripts/platforms.py to regenerate: ' + ', '.join(stale))
    return sorted(manifests())


def write(root=ROOT):
    for name, data in manifests().items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(render(data))
    return check(root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail instead of writing when a manifest is stale')
    args = parser.parse_args()
    try:
        files = check() if args.check else write()
    except ValueError as error:
        parser.exit(1, str(error) + '\n')
    print(('Checked: ' if args.check else 'Generated: ') + ', '.join(files))
