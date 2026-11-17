import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rppa', ROOT / 'rppa.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class ToolboxTests(unittest.TestCase):
    def setUp(self):
        scratch = (ROOT / '.research/tests').resolve()
        assert scratch.is_relative_to(ROOT.resolve())
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.project = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def test_catalog_matches_locked_providers(self):
        lock = json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))
        expected = {(s['id'], p) for s in lock['sources'] for p in s['skills']}
        self.assertEqual(expected, {(s['source'], s['path']) for s in app.SKILLS.values()})

    def test_exact_upstream_name_alias(self):
        self.assertEqual(app.resolve('nature-reader')['id'], 'read')

    def test_missing_input_does_not_create_task(self):
        with self.assertRaises(ValueError):
            app.run_task(['read'], 'read', self.project, [self.project/'absent.pdf'])
        self.assertFalse((self.project/'.rppa').exists())

    def test_unprepared_dependency_has_actionable_error(self):
        with patch.object(app, 'ready', return_value=False), self.assertRaisesRegex(ValueError, 'setup read'):
            app.run_task(['read'], 'read', self.project)

    def test_revision_order_and_material_paths(self):
        material = self.project/'review comments.txt'
        material.write_text('comments', encoding='utf-8')
        with patch.object(app, 'ready', return_value=True):
            flow = app.FLOWS['revision']
            path = app.run_task(flow['steps'], 'Revise', self.project, [material], flow=flow)
        text = path.read_text(encoding='utf-8')
        self.assertIn(str(material), text)
        self.assertEqual(text.count(str(app.entry(app.SKILLS['review']))), 2)
        self.assertLess(text.index(str(app.entry(app.SKILLS['review']))), text.index(str(app.entry(app.SKILLS['write']))))

    def test_prompt_mode_never_launches_model(self):
        with patch.object(app, 'ready', return_value=True), patch.object(app.subprocess, 'run') as run:
            app.run_task(['polish'], 'Polish', self.project)
            run.assert_not_called()

    def test_codex_uses_argument_array_and_project(self):
        with patch.object(app, 'ready', return_value=True), patch.object(app.shutil, 'which', return_value='codex'), patch.object(app.subprocess, 'run') as run:
            task = app.run_task(['read'], 'Task with $() ; quotes', self.project, agent='codex')
            args = run.call_args.args[0]
            self.assertEqual(args[:3], ['codex', '-C', str(self.project)])
            self.assertIn(str(task), args[3])
            self.assertNotIn('shell', run.call_args.kwargs)

    def test_install_generates_both_hosts(self):
        with patch.object(app, 'ready', return_value=True):
            for host, folder in [('codex', '.agents'), ('claude', '.claude')]:
                app.install(self.project, host)
                files = list((self.project/folder/'skills').glob('*/SKILL.md'))
                self.assertEqual(len(files), 9)
                self.assertIn(str(app.entry(app.SKILLS['read'])), (self.project/folder/'skills/rppa-read/SKILL.md').read_text(encoding='utf-8'))

    def test_install_conflict_makes_no_partial_changes(self):
        target = self.project/'.agents/skills/rppa-review/SKILL.md'
        target.parent.mkdir(parents=True)
        target.write_text('user work', encoding='utf-8')
        with patch.object(app, 'ready', return_value=True), self.assertRaises(ValueError):
            app.install(self.project, 'codex')
        self.assertEqual(target.read_text(encoding='utf-8'), 'user work')
        self.assertFalse((self.project/'.agents/skills/rppa-read').exists())

    def test_init_preserves_user_brief(self):
        (self.project/'PROJECT.md').write_text('my brief', encoding='utf-8')
        app.init_project(self.project)
        self.assertEqual((self.project/'PROJECT.md').read_text(encoding='utf-8'), 'my brief')
        self.assertTrue((self.project/'outputs').is_dir())


if __name__ == '__main__':
    unittest.main()
