#!/usr/bin/env python3
"""Regression tests for quote-independent URL SVG normalization."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "scripts" / "build-icons.py"


def load_build_module():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("diagram_design_build_icons", BUILD)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load build-icons.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    build_icons = load_build_module()
    svg = (
        "<svg viewBox='0 0 32 16'>"
        "<path style='fill:#123456;stroke:#654321' d='M0 0h32v16H0z'/>"
        "<circle fill='#abcdef' stroke='#111111' cx='8' cy='8' r='4'/>"
        "</svg>"
    )
    normalized = build_icons.normalize_url(svg)
    if 'viewBox="0 0 32 16"' not in normalized:
        raise AssertionError(f"single-quoted viewBox was not preserved: {normalized}")
    if any(color in normalized for color in ("#123456", "#654321", "#abcdef", "#111111")):
        raise AssertionError(f"source colors escaped normalization: {normalized}")
    if normalized.count('fill="currentColor"') < 2:
        raise AssertionError(f"single-quoted fills were not normalized: {normalized}")
    if 'stroke="currentColor"' not in normalized:
        raise AssertionError(f"single-quoted strokes were not normalized: {normalized}")
    print("PASS: URL SVG normalization handles single-quoted attributes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
