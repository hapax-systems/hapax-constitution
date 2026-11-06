<!-- hapax-sdlc:preamble:begin -->
<!-- hapax-public:surface=github.repo.hapax-constitution.readme.preamble:begin -->

# hapax-constitution

`hapax-constitution` anchors governance and public metadata for **Hapax Research Lab** repositories ([hapaxresearch.com](https://hapaxresearch.com)).

## Reader promise

Governance specification and repo-presentation authority for Hapax Research Lab, with a clear hapax-sdlc tooling boundary.

## Reader value

Gives reviewers one auditable source for names, licenses, support boundaries, and claim ceilings, reducing public-surface drift.

## Claim ceiling

Specification plus tooling split. Not the Hapax runtime. Not a blanket Apache or open-source statement for the whole repository.

## License and rights

Split posture: specification and publication metadata use CC BY-NC-ND 4.0; runnable hapax-sdlc tooling uses Apache-2.0. Do not describe the whole repository as Apache or open source.

Rendered summary: CC BY-NC-ND 4.0 (specification text, no derivatives; runnable hapax-sdlc tooling under Apache-2.0). See `LICENSE`, `NOTICE.md`, `CITATION.cff`, and `.zenodo.json` for the authority surfaces.

## Public boundary

- Issues are redirect-only; no discussions, no pull requests accepted; see `CONTRIBUTING.md` and `SUPPORT.md`
- Published by **Hapax Research Lab** (`hrl-han`, [hapaxresearch.com](https://hapaxresearch.com)). Legal entity (as filed): Hapax Research LLC, organized in Wyoming on 2026-05-10, filing ID 2026-001973400.
- Security disclosures and factual correction proposals: `hrl-han@hapaxresearch.com` (see `SECURITY.md` and [hapaxresearch.com/about/#contact](https://hapaxresearch.com/about/#contact)). The network commits to receipt, retention and published correction. It promises no response time.
- Public copy uses `hapax-systems` organization links for first-party repositories; README text is orientation rather than a live runtime receipt.
- Governance reference: https://github.com/hapax-systems/hapax-constitution

## Portfolio position

Anchor for repository metadata and governance across Hapax Research Lab. Defines axioms, implications, canons, and precedent records consumed through `hapax-sdlc`.

<!-- hapax-public:surface=github.repo.hapax-constitution.readme.preamble:end -->
<!-- hapax-sdlc:preamble:end -->

`hapax-constitution` is the governance specification and public metadata
authority for Hapax Research Lab repositories.

It defines axioms, implications, precedents, and renderers. These surfaces keep
repo presentation, license posture, support boundaries, reader value, and
public claims aligned across Hapax Research Lab projects. It is not the Hapax
runtime. It is not a blanket open-source license for the broader portfolio.

## What Lives Here

| Area | Purpose | Reader value |
|---|---|---|
| `axioms/` | Constitutional axioms, implications, canons, and precedent material. | Lets reviewers inspect the governance commitments that other repos cite. |
| `domains/` | Domain-specific governance extensions and safety vocabulary. | Keeps specialized boundaries explicit instead of scattered through local prose. |
| `sdlc/render/` | Deterministic renderers for repo metadata and GitHub presentation files. | Reduces public-copy drift by generating repeated frontmatter from one authority. |
| `sdlc/render/repos.yaml` | Canonical registry for repo names, licenses, claim ceilings, reader promises, and reader value. | Gives auditors one place to check how each repo is named, positioned, and bounded. |
| `research/` | Research notes and landscape material that require their own claim gates before publication. | Separates exploratory material from public claims until evidence and review are current. |

## Public Metadata Pipeline

The `hapax-sdlc` renderer produces first-party repository presentation
artifacts from the registry:

| Artifact | Render Mode | Reader value |
|---|---|---|
| `CITATION.cff` | full overwrite | Keeps citation metadata consistent with the repo's actual posture. |
| `codemeta.json` | full overwrite | Gives machine-readable consumers the same identity and license boundary. |
| `.zenodo.json` | full overwrite | Carries archive metadata without implying broader runtime rights. |
| `NOTICE.md` | full overwrite | States reader promise, reader value, claim ceiling, and license authority in one stable file. |
| `CONTRIBUTING.md` | full overwrite | Makes contribution refusal or redirect policy consistent across repos. |
| `SECURITY.md` | full overwrite | Publishes a disclosure path without turning GitHub into support intake. |
| `SUPPORT.md` | full overwrite | Separates inspection/citation from support, SLA, or commercial promises. |
| `GOVERNANCE.md` | full overwrite | Points each repo back to the appropriate governance authority. |
| `.github/ISSUE_TEMPLATE/config.yml` | full overwrite | Keeps Issues as redirect surfaces instead of accidental queues. |
| `README.md` preamble | section replacement | Preserves repo-specific bodies while keeping public frontmatter aligned. |
| `hapax-systems/.github/profile/README.md` | organization profile | Presents portfolio value and license boundaries from the same registry. |

```bash
python -m sdlc.render --repo hapax-constitution
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

## Related Surfaces

- [Hapax Research Lab](https://hapaxresearch.com): public research portal, published records, and identity verification surface.
- [reins](https://github.com/hapax-systems/reins): source-available product front door for read and command-preview.
- [hapax-spine](https://github.com/hapax-systems/hapax-spine): source-available runtime mechanism layer behind Reins.
- [hapax-research-ledger](https://github.com/hapax-systems/hapax-research-ledger): public-domain numeric evidence ledger.

---

*HACA-C v0.3.15, the lab's draft rule for labelling machine-made text, not an external certification. No request to a natural person to approve the final wording, and no such approval, was found in hrl-han's sending, review and coordination records when the text was released. hrl-han releases a text once its checking is complete, under a standing rule that hrl-han's principal, who is not named in this text, adopted before the text was drafted. Review record: https://hapaxresearch.com/review-record/ (open to anyone). This label records how the text was made; it does not certify that the text is true. An unaltered record can contain false claims or miss relevant events.*
