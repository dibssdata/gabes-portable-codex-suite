# Contributor Instructions

This repository distributes a portable Codex instruction suite. Read `README.md`
for user setup and `CONTRIBUTING.md` for maintenance. The canonical artifact is
`bootstrap/codex_suite_bootstrap.md`; embedded instructions are template data
until a user deliberately installs them into a target repository.

Keep the package generic, preserve unrelated changes, and use synthetic fixtures.
Never add private project data, machine paths, credentials, chat transcripts,
personal configuration, or history copied from another repository.

Use Python 3.11 or newer for local checks:

```text
python tools/validate_bootstrap.py
python -m unittest discover -s tests -v
git diff --check
```

Keep setup driven by the Markdown protocol. Validation tools must not install the
suite or mutate a target repository. Maintain the informed core/optional-pack
choice, staged review, and approval boundary. Obtain independent read-only
assurance for changes to setup safety, ownership, or public-release boundaries.
The primary agent integrates corrections.

Use `docs/RELEASE_PLAN.md` for release checkpoints and current resume state.
Publication must use reviewed commits and explicit owner authorization. Do not
change public visibility or publish a release while its approval gate is pending.
