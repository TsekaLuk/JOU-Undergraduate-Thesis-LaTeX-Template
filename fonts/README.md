# Fonts

## 字体加载策略（优先商业字体）

**毕业论文需要标准化，优先使用商业字体**

模板自动按以下优先级加载字体：

1. **优先级 1 - 本地商业字体文件**
   `fonts/proprietary/` 目录中的字体文件（手动放入）

2. **优先级 2 - 系统商业字体**
   操作系统已安装的标准字体（跨平台自动检测）
   - Windows: SimSun, SimHei, KaiTi, FangSong, Times New Roman, Arial
   - macOS: STSong, STHeiti, STKaiti, STFangsong, Times New Roman, Arial
   - Linux: 需手动安装 Windows 字体或使用 wine-fonts

3. **优先级 3 - 开源字体（应急方案）**
   `fonts/opensource/` 仓库内置字体
   - ⚠️ **仅作临时应急**，对齐度降低至 80-85%
   - ⚠️ **编译时会输出醒目警告**，提示安装商业字体
   - ⚠️ **不推荐用于最终提交**

---

## 字体自动选择（用户友好）

### 默认模式（智能选择 + 简洁提示）

模板会**自动选择最佳可用字体**，不会阻止编译：

**有商业字体时**：
```
===============================================
Font Mode: system-licensed
Status: Using system commercial fonts (Excellent)
===============================================
```

**无商业字体时**：
```
===============================================
Font Mode: oss
Status: Using open source fonts (Good for preview)
===============================================

TIP: For best alignment with the official handbook,
     install commercial fonts on your system.
     Check: python3 scripts/check_fonts.py
```

开源字体完全可用于：
- ✅ 日常编辑和预览
- ✅ 排版调整和内容修改
- ✅ 与导师讨论初稿

### 严格模式（最终提交检查）

**仅在最终提交前**启用，确保使用商业字体：

```latex
% main.tex
\documentclass[strictfonts]{jouthesis}
```

此时缺少商业字体会终止编译并提示安装。

---

## 推荐配置（确保最佳对齐）

### Windows 用户

系统已预装所需中文字体，只需确保安装了 Times New Roman 和 Arial（Office 自带）。

### macOS 用户

系统已预装华文字库（STSong, STKaiti 等）和 Times New Roman。

### Linux 用户

安装 Windows 字体包以获得最佳对齐：

```bash
# Ubuntu / Debian
sudo apt install ttf-mscorefonts-installer

# Arch Linux
yay -S ttf-ms-fonts

# 或手动安装（需获得字体授权）
sudo mkdir -p /usr/share/fonts/truetype/msfonts
sudo cp SimSun.ttf SimHei.ttf KaiTi.ttf FangSong.ttf /usr/share/fonts/truetype/msfonts/
sudo fc-cache -fv
```

---

## Open-source font mapping (仅供参考)

| Handbook font | Default bundled replacement |
| --- | --- |
| Times New Roman | Tinos |
| Arial | Noto Sans CJK SC |
| Courier New | Courier Prime |
| 宋体 / 华文中宋 | Noto Serif CJK SC |
| 黑体 | Noto Sans CJK SC |
| 楷体 / 楷体_GB2312 / 华文楷体 | LXGW WenKai GB |
| 仿宋_GB2312 / 华文仿宋 | FandolFang |
| 方正小标宋简体 | Noto Serif CJK SC Black |
| 华文行楷 | LXGW WenKai GB Medium |
| 隶书 | Noto Serif CJK SC Black |

## Proprietary override files

If you have a valid font license, place files with these exact names under `fonts/proprietary/`:

- `TimesNewRoman-Regular.ttf`
- `TimesNewRoman-Bold.ttf`
- `Arial-Regular.ttf`
- `Arial-Bold.ttf`
- `CourierNew-Regular.ttf`
- `CourierNew-Bold.ttf`
- `SimSun.ttf`
- `SimHei.ttf`
- `KaiTi_GB2312.ttf`
- `FangSong_GB2312.ttf`
- `FangZhengXiaoBiaoSongJianTi.ttf`
- `STXingkai.ttf`

When the proprietary files are present, the template automatically switches to `licensed` font mode for the corresponding families.
