# 项目架构文档

## 项目定位

YouTube 字幕对话稿人物标注工具。把长字幕清洗、分块、识别人名，导出带人物标注的 Markdown 对话稿。

## 目录结构

```
subtitle_dialogue_project_docs/
├── CLAUDE.md                     # AI 开发规范
├── README.md                     # 项目说明
├── PROJECT_STATUS.md             # 当前进度
├── architecture.md               # 本文件
├── 01-requirements.md            # 需求文档
├── 02-project-design.md          # 设计文档
├── 03-module-split.md            # 模块拆分
├── 04-task-plan.md               # 任务计划
├── 05-data-format.md             # 数据格式规范
├── 06-ai-prompt-plan.md          # AI Prompt 计划
├── 07-acceptance-smoke.md        # 验收清单
├── samples/
│   ├── sample_subtitle.txt       # 小样例 (~945B)
│   └── large_sample.txt          # 大样例 (~5.5KB)
└── src/
    ├── main.py                   # CLI 入口
    ├── subtitle_input.py         # 输入读取
    ├── subtitle_cleaner.py       # 清洗
    ├── subtitle_splitter.py      # 分块
    ├── speaker_analyzer.py       # 人物识别 (mock)
    ├── speaker_normalizer.py     # 人物统一
    ├── markdown_exporter.py      # Markdown 导出
    └── ui_tkinter.py             # tkinter GUI
```

## 处理流水线

```
原始文本
  → subtitle_input      读取文件或文本
  → subtitle_cleaner     清洗（去空行、统一换行）
  → subtitle_splitter    分块（句子边界切分 + 上下文重叠）
  → speaker_analyzer     单块人物识别（当前为 mock）
  → speaker_normalizer   全局人物统一（speaker_map + id 映射）
  → markdown_exporter    导出 Markdown（标题 + 人物表 + 正文对话）
```

## 模块依赖关系

```
main.py ─────────────────────────────────────┐
  ├── subtitle_input.py                      │
  ├── subtitle_cleaner.py                    │
  ├── subtitle_splitter.py                   │ 所有业务模块
  ├── speaker_analyzer.py                    │ 零内部依赖
  ├── speaker_normalizer.py                  │
  └── markdown_exporter.py                   │
                                             │
ui_tkinter.py ───────────────────────────────┘
  ├── subtitle_cleaner.py
  ├── subtitle_splitter.py
  ├── speaker_analyzer.py
  ├── speaker_normalizer.py
  └── markdown_exporter.py
```

所有业务模块（cleaner / splitter / analyzer / normalizer / exporter）均为叶子节点，零项目内依赖。`main.py` 和 `ui_tkinter.py` 是两个入口，负责流程编排。

## 模块职责与接口

### subtitle_input.py
- `read_from_text(text) -> str`
- `read_from_file(path) -> str`

### subtitle_cleaner.py
- `clean_subtitle(raw_text) -> str`

### subtitle_splitter.py
- `split_subtitle(text, max_chunk_size=8000, context_size=500, force_split=False) -> list[dict]`
- `split_subtitle_forced(text, max_chunk_size=8000, context_size=500) -> list[dict]`
- chunk 格式：`{chunk_id, text, context_before, context_after}`

### speaker_analyzer.py
- `mock_analyze_chunk(chunk) -> dict`
- 输出格式：`{chunk_id, people, dialogues, warnings}`

### speaker_normalizer.py
- `normalize_speakers(chunk_results) -> dict`
- 输出格式：`{speaker_map, chunks}`

### markdown_exporter.py
- `export_markdown(normalized, title="对话稿") -> str`

## 数据流格式

```
chunk:          {chunk_id, text, context_before, context_after}
analyze 结果:   {chunk_id, people[], dialogues[], warnings[]}
normalize 结果: {speaker_map[], chunks[]}
```

## 当前状态

- Task 1-7 全部完成
- speaker_analyzer 为 mock 实现（按行交替分配说话人）
- 无测试、无 requirements.txt、src/ 无 __pyhaven__.py
- 仅标准库依赖（Python 3.14 + tkinter）

## 待办

- 接真实 API（仅需改 speaker_analyzer.py）
- 补测试
- 补 requirements.txt / pyproject.toml
- src/ 加 __init__.py（消除 sys.path.insert hack）
