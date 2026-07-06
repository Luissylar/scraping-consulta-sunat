from abc import ABC, abstractmethod
from typing import Any, Optional

from ..queries import QueryType


_REPLACEMENTS = {
    "ó": "o", "í": "i", "é": "e", "á": "a", "ú": "u",
    "ñ": "n", "Ó": "O", "Í": "I", "É": "E", "Á": "A", "Ú": "U", "Ñ": "N",
}


def normalize_key(header: str) -> str:
    key = header.lower().strip().rstrip(":")
    for old, new in _REPLACEMENTS.items():
        key = key.replace(old, new)
    for ch in (" ", "/", ".", "\u00b0", "\u00ba"):
        key = key.replace(ch, "_")
    key = "_".join(filter(None, key.split("_")))
    return key


def clear_text(text: str) -> str:
    if not text:
        return ""
    cleaned = " ".join(text.split())
    if " - " in cleaned:
        parts = [part.strip() for part in cleaned.split("-", 1)]
        return " - ".join(parts)
    return cleaned


class BaseProcessor(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        ...

    @abstractmethod
    def parse(self, html_content: str) -> Any:
        ...
