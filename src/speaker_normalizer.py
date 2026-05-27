"""人物统一模块：汇总所有 chunk 的人物，生成全局 speaker_map，替换局部 speaker_id。"""


def normalize_speakers(chunk_results: list) -> dict:
    """汇总所有 chunk 的识别结果，生成全局 speaker_map 并统一人物标识。

    Args:
        chunk_results: mock_analyze_chunk 返回的列表，每个元素包含 chunk_id, people, dialogues, warnings

    Returns:
        包含 speaker_map 和 chunks 的字典
    """
    if not chunk_results:
        return {"speaker_map": [], "chunks": []}

    # 收集所有人物，按 name 聚合
    name_groups = {}  # name -> { speaker_id, role, evidence, confidence, source_chunks }
    id_mapping = {}  # (chunk_id, local_speaker_id) -> global_speaker_id

    for result in chunk_results:
        chunk_id = result["chunk_id"]
        for person in result.get("people", []):
            name = person["speaker_name"]
            local_id = person["speaker_id"]
            confidence = person.get("confidence", 0.0)

            if name not in name_groups:
                name_groups[name] = {
                    "name": name,
                    "role": person.get("role", "unknown"),
                    "evidence": person.get("evidence", ""),
                    "confidence": confidence,
                    "source_chunks": [],
                    "local_ids": set()
                }

            group = name_groups[name]
            group["source_chunks"].append(chunk_id)
            group["local_ids"].add(local_id)
            # 取最高置信度
            if confidence > group["confidence"]:
                group["confidence"] = confidence

    # 构建全局 speaker_map 和 id 映射
    speaker_map = []
    for global_idx, (name, group) in enumerate(name_groups.items(), start=1):
        global_id = f"G{global_idx}"
        aliases = sorted(group["local_ids"])
        speaker_map.append({
            "global_speaker_id": global_id,
            "name": name,
            "aliases": aliases,
            "role": group["role"],
            "confidence": group["confidence"]
        })

        # 为该人物在所有出现过的 chunk 中建立映射
        for chunk_id in group["source_chunks"]:
            for local_id in group["local_ids"]:
                id_mapping[(chunk_id, local_id)] = global_id

    # 替换每个 chunk 的 dialogues 中的 speaker_id
    chunks = []
    for result in chunk_results:
        chunk_id = result["chunk_id"]
        new_dialogues = []
        for d in result.get("dialogues", []):
            local_id = d["speaker_id"]
            global_id = id_mapping.get((chunk_id, local_id), local_id)
            new_dialogues.append({
                **d,
                "speaker_id": global_id
            })

        chunks.append({
            "chunk_id": chunk_id,
            "dialogues": new_dialogues,
            "warnings": result.get("warnings", [])
        })

    return {
        "speaker_map": speaker_map,
        "chunks": chunks
    }
