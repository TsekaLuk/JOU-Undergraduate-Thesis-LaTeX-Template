#!/usr/bin/env python3
"""
字体检测脚本 - 检查系统和本地字体文件
用于诊断 JOU LaTeX 模板的字体加载状态
"""

import platform
import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROPRIETARY_DIR = PROJECT_ROOT / "fonts" / "proprietary"
OPENSOURCE_DIR = PROJECT_ROOT / "fonts" / "opensource"
WPS_FONT_DIRS = [
    Path("/Applications/wpsoffice.app/Contents/Resources/office6/fonts"),
    Path("/Applications/WPS Office.app/Contents/Resources/office6/fonts"),
    Path("/opt/kingsoft/wps-office/office6/fonts"),
    Path("/usr/share/fonts/wps-office"),
]

WINDOWS_FONT_DIRS = [
    Path("C:/Windows/Fonts"),
    Path("C:/WINDOWS/Fonts"),
]

for env_name in ("WINDIR", "SystemRoot"):
    value = os.environ.get(env_name)
    if value:
        WINDOWS_FONT_DIRS.insert(0, Path(value) / "Fonts")

for env_name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
    value = os.environ.get(env_name)
    if not value:
        continue
    base = Path(value)
    WPS_FONT_DIRS.extend(
        [
            base / "WPS Office" / "office6" / "fonts",
            base / "Kingsoft" / "WPS Office" / "office6" / "fonts",
        ]
    )

WPS_FONT_DIRS.extend(
    [
        Path("C:/Program Files/WPS Office/office6/fonts"),
        Path("C:/Program Files (x86)/WPS Office/office6/fonts"),
        Path("C:/Program Files/Kingsoft/WPS Office/office6/fonts"),
        Path("C:/Program Files (x86)/Kingsoft/WPS Office/office6/fonts"),
    ]
)

# 必需的字体定义
REQUIRED_FONTS = {
    "拉丁字体（标准学术）": {
        "Times New Roman": ["Times New Roman", "TimesNewRoman-Regular.ttf"],
        "Arial": ["Arial", "Arial-Regular.ttf"],
        "Courier New": ["Courier New", "CourierNew-Regular.ttf"],
    },
    "中文字体（标准学术）": {
        "宋体": ["SimSun", "STSong", "SimSun.ttf"],
        "黑体": ["SimHei", "STHeiti", "SimHei.ttf"],
        "楷体": ["KaiTi_GB2312", "STKaiti", "KaiTi_GB2312.ttf"],
        "仿宋": ["FangSong", "STFangsong", "FangSong_GB2312.ttf"],
    },
    "特殊字体": {
        "方正小标宋-通用": ["FZXiaoBiaoSong-B05", "FangZhengXiaoBiaoSongJianTi.ttf"],
        "华文行楷": ["STXingkai", "STXingkai.ttf"],
    },
    "WPS 兼容字体（可选）": {
        "汉仪楷体": ["HYKaiTiKW", "HYKaiTiKW.ttf"],
        "汉仪书宋二": ["HYShuSongErKW", "HYShuSongErKW.ttf"],
        "汉仪中黑": ["HYZhongHeiKW", "HYZhongHeiKW.ttf"],
        "方正小标宋": ["FZXBSJW--GB1-0", "FZXBSJW--GB1-0.ttf"],
        "方正仿宋": ["FZFSK--GBK1-0", "FZFSK--GBK1-0.ttf"],
    },
}

# 开源字体兜底方案
OPENSOURCE_FONTS = {
    "Tinos": "Tinos-Regular.ttf",
    "Courier Prime": "CourierPrime-Regular.ttf",
    "Noto Serif CJK SC": "NotoSerifCJKsc-Regular.otf",
    "Noto Sans CJK SC": "NotoSansCJKsc-Regular.otf",
    "LXGW WenKai GB": "LXGWWenKaiGB-Regular.ttf",
    "FandolFang": "FandolFang-Regular.otf",
}

WINDOWS_FONT_FILES = {
    "Times New Roman": ["times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"],
    "Arial": ["arial.ttf", "arialbd.ttf"],
    "Courier New": ["cour.ttf", "courbd.ttf"],
    "宋体": ["simsun.ttc"],
    "黑体": ["simhei.ttf"],
    "楷体": ["simkai.ttf"],
    "仿宋": ["simfang.ttf"],
    "方正小标宋-通用": ["FZXBSJW.TTF"],
    "华文行楷": ["STXINGKA.TTF"],
}


def check_system_font(font_name: str) -> bool:
    """检查系统是否安装了指定字体"""
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            result = subprocess.run(
                ["fc-list", ":", "family"],
                capture_output=True,
                text=True,
                check=True
            )
            return font_name in result.stdout
        elif system == "Linux":
            result = subprocess.run(
                ["fc-list", ":", "family"],
                capture_output=True,
                text=True,
                check=True
            )
            return font_name in result.stdout
        elif system == "Windows":
            # Windows 下使用 fontconfig (如果安装了 MiKTeX/TeX Live)
            try:
                result = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                if font_name in result.stdout:
                    return True
                return check_windows_font_files(font_name)
            except FileNotFoundError:
                return check_windows_font_files(font_name)
    except Exception:
        if system == "Windows":
            return check_windows_font_files(font_name)
        return False

    return False


