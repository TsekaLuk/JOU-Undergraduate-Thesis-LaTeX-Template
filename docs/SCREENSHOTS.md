# 截图指南

README 截图已经改成脚本生成，不再依赖手工截屏或手工拼图。

## 生成命令

```bash
make readme-images
make cover-diff
```

## README 预览产物

`make readme-images` 会生成：

- `docs/images/cover-compare.png`
- `docs/images/thesis-gallery.png`
- `docs/images/abstract-compare.png`
- `docs/images/body-compare.png`
- `docs/images/forms-gallery.png`

这些图用于 README 的产品化展示区：

- `cover-compare.png`：封面横向对比
- `thesis-gallery.png`：论文主模板六宫格
- `abstract-compare.png` / `body-compare.png`：关键版式细节对比
- `forms-gallery.png`：配套模板六宫格

## 技术验证产物

`make cover-diff` 会生成：

- `docs/assets/thesis-cover-overlay.png`
- `docs/assets/thesis-cover-overlay-focus.png`
- `docs/assets/thesis-cover-diff.png`
- `docs/assets/thesis-cover-diff-focus.png`
- `docs/assets/thesis-cover-checker.png`
- `docs/assets/thesis-cover-checker-focus.png`

这些图用于人工排查字体和几何残差，不作为 README 首屏展示图。

## 当前页面映射

README 预览使用以下页面基线：

- 封面：工作手册 PDF 第 39 页 vs `main.pdf` 第 1 页
- 中文摘要：工作手册 PDF 第 41 页 vs `main.pdf` 第 3 页（README 使用摘要内容区裁剪，不包含手册注释区）
- 正文样页：工作手册 PDF 第 45 页 vs `body-sample.pdf` 第 1 页
- 论文画廊：`main.pdf` 第 1 / 3 / 4 / 5 / 7 / 14 页
- 表单画廊：`topic-selection.pdf`、`task-book-science.pdf`、`proposal-science.pdf`、`midterm-check.pdf`、`thesis-evaluation.pdf`、`defense-record.pdf`

## 检查清单

- 先运行 `make`，确保 `main.pdf` 为最新产物
- 确认 `templates/` 下代表性表单 PDF 存在
- 生成完截图后，确认 README 引用的路径与文件名一致
- 如需检查最后残差，优先查看 `docs/assets/` 中的 diff/checker 产物
