# Font Strategy

## Principle

Most last-mile drift on thesis covers and forms is glyph-metric drift, not geometry drift.

Fix the font source before overfitting positions.

## Allowed modes

Use this order:

1. private commercial-font overrides already owned by the client
2. system or WPS-installed commercial fonts
3. repository-managed open-source fallbacks

Do not commit commercial font binaries into a public repository.

## Cross-platform rule

The build must stay usable on:

- Windows
- macOS
- Linux

That means:

- commercial fonts may be optional
- open-source fallbacks must still compile cleanly
- the font routing layer must probe OS-specific locations

## Windows priority

Treat Windows as a first-class target because many clients review the output there.

Probe, in order:

- `fonts/proprietary/`
- `C:/Windows/Fonts`
- common WPS font directories under `Program Files`, `Program Files (x86)`, and `LOCALAPPDATA`
- bundled open-source fonts

If the client uses a non-standard install path, provide a local override file rather than hardcoding machine-specific paths into version-controlled files.

## Decision rules

- If the remaining drift is clearly in glyph shapes or character widths, switch font mode instead of moving boxes again.
- If a README compare image still shows heavy ghosting after geometry adjustments, inspect the embedded font names first.
- Use strict mode or font checks before calling the output "submission-ready".
