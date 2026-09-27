# Contributing

Edit `bootstrap/codex_suite_bootstrap.md` for reusable suite changes. Keep the
README focused on helping a new user start, and keep client claims dated and
linked to official documentation. Templates should remain portable and contain
no personal data or repository-specific history.

Use Python 3.11+ and the standard library:

```text
python tools/validate_bootstrap.py
python -m unittest discover -s tests -v
git diff --check
```

The validator is read-only. Test helpers write only to disposable directories.
Tests exercise structural rejection and rendering contracts; they cannot prove
an AI will obey every prose instruction or that every client discovers an agent.
Use a real client smoke check before advertising new client compatibility.

Keep changes focused. Add tests for malformed artifacts, path safety, ownership,
version identity, optional-pack completeness, and other meaningful boundaries.
Avoid tests that merely search for a sentence in documentation.

## Release procedure

1. Change the suite version when changing any embedded payload. Update the
   README download name and CHANGELOG in the same revision.
2. Run the local checks, inspect every publishable path, and obtain independent
   assurance when setup safety or ownership changes.
3. Commit the exact reviewed files. Run GitHub validation on that commit.
4. Prepare a release directory from that commit: the bootstrap renamed to
   `codex-suite-bootstrap-v<version>.md`, `LICENSE`, and `SHA256SUMS.txt` containing
   hashes of those two files. Do not include fixtures, local reports, or caches.
5. Create a draft release and upload the verified assets. Compare the downloaded
   draft assets against the local hashes before publishing.
6. Publish only with owner authorization. Never replace a released artifact in
   place; create a new version. Report the tag, commit, asset hashes, validation,
   and any unverified client behavior.

Checksums are hashes of the release bytes. The validator also prints a separate
normalized manifest digest; do not use that digest as a download checksum.

CI runs with read-only repository permissions and pinned actions. Release
publication is manual. Keep the first distribution small; add installers,
marketplace packaging, or more automation only when repeated use demonstrates
a concrete need.
