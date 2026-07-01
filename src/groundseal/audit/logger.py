from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from groundseal.models.source import utc_now_iso


class AuditLogger:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_retrieval(self, event: dict[str, Any]) -> None:
        event["timestamp"] = utc_now_iso()
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def count_events(self) -> int:
        if not self.log_path.exists():
            return 0
        return sum(1 for line in self.log_path.read_text().splitlines() if line.strip())
