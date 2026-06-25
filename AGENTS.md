# hapax-constitution Agent Instructions

This repository belongs to Hapax and must remain under `hapax-systems`. Do not
create, move, or point Hapax repository automation at `ryanklee`.

## Review Guidelines

External GitHub App reviewers such as CodeRabbit, Claude, and Codex are
advisory. Their comments can be useful input, but they are not authoritative
merge or release gates unless a governed Hapax task explicitly routes them into
the review process.

- Keep Codecov and Semgrep advisory signal sources unless a governed task
  promotes a specific stable aggregate context.
- Preserve the `all-green` aggregate for branch protection and release tooling.
- Do not print or persist plaintext secrets; use GitHub Secrets, `pass`, or
  `hapax-secrets`.
- Treat axiom, implication, precedent, and schema edits as governance changes;
  validate YAML and consistency checks before marking a PR ready.
