#!/usr/bin/env python3
"""Download redistributable fonts used by the JOU template."""

from __future__ import annotations

import io
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = PROJECT_ROOT / "fonts" / "opensource"
LICENSE_DIR = FONT_DIR / "licenses"
TMP_DIR = PROJECT_ROOT / "tmp" / "font-downloads"

FILES = [
    (
        "Tinos-Regular.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/apache/tinos/Tinos-Regular.ttf",
    ),
    (
        "Tinos-Bold.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/apache/tinos/Tinos-Bold.ttf",
    ),
    (
        "Tinos-Italic.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/apache/tinos/Tinos-Italic.ttf",
    ),
    (
        "Tinos-BoldItalic.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/apache/tinos/Tinos-BoldItalic.ttf",
    ),
    (
        "CourierPrime-Regular.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/courierprime/CourierPrime-Regular.ttf",
    ),
    (
        "CourierPrime-Bold.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/courierprime/CourierPrime-Bold.ttf",
    ),
    (
        "NotoSerifCJKsc-Regular.otf",
        "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Regular.otf",
    ),
    (
        "NotoSerifCJKsc-Bold.otf",
        "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Bold.otf",
    ),
    (
        "NotoSerifCJKsc-Black.otf",
        "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Black.otf",
    ),
    (
        "NotoSansCJKsc-Regular.otf",
        "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
    ),
    (
        "NotoSansCJKsc-Bold.otf",
        "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf",
    ),
    (
        "LXGWWenKaiGB-Regular.ttf",
        "https://github.com/lxgw/LxgwWenkaiGB/releases/download/v1.521/LXGWWenKaiGB-Regular.ttf",
    ),
    (
        "LXGWWenKaiGB-Medium.ttf",
        "https://github.com/lxgw/LxgwWenkaiGB/releases/download/v1.521/LXGWWenKaiGB-Medium.ttf",
    ),
]

LICENSE_FILES = [
    (
        "Apache-2.0-Tinos.txt",
        "https://raw.githubusercontent.com/google/fonts/main/apache/tinos/LICENSE.txt",
    ),
    (
        "OFL-CourierPrime.txt",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/courierprime/OFL.txt",
    ),
    (
        "OFL-Noto-CJK.txt",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserif/OFL.txt",
    ),
    (
        "OFL-LXGWWenKaiGB.txt",
        "https://raw.githubusercontent.com/lxgw/LxgwWenkaiGB/main/OFL.txt",
    ),
]

FANDOL_ZIP = "https://mirrors.ctan.org/fonts/fandol.zip"
FANDOL_MEMBER = "fandol/FandolFang-Regular.otf"
FANDOL_LICENSE_MEMBER = "fandol/COPYING"


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:
        return response.read()


def download_file(target: Path, url: str) -> None:
    if target.exists():
        print(f"skip  {target.relative_to(PROJECT_ROOT)}")
        return
    print(f"fetch {target.name}")
    target.write_bytes(fetch(url))


def extract_from_zip(target: Path, zip_url: str, member: str) -> None:
    if target.exists():
        print(f"skip  {target.relative_to(PROJECT_ROOT)}")
        return
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = TMP_DIR / "fandol.zip"
    if not zip_path.exists():
        print("fetch fandol.zip")
        zip_path.write_bytes(fetch(zip_url))
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(member) as source, target.open("wb") as sink:
            shutil.copyfileobj(source, sink)
    print(f"extract {target.name}")


def main() -> int:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in FILES:
        download_file(FONT_DIR / filename, url)

    extract_from_zip(FONT_DIR / "FandolFang-Regular.otf", FANDOL_ZIP, FANDOL_MEMBER)

    for filename, url in LICENSE_FILES:
        download_file(LICENSE_DIR / filename, url)

    extract_from_zip(LICENSE_DIR / "GPL-Fandol.txt", FANDOL_ZIP, FANDOL_LICENSE_MEMBER)

    print("\nfont bootstrap complete")
    print(f"fonts dir: {FONT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
