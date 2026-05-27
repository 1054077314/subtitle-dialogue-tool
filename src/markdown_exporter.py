"""Markdown 导出模块：将标准化后的对话结果导出为 Markdown 格式。"""


def export_markdown(normalized: dict, title: str = "对话稿") -> str:
    """将 normalize_speakers 的输出导出为 Markdown 字符串。

    Args:
        normalized: normalize_speakers 返回的字典，包含 speaker_map 和 chunks
        title: Markdown 标题

    Returns:
        Markdown 格式的完整文本
    """
    speaker_map = normalized.get("speaker_map", [])
    chunks = normalized.get("chunks", [])

    lines = []

    # 标题
    lines.append(f"# {title}")
    lines.append("")

    # 人物表
    if speaker_map:
        lines.append("## 人物表")
        lines.append("")
        lines.append("| ID | 姓名 | 角色 |")
        lines.append("|---|---|---|")
        for sp in speaker_map:
            lines.append(f"| {sp['global_speaker_id']} | {sp['name']} | {sp['role']} |")
        lines.append("")

    # 正文对话
    lines.append("## 对话")
    lines.append("")

    for chunk in chunks:
        for d in chunk.get("dialogues", []):
            speaker_name = d.get("speaker_name", d.get("speaker_id", "Unknown"))
            text = d.get("text", "")
            lines.append(f"**{speaker_name}：** {text}")
            lines.append("")

    return "\n".join(lines)
