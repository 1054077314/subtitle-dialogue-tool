"""命令行入口：支持从文本或文件读取字幕，输出清洗结果，支持分块。"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from subtitle_input import read_from_text, read_from_file
from subtitle_cleaner import clean_subtitle
from subtitle_splitter import split_subtitle, split_subtitle_forced
from speaker_analyzer import mock_analyze_chunk
from speaker_normalizer import normalize_speakers
from markdown_exporter import export_markdown


def parse_args(args: list) -> dict:
    """解析命令行参数。"""
    result = {
        "input_type": None,
        "input_value": None,
        "split": False,
        "mock_analyze_first": False,
        "mock_analyze_all": False,
        "max_chunk_size": 8000,
        "context_size": 500,
        "output_json": False,
        "normalize_speakers": False,
        "export_markdown": False
    }

    i = 0
    while i < len(args):
        if args[i] == "--text":
            if i + 1 >= len(args):
                print("Error: subtitle text required after --text")
                sys.exit(1)
            result["input_type"] = "text"
            result["input_value"] = args[i + 1]
            i += 2
        elif args[i] == "--split":
            result["split"] = True
            i += 1
        elif args[i] == "--mock-analyze-first":
            result["mock_analyze_first"] = True
            i += 1
        elif args[i] == "--mock-analyze-all":
            result["mock_analyze_all"] = True
            i += 1
        elif args[i] == "--max-chunk-size":
            if i + 1 >= len(args):
                print("Error: value required after --max-chunk-size")
                sys.exit(1)
            try:
                result["max_chunk_size"] = int(args[i + 1])
            except ValueError:
                print("Error: --max-chunk-size must be an integer")
                sys.exit(1)
            i += 2
        elif args[i] == "--context-size":
            if i + 1 >= len(args):
                print("Error: value required after --context-size")
                sys.exit(1)
            try:
                result["context_size"] = int(args[i + 1])
            except ValueError:
                print("Error: --context-size must be an integer")
                sys.exit(1)
            i += 2
        elif args[i] == "--json":
            result["output_json"] = True
            i += 1
        elif args[i] == "--normalize-speakers":
            result["normalize_speakers"] = True
            i += 1
        elif args[i] == "--export-markdown":
            result["export_markdown"] = True
            i += 1
        elif not args[i].startswith("--"):
            result["input_type"] = "file"
            result["input_value"] = args[i]
            i += 1
        else:
            print(f"Error: unknown option {args[i]}")
            sys.exit(1)

    return result


def main():
    args = parse_args(sys.argv[1:])

    if not args["input_type"]:
        print("Usage:")
        print("  python main.py <subtitle_file_path> [--split] [--json]")
        print("  python main.py --text <subtitle_text> [--split] [--json]")
        print("  python main.py <subtitle_file_path> --mock-analyze-first")
        print("  python main.py <subtitle_file_path> --mock-analyze-all")
        print("")
        print("Options:")
        print("  --split              Split subtitle into chunks")
        print("  --mock-analyze-first Analyze first chunk with mock speaker detection")
        print("  --mock-analyze-all   Analyze all chunks with mock speaker detection")
        print("  --normalize-speakers Normalize speakers across all chunks (use with --mock-analyze-all)")
        print("  --export-markdown    Export to Markdown (use with --mock-analyze-all --normalize-speakers)")
        print("  --json               Output in JSON format")
        print("  --max-chunk-size N   Max chunk size in characters (default: 8000)")
        print("  --context-size N     Context overlap size in characters (default: 500)")
        print("")
        print("Example:")
        print('  python main.py sample.txt')
        print('  python main.py sample.txt --split')
        print('  python main.py sample.txt --split --json')
        print('  python main.py sample.txt --mock-analyze-first')
        print('  python main.py sample.txt --mock-analyze-all')
        print('  python main.py --text "Hello everyone. Welcome back." --split')
        sys.exit(1)

    # 读取输入
    if args["input_type"] == "text":
        try:
            raw_text = read_from_text(args["input_value"])
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        try:
            raw_text = read_from_file(args["input_value"])
        except FileNotFoundError:
            print(f"Error: file not found - {args['input_value']}")
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # 清洗
    try:
        cleaned = clean_subtitle(raw_text)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # mock 人物识别（仅第一个 chunk）
    if args["mock_analyze_first"]:
        try:
            chunks = split_subtitle(
                cleaned,
                max_chunk_size=args["max_chunk_size"],
                context_size=args["context_size"]
            )
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        if not chunks:
            print("Error: no chunks produced")
            sys.exit(1)

        first_chunk = chunks[0]
        result = mock_analyze_chunk(first_chunk)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # mock 人物识别（所有 chunk）
    if args["mock_analyze_all"]:
        try:
            chunks = split_subtitle_forced(
                cleaned,
                max_chunk_size=args["max_chunk_size"],
                context_size=args["context_size"]
            )
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        results = []
        for chunk in chunks:
            result = mock_analyze_chunk(chunk)
            results.append(result)

        if args["normalize_speakers"]:
            normalized = normalize_speakers(results)
            if args["export_markdown"]:
                md = export_markdown(normalized)
                print(md)
            else:
                print(json.dumps(normalized, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 分块
    if args["split"]:
        try:
            chunks = split_subtitle(
                cleaned,
                max_chunk_size=args["max_chunk_size"],
                context_size=args["context_size"]
            )
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        if args["output_json"]:
            print(json.dumps(chunks, ensure_ascii=False, indent=2))
        else:
            for chunk in chunks:
                print(f"=== Chunk {chunk['chunk_id']} ===")
                if chunk["context_before"]:
                    print(f"[Context Before]")
                    print(chunk["context_before"])
                    print("")
                print(chunk["text"])
                if chunk["context_after"]:
                    print("")
                    print(f"[Context After]")
                    print(chunk["context_after"])
                print("")
    else:
        print(cleaned)


if __name__ == "__main__":
    main()
