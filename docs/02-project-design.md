# 项目设计文档

## 1. 项目定位

这是一个字幕结构化处理工具，不是完整视频平台。核心目标是把长字幕变成带人物标注的对话稿。

第一版优先保证处理链路跑通，不追求复杂 UI 和完整平台功能。

## 2. 推荐技术栈

### 前端

可选：

- React + Vite
- Vue + Vite
- 简单 HTML 页面

第一版也可以只做命令行脚本。

### 后端

可选：

- Node.js + Express
- Python + FastAPI

如果只是本地工具，建议优先 Python 脚本。

### 数据存储

第一版不需要数据库。

中后期可以增加：

- SQLite：保存处理记录。
- JSON 文件：保存中间结果。
- Markdown 文件：保存最终结果。

## 3. 核心处理流程

```text
原始字幕
→ cleanSubtitle()
→ splitSubtitle()
→ analyzeChunkWithLLM()
→ mergeChunkResults()
→ normalizeSpeakers()
→ exportMarkdown()
```

## 4. 核心模块

| 模块 | 职责 |
|---|---|
| 输入模块 | 接收字幕文本 |
| 清洗模块 | 去除噪声、整理换行 |
| 分块模块 | 按句子和长度分块 |
| AI 识别模块 | 调用大模型识别人物和对话 |
| 合并模块 | 合并各分块结果 |
| 人物统一模块 | 统一 speaker_id 和 speaker_name |
| 导出模块 | 导出 Markdown / JSON |

## 5. 分块原则

不要按固定 8000 字硬切。

推荐规则：

- 优先按句号、问号、感叹号切。
- 尽量保留完整句子。
- 每块正文约 6000-8000 字。
- 每块带 300-500 字前文重叠。
- 重叠内容只用于上下文，不进入最终输出。

## 6. 人物识别原则

模型不能确定人物时，不要强行猜名字。

规则：

- 能识别真实姓名时，用真实姓名。
- 只能判断角色时，用 `Host`、`Guest`、`Narrator`。
- 无法判断时，用 `Unknown Speaker`。
- 每个人物必须带 evidence 字段说明依据。

## 7. 合并原则

合并时需要解决：

- 同一人物不同名称。
- 不同人物被误合并。
- 分块重叠内容重复。
- 低置信度人物标注。

合并优先级：

```text
真实姓名 > 稳定角色名 > speaker_id > Unknown Speaker
```

## 8. 第一版不做的功能

- 不做账号登录。
- 不做数据库。
- 不做 YouTube 自动下载。
- 不做视频播放器。
- 不做多人协作。
- 不做复杂权限。
- 不做自动发布。

## 9. UI 输入输出说明

### 输入方式

1. **粘贴文本**：直接在输入框粘贴字幕内容。
2. **导入文件**：点击"选择 txt 文件"，选择 .txt 文件后内容自动填入输入框。

### 可调参数

- **max_chunk_size**：每块最大字符数，默认 8000。值越小分块越多。
- **context_size**：前后重叠上下文字符数，默认 500。必须小于 max_chunk_size / 2。

### 处理流程

点击"开始处理"后，UI 调用现有模块完成：

```text
clean_subtitle → split_subtitle_forced → mock_analyze_chunk → normalize_speakers → export_markdown
```

### 输出

- **界面展示**：Markdown 结果直接显示在输出区。
- **文件保存**：点击"保存为 output.md"，选择位置导出 .md 文件。

### 操作按钮

| 按钮 | 功能 |
|------|------|
| 选择 txt 文件 | 导入 .txt 字幕文件到输入框 |
| 清空 | 清空输入框和输出框 |
| 开始处理 | 运行完整 mock pipeline |
| 保存为 output.md | 将 Markdown 结果保存到文件 |
