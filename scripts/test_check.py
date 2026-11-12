import shutil
import tempfile
import unittest
from pathlib import Path
from check import ROOT, validate
import platforms


class SkillSources(unittest.TestCase):
    def test_current_skills(self):
        self.assertEqual(['australian-course-application', 'australian-immigration-planning', 'website-feedback'], validate())

    def test_missing_reference_and_unsafe_files_are_rejected(self):
        for case in ('reference', 'name', 'dependency', 'symlink', 'private-file'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT / 'skills', root / 'skills')
                skill = root / 'skills/website-feedback'
                if case == 'reference':
                    (skill / 'references/setup.md').unlink()
                elif case == 'name':
                    entry = skill / 'SKILL.md'
                    entry.write_text(entry.read_text().replace('name: website-feedback', 'name: other'))
                elif case == 'dependency':
                    (skill / 'agents/openai.yaml').write_text('url: https://wrong.example')
                elif case == 'symlink':
                    (skill / 'external.md').symlink_to(root / 'outside')
                else:
                    (skill / '.env').write_text('TEST_ONLY=1')
                with self.assertRaises(ValueError):
                    validate(root)



class PlatformManifests(unittest.TestCase):
    def test_committed_manifests_are_generated_and_only_claude_carries_the_application(self):
        self.assertEqual(sorted(platforms.manifests()), platforms.check())
        self.assertNotIn('australian-course-application', platforms.SKILLS)
        self.assertLess(set(platforms.SKILLS), set(validate()))
        self.assertEqual(set(platforms.CLAUDE_SKILLS), set(validate()))
        claude = '.claude-plugin/marketplace.json'
        for name, data in platforms.manifests().items():
            text = platforms.render(data)
            if name == claude:
                self.assertEqual(platforms.CLAUDE_SKILL_PATHS, data['plugins'][0]['skills'])
            else:
                self.assertNotIn('australian-course-application', text, name)
            if 'skills' in data:
                self.assertEqual(platforms.SKILL_PATHS, data['skills'], name)

    def test_stale_or_missing_manifest_is_rejected(self):
        for case in ('stale', 'missing', 'skill'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT / 'skills', root / 'skills')
                shutil.copytree(ROOT / 'assets', root / 'assets')
                platforms.write(root)
                if case == 'stale':
                    (root / '.mcp.json').write_text('{}\n')
                elif case == 'missing':
                    (root / '.codex-plugin/plugin.json').unlink()
                else:
                    shutil.rmtree(root / 'skills/website-feedback')
                with self.assertRaises(ValueError):
                    platforms.check(root)


if __name__ == '__main__':
    unittest.main()
