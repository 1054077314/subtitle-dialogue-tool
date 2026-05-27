"""字幕分块模块：按句子边界切分字幕，添加前后重叠上下文。"""

import re


def split_subtitle(text: str, max_chunk_size: int = 8000, context_size: int = 500, force_split: bool = False) -> list:
    """按句子边界切分字幕。

    Args:
        text: 清洗后的字幕文本
        max_chunk_size: 每个 chunk 的最大字符数，默认 8000
        context_size: 前后重叠上下文的字符数，默认 500
        force_split: 强制分块，即使文本长度不超过 max_chunk_size

    Returns:
        chunk 列表，每个 chunk 包含 chunk_id, text, context_before, context_after
    """
    if not text or not text.strip():
        raise ValueError("input text cannot be empty")

    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be positive")

    if context_size < 0:
        raise ValueError("context_size must be non-negative")

    if context_size * 2 >= max_chunk_size:
        raise ValueError("context_size too large relative to max_chunk_size")

    # 按句子边界切分
    sentences = _split_into_sentences(text)

    if not sentences:
        raise ValueError("no sentences found in text")

    # 非强制模式下，如果总长度不超过 max_chunk_size，返回单个 chunk
    total_length = sum(len(s) for s in sentences) + len(sentences) - 1  # 加换行符
    if total_length <= max_chunk_size and not force_split:
        return [{
            "chunk_id": 1,
            "text": text,
            "context_before": "",
            "context_after": ""
        }]

    # 分块
    chunks = _build_chunks(sentences, max_chunk_size, context_size)

    return chunks


def split_subtitle_forced(text: str, max_chunk_size: int = 8000, context_size: int = 500) -> list:
    """强制分块模式：确保输出多个 chunk，即使文本较短。

    内部根据文本长度自动调整 max_chunk_size 和 context_size。
    """
    text_len = len(text)
    if text_len <= max_chunk_size:
        force_max = max(500, text_len // 2)
    else:
        force_max = max_chunk_size

    force_ctx = min(context_size, force_max // 4)

    return split_subtitle(text, max_chunk_size=force_max, context_size=force_ctx, force_split=True)


def _split_into_sentences(text: str) -> list:
    """将文本按句子边界切分。

    分割点：句号、问号、感叹号后面跟空白或换行，但排除常见缩写（Dr., Mr., Mrs. 等）。
    """
    # 先保护常见缩写
    protected = text
    abbreviations = [
        (r'\bDr\.', 'Dr<<DOT>>'),
        (r'\bMr\.', 'Mr<<DOT>>'),
        (r'\bMrs\.', 'Mrs<<DOT>>'),
        (r'\bMs\.', 'Ms<<DOT>>'),
        (r'\bProf\.', 'Prof<<DOT>>'),
        (r'\bSt\.', 'St<<DOT>>'),
        (r'\bvs\.', 'vs<<DOT>>'),
        (r'\be\.g\.', 'e<<DOT>>g<<DOT>>'),
        (r'\bi\.e\.', 'i<<DOT>>e<<DOT>>'),
    ]

    for pattern, replacement in abbreviations:
        protected = re.sub(pattern, replacement, protected)

    # 按句子结束符切分
    parts = re.split(r'(?<=[.!?])\s+', protected.strip())

    # 恢复缩写
    sentences = []
    for s in parts:
        restored = s.replace('<<DOT>>', '.')
        if restored.strip():
            sentences.append(restored)

    return sentences


def _build_chunks(sentences: list, max_chunk_size: int, context_size: int) -> list:
    """根据句子列表构建 chunks。"""
    chunks = []
    current_chunk_sentences = []
    current_chunk_length = 0
    chunk_id = 1

    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        # 计算加入这个句子后的长度（加上换行符）
        new_length = current_chunk_length + len(sentence) + (1 if current_chunk_sentences else 0)

        if new_length <= max_chunk_size or not current_chunk_sentences:
            # 可以加入当前 chunk
            current_chunk_sentences.append(sentence)
            current_chunk_length = new_length
            i += 1
        else:
            # 当前 chunk 已满，保存并开始新 chunk
            chunk_text = "\n".join(current_chunk_sentences)
            context_before = _get_context_before(sentences, i - len(current_chunk_sentences), context_size)
            context_after = _get_context_after(sentences, i, context_size)

            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "context_before": context_before,
                "context_after": context_after
            })

            chunk_id += 1
            current_chunk_sentences = []
            current_chunk_length = 0

    # 处理最后一个 chunk
    if current_chunk_sentences:
        chunk_text = "\n".join(current_chunk_sentences)
        context_before = _get_context_before(sentences, len(sentences) - len(current_chunk_sentences), context_size)
        context_after = ""

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "context_before": context_before,
            "context_after": context_after
        })

    # 补充 context_after（需要从后往前填充）
    _fill_context_after(chunks, sentences, context_size)

    return chunks


def _get_context_before(sentences: list, start_index: int, context_size: int) -> str:
    """获取指定位置之前的上下文。"""
    if start_index <= 0:
        return ""

    context_parts = []
    total_length = 0

    for i in range(start_index - 1, -1, -1):
        sentence = sentences[i]
        if total_length + len(sentence) + 1 > context_size:
            break
        context_parts.insert(0, sentence)
        total_length += len(sentence) + 1

    return "\n".join(context_parts)


def _get_context_after(sentences: list, end_index: int, context_size: int) -> str:
    """获取指定位置之后的上下文。"""
    if end_index >= len(sentences):
        return ""

    context_parts = []
    total_length = 0

    for i in range(end_index, len(sentences)):
        sentence = sentences[i]
        if total_length + len(sentence) + 1 > context_size:
            break
        context_parts.append(sentence)
        total_length += len(sentence) + 1

    return "\n".join(context_parts)


def _fill_context_after(chunks: list, sentences: list, context_size: int) -> None:
    """填充所有 chunk 的 context_after。"""
    if len(chunks) <= 1:
        return

    # 记录每个 chunk 对应的句子范围
    sentence_index = 0
    for chunk in chunks:
        chunk_text = chunk["text"]
        chunk_sentences = chunk_text.split("\n")

        # 找到这个 chunk 结束的位置
        sentence_index += len(chunk_sentences)

        # 获取 context_after
        chunk["context_after"] = _get_context_after(sentences, sentence_index, context_size)

    # 最后一个 chunk 的 context_after 为空
    chunks[-1]["context_after"] = ""