def check_local_font(filename: str) -> tuple[bool, str]:
    """检查本地字体文件（proprietary 或 opensource）"""
    prop_file = PROPRIETARY_DIR / filename
    oss_file = OPENSOURCE_DIR / filename

    if prop_file.exists():
        return True, "proprietary"
    elif oss_file.exists():
        return True, "opensource"
    else:
        return False, ""


def check_wps_bundled_font(candidates: list[str]) -> tuple[bool, str]:
    """检查 WPS 应用包内置字体文件"""
    for font_dir in WPS_FONT_DIRS:
        for candidate in candidates:
            if (font_dir / candidate).exists():
                return True, str(font_dir / candidate)
    return False, ""


def check_windows_font_files(font_name: str) -> bool:
    """Windows 下检查 C:\\Windows\\Fonts 中的字体文件"""
    candidates = WINDOWS_FONT_FILES.get(font_name, [])
    for font_dir in WINDOWS_FONT_DIRS:
        for candidate in candidates:
            if (font_dir / candidate).exists():
                return True
    return False


def find_windows_font_file(font_name: str) -> str:
    """返回 Windows 字体文件路径"""
    candidates = WINDOWS_FONT_FILES.get(font_name, [])
    for font_dir in WINDOWS_FONT_DIRS:
        for candidate in candidates:
            path = font_dir / candidate
            if path.exists():
                return str(path)
    return ""


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*72}")
    print(f"  {title}")
    print(f"{'='*72}\n")


def print_font_status(name: str, status: str, color: str = ""):
    """打印字体状态"""
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m"
    }
    c = colors.get(color, "")
    reset = colors["reset"] if color else ""
    print(f"  {name:30s} {c}{status}{reset}")


