import json
import os
from typing import Any, List, Dict


class MemoryBank:
    def __init__(self, memory_path: str) -> None:
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        if not os.path.exists(memory_path):
            self._write_memory([])

    def _read_memory(self) -> List[Dict[str, Any]]:
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_memory(self, data: List[Dict[str, Any]]) -> None:
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def append_entry(self, entry: Dict[str, Any]) -> None:
        data = self._read_memory()
        data.append(entry)
        self._write_memory(data)

    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_memory()
