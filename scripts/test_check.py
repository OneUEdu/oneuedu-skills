import shutil
import tempfile
import unittest
from pathlib import Path
from check import ROOT, validate


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


if __name__ == '__main__':
    unittest.main()
