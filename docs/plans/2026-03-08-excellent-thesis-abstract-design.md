# Excellent Thesis Abstract Template Design

## Goal

Add a dedicated LaTeX template for the official JOU "本科校级优秀毕业实习与设计（论文）摘要" submission while reusing shared thesis metadata and existing font assets.

## Source of truth

- `references/江苏海洋大学本科校级优秀毕业实习与设计（论文）摘要格式说明.doc`
- The rendered sample pages contained in that document

## Constraints

- This is a separate submission artifact, not the thesis abstract page reused as-is.
- The final template should generate only the formal submission pages, not the trailing instruction pages from the Word reference.
- The abstract body should remain independently editable because the official guidance requires a distilled standalone short paper of about 3000 Chinese characters.
- Shared metadata should be entered once and reused by both `main.tex` and the new template.

## Decision

Use a separate report template instead of extending `jouthesis.cls`.

### Why

- The official abstract uses a different page model:
  - first-page full-width title and Chinese abstract block
  - two-column body text
  - separate author bio and English abstract block
- Folding this into the thesis class would couple two very different document structures and raise regression risk for the main thesis workflow.

## File structure

- Add `contents/shared/metadata.tex` for reusable thesis metadata.
- Update `main.tex` to read shared metadata and map it into the thesis class fields.
- Add `styles/jouexcellentabstract.sty` for the abstract-specific layout rules.
- Add `templates/reports/excellent-thesis-abstract.tex` as the user-facing entrypoint.
- Add dedicated editable content files under `contents/excellent-abstract/`:
  - `keywords.tex`
  - `cn-abstract.tex`
  - `body.tex`
  - `en-abstract.tex`

## Shared metadata boundary

Shared metadata will include:

- Chinese title
- English title
- author name
- student id
- college / program / class
- supervisor name
- thesis category
- school year
- cover/submission dates
- author bio
- first-page supervisor note

The new abstract body, Chinese abstract, English abstract, and keywords stay outside the shared metadata layer.

## Layout plan

- Base class: `ctexart`
- Page setup:
  - A4
  - top `3cm`
  - bottom `2cm`
  - inner `1.7cm`
  - outer `2cm`
  - twoside
- First page:
  - full-width title block
  - author/supervisor line
  - college/program line
  - Chinese abstract and keywords
- Main content:
  - two-column layout starting on page 1 after the Chinese abstract block
  - numbered headings `1`, `1.1`, `1.1.1`
  - third-level heading run-in style
- Footer:
  - centered page number in the sample style
- Header:
  - centered running title matching the official submission title
- Optional fixed first-page supervisor note:
  - rendered as an overlay text block near the bottom left of page 1

## Reuse plan

- Reuse `styles/joufonts.sty` for cross-platform font discovery and fallback.
- Reuse the shared bibliography file `references/refs.bib`.
- Reuse existing figures if the sample content needs a placeholder image.

## Documentation updates

- Document the new template in `templates/README.md`.
- Update top-level README counts to distinguish handbook templates from the new excellent-abstract template.

## Verification

- Compile `main.tex` after the metadata refactor.
- Compile `templates/reports/excellent-thesis-abstract.tex`.
- Confirm the new template produces a valid PDF and the main thesis still builds.
