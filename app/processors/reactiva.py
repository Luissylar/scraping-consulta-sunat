from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor


class ReactivaPeruProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "reactiva_peru"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getReactivaPeru",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        label = soup.select_one("span.label")
        if label:
            result["tiene_deuda_coactiva_mayor_a_1_uit"] = label.get_text(strip=True)

        for h5 in soup.find_all("h5"):
            text = h5.get_text(strip=True)
            if "actualizada al" in text:
                result["fecha_actualizacion"] = text.split("actualizada al")[-1].strip()
            elif "Decreto Legislativo" in text:
                result["decreto_legislativo"] = text

        return result
