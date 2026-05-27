# 模块拆分文档

## 1. subtitle-input 模块

职责：

- 接收用户输入的字幕文本。
- 判断输入是否为空。
- 判断文本长度。
- 保存原始输入。

输入：

```text
rawSubtitleText
```

输出：

```json
{
  "raw_text": "...",
  "length": 12345
}
```

## 2. subtitle-cleaner 模块

职责：

- 清理多余空行。
- 清理无意义符号。
- 统一换行。
- 保留时间戳信息。

输入：

```text
rawSubtitleText
```

输出：

```text
cleanSubtitleText
```

禁止：

- 不要改写原文意思。
- 不要翻译字幕。
- 不要自行补内容。

## 3. subtitle-splitter 模块

职责：

- 按句子边界切分字幕。
- 控制每块长度。
- 添加重叠上下文。

输入：

```text
cleanSubtitleText
```

输出：

```json
[
  {
    "chunk_id": 1,
    "text": "...",
    "context_before": "...",
    "context_after": "..."
  }
]
```

## 4. speaker-analyzer 模块

职责：

- 调用大模型。
- 识别当前分块中的人物。
- 输出结构化 JSON。

输入：

```json
{
  "chunk_id": 1,
  "text": "...",
  "context_before": "...",
  "context_after": "..."
}
```

输出：

```json
{
  "chunk_id": 1,
  "people": [],
  "dialogues": []
}
```

## 5. result-merger 模块

职责：

- 合并所有分块结果。
- 去除重叠片段造成的重复。
- 保留原顺序。

输入：

```json
[
  {
    "chunk_id": 1,
    "dialogues": []
  }
]
```

输出：

```json
{
  "people": [],
  "dialogues": []
}
```

## 6. speaker-normalizer 模块

职责：

- 建立全局人物表。
- 合并同一人物的不同称呼。
- 标记低置信度人物。

输出：

```json
{
  "speaker_map": {
    "S1": "Host",
    "S2": "Nick"
  }
}
```

## 7. markdown-exporter 模块

职责：

- 输出人物表。
- 输出正文对话。
- 标记不确定人物。

输出：

```md
# 对话稿
```
