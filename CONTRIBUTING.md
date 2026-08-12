# Contributing to Diagram Design

Thanks for wanting to contribute — this project only gets better with more eyes on it.

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) first. All contributions are expected to keep the community welcoming.

---

## What this project is

Diagram Design is an agent skill (Claude Code, Codex, Pi) that produces editorial-quality diagrams as self-contained HTML files. The repo is documentation-first: `skills/diagram-design/SKILL.md` is the index, each of the 27 diagram types has its own reference file, and the extractor scripts in `skills/diagram-design/scripts/` turn draw.io and Mermaid sources into a structured IR.

See [README.md](README.md) for the full picture, including the design system and the import/export flows.

---

## Before you start

- **Create an issue first** for anything non-trivial (new type, behavior change, import grammar work). Small fixes and docs can go straight to a PR.
- **Work on a branch** — never commit directly to `main`.
- **Keep the scope tight.** One PR = one concern. Mixing a new diagram type with a docs rewrite makes review slow.
- **Python 3.10+ is required** for the development scripts (CI runs 3.11).

---

## Validation gates

Every validation gate below must pass before a PR is ready. They also run automatically as GitHub Actions CI (`.github/workflows/ci.yml`).

| What it checks | Command |
|---|---|
| Accessible SVG contract (unit tests for the a11y linter) | `python3 scripts/test-lint-a11y.py` |
| Skin conformance of every example (colors, fonts, a11y) | `python3 scripts/lint-skin.py --all --baseline` |
| A single file, e.g. a new example | `python3 scripts/lint-skin.py skills/diagram-design/assets/example-my-type.html` |
| Sequence-doc consistency (ATL fragments, budgets) | `python3 scripts/verify-sequence-oauth.py` |
| draw.io import path (real extractor vs fixtures + docs sync) | `python3 scripts/verify-drawio-import.py` |
| Mermaid import path (grammars, adversarial input, caps, docs sync) | `python3 scripts/verify-mermaid-import.py` |
| Generated icon assets are up to date (`icons.html`, `primitive-icons.md`) | `python3 scripts/build-icons.py` then `git diff --exit-code` on the two generated files |

Run them all at once before pushing:

```bash
python3 scripts/test-lint-a11y.py \
  && python3 scripts/lint-skin.py --all --baseline \
  && python3 scripts/verify-sequence-oauth.py \
  && python3 scripts/verify-drawio-import.py \
  && python3 scripts/verify-mermaid-import.py
```

### If a gate fails

- **`lint-skin.py`:** the failure message names the file, line, and category (`color`, `font-family`, `a11y`, `external-asset`, `pure-black`, `script`). Colors must come from the palette in `skills/diagram-design/references/style-guide.md`; fonts from the allowed list; diagrams must satisfy the accessible SVG contract (see below).
- **`verify-*.py`:** the extractor's real behavior no longer matches its fixture or the documentation, or the reference/command/prompt wiring drifted. Fix the source of truth — do not widen a test to avoid a failure.
- **Icon assets:** you changed `scripts/vendor/icons/` or `scripts/build-icons.py` and the generated files went stale. Rerun `python3 scripts/build-icons.py` and commit the regenerated files.

Do **not** add a file to `scripts/lint-skin-baseline.txt` to get your example through. The baseline exists only for legacy pre-2.0 examples that legitimately predate the current skin, and it still receives a11y checks.

---

## The accessible SVG contract (a11y)

Every diagram `<svg>` must satisfy the contract enforced by the linter:

1. `role="img"` and `aria-labelledby` naming the `<title>` **and** `<desc>`.
2. `<title>` is the **first child** of `<svg>` (before `<defs>`).
3. IDs are prefixed per diagram and variant: `<slug>-title` / `<slug>-desc` — for `example-loop-dark.html` the slug is `loop-dark`, so the IDs are `loop-dark-title` / `loop-dark-desc`. Bare `title`/`desc` IDs and duplicate IDs are rejected.
4. `<title>` is the short subject name (≈ the `<h1>`, ≤ 60 chars); `<desc>` is one sentence describing the *content*, not the geometry.
5. Purely decorative SVGs (`aria-hidden="true"`) are exempt.

The contract lives in `scripts/lint-skin.py` (`lint_accessible_svgs`) and is unit-tested by `scripts/test-lint-a11y.py`. When in doubt, pattern-match an existing example.

---

## Working on examples (diagrams)

Every diagram type ships three variants: minimal light (`example-<type>.html`), minimal dark (`example-<type>-dark.html`), and full editorial (`example-<type>-full.html`).

1. Copy the closest template (`skills/diagram-design/assets/template.html`, `template-dark.html`, or `template-full.html`).
2. Load the matching `references/type-<name>.md` and follow its layout conventions.
3. Replace the eyebrow, h1, and SVG body; replace the `[diagram-slug]` placeholders with your file's slug and keep the `<title>`/`<desc>` slots filled.
4. Run the taste gate in `SKILL.md` §9, then the linter:

```bash
python3 scripts/lint-skin.py skills/diagram-design/assets/example-my-type.html
```

New examples should be added to the gallery (`assets/index.html`) so they stay browsable.

## Adding a new diagram type

1. Write `skills/diagram-design/references/type-<name>.md` — layout conventions, anti-patterns, and a worked pattern for that type. Mirror an existing reference's structure.
2. Add the row to the selection table in `skills/diagram-design/SKILL.md` §3.
3. Add the three example variants (see above) and register them in the gallery.
4. Run the full gate suite — new examples are linted automatically by `--all`.

## Changing the icon set

Icons are generated, never hand-edited:

1. Add or replace the source SVG in `scripts/vendor/icons/<source>/` (`tabler/`, `simple/`, …). Keep license provenance in `THIRD_PARTY_LICENSES.md` accurate.
2. Regenerate and verify:

```bash
python3 scripts/build-icons.py
git diff --exit-code -- skills/diagram-design/assets/icons.html skills/diagram-design/references/primitive-icons.md
```

## Touching the import paths

- draw.io: `skills/diagram-design/scripts/drawio_extract.py` — must pass `scripts/verify-drawio-import.py`, which drives the extractor against `scripts/fixtures/sample-architecture.drawio` in all four container formats (raw XML, deflate+base64, PNG-embedded, SVG-embedded).
- Mermaid: `skills/diagram-design/scripts/mermaid_extract.py` — must pass `scripts/verify-mermaid-import.py`, which covers every supported grammar, multi-block Markdown, adversarial labels, trust-boundary behavior, resource caps, and named failures.

Both scripts treat their input as **untrusted data** — they never render, fetch, or execute source content. Keep it that way. If you add a grammar or a new security boundary, extend the corresponding verifier with a fixture before merging.

Documentation and wiring must stay in sync: the import references, `SKILL.md` §11, the slash commands in `commands/`, and the Pi prompt templates in `prompts/` each describe the same flows. The verifiers check this — keep both sides updated in one PR.

## Documentation

Most of this repo *is* documentation. When behavior changes, update the affected reference files and the README in the same PR. Loose ends here are what the verifiers and reviewers will catch.

---

## Commit and PR conventions

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, e.g. `fix(import): support current Mermaid syntax`, `ci: verify Mermaid imports`, `docs(onboarding): clarify the URL flow`. Keep summaries short and imperative.

A good PR:

- has a clear title and a description that says *what* changed and *why*;
- mentions how you tested it (which gates you ran);
- keeps generated and source files consistent (extractor + verifier + reference + command in one change);
- is rebased on `main` and green on CI.

## Questions?

Open a discussion or comment on the relevant issue. If it's about security, use the private reporting path in [SECURITY.md](SECURITY.md).