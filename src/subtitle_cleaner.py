"""字幕清洗模块：清理多余空行、异常换行，保留原文内容。"""


def clean_subtitle(raw_text: str) -> str:
    """清洗字幕文本。

    规则：
    1. 统一换行符为 \\n
    2. 清理连续空行，保留单个换行
    3. 去除每行首尾空白
    4. 保留时间戳信息
    5. 不改写原文意思
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("input text cannot be empty")

    # 统一换行符
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # 按行处理
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned_lines.append(stripped)

    # 用单个换行连接
    result = "\n".join(cleaned_lines)

    if not result:
        raise ValueError("cleaned content is empty")

    return result
