from abc import ABC, abstractmethod
from typing import Any, Optional

from ..queries import QueryType


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
