"""字幕输入模块：接收文本或文件路径，返回原始字幕内容。"""


def read_from_text(text: str) -> str:
    """从用户粘贴的文本读取字幕。"""
    if not text or not text.strip():
        raise ValueError("input text cannot be empty")
    return text


def read_from_file(file_path: str) -> str:
    """从本地 txt 文件读取字幕。"""
    if not file_path or not file_path.strip():
        raise ValueError("file path cannot be empty")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        raise ValueError("file content is empty")

    return content
