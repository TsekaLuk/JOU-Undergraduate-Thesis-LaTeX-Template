# Workflow

## 1. Inputs

Collect three kinds of sources when they are available:

- `.docx`: the editable thesis handbook or form package
- unpacked Word XML: structural source of tables, line spacing, sections, and style names
- WPS- or Word-exported PDF: visual baseline for the stakeholder-facing output

If the task mentions "像素级对齐", do not rely on XML alone.

## 2. Baseline hierarchy

Use this precedence order:

1. WPS-exported PDF for visual truth
2. Word XML for structural truth
3. Visible handbook text for explicit school rules

Do not fight the render baseline with XML-only assumptions. If the stakeholder is checking in WPS, WPS wins.

## 3. Page mapping

Map the reference pages to LaTeX outputs before editing styles.

Typical buckets:

- cover
- declarations and authorization
- Chinese abstract
- English abstract
- table of contents
- body sample page
- handbook forms

Store the mapping in scripts or tests so it does not live only in chat history.

## 4. Alignment loop

Run the loop in this order:

1. choose font mode
2. adjust page geometry
3. adjust blocks, tables, and vertical rhythm
4. regenerate compare images
5. inspect drift
6. encode stable rules in tests

Do not fine-tune positions before the font source is stable.

## 5. Priority order for edits

Prefer these files first:

- `styles/joufonts.sty`
- `styles/jouthesis.cls`
- `styles/jouhandbook.sty`
- template-specific `.tex` files under `templates/`

Touch sample content only when the rendered output is wrong because of demo data, not because the class/layout is wrong.

## 6. Preview artifacts

Keep two artifact families:

- README previews: side-by-side, readable, audience-facing
- technical diagnostics: overlay, diff, checkerboard

In this repository:

- `scripts/generate_readme_images.py` produces `docs/images/*.png`
- `scripts/generate_cover_diff.py` produces `docs/assets/*.png`

## 7. Claiming success

Only say the template is aligned when:

- the reference mapping is explicit
- the font mode is known
- the compare images are close by eye
- the regression tests pass
