from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.validate_bootstrap import CORE, OPTIONAL, recorded_date, render, validate_source


SOURCE = Path(__file__).resolve().parents[1] / 'bootstrap/codex_suite_bootstrap.md'


class BootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding='utf-8')
        cls.package = validate_source(cls.source)

    def test_release_identity(self):
        self.assertEqual(self.package.version, '1.1.2')
        self.assertEqual(self.package.digest,
                         '9afd96adbdc139381e4ca850610edc28c854bf5c50757ea95508f777340fe07d')

    def test_line_endings_do_not_change_manifest_identity(self):
        windows = self.source.replace('\n', '\r\n')
        self.assertEqual(validate_source(windows).digest, self.package.digest)

    def test_profiles_render_all_or_none_optional_paths(self):
        for profile, expected in [('core', 7), ('core+workflow-assurance', 9)]:
            with self.subTest(profile=profile), TemporaryDirectory() as directory:
                rendered = render(self.package, profile, '2026-09-27')
                self.assertEqual(len(rendered), expected)
                self.assertTrue(set(CORE).issubset(rendered))
                self.assertEqual(len(set(rendered) & set(OPTIONAL)), expected - 7)
                for name, payload in rendered.items():
                    self.assertNotIn('@@', payload)
                    target = Path(directory) / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(payload, encoding='utf-8', newline='\n')
                actual = {item.relative_to(directory).as_posix()
                          for item in Path(directory).rglob('*') if item.is_file()}
                self.assertEqual(actual, set(rendered))

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            render(self.package, 'skill-only', '2026-09-27')

    def test_same_version_change_gets_different_digest(self):
        changed = self.source.replace('## Codex Suite\n', '## Changed Suite\n', 1)
        package = validate_source(changed)
        self.assertEqual(package.version, self.package.version)
        self.assertNotEqual(package.digest, self.package.digest)

    def test_malformed_or_duplicate_markers_rejected(self):
        cases = [
            self.source.replace('<!-- END FILE: AGENTS.md -->', '<!-- END FILE: other.md -->'),
            self.source + '\n<!-- BEGIN FILE: extra.md | OWNERSHIP: suite_managed -->\n',
            self.source.replace('<!-- CODEX-SUITE:END -->', ''),
        ]
        for candidate in cases:
            with self.subTest(candidate_length=len(candidate)), self.assertRaises(ValueError):
                validate_source(candidate)

    def test_unsafe_or_duplicate_paths_rejected(self):
        for name in ['../outside.md', '/absolute.md', 'C:/absolute.md',
                     'docs/../outside.md', 'docs\\outside.md', 'AGENTS.md']:
            changed = self.source.replace('docs/codex/work/template.md', name)
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_source(changed)

    def test_missing_optional_block_rejected(self):
        start = self.source.index('<!-- BEGIN FILE: .codex/agents/')
        end = self.source.index('<!-- END FILE: .codex/agents/assurance-reviewer.toml -->')
        end += len('<!-- END FILE: .codex/agents/assurance-reviewer.toml -->')
        with self.assertRaises(ValueError):
            validate_source(self.source[:start] + self.source[end:])

    def test_manifest_and_ownership_changes_rejected(self):
        candidates = [
            self.source.replace('OWNERSHIP: target_managed', 'OWNERSHIP: suite_managed'),
            self.source.replace('| Profile-dependent |', '| Yes |', 1),
            self.source.replace('@@INSTALLED_ON@@', '@@UNDECLARED@@'),
        ]
        for candidate in candidates:
            with self.subTest(candidate_length=len(candidate)), self.assertRaises(ValueError):
                validate_source(candidate)

    def test_agent_cannot_silently_gain_settings_or_write_access(self):
        for candidate in [
            self.source.replace('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"'),
            self.source.replace('name = "assurance_reviewer"',
                                'name = "assurance_reviewer"\nmodel = "example-model"'),
        ]:
            with self.subTest(candidate_length=len(candidate)), self.assertRaises(ValueError):
                validate_source(candidate)

    def test_repeated_render_is_identical_with_original_installation_date(self):
        first = render(self.package, 'core+workflow-assurance', '2026-09-27')
        second = render(self.package, 'core+workflow-assurance', '2026-09-27')
        self.assertEqual(first, second)

    def test_replay_on_later_day_reuses_recorded_date(self):
        first = render(self.package, 'core', '2026-09-27')
        later = render(self.package, 'core', '2026-10-01', first['AGENTS.md'])
        self.assertEqual(later, first)
        with_pack = render(self.package, 'core+workflow-assurance', '2026-10-01',
                           first['AGENTS.md'])
        self.assertEqual({name: with_pack[name] for name in CORE}, first)

    def test_order_and_required_root_identity_fields(self):
        start = '<!-- CODEX-SUITE:BEGIN version=1.1.2 digest=@@MANIFEST_SHA256@@ installed=@@INSTALLED_ON@@ -->'
        end = '<!-- CODEX-SUITE:END -->'
        candidates = [
            self.source.replace(start, 'SWAP_MARKER').replace(end, start).replace('SWAP_MARKER', end),
            self.source.replace(' digest=@@MANIFEST_SHA256@@', ''),
            self.source.replace(' installed=@@INSTALLED_ON@@', ''),
        ]
        for candidate in candidates:
            with self.subTest(candidate_length=len(candidate)), self.assertRaises(ValueError):
                validate_source(candidate)

    def test_lowercase_and_unterminated_tokens_rejected(self):
        for token in ['@@unknown@@', '@@Unknown-Token@@', '@@unfinished']:
            with self.subTest(token=token), self.assertRaises(ValueError):
                validate_source(self.source.replace('## Codex Suite', '## Codex Suite ' + token))

    def test_missing_conflicting_and_invalid_recorded_dates_rejected(self):
        installed = render(self.package, 'core', '2026-09-27')['AGENTS.md']
        candidates = [
            installed.replace(' installed=2026-09-27', ''),
            installed + installed.replace('2026-09-27', '2026-10-01'),
            installed.replace('2026-09-27', '2026-02-30'),
        ]
        for candidate in candidates:
            with self.subTest(candidate_length=len(candidate)), self.assertRaises(ValueError):
                recorded_date(candidate)


if __name__ == '__main__':
    unittest.main()
