import json
import os
from typing import Dict


class Metrics:
    def __init__(self, metrics_path: str) -> None:
        self.metrics_path = metrics_path
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        if not os.path.exists(metrics_path):
            self._write_metrics({})

    def _read_metrics(self) -> Dict[str, int]:
        with open(self.metrics_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_metrics(self, data: Dict[str, int]) -> None:
        with open(self.metrics_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def increment(self, key: str, amount: int = 1) -> None:
        data = self._read_metrics()
        data[key] = data.get(key, 0) + amount
        self._write_metrics(data)

    def get_all(self) -> Dict[str, int]:
        return self._read_metrics()
