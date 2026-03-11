#!/usr/bin/env python3
"""
一键导入标准学术字体到 fonts/proprietary/

优先从常见目录中查找字体文件并按模板期望的规范文件名复制：
- Windows: C:/Windows/Fonts 与常见 WPS 安装目录
- macOS: /System/Library/Fonts, /Library/Fonts, ~/Library/Fonts
- Linux: 常见系统字体目录与 WPS 目录
- 用户桌面字体文件夹: ~/Desktop/毕业论文字体, ~/Desktop/fonts, ~/Desktop
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROPRIETARY_DIR = PROJECT_ROOT / "fonts" / "proprietary"

CORE_FONT_TARGETS = [
    {
        "dest": "TimesNewRoman-Regular.ttf",
        "label": "Times New Roman Regular",
        "candidates": [
            "TimesNewRoman-Regular.ttf",
            "Times New Roman.ttf",
            "times.ttf",
        ],
    },
    {
        "dest": "TimesNewRoman-Bold.ttf",
        "label": "Times New Roman Bold",
        "candidates": [
            "TimesNewRoman-Bold.ttf",
            "Times New Roman Bold.ttf",
            "timesbd.ttf",
        ],
    },
    {
        "dest": "Arial-Regular.ttf",
        "label": "Arial Regular",
        "candidates": [
            "Arial-Regular.ttf",
            "Arial.ttf",
            "arial.ttf",
        ],
    },
    {
        "dest": "Arial-Bold.ttf",
        "label": "Arial Bold",
        "candidates": [
            "Arial-Bold.ttf",
            "Arial Bold.ttf",
            "arialbd.ttf",
        ],
    },
    {
        "dest": "CourierNew-Regular.ttf",
        "label": "Courier New Regular",
        "candidates": [
            "CourierNew-Regular.ttf",
            "Courier New.ttf",
            "cour.ttf",
        ],
    },
    {
        "dest": "CourierNew-Bold.ttf",
        "label": "Courier New Bold",
        "candidates": [
            "CourierNew-Bold.ttf",
            "Courier New Bold.ttf",
            "courbd.ttf",
        ],
    },
    {
        "dest": "SimSun.ttc",
        "label": "宋体",
        "candidates": [
            "SimSun.ttc",
            "宋体.ttc",
            "simsun.ttc",
        ],
    },
    {
        "dest": "SimHei.ttf",
        "label": "黑体",
        "candidates": [
            "SimHei.ttf",
            "黑体.ttf",
            "simhei.ttf",
        ],
    },
    {
        "dest": "KaiTi_GB2312.ttf",
        "label": "楷体_GB2312",
        "candidates": [
            "KaiTi_GB2312.ttf",
            "楷体_GB2312.ttf",
            "KaiTi.ttf",
            "楷体.ttf",
            "simkai.ttf",
        ],
    },
    {
        "dest": "FangSong_GB2312.ttf",
        "label": "仿宋_GB2312",
        "candidates": [
            "FangSong_GB2312.ttf",
            "仿宋_GB2312.ttf",
            "FangSong.ttf",
            "仿宋.ttf",
            "simfang.ttf",
        ],
    },
    {
        "dest": "FangZhengXiaoBiaoSongJianTi.ttf",
        "label": "方正小标宋简体",
        "candidates": [
            "FangZhengXiaoBiaoSongJianTi.ttf",
            "方正小标宋简体.ttf",
            "方正小标宋简.ttf",
            "FZXBSJW.TTF",
            "FZXBSJW--GB1-0.ttf",
        ],
    },
    {
        "dest": "STXingkai.ttf",
        "label": "华文行楷",
        "candidates": [
            "STXingkai.ttf",
            "STXINGKA.TTF",
            "华文行楷.ttf",
        ],
    },
]

OPTIONAL_FONT_TARGETS = [
    {
        "dest": "STLiti.ttf",
        "label": "华文隶书",
        "candidates": [
            "STLiti.ttf",
            "华文隶书.ttf",
        ],
    },
]


def unique_existing_dirs(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in paths:
        resolved = str(path.expanduser())
        if resolved in seen:
            continue
        seen.add(resolved)
        if Path(resolved).exists():
            ordered.append(Path(resolved))
    return ordered


def default_search_dirs() -> list[Path]:
    home = Path.home()
    system = platform.system()
    paths: list[Path] = [
        home / "Desktop" / "毕业论文字体",
        home / "Desktop" / "fonts",
        home / "Desktop",
    ]

    if system == "Darwin":
        paths.extend(
            [
                Path("/System/Library/Fonts"),
                Path("/System/Library/Fonts/Supplemental"),
                Path("/Library/Fonts"),
                home / "Library" / "Fonts",
                Path("/Applications/wpsoffice.app/Contents/Resources/office6/fonts"),
                Path("/Applications/WPS Office.app/Contents/Resources/office6/fonts"),
            ]
        )
    elif system == "Windows":
        for env_name in ("WINDIR", "SystemRoot"):
            value = os.environ.get(env_name)
            if value:
                paths.append(Path(value) / "Fonts")
        for env_name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            value = os.environ.get(env_name)
            if not value:
                continue
            base = Path(value)
            paths.extend(
                [
                    base / "WPS Office" / "office6" / "fonts",
                    base / "Kingsoft" / "WPS Office" / "office6" / "fonts",
                ]
            )
        paths.extend(
            [
                Path("C:/Windows/Fonts"),
                Path("C:/WINDOWS/Fonts"),
                Path("C:/Program Files/WPS Office/office6/fonts"),
                Path("C:/Program Files (x86)/WPS Office/office6/fonts"),
                Path("C:/Program Files/Kingsoft/WPS Office/office6/fonts"),
                Path("C:/Program Files (x86)/Kingsoft/WPS Office/office6/fonts"),
            ]
        )
    else:
        paths.extend(
            [
                Path("/usr/share/fonts"),
                Path("/usr/local/share/fonts"),
                home / ".local" / "share" / "fonts",
                Path("/opt/kingsoft/wps-office/office6/fonts"),
                Path("/usr/share/fonts/wps-office"),
            ]
        )

    return unique_existing_dirs(paths)


def find_source(search_dirs: list[Path], candidates: list[str]) -> Path | None:
    candidate_map = {candidate.lower(): candidate for candidate in candidates}
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        try:
            for entry in search_dir.iterdir():
                if not entry.is_file():
                    continue
                if entry.name.lower() in candidate_map:
                    return entry
        except PermissionError:
            continue
    return None


def copy_target(target: dict[str, object], search_dirs: list[Path], force: bool, dry_run: bool) -> tuple[str, str]:
    dest = PROPRIETARY_DIR / str(target["dest"])
    if dest.exists() and not force:
        return "skipped", f"{target['label']}: 已存在 {dest.name}"

    source = find_source(search_dirs, list(target["candidates"]))
    if not source:
        return "missing", f"{target['label']}: 未找到候选文件"

    if dry_run:
        return "planned", f"{target['label']}: {source} -> {dest.name}"

    PROPRIETARY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    return "copied", f"{target['label']}: {source} -> {dest.name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="一键导入本机或系统字体到 fonts/proprietary/")
    parser.add_argument(
        "--search-dir",
        action="append",
        default=[],
        help="额外搜索目录，可多次传入",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖已存在的目标字体文件",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印导入计划，不执行复制",
    )
    parser.add_argument(
        "--skip-optional",
        action="store_true",
        help="跳过华文行楷/华文隶书等可选字体",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = list(CORE_FONT_TARGETS)
    if not args.skip_optional:
        targets.extend(OPTIONAL_FONT_TARGETS)

    extra_dirs = [Path(path).expanduser() for path in args.search_dir]
    search_dirs = unique_existing_dirs(extra_dirs + default_search_dirs())

    print("==> 字体导入搜索目录:")
    for path in search_dirs:
        print(f"  - {path}")

    copied = 0
    skipped = 0
    missing = 0
    planned = 0

    print("\n==> 开始导入字体...")
    for target in targets:
        status, message = copy_target(target, search_dirs, args.force, args.dry_run)
        if status == "copied":
            copied += 1
            prefix = "✓"
        elif status == "skipped":
            skipped += 1
            prefix = "-"
        elif status == "planned":
            planned += 1
            prefix = "•"
        else:
            missing += 1
            prefix = "!"
        print(f"{prefix} {message}")

    print("\n==> 导入完成")
    if args.dry_run:
        print(f"计划复制: {planned}")
    else:
        print(f"已复制: {copied}")
    print(f"已跳过: {skipped}")
    print(f"未找到: {missing}")

    if not args.dry_run:
        print("\n下一步:")
        print("  1. 运行 python3 scripts/check_fonts.py")
        print("  2. 运行 make")

    return 0


if __name__ == "__main__":
    sys.exit(main())
