# 字体缺失警告示例

## 场景：用户系统没有商业字体

当用户编译论文但系统缺少商业字体时，会看到以下警告：

---

## 默认模式输出（警告但继续编译）

```
This is XeTeX, Version 3.141592653-2.6-0.999995 (TeX Live 2024)

===============================================
JOU Font Mode: oss
===============================================

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! 错误: 未检测到商业字体                  !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

毕业论文需要标准化，必须使用商业字体！
当前未找到任何商业字体（对齐度将降低至 80-85%）

解决方案:

>>> 第一步：运行字体检测脚本

    python3 scripts/check_fonts.py

>>> 第二步：根据你的操作系统安装字体

    Windows 用户:
    - 检查 C:\Windows\Fonts 是否有宋体、楷体、仿宋
    - 如缺失，安装 Microsoft Office (自带标准字体)

    macOS 用户:
    - 打开「字体册」应用
    - 搜索 STSong, STKaiti, STFangsong
    - 如缺失，从系统安装盘恢复字体

    Linux 用户:
    - Ubuntu/Debian: sudo apt install ttf-mscorefonts-installer
    - Arch Linux:    yay -S ttf-ms-fonts
    - 安装后运行:    fc-cache -fv

>>> 第三步（可选）：手动下载字体

    将以下字体文件放入 fonts/proprietary/:
    - SimSun.ttf (宋体)
    - SimHei.ttf (黑体)
    - KaiTi_GB2312.ttf (楷体)
    - FangSong_GB2312.ttf (仿宋)
    - TimesNewRoman-Regular.ttf

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! 警告模式：继续使用开源字体（对齐度降低）!
! 提示：如需强制检查，添加 strictfonts 选项!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

[1] [2] [3] ... (继续编译)
```

---

## 严格模式输出（阻止编译）

启用 `strictfonts` 选项后：

```latex
\documentclass[strictfonts]{jouthesis}
```

编译输出：

```
This is XeTeX, Version 3.141592653-2.6-0.999995 (TeX Live 2024)

===============================================
JOU Font Mode: oss
===============================================

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! 错误: 未检测到商业字体                  !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

[... 同样的安装指南 ...]

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! 严格字体检查已启用，编译终止          !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Package joufonts Error: Commercial fonts required but not found!
Strict font checking is enabled.

Run: python3 scripts/check_fonts.py
See above for installation instructions.

See the joufonts package documentation for explanation.
Type  H <return>  for immediate help.
 ...

l.123 \begin{document}

?
! Emergency stop.
```

---

## 成功检测到商业字体

当系统有商业字体时，简洁输出：

```
This is XeTeX, Version 3.141592653-2.6-0.999995 (TeX Live 2024)

===============================================
JOU Font Mode: system-licensed
===============================================

[1] [2] [3] ... (正常编译)
```

---

## 对比：之前 vs 现在

### 之前（静默fallback）

```
This is XeTeX...
[1] [2] [3] ...
Output written on main.pdf (25 pages).
```

**问题**:
- ❌ 用户不知道使用了错误的字体
- ❌ 对齐度降低但无提示
- ❌ 不知道如何修复

### 现在（醒目警告）

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! 错误: 未检测到商业字体                  !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

>>> 第一步：运行字体检测脚本
    python3 scripts/check_fonts.py

>>> 第二步：根据你的操作系统安装字体
    [详细安装命令...]
```

**优势**:
- ✅ 用户立即知道有问题
- ✅ 清晰的分步解决方案
- ✅ 平台特定的安装命令
- ✅ 可选的严格模式强制修复

---

## 使用建议

### 开发阶段

使用默认模式（警告但继续）：

```bash
make  # 会看到警告，但可以预览
```

### 最终提交前

启用严格模式，确保字体正确：

```latex
% main.tex
\documentclass[strictfonts]{jouthesis}
```

```bash
make  # 缺少字体会直接报错，强制修复
```

---

## 平台特定示例

### Windows 用户看到的警告

```
    Windows 用户:
    - 检查 C:\Windows\Fonts 是否有宋体、楷体、仿宋
    - 如缺失，安装 Microsoft Office (自带标准字体)
```

### macOS 用户看到的警告

```
    macOS 用户:
    - 打开「字体册」应用
    - 搜索 STSong, STKaiti, STFangsong
    - 如缺失，从系统安装盘恢复字体
```

### Linux 用户看到的警告

```
    Linux 用户:
    - Ubuntu/Debian: sudo apt install ttf-mscorefonts-installer
    - Arch Linux:    yay -S ttf-ms-fonts
    - 安装后运行:    fc-cache -fv
```

---

## 总结

新的警告机制确保：

1. **用户不会在不知情的情况下使用错误字体**
2. **提供清晰的、可操作的解决方案**
3. **支持两种模式满足不同需求**
   - 开发预览：警告但继续
   - 最终提交：严格检查
4. **跨平台支持**，每个系统都有具体的安装命令
