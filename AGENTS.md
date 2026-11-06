# hapax-constitution Agent Instructions

This repository is maintained by **Hapax Research Lab** (`hrl-han@hapaxresearch.com`)
and must remain under the `hapax-systems` GitHub organization. Do not create,
move, or point Hapax Research Lab repository automation at personal accounts
outside `hapax-systems`.

## Review Guidelines

External GitHub App reviewers such as CodeRabbit, Claude, and Codex are
advisory. Their comments can be useful input, but they are not authoritative
merge or release gates unless a governed Hapax Research Lab task explicitly
routes them into the review process.

- Keep Codecov and Semgrep advisory signal sources unless a governed task
  promotes a specific stable aggregate context.
- Preserve the `all-green` aggregate for branch protection and release tooling.
- Do not print or persist plaintext secrets; use GitHub Secrets or approved
  local secret stores.
- Treat axiom, implication, precedent, and schema edits as governance changes;
  validate YAML and consistency checks before marking a PR ready.
