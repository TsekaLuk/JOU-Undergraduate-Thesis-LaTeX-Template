# E2E Contract

## Structural gates

Encode these expectations in tests whenever they become stable:

- required source files exist
- required LaTeX templates exist
- required PDF outputs exist
- page count and orientation are correct
- page anchors appear in the right order
- handbook table grids match the intended LaTeX widths
- font mode and embedded fonts match the active routing policy

## Render gates

Use rendered-image checks for the highest-risk pages:

- thesis cover
- abstract pages
- first body page
- any handbook form with dense table geometry

Do not rely on one global pixel threshold for every page. Use page-specific checks or focused crops when needed.

## README artifact gates

README previews should satisfy:

- side-by-side, not overlay
- readable without zooming into a raw PDF
- derived from real repository outputs
- reproducible from scripts, not manual screenshot stitching

Technical artifacts should satisfy:

- stored separately from README previews
- available for manual debugging
- regenerated from a single command

## Suggested command set

Use repository commands where possible:

```bash
make
make readme-images
make cover-diff
make test
```

If a command is missing, add it before claiming the workflow is reusable.
