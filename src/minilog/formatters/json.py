import json
from typing import Optional

from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter


class JsonFormatter(Formatter):
    def __init__(self, indent: Optional[int] = None, sort_keys: bool = False):
        self.indent = indent
        self.sort_keys = sort_keys

    def format(self, event: LogEvent) -> str:
        payload = {
            "timestamp": event.timestamp.isoformat(timespec="seconds"),
            "level": event.level.name,
            "message": event.message,
        }
        return json.dumps(payload, indent=self.indent, sort_keys=self.sort_keys, ensure_ascii=False)
