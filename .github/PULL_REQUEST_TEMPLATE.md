## What does this PR do?

<!-- One or two sentences: what changed and why. -->

## Validation gates

<!-- Mark what you ran and that it passed. CI runs all of these on the PR too. -->

- [ ] `python3 scripts/test-lint-a11y.py`
- [ ] `python3 scripts/lint-skin.py --all --baseline`
- [ ] `python3 scripts/verify-sequence-oauth.py`
- [ ] `python3 scripts/verify-drawio-import.py`
- [ ] `python3 scripts/verify-mermaid-import.py`
- [ ] `git diff --exit-code` green after `python3 scripts/build-icons.py` (if icons changed)
- [ ] Docs updated in the same PR where behavior changed

## Checklist

- [ ] No new entries added to `scripts/lint-skin-baseline.txt`
- [ ] Generated and source files are consistent (extractor ↔ verifier ↔ reference ↔ command)
- [ ] Accessible SVG contract satisfied for new/changed examples
- [ ] Code of Conduct respected

## Related issues

<!-- Link any issues this closes, e.g. "Closes #12". -->