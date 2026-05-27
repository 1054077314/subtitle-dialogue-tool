"""简单 tkinter UI：输入字幕文本，处理后显示并保存 Markdown。"""

import sys
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from subtitle_cleaner import clean_subtitle
from subtitle_splitter import split_subtitle_forced
from speaker_analyzer import mock_analyze_chunk
from speaker_normalizer import normalize_speakers
from markdown_exporter import export_markdown


class App:
    def __init__(self, root):
        root.title("字幕对话稿生成器")
        root.geometry("800x600")

        # 输入区
        tk.Label(root, text="字幕文本：").pack(anchor="w", padx=8, pady=(8, 0))
        self.input_box = scrolledtext.ScrolledText(root, height=12)
        self.input_box.pack(fill="both", expand=True, padx=8, pady=4)

        # 参数区
        param_frame = tk.Frame(root)
        param_frame.pack(fill="x", padx=8, pady=2)
        tk.Label(param_frame, text="max_chunk_size:").pack(side="left")
        self.max_chunk_var = tk.StringVar(value="8000")
        tk.Entry(param_frame, textvariable=self.max_chunk_var, width=8).pack(side="left", padx=(2, 12))
        tk.Label(param_frame, text="context_size:").pack(side="left")
        self.context_var = tk.StringVar(value="500")
        tk.Entry(param_frame, textvariable=self.context_var, width=8).pack(side="left", padx=(2, 12))
        tk.Button(param_frame, text="清空", command=self.clear).pack(side="left", padx=(8, 0))

        # 按钮区
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=8, pady=4)
        tk.Button(btn_frame, text="选择 txt 文件", command=self.open_file).pack(side="left")
        tk.Button(btn_frame, text="开始处理", command=self.process).pack(side="left", padx=(8, 0))
        tk.Button(btn_frame, text="保存为 output.md", command=self.save).pack(side="left", padx=(8, 0))

        self.status_label = tk.Label(btn_frame, text="", fg="gray")
        self.status_label.pack(side="right")

        # 输出区
        tk.Label(root, text="Markdown 结果：").pack(anchor="w", padx=8, pady=(4, 0))
        self.output_box = scrolledtext.ScrolledText(root, height=16)
        self.output_box.pack(fill="both", expand=True, padx=8, pady=4)

        self.last_markdown = ""

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", content)
        self.status_label.config(text=f"已加载 {os.path.basename(path)}")

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.last_markdown = ""
        self.status_label.config(text="已清空")

    def process(self):
        raw = self.input_box.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("提示", "请输入字幕文本")
            return

        try:
            max_chunk_size = int(self.max_chunk_var.get())
            context_size = int(self.context_var.get())
        except ValueError:
            messagebox.showwarning("提示", "分块参数必须为整数")
            return

        try:
            cleaned = clean_subtitle(raw)
            chunks = split_subtitle_forced(cleaned, max_chunk_size=max_chunk_size, context_size=context_size)
            results = [mock_analyze_chunk(c) for c in chunks]
            normalized = normalize_speakers(results)
            md = export_markdown(normalized)
        except Exception as e:
            messagebox.showerror("处理出错", str(e))
            return

        self.last_markdown = md
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", md)
        self.status_label.config(text=f"完成：{len(chunks)} 个 chunk，{len(results)} 条分析结果")

    def save(self):
        if not self.last_markdown:
            messagebox.showwarning("提示", "请先处理字幕")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md")],
            initialfile="output.md"
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.last_markdown)
        self.status_label.config(text=f"已保存到 {path}")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
