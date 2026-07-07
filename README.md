<!-- hapax-sdlc:preamble:begin -->

# hapax-constitution

`hapax-constitution` anchors governance and public metadata for Hapax Systems repositories.

## Reader promise

Governance specification and repo-presentation authority for Hapax Systems, with a clear hapax-sdlc tooling boundary.

## Claim ceiling

Specification plus tooling split. Not the Hapax runtime. Not a blanket Apache or open-source statement for the whole repository.

## License and rights

Split posture: specification and publication metadata use CC BY-NC-ND; runnable hapax-sdlc tooling uses Apache-2.0. Do not describe the whole repository as Apache or open source.

Rendered summary: CC BY-NC-ND 4.0 (specification text, no derivatives). See `LICENSE`, `NOTICE.md`, `CITATION.cff`, and `.zenodo.json` for the authority surfaces.

## Public boundary

- Issues are redirect-only; no discussions, no pull requests accepted; see `CONTRIBUTING.md` and `SUPPORT.md`
- Public copy must use `hapax-systems` organization links for first-party Hapax repositories.
- Publication, weblog, RSS, social, DOI/archive, and other public fanout paths must route through the governed publication bus or a documented guarded legacy surface.
- Governance reference: https://github.com/hapax-systems/hapax-constitution

## Portfolio position

Anchor for repo metadata and governance. Defines axioms, implications, canons, and precedent records. Other first-party repos consume it through `hapax-sdlc`.

<!-- hapax-sdlc:preamble:end -->

# hapax-constitution

`hapax-constitution` is the governance specification and public metadata
authority for Hapax Systems repositories.

It defines axioms, implications, precedents, and renderers. These surfaces keep
repo presentation, license posture, support boundaries, and public claims
aligned across Hapax Systems projects. It is not the Hapax runtime. It is not a
blanket open-source license for the broader portfolio.

## What Lives Here

| Area | Purpose |
|---|---|
| `axioms/` | Constitutional axioms, implications, canons, and precedent material. |
| `domains/` | Domain-specific governance extensions and safety vocabulary. |
| `sdlc/render/` | Deterministic renderers for repo metadata and GitHub presentation files. |
| `sdlc/render/repos.yaml` | Canonical registry for repo names, licenses, claim ceilings, and reader promises. |
| `research/` | Research notes and landscape material that require their own claim gates before publication. |

## Public Metadata Pipeline

The `hapax-sdlc` renderer produces first-party repository presentation
artifacts from the registry:

| Artifact | Render Mode |
|---|---|
| `CITATION.cff` | full overwrite |
| `codemeta.json` | full overwrite |
| `.zenodo.json` | full overwrite |
| `NOTICE.md` | full overwrite |
| `CONTRIBUTING.md` | full overwrite |
| `SECURITY.md` | full overwrite |
| `SUPPORT.md` | full overwrite |
| `GOVERNANCE.md` | full overwrite |
| `.github/ISSUE_TEMPLATE/config.yml` | full overwrite |
| `README.md` preamble | section replacement |
| `hapax-systems/.github/profile/README.md` | organization profile |

```bash
python -m sdlc.render --repo hapax-council
python -m sdlc.render --all --check
python -m sdlc.render --org-profile --check
```

## License And Rights

This repository has a split posture. Specification and publication metadata
use CC BY-NC-ND unless a file says otherwise. Runnable `hapax-sdlc` tooling
uses Apache-2.0. Describe the tooling separately from the specification text.

## Claim Ceiling

Public copy may describe the governance spec, the renderer, the repo registry,
and the policy boundaries they encode. It must not imply that the constitution
alone ships the Hapax runtime, Reins write authority, a general lifecycle
framework, public support, or commercial service terms.

## Related Repositories

- [hapax-council](https://github.com/hapax-systems/hapax-council): source-visible research/runtime artifact.
- [agentgov](https://github.com/hapax-systems/agentgov): MIT adoption commons for portable governance hooks.
- [reins](https://github.com/hapax-systems/reins): source-available product front door for read and command-preview.
