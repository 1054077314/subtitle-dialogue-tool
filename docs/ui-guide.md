# UI 使用说明

## 启动

```bash
python src/ui_tkinter.py
```

需要 Python 3.10+ 和 tkinter（Python 默认安装）。

## 界面说明

### 输入区

- **字幕文本框**：可直接粘贴字幕文本，也可通过"选择 txt 文件"按钮导入。
- **选择 txt 文件**：打开文件选择窗口，选择 .txt 文件后内容自动填入输入框。
- **清空**：清空输入框和输出框。

### 参数区

- **max_chunk_size**：每块最大字符数，默认 8000。值越小，分块越多。
- **context_size**：前后重叠上下文字符数，默认 500。必须小于 max_chunk_size 的 1/2。

### 操作按钮

- **开始处理**：运行完整 pipeline（清洗 → 分块 → mock 分析 → 人物统一 → 导出 Markdown）。
- **保存为 output.md**：将 Markdown 结果保存到指定位置。

### 输出区

- 显示生成的 Markdown 结果，包含标题、人物表和正文对话。

## 操作流程

1. 启动程序
2. 粘贴字幕文本，或点击"选择 txt 文件"导入
3. （可选）调整 max_chunk_size 和 context_size
4. 点击"开始处理"
5. 在输出区查看 Markdown 结果
6. 点击"保存为 output.md"导出文件

## 注意事项

- 输入不能为空，否则会弹出提示
- 分块参数必须合理：context_size < max_chunk_size / 2
- 当前使用 mock 人物识别（按行交替分配说话人），非真实 AI 识别
