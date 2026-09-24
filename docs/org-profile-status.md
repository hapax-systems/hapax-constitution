# Recheck organization profile status

The profile's September 24, 2026 status date describes a historical inspection.
Rendering the page does not repeat that inspection or update the date. Before
releasing a profile revision, run this read-only witness from the repository
root with Bash, Git, GitHub CLI, ripgrep and sha256sum available. GitHub CLI must
already have its normal authenticated access; do not put credentials in the
command or captured output.

```bash
# Use a new output path for each observation; preserve previous evidence.
(set -o noclobber; bash docs/recheck-org-profile.sh > /tmp/org-profile-status-NEW.txt)
```

The command records the observation time, source revision and content hashes,
the profile's historical status line, the current public repository inventory,
the explicitly linked spine v0.1.1 release, GitHub's latest spine release, and
agentgov's archive state, published release and license source at a pinned commit. It stops on a
failed command; a partial capture is failed evidence, not a passing recheck.
It performs no source, registry, repository-setting or publication mutations.

Compare the inventory with every repository linked in the generated profile.
Confirm that agentgov is still archived and inspect its pinned license text;
GitHub's SPDX detection alone is not license authority. Confirm that spine's
linked v0.1.1 release is public and not a draft. The profile names a particular
artifact, not the latest release, so a newer release does not invalidate that
snapshot link. This witness does not install a package or prove runtime behavior.

Keep the original dated evidence and this fresh observation separate. A recheck
today cannot establish what was available on an earlier date. If current facts
contradict the copy, hold publication and correct the source under its review
process. Any change to the status date or other generated copy requires a new
byte fixture and digest, a matching `.github/profile/README.md` candidate and
independent review. Never advance the date just because rendering succeeded.
