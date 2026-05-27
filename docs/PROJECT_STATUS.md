# 项目状态总结

## 1. 已完成的 Task

| Task | 状态 | 说明 |
|------|------|------|
| Task 1 | 完成 | 字幕输入与清洗（subtitle_input + subtitle_cleaner） |
| Task 2 | 完成 | 字幕分块（subtitle_splitter，支持句子边界切分 + 上下文重叠） |
| Task 3 | 完成 | Mock 人物识别（speaker_analyzer，按行交替分配说话人） |
| Task 4 | 完成 | Mock 分块分析（--mock-analyze-all，强制分块逻辑） |
| Task 5 | 完成 | 人物统一（speaker_normalizer，全局 speaker_map + id 映射） |
| Task 6 | 完成 | Markdown 导出（markdown_exporter，标题 + 人物表 + 正文对话） |
| Task 7 | 完成 | 简单 tkinter UI（ui_tkinter.py） |
| Phase 2 | 完成 | UI 完善：清空按钮、分块参数输入、UI 使用文档 |

## 2. 运行命令

```bash
# CLI 命令
python src/main.py <文件>                              # 清洗输出
python src/main.py <文件> --split                      # 分块显示
python src/main.py <文件> --mock-analyze-first         # 第一个 chunk mock 分析
python src/main.py <文件> --mock-analyze-all           # 所有 chunk mock 分析
python src/main.py <文件> --mock-analyze-all --normalize-speakers          # + 人物统一
python src/main.py <文件> --mock-analyze-all --normalize-speakers --export-markdown  # + 导出 MD
python src/main.py <文件> --mock-analyze-all --normalize-speakers --export-markdown --max-chunk-size 500 --context-size 100

# UI 命令
python src/ui_tkinter.py
```

## 3. 核心文件结构

```
src/
├── main.py                 # CLI 入口，参数解析，流程编排
├── subtitle_input.py       # 字幕输入（文件/文本）
├── subtitle_cleaner.py     # 清洗（去空行、统一换行）
├── subtitle_splitter.py    # 分块（句子边界切分 + force_split）
├── speaker_analyzer.py     # mock 人物识别（按行交替）
├── speaker_normalizer.py   # 人物统一（全局 id 映射）
├── markdown_exporter.py    # Markdown 导出
└── ui_tkinter.py           # tkinter UI
samples/
├── sample_subtitle.txt     # 小样例（~945 字节）
└── large_sample.txt        # 大样例（~5568 字节）
```

## 4. 还没做的功能

- **真实 API 调用** — speaker_analyzer 目前是 mock，未接任何 LLM
- **真实人物识别** — 未做基于内容的说话人推断
- **字幕自动下载** — 未接 YouTube API
- **数据库存储** — 全部内存处理
- **云端部署 / 多用户** — 未涉及
- **复杂前端 UI** — tkinter 仅最小可用

## 5. 接真实 API 应该只改哪个模块

**只改 `src/speaker_analyzer.py`。**

该模块的职责边界清晰：输入一个 chunk dict，输出 `{chunk_id, people, dialogues, warnings}`。当前 mock 实现按行交替分配说话人，接真实 API 只需替换 `mock_analyze_chunk` 函数体，其余模块（cleaner → splitter → normalizer → exporter）无需改动。
