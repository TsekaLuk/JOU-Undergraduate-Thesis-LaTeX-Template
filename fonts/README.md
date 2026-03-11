# Fonts

## 目标

这个模板的默认字体策略是“规范四字体优先”，不是“追某一份 WPS PDF 的私有字库”。

论文排版首先要满足学校常见学术字体语义：

- `楷体_GB2312`
- `宋体`
- `黑体`
- `Times New Roman`

WPS 字体仍然支持，但只是兼容兜底，不是默认优先级。

## 字体优先级

### 1. `fonts/proprietary/` 本地正式字体

如果你已经拥有合法字体文件，把它们放在 `fonts/proprietary/`，模板会优先使用。

如果不想手动复制，可直接运行：

```bash
make import-fonts
```

该命令会自动扫描系统字体目录、WPS 安装目录，以及桌面上的常见字体文件夹（如 `~/Desktop/毕业论文字体`），并按模板约定文件名复制到 `fonts/proprietary/`。

推荐文件名：

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
- `STLiti.ttf`（可选）

### 2. 系统标准学术字体

模板会优先探测系统上的标准字体：

- Windows:
  - `C:/Windows/Fonts/times.ttf`
  - `C:/Windows/Fonts/simsun.ttc`
  - `C:/Windows/Fonts/simhei.ttf`
  - `C:/Windows/Fonts/simkai.ttf`
  - `C:/Windows/Fonts/simfang.ttf`
- 系统字体名:
  - `Times New Roman`
  - `SimSun`
  - `SimHei`
  - `KaiTi_GB2312` / `KaiTi`
  - `FangSong_GB2312` / `FangSong`
- macOS:
  - `STSong`
  - `STHeiti`
  - `STKaiti`
  - `STFangsong`

### 3. WPS 兼容字体

当标准学术字体不可用时，模板才会尝试：

- WPS 安装目录中的内置字体
- 系统已安装的 `HY...` / `FZ...` 字体

这层的目标是“兼容可用”，不是“默认优先”。

### 4. `fonts/opensource/` 开源兜底

仓库自带开源字体用于跨平台稳定编译：

- `Tinos`
- `Courier Prime`
- `Noto Serif CJK SC`
- `Noto Sans CJK SC`
- `LXGW WenKai GB`
- `FandolFang`

这层适合：

- 日常编辑
- CI 编译
- Linux/macOS/Windows 一致预览

但它不是理想的最终提交字体层。

## 模式说明

### `licensed`

使用 `fonts/proprietary/` 中的正式字体。  
这是最稳的高质量交付模式。

### `system-licensed`

使用系统已有的标准学术字体。  
这是最推荐的日常模式，尤其适合 Windows 用户。

### `wps-compat`

标准学术字体不完整时，使用 WPS 兼容字体。  
可用，但不是模板默认目标。

### `oss`

只使用仓库内置开源字体。  
适合预览、开发、CI，不建议作为最终提交的理想模式。

## Windows 用户建议

Windows 是最容易命中标准四字体的平台。

推荐顺序：

1. 直接使用系统 / Office 自带字体
2. 如果客户机路径特殊，配置 `styles/joufontspaths.local.tex`
3. 如果标准字体不完整，再让模板回退到 WPS 兼容字体

## 检查命令

```bash
python3 scripts/check_fonts.py
```

这个脚本会告诉你当前落在哪个模式，并指出缺的标准字体。

## 开源映射

| 标准字体 | 开源兜底 |
| --- | --- |
| Times New Roman | Tinos |
| Courier New | Courier Prime |
| 宋体 | Noto Serif CJK SC |
| 黑体 | Noto Sans CJK SC |
| 楷体 / 楷体_GB2312 | LXGW WenKai GB |
| 仿宋 / 仿宋_GB2312 | FandolFang |
| 方正小标宋简体 | Noto Serif CJK SC Black |
| 行楷 | LXGW WenKai GB Medium |

## 说明

公共仓库不会分发商业字体文件。  
如果你有合法授权，把字体放进 `fonts/proprietary/` 即可，模板会自动接管。
