# hapax-constitution

`hapax-constitution` is the governance specification and public metadata
authority for the Hapax Systems repository constellation.

It defines the axiom, implication, precedent, and renderer surfaces that keep
repo presentation, licensing, support boundaries, and public claims aligned
across Hapax Systems projects. It is not the Hapax runtime and it is not a
blanket open-source license for the broader portfolio.

## What Lives Here

| Area | Purpose |
|---|---|
| `axioms/` | Constitutional axioms, implications, canons, and precedent material. |
| `domains/` | Domain-specific governance extensions and safety vocabulary. |
| `sdlc/render/` | Deterministic renderers for repo metadata and GitHub presentation files. |
| `sdlc/render/repos.yaml` | Canonical registry for first-party repo naming, license posture, claim ceiling, and reader promise. |
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
are citation-oriented and non-commercial/no-derivatives unless a file states a
more specific license. Runnable `hapax-sdlc` tooling is Apache-2.0 and must be
described separately from the specification text.

## Claim Ceiling

Public copy may describe the governance specification, the renderer, the
repository registry, and the policy boundaries they encode. It must not imply
that the constitution alone ships the Hapax runtime, Reins write authority, a
general lifecycle framework, public support, or commercial service terms.

## Related Repositories

- [hapax-council](https://github.com/hapax-systems/hapax-council): source-visible research/runtime artifact.
- [agentgov](https://github.com/hapax-systems/agentgov): MIT adoption commons for portable governance hooks.
- [reins](https://github.com/hapax-systems/reins): source-available product front door for read and command-preview.
