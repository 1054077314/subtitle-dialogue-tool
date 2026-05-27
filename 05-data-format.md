# 数据格式约定

## 1. Chunk 数据格式

```json
{
  "chunk_id": 1,
  "start_index": 0,
  "end_index": 8000,
  "context_before": "",
  "text": "current chunk text",
  "context_after": "next context text"
}
```

## 2. 单块 AI 返回格式

```json
{
  "chunk_id": 1,
  "people": [
    {
      "speaker_id": "S1",
      "speaker_name": "Host",
      "role": "host",
      "evidence": "opens the conversation and asks questions",
      "confidence": 0.85
    }
  ],
  "dialogues": [
    {
      "order": 1,
      "speaker_id": "S1",
      "speaker_name": "Host",
      "text": "Hello everyone, welcome back.",
      "confidence": 0.86
    }
  ],
  "warnings": []
}
```

## 3. 全局人物表格式

```json
{
  "speaker_map": [
    {
      "global_speaker_id": "G1",
      "name": "Host",
      "aliases": ["Speaker 1", "Interviewer"],
      "role": "host",
      "confidence": 0.88
    }
  ]
}
```

## 4. 最终结果格式

```json
{
  "title": "Transcript Dialogue",
  "speakers": [],
  "dialogues": [],
  "warnings": []
}
```

## 5. Markdown 输出格式

```md
# 对话稿

## 人物表

- Host：主持人
- Nick：嘉宾

## 正文

**Host：** Hello everyone.

**Nick：** Thanks for having me.
```
