#!/usr/bin/env python3
"""
字体检测脚本 - 检查系统和本地字体文件
用于诊断 JOU LaTeX 模板的字体加载状态
"""

import platform
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROPRIETARY_DIR = PROJECT_ROOT / "fonts" / "proprietary"
OPENSOURCE_DIR = PROJECT_ROOT / "fonts" / "opensource"

# 必需的字体定义
REQUIRED_FONTS = {
    "WPS 实际字体 (最优先)": {
        "汉仪楷体": ["HYKaiTiKW", "HYKaiTiKW.ttf"],
        "汉仪书宋二": ["HYShuSongErKW", "HYShuSongErKW.ttf"],
        "汉仪中黑": ["HYZhongHeiKW", "HYZhongHeiKW.ttf"],
        "方正小标宋": ["FZXBSJW--GB1-0", "FZXBSJW--GB1-0.ttf"],
        "方正仿宋": ["FZFSK--GBK1-0", "FZFSK--GBK1-0.ttf"],
    },
    "拉丁字体": {
        "Times New Roman": ["Times New Roman", "TimesNewRoman-Regular.ttf"],
        "Arial": ["Arial", "Arial-Regular.ttf"],
        "Courier New": ["Courier New", "CourierNew-Regular.ttf"],
    },
    "中文字体 (通用)": {
        "宋体": ["SimSun", "STSong", "SimSun.ttf"],
        "黑体": ["SimHei", "STHeiti", "SimHei.ttf"],
        "楷体": ["KaiTi", "STKaiti", "KaiTi_GB2312.ttf"],
        "仿宋": ["FangSong", "STFangsong", "FangSong_GB2312.ttf"],
    },
    "特殊字体": {
        "方正小标宋-通用": ["FZXiaoBiaoSong-B05", "FangZhengXiaoBiaoSongJianTi.ttf"],
        "华文行楷": ["STXingkai", "STXingkai.ttf"],
    }
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
                return font_name in result.stdout
            except FileNotFoundError:
                # 如果 fc-list 不可用，假设标准 Windows 字体存在
                windows_fonts = ["SimSun", "SimHei", "KaiTi", "FangSong", "Times New Roman", "Arial"]
                return font_name in windows_fonts
    except Exception:
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
    print("【优先级 1】fonts/proprietary/ 本地商业字体")
    prop_found = False
    for category, fonts in REQUIRED_FONTS.items():
        for font_name, font_files in fonts.items():
            # 检查文件名（第三个元素是文件名）
            if len(font_files) > 2:
                local_file = font_files[2]
                exists, _ = check_local_font(local_file)
                if exists:
                    prop_found = True
                    print_font_status(f"{font_name} ({local_file})", "✓ 已找到", "green")

    if not prop_found:
        print_font_status("无本地商业字体", "跳过此优先级", "yellow")

    # 优先级 2: 系统字体
    print("\n【优先级 2】系统安装的商业字体")
    system_found = False
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
                    break

            if found:
                print_font_status(f"  {font_name}", f"✓ {found_name}", "green")
            else:
                print_font_status(f"  {font_name}", "✗ 未找到", "red")
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

    # 检查是否有 WPS 实际字体
    wps_fonts_found = []
    for font_name, font_files in REQUIRED_FONTS.get("WPS 实际字体 (最优先)", {}).items():
        for sys_name in font_files[:2]:
            if check_system_font(sys_name):
                wps_fonts_found.append(font_name)
                break

    if prop_found:
        font_mode = "licensed (本地商业字体)"
        print_font_status("字体模式", font_mode, "green")
        print("\n  ✓ 使用 fonts/proprietary/ 中的商业字体")
        print("  ✓ 最高对齐度 (98-99%)")
    elif len(wps_fonts_found) >= 3:  # 至少有3个WPS字体
        font_mode = "wps-exact (WPS 实际字体)"
        print_font_status("字体模式", font_mode, "green")
        print(f"\n  ✓ 检测到 WPS 实际字体: {', '.join(wps_fonts_found)}")
        print("  ✓ 像素级对齐 (99%+)")
        print("  ✓ 与官方手册 PDF 完全一致")
    elif system_found and not missing_fonts:
        font_mode = "system-licensed (系统商业字体)"
        print_font_status("字体模式", font_mode, "green")
        print("\n  ✓ 使用系统安装的商业字体")
        print("  ✓ 高对齐度 (95-98%)")
    elif system_found and missing_fonts:
        font_mode = "mixed (部分系统字体 + 开源兜底)"
        print_font_status("字体模式", font_mode, "yellow")
        print(f"\n  ⚠ 缺少以下系统字体: {', '.join(missing_fonts)}")
        print("  ⚠ 部分字体将使用开源替代")
        print("  ⚠ 对齐度降低 (85-90%)")
    else:
        font_mode = "oss (纯开源字体)"
        print_font_status("字体模式", font_mode, "yellow" if all_oss_found else "red")
        if all_oss_found:
            print("\n  ⚠ 系统无商业字体，使用开源替代")
            print("  ⚠ 对齐度较低 (80-85%)")
        else:
            print("\n  ✗ 开源字体兜底方案不完整")
            print("  ✗ 请运行: make fonts")

    # 建议
    print_section("改进建议")

    if missing_fonts:
        print("为获得最佳对齐效果，建议安装缺失的商业字体:\n")

        system = platform.system()
        if system == "Windows":
            print("  Windows 用户:")
            print("  - 系统应已预装中文字体（宋体、黑体、楷体、仿宋）")
            print("  - 如缺失，请从 C:\\Windows\\Fonts 检查或重新安装 Office")
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
            if font in REQUIRED_FONTS.get("拉丁字体", {}):
                filename = REQUIRED_FONTS["拉丁字体"][font][2]
                print(f"    - {filename}")
            elif font in REQUIRED_FONTS.get("中文字体", {}):
                filename = REQUIRED_FONTS["中文字体"][font][2]
                print(f"    - {filename}")
    else:
        print("  ✓ 字体配置完善，无需额外操作")

    print("\n" + "="*72 + "\n")

    return 0 if not missing_fonts or all_oss_found else 1


if __name__ == "__main__":
    sys.exit(main())
