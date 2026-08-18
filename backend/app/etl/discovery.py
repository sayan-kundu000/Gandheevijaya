import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from backend.app.etl.schemas import ImportErrorItem, RawQuestionImportRecord

logger = logging.getLogger("gandheevijaya.etl.discovery")


class ContentDiscoverer:
    """
    Discovers, parses, and joins JSON question files.
    Handles parallel dataset triples (quesj/*q.json, ansj/*a.json, solnj/*s.json)
    as well as standalone combined JSON question files.
    """

    @staticmethod
    def discover_and_load(
        source_path: str,
    ) -> Tuple[List[Tuple[RawQuestionImportRecord, str]], List[ImportErrorItem]]:
        path = Path(source_path)
        records_with_file: List[Tuple[RawQuestionImportRecord, str]] = []
        errors: List[ImportErrorItem] = []

        if not path.exists():
            errors.append(
                ImportErrorItem(
                    file=source_path,
                    field="path",
                    error_message=f"Specified source path '{source_path}' does not exist.",
                )
            )
            return records_with_file, errors

        # Collect all JSON files under source path
        if path.is_file():
            json_files = [path]
        else:
            json_files = list(path.rglob("*.json"))

        # Group files by quesj, ansj, solnj if directory structure exists
        ques_files = [f for f in json_files if "quesj" in f.parts or f.name.endswith("q.json")]
        ans_files = {f.name.replace("a.json", "q.json"): f for f in json_files if "ansj" in f.parts or f.name.endswith("a.json")}
        sol_files = {f.name.replace("s.json", "q.json"): f for f in json_files if "solnj" in f.parts or f.name.endswith("s.json")}

        if ques_files:
            # Multi-file dataset triple loader
            for q_file in ques_files:
                rel_path = str(q_file)
                q_data = ContentDiscoverer._read_json_file(q_file, errors)
                if not q_data:
                    continue

                a_file = ans_files.get(q_file.name)
                a_map: Dict[str, str] = {}
                if a_file:
                    a_data = ContentDiscoverer._read_json_file(a_file, errors) or []
                    for item in a_data:
                        if isinstance(item, dict) and "id" in item:
                            a_map[item["id"]] = str(item.get("correct_answer", ""))

                s_file = sol_files.get(q_file.name)
                s_map: Dict[str, str] = {}
                if s_file:
                    s_data = ContentDiscoverer._read_json_file(s_file, errors) or []
                    for item in s_data:
                        if isinstance(item, dict) and "id" in item:
                            s_map[item["id"]] = str(item.get("explanation", ""))

                for idx, raw_item in enumerate(q_data):
                    if not isinstance(raw_item, dict):
                        errors.append(
                            ImportErrorItem(
                                file=rel_path,
                                record_id=f"Index #{idx}",
                                field="record",
                                error_message="Question item is not a valid JSON object.",
                            )
                        )
                        continue

                    rec_id = raw_item.get("id")
                    if rec_id:
                        if rec_id in a_map and "correct_answer" not in raw_item:
                            raw_item["correct_answer"] = a_map[rec_id]
                        if rec_id in s_map and "explanation" not in raw_item:
                            raw_item["explanation"] = s_map[rec_id]

                    try:
                        parsed_record = RawQuestionImportRecord.model_validate(raw_item)
                        records_with_file.append((parsed_record, rel_path))
                    except Exception as exc:
                        errors.append(
                            ImportErrorItem(
                                file=rel_path,
                                record_id=str(rec_id or f"Index #{idx}"),
                                field="schema",
                                error_message=f"Pydantic parsing error: {exc}",
                            )
                        )
        else:
            # Standalone combined JSON file loader
            for j_file in json_files:
                rel_path = str(j_file)
                j_data = ContentDiscoverer._read_json_file(j_file, errors)
                if not j_data:
                    continue

                if isinstance(j_data, dict):
                    j_data = [j_data]

                for idx, raw_item in enumerate(j_data):
                    if not isinstance(raw_item, dict):
                        continue
                    rec_id = raw_item.get("id")
                    try:
                        parsed_record = RawQuestionImportRecord.model_validate(raw_item)
                        records_with_file.append((parsed_record, rel_path))
                    except Exception as exc:
                        errors.append(
                            ImportErrorItem(
                                file=rel_path,
                                record_id=str(rec_id or f"Index #{idx}"),
                                field="schema",
                                error_message=f"Pydantic parsing error: {exc}",
                            )
                        )

        return records_with_file, errors

    @staticmethod
    def _read_json_file(file_path: Path, errors: List[ImportErrorItem]) -> Optional[List[Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            errors.append(
                ImportErrorItem(
                    file=str(file_path),
                    field="file",
                    error_message=f"Failed to open or parse JSON file: {exc}",
                )
            )
            return None
