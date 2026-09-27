# Gabe's Portable Codex Suite

A shareable Markdown file that helps Codex set up consistent planning, reviews,
safety boundaries, pause/resume, and progress reporting inside your own project.
Choose a small core or add a workflow skill and an assurance reviewer during setup.

## Start in about a minute

1. Download `codex-suite-bootstrap-v1.1.2.md` and `LICENSE` from this repository's
   **Releases** page. Until a release is published, open
   [the bootstrap](bootstrap/codex_suite_bootstrap.md), choose **Raw**, and save it.
2. Open **your own project folder** in a local Codex client. Make that folder the
   primary project. Save the downloaded file where Codex can read it.
3. Give Codex the prompt below, with the file attached or its path identified.
4. Choose the core or optional pack, review the proposed changes, and approve the
   staged installation when satisfied. Then open `docs/codex/README.md` in your project.

```text
Read the entire Portable Codex Suite Bootstrap before acting.

Inspect this repository, prepare the target project profile, and explain the
core and core+workflow-assurance options so I can opt in or out.

After I choose, stage the proposed suite outside tracked repository paths.
Do not merge anything yet. Return the selected manifest, conflicts, validation
results, and proposed diff for my review.
```

When the proposed diff is acceptable:

```text
I approve merging exactly the staged suite paths using the selected capability
profile. Preserve all existing instructions and unrelated changes, run the
documented validation, and report rollback instructions.
```

Keep the bootstrap you installed; updates use it to verify existing managed
content. You can commit the generated suite to your own repository for teammates.
There is no shell installer to execute. Python is needed only for this package's
maintainer checks, not as a prerequisite for reading the bootstrap.

## Choose what fits

| Choice | Useful when | Tradeoff |
| --- | --- | --- |
| `core` | You want planning and safety guidance, usually work on small tasks, or already have suitable skills/agents | Seven generated paths; request tracked work and reviews through ordinary prompts |
| `core+workflow-assurance` | You regularly create/resume plans or need nonauthor milestone reviews | Nine generated paths; adds skill discovery context and reviewer token use when invoked |

The optional pack contains one tracked-work skill and one reviewer configured
for read-only work. Model and effort selection remain flexible. Both profiles
use the same approval rules. You can add or remove the complete pack later after
reviewing a staged diff.

The core generates `AGENTS.md` plus six files under `docs/codex/`: a user manual,
operating contract, project profile, model-routing guide, work guide, and plan
template. The optional files live under `.agents/skills/` and `.codex/agents/`.
Existing repository instructions and unrelated files are preserved.

## Which app should I use?

This is repository-local and does not require VS Code. Use a current local Codex
client with access to your project: the CLI, Codex in the desktop app, or the IDE
extension. In the terminal, start `codex` from your project folder; in an editor
or desktop app, select your project as the primary folder.

A normal ChatGPT web upload does not install files on your computer. Client
availability, permissions, and custom-agent support must be checked during setup.
If a capability is unavailable, Codex should explain the limitation rather than
claim successful activation. Start a fresh session after installation and ask
Codex to list the repository instructions and optional components it recognizes.

Official references: [projects and folders](https://learn.chatgpt.com/docs/projects),
[repository skills](https://learn.chatgpt.com/docs/build-skills), and
[custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Documentation reviewed 2026-09-27; client behavior may change.

## Everyday prompts

| Need | Prompt |
| --- | --- |
| Small fix | "Make the smallest root-cause fix and run focused validation." |
| Choose work | "Review the repository and recommend the next best bounded task." |
| Plan | "Create a tracked work plan with goals, exclusions, checkpoints, validation, and the exact next action." |
| Continue | "Proceed with one complete validated checkpoint." |
| Investigate | "Pause implementation and investigate the evidence contradicting our plan." |
| Resume | "Read the active plan, reconcile repository changes, and resume its next safe action." |
| Optional skill | "Use the codex-project-workflow skill to resume this active plan." |
| Independent review | "Have assurance_reviewer review this milestone without editing files." |

The normal default is one primary agent. Independent review is for meaningful
risks and milestones. Instructions guide behavior; actual sandbox and tool
permissions still control access. Verify the effective permissions before
assuming an agent is technically confined to read-only work.

Model names in the artifact are dated examples, not requirements. Use models
available in your account according to task complexity and consequence. The
optional reviewer does not pin a model.

## Updating and customization

Download a specific newer release and give Codex both that file and the previous
bootstrap. Ask it to inspect and stage an update. Keep your accepted
`project_profile.md`; it contains your repository's facts and owner decisions.
If managed instructions were locally changed, resolve the conflict before merging.

For an add/remove capability change, say which profile you want and follow the
same staging process. To remove the suite, request a reviewed removal plan that
preserves the target profile and all unrelated instructions and work.

Keep local facts in the target profile. Propose reusable policy changes in the
bootstrap so there is one maintained source. Do not copy this distribution
repository's contributor `AGENTS.md` into your own project.

## Sharing with a friend

Send the repository link and point them to **Start in about a minute**. For an
offline handoff, send only the released Markdown file and `LICENSE`; include
`SHA256SUMS.txt` if they want to verify the download. No account credentials,
personal settings, project-specific profile, or prior conversation is needed.

For a stable handoff, use a versioned release. A raw file on `main` can change.
Cloning this repository is useful for contributors; installing into your own
project still begins with the prompt above.

Release checksums describe the actual download bytes. The bootstrap's manifest
digest separately identifies the normalized embedded templates. They are
different hashes with different purposes. On Windows, compare a download with
`Get-FileHash <downloaded-file> -Algorithm SHA256`; on macOS use
`shasum -a 256 <downloaded-file>`; on Linux use `sha256sum <downloaded-file>`.

## Troubleshooting

- **Codex reads the wrong project:** select your target folder as primary, then
  start a new session there.
- **An existing instruction conflicts:** preserve it and review the proposed
  resolution. Setup must not silently replace it.
- **A skill or reviewer is unavailable:** check the selected profile and client
  discovery. Core guidance remains usable; required independent review still
  needs an available nonauthor agent or human.
- **Work feels too procedural:** use one-shot prompts for small changes and ask
  what concrete failure each extra workflow step prevents.
- **Setup cannot write a protected path:** keep its permissions intact and let
  Codex report the exact blocked operation and a safe next step.

## Maintenance and license

See [contribution instructions](CONTRIBUTING.md), [security reporting](SECURITY.md),
and [changes](CHANGELOG.md). This is an independent community project, not an
official OpenAI product.

Released under the [MIT license](LICENSE). You may use, adapt, and share the suite
subject to that license; preserve its notice when redistributing substantial copies.
