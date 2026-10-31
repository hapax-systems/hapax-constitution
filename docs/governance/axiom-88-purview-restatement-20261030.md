# Axiom 88: correct-forward of #98

R-2 rows `axiom:interpersonal_transparency`, `implication:it-inference-001`, and
`implication:it-backend-001` bind this slice, its declarations, tests and this record.
Accepted inventory (vault-relative):
`30-areas/hapax/frame/governance-lineage-inventory-20261030/R2-SIGNABLE-20261030T080805Z-INTERPERSONAL-TRANSPARENCY.md`,
SHA-256 `a6406d1a254c0ef737d370c93af0e9f759b41e4476af10dcb3456fec8000bd28`.
INDEX v2 SHA-256 `6ba934f9de2d71146ed8d05d72c1384810d9893c3e8457b17346c53268218fea`.
These bindings identify accepted lineage; they do not assert runtime activation.

The operator's 2026-10-30 04:40:45Z ruling rejects `it-public-role-001`.
This correct-forward replaces #98's public-figure carve-out with the bounded
purview now reviewed and merged in Council. It copies the axiom text and
structured purview from Council `b130753fff967191337311d0b0eec90a0eb256b4` exactly.
Users of the system and household or studio sensor subjects remain protected;
public-interest persons' public conduct and discourse is outside that purview.
Household or studio sensor data stays protected whoever the subject is, including
persons of public interest. Modeling behavior or outcomes does not remove that
protection. Opt-in, inspection, revocation and purge rights remain unchanged.

`purview` is a declarative jurisdiction record, not a runtime exemption. This
slice does not change consumers, publish an evaluation of a person, or certify
runtime behavior. Independent review and the governed release remain required.

## Superseded registry text

Verbatim from constitution `c0a3f81dac89d88473ffa51f520ab29ccecab52e` (#98).
R-2 row `axiom:interpersonal_transparency`. Historical, not operative authority:

```yaml
  - id: interpersonal_transparency
    text: >
      The system must not maintain persistent state about any non-operator
      person who uses, interacts with, or is perceived by the system, without
      an active consent contract. A consent contract requires explicit opt-in
      by the subject, grants the subject inspection access to all data the
      system holds about them, and is revocable by either party at any time.
      Upon revocation, the system purges all subject-specific persistent
      state. This axiom does not govern attention to public figures,
      organizations, or their public statements in matters of public
      discourse: the system may record their public positions and publish its
      own sourced, revisable evaluation of them, each statement remaining open
      to requested revision and correction via unpaid THIEH.
    weight: 88
    type: hardcoded
    created: "2026-03-13"
    status: active
    supersedes:
    scope: constitutional
    domain:
```

## Recheck

In the repository's uv environment:

```sh
uv run --no-sync pytest tests/test_axiom_88_purview.py -q --basetemp=/tmp/pytest-cx-teal
uv run --no-sync python sdlc/consistency_check.py --json --check-resolutions
```

The test pins the reviewed Council text digest and the exact predecessor block,
checks the subject rights and mixed-data declaration, and preserves other fields.
Source-removal controls are recorded in the linked task's evidence packet.
