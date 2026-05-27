"""人物识别模块（mock 版本）：对单个 chunk 进行人物识别，返回固定结构 JSON。"""


def mock_analyze_chunk(chunk: dict) -> dict:
    """对单个 chunk 进行 mock 人物识别。

    Args:
        chunk: 分块数据，包含 chunk_id, text, context_before, context_after

    Returns:
        包含 chunk_id, people, dialogues, warnings 的字典
    """
    chunk_id = chunk.get("chunk_id", 1)
    text = chunk.get("text", "")

    # 简单按行拆分作为对话
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # mock: 固定返回两个人物
    people = [
        {
            "speaker_id": "S1",
            "speaker_name": "Speaker A",
            "role": "host",
            "evidence": "mock: identified as first speaker",
            "confidence": 0.80
        },
        {
            "speaker_id": "S2",
            "speaker_name": "Speaker B",
            "role": "guest",
            "evidence": "mock: identified as second speaker",
            "confidence": 0.75
        }
    ]

    # mock: 按行交替分配说话人
    dialogues = []
    for i, line in enumerate(lines):
        speaker_id = "S1" if i % 2 == 0 else "S2"
        speaker_name = "Speaker A" if i % 2 == 0 else "Speaker B"
        dialogues.append({
            "order": i + 1,
            "speaker_id": speaker_id,
            "speaker_name": speaker_name,
            "text": line,
            "confidence": 0.80
        })

    warnings = []
    if not lines:
        warnings.append("empty chunk text")

    return {
        "chunk_id": chunk_id,
        "people": people,
        "dialogues": dialogues,
        "warnings": warnings
    }


if __name__ == "__main__":
    # 示例运行
    sample_chunk = {
        "chunk_id": 1,
        "text": "Hello everyone, welcome to the show.\nThanks for having me, it's great to be here.\nSo tell us about your latest project.",
        "context_before": "",
        "context_after": ""
    }

    import json
    result = mock_analyze_chunk(sample_chunk)
    print(json.dumps(result, indent=2, ensure_ascii=False))
