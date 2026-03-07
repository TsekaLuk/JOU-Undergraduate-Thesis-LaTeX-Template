---
name: word-handbook-to-latex-alignment
description: Align university thesis handbooks, graduation-form packages, and Word/WPS layout requirements to LaTeX templates with both structural and render fidelity. Use when converting a school thesis manual or form bundle from .docx, Word XML, and WPS/Word-exported PDFs into LaTeX; when tightening page-by-page alignment; when choosing a font strategy for Windows/macOS/Linux; or when encoding the alignment contract into E2E/TDD tests and README preview artifacts.
---

# Word Handbook To Latex Alignment

Use this skill when the repository needs a repeatable SOP from handbook sources to LaTeX outputs instead of ad hoc visual tweaking.

## Workflow

1. Lock the sources before touching LaTeX.
Read [references/workflow.md](references/workflow.md) and gather the `.docx`, unpacked Word XML, and at least one WPS- or Word-exported PDF. If the stakeholder cares about "what it looks like in WPS", treat that exported PDF as the render baseline.

2. Decide the font mode before adjusting geometry.
Read [references/font-strategy.md](references/font-strategy.md). Prefer local or system commercial fonts already present on the client machine. Do not commit commercial font binaries into a public repository.

3. Converge one page family at a time.
Start with cover, then declarations and abstracts, then body pages, then handbook forms. Regenerate comparison artifacts after each round instead of judging by memory.

4. Encode every stable rule in tests.
Read [references/e2e-contract.md](references/e2e-contract.md). Add structural tests for page count, anchors, table grids, font mode, and page ordering before claiming alignment.

5. Separate README previews from technical diagnostics.
Use side-by-side preview images for the README and keep overlay/diff/checker outputs as engineering artifacts.

## Repo entry points

- `styles/joufonts.sty`: font routing and cross-platform fallback
- `styles/jouthesis.cls`: thesis cover, abstracts, body layout
- `styles/jouhandbook.sty`: handbook-form shared layout primitives
- `scripts/generate_readme_images.py`: side-by-side README previews and form gallery
- `scripts/generate_cover_diff.py`: overlay, diff, and checkerboard diagnostics
- `tests/test_pixel_perfect_alignment.py`: handbook template contract
- `tests/test_thesis_alignment.py`: thesis-specific layout contract
- `tests/test_cover_alignment.py`: focused cover checks
- `tests/test_cross_platform_font_support.py`: Windows/macOS/Linux font-path contract

## Decision rules

- Use the WPS-exported PDF as the render truth when the stakeholder judges the result visually in WPS.
- Use Word XML as the structural truth for tables, sections, line spacing, and paragraph properties.
- Do not claim "pixel-perfect" unless both the compare images and the tests look clean.
- Prefer private commercial-font overrides over endless geometric fine-tuning when the remaining drift is obviously glyph-metric related.
- Keep README images human-readable; move overlay/diff/checker assets lower in the docs.

## References

- Read [references/workflow.md](references/workflow.md) for the execution sequence.
- Read [references/font-strategy.md](references/font-strategy.md) before touching fonts or cross-platform routing.
- Read [references/e2e-contract.md](references/e2e-contract.md) before adding or relaxing tests.
