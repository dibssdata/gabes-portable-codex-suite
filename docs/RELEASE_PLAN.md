# First Public Distribution

## Outcome and boundary

Deliver Gabe's Portable Codex Suite as a self-contained, MIT-licensed repository
and a versioned Markdown download with a checksum. A friend can start from the
README, choose the core or optional capability pack, and review installation.

The repository has independent Git history and only explicitly reviewed generic
files. No personal configurations, private project data, inherited Git objects,
installer, plugin, or account credentials belong in this distribution.

## Checkpoints

| Step | Deliverable | Status | Recommended capability |
| --- | --- | --- | --- |
| 1 | Name, owner, license, and export boundary | completed | Everyday primary / medium |
| 2 | Independent local repository and single-artifact export | completed | Everyday primary / medium |
| 3 | User README, prompts, and contribution guidance | completed | Everyday primary / medium |
| 4 | Read-only validator and CI | completed | Everyday primary / high |
| 5 | Both-profile fixtures and failure cases | completed | Everyday primary / high |
| 6 | Independent privacy and release assurance | completed | Complex primary / high + nonauthor reviewer |
| 7 | Private remote and hosted validation | in_progress | Everyday primary / medium |
| 8 | Public visibility and versioned release | pending | Complex primary / high + owner approval |

## Decisions

- Display name: Gabe's Portable Codex Suite.
- Repository name: `gabes-portable-codex-suite`.
- License: MIT, copyright attributed to Gabe.
- Export: one generic bootstrap; public supporting files are written for this repository.
- Publishing sequence: reviewed local tree, private remote, hosted checks, then
  public visibility and release after the owner approves the concrete result.
- Commit metadata uses the account's GitHub no-reply address.

## Validation and assurance

Local checks pass: 15 unit tests, both-profile rendering, an empty Git fixture,
template navigation, malformed input and unsafe-path rejection, version/digest
identity, and nine simulated rollback boundaries. The simulations model the
written contract; they do not prove autonomous agent behavior.

All 13 staged paths pass private-data and secret scans. The only absolute-path
scan exception is a synthetic drive-path rejection fixture in the tests.
The repository has an independent object store with no inherited commits,
alternates, or submodules.

Independent read-only assurance passed after corrections for recorded-date reuse,
removal/recovery, full root-marker identity checks, and filesystem containment.
Reviewer Lagrange attested nonauthorship and no edits. The reviewed package tree
was `f1f504f4b342d77d4e90f6f393caaf19167ee39f`; this entry records its result.
Eight full-removal recovery simulations preserve profiles, plans, and root text.
Windows denied symlink fixture creation (1314), so live redirected-ancestor
verification remains unverified. Custom-agent client discovery also remains a
target-setup check. These limits do not imply runtime sandbox guarantees.

Version `1.1.2` manifest digest:
`9afd96adbdc139381e4ca850610edc28c854bf5c50757ea95508f777340fe07d`.
Hosted validation and public-release authorization remain pending.

## Resume

Push only the reviewed files to the new private remote, verify hosted checks and
draft-release asset hashes, then prepare the exact public-release approval summary.
Do not mark public distribution complete while visibility or release is pending.