def main():
    print_section("江苏海洋大学本科论文 LaTeX 模板 - 字体检测")

    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"项目根目录: {PROJECT_ROOT}")

    font_mode = "未知"
    missing_fonts = []

    # 检查字体优先级
    print_section("字体加载优先级检测")

    # 优先级 1: 本地 proprietary 文件
    print("【优先级 1】fonts/proprietary/ 本地标准字体")
    prop_found = False
    for category, fonts in REQUIRED_FONTS.items():
        for font_name, font_files in fonts.items():
            local_file = next(
                (candidate for candidate in reversed(font_files) if "." in candidate),
                "",
            )
            if local_file:
                exists, source = check_local_font(local_file)
                if exists and source == "proprietary":
                    prop_found = True
                    print_font_status(f"{font_name} ({local_file})", "✓ 已找到", "green")

    if not prop_found:
        print_font_status("无本地标准字体", "跳过此优先级", "yellow")

    # 优先级 2: 系统字体
    print("\n【优先级 2】系统安装的标准学术字体")
    system_found = False
    standard_system_found = False
    for category, fonts in REQUIRED_FONTS.items():
        print(f"\n  {category}:")
        for font_name, font_files in fonts.items():
            # 检查所有可能的系统字体名称
            found = False
            found_name = ""
            for sys_name in font_files[:2]:  # 前两个是系统字体名称
                if check_system_font(sys_name):
                    found = True
                    found_name = sys_name
                    system_found = True
                    if category != "WPS 兼容字体（可选）":
                        standard_system_found = True
                    break

            if not found and category == "WPS 兼容字体（可选）":
                bundled, bundled_path = check_wps_bundled_font(
                    {
                        "汉仪楷体": ["HYKaiTiJ.ttf"],
                        "汉仪书宋二": ["FZSSK.ttf"],
                        "汉仪中黑": ["HYZhongJianHeiJ.ttf", "HYQiHei-55J.ttf"],
                        "方正小标宋": ["FZSSK.ttf"],
                        "方正仿宋": ["FZFSK.ttf"],
                    }.get(font_name, [])
                )
                if bundled:
                    found = True
                    found_name = bundled_path
                    system_found = True

            if not found and platform.system() == "Windows":
                win_font_path = find_windows_font_file(font_name)
                if win_font_path:
                    found = True
                    found_name = win_font_path
                    system_found = True
                    if category != "WPS 兼容字体（可选）":
                        standard_system_found = True

            if found:
                print_font_status(f"  {font_name}", f"✓ {found_name}", "green")
            else:
                print_font_status(f"  {font_name}", "✗ 未找到", "red")
                if category != "WPS 兼容字体（可选）":
                    missing_fonts.append(font_name)

    # 优先级 3: 开源字体兜底
    print("\n【优先级 3】fonts/opensource/ 开源字体兜底")
    all_oss_found = True
    for font_name, filename in OPENSOURCE_FONTS.items():
        exists, _ = check_local_font(filename)
        if exists:
            print_font_status(font_name, "✓ 已找到", "green")
        else:
            print_font_status(font_name, "✗ 缺失（需运行 make fonts）", "red")
            all_oss_found = False

    # 确定字体模式
    print_section("字体模式诊断")

    # 检查是否有 WPS 兼容字体
    wps_fonts_found = []
    for font_name, font_files in REQUIRED_FONTS.get("WPS 兼容字体（可选）", {}).items():
        for sys_name in font_files[:2]:
            if check_system_font(sys_name):
                wps_fonts_found.append(font_name)
                break
        else:
            bundled, _ = check_wps_bundled_font(
                {
                    "汉仪楷体": ["HYKaiTiJ.ttf"],
                    "汉仪书宋二": ["FZSSK.ttf"],
                    "汉仪中黑": ["HYZhongJianHeiJ.ttf", "HYQiHei-55J.ttf"],
                    "方正小标宋": ["FZSSK.ttf"],
                    "方正仿宋": ["FZFSK.ttf"],
                }.get(font_name, [])
            )
            if bundled:
                wps_fonts_found.append(font_name)

    if prop_found:
        font_mode = "licensed (本地标准字体)"
        print_font_status("字体模式", font_mode, "green")
        print("\n  ✓ 使用 fonts/proprietary/ 中的标准学术字体")
        print("  ✓ 最适合最终提交与跨平台复现")
    elif standard_system_found and not missing_fonts:
        font_mode = "system-licensed (系统标准字体)"
        print_font_status("字体模式", font_mode, "green")
        print("\n  ✓ 使用系统安装的标准学术字体")
        print("  ✓ 符合楷体_GB2312 / 宋体 / 黑体 / Times New Roman 优先策略")
    elif len(wps_fonts_found) >= 3:  # 至少有3个WPS兼容字体
        font_mode = "wps-compat (WPS 兼容字体)"
        print_font_status("字体模式", font_mode, "green")
        print(f"\n  ✓ 检测到 WPS 兼容字体: {', '.join(wps_fonts_found)}")
        print("  ✓ 可作为标准学术字体缺失时的兼容兜底")
    elif system_found and missing_fonts:
        font_mode = "mixed (部分标准字体 + 开源兜底)"
        print_font_status("字体模式", font_mode, "yellow")
        print(f"\n  ⚠ 缺少以下标准字体: {', '.join(missing_fonts)}")
        print("  ⚠ 部分内容将使用开源替代")
        print("  ⚠ 适合预览，不是理想的最终交付状态")
    else:
        font_mode = "oss (开源兜底字体)"
        print_font_status("字体模式", font_mode, "yellow" if all_oss_found else "red")
        if all_oss_found:
            print("\n  ⚠ 系统无标准学术字体，使用开源替代")
            print("  ⚠ 适合预览和开发，不建议直接作为最终交付")
        else:
            print("\n  ✗ 开源字体兜底方案不完整")
            print("  ✗ 请运行: make fonts")

    # 建议
    print_section("改进建议")

    if missing_fonts:
        print("为获得最佳学术排版效果，建议补齐缺失的标准字体:\n")

        system = platform.system()
        if system == "Windows":
            print("  Windows 用户:")
            print("  - 优先使用系统自带或 Office 自带的 Times New Roman / SimSun / SimHei / KaiTi / FangSong")
            print("  - 安装 WPS 可作为兼容兜底，模板会自动探测常见安装目录")
            print("  - 系统字体目录默认检查: C:\\Windows\\Fonts")
            print("  - WPS 字体目录默认检查: Program Files / Program Files (x86) / LOCALAPPDATA")
            print("  - 若安装路径特殊，可在 styles/joufontspaths.local.tex 中覆盖字体目录")
        elif system == "Darwin":
            print("  macOS 用户:")
            print("  - 系统已预装华文字库（STSong, STHeiti, STKaiti, STFangsong）")
            print("  - 如缺失，请从「字体册」应用检查")
        elif system == "Linux":
            print("  Linux 用户:")
            print("  - 安装 Windows 字体包:")
            print("    sudo apt install ttf-mscorefonts-installer  # Ubuntu/Debian")
            print("    yay -S ttf-ms-fonts                          # Arch Linux")

        print("\n  或者，将字体文件手动放入 fonts/proprietary/:")
        for font in missing_fonts:
            if font in REQUIRED_FONTS.get("拉丁字体（标准学术）", {}):
                filename = REQUIRED_FONTS["拉丁字体（标准学术）"][font][1]
                print(f"    - {filename}")
            elif font in REQUIRED_FONTS.get("中文字体（标准学术）", {}):
                filename = REQUIRED_FONTS["中文字体（标准学术）"][font][2]
                print(f"    - {filename}")
            elif font in REQUIRED_FONTS.get("特殊字体", {}):
                filename = REQUIRED_FONTS["特殊字体"][font][1]
                print(f"    - {filename}")
    else:
        print("  ✓ 字体配置完善，无需额外操作")

    print("\n" + "="*72 + "\n")

    return 0 if not missing_fonts or all_oss_found else 1


if __name__ == "__main__":
    sys.exit(main())
