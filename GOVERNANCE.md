# Governance

This repository holds the canonical axiom registry for the Hapax operating environment. The whole constellation uses this registry.

## Authority

Single operator. There is no multi-stakeholder governance body. The single-operator axiom (weight 100) forecloses shared-decision structures.

## Mechanism

- Axioms in `axioms/registry.yaml`.
- Implications graduated across enforcement tiers (T0 block, T1 review, T2 warn, T3 lint).
- Precedents in `axioms/precedents/`, append-only with supersession tracking.

## Change process

Changes to `axioms/registry.yaml` always carry L-complexity. There is no review committee. The operator reviews changes against the constitutional canons: textualist, purposivist, absurdity, and omitted-case.

## Downstream

Other constellation repos consume this registry. Their `GOVERNANCE.md` redirects back here.
