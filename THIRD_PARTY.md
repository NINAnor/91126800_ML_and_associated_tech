# Third-party software

This document records third-party software vendored into this repository that is not installed through the project's Python tooling.

## mermaid.min.js

- **Purpose:** renders mermaid diagrams in the mdBook HTML output (see `book.toml`).
- **Upstream:** [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid)
- **Version:** mermaid v11.x, as bundled by [mdbook-mermaid v0.17.0](https://github.com/badboy/mdbook-mermaid/tree/v0.17.0)
- **License:** MIT — see upstream `LICENSE` at https://github.com/mermaid-js/mermaid/blob/develop/LICENSE
- **Copied as:** pristine minified bundle, no local modifications.
- **Companion:** `mermaid-init.js` is the initializer shipped alongside `mdbook-mermaid` (MPL-2.0, https://mozilla.org/MPL/2.0/).

## src/case_study

The case-study folder contains Python scripts and shell scripts used as a worked example in the book. It is teaching material maintained in this repository and is excluded from the project's linting/CI tooling (`ruff`, `deptry`, `prek`); see `pyproject.toml` and `prek.toml`.
