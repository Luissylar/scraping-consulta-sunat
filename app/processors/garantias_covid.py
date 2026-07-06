from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor


class GarantiasCovidProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "garantias_covid"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getPGarantiaCOVID19",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        label = soup.select_one("h4 span.label")
        if label:
            result["tiene_deuda_mayor_a_uit"] = label.get_text(strip=True).upper()

        h5_list = soup.find_all("h5")
        for h5 in h5_list:
            text = h5.get_text(strip=True)
            if "actualizada al" in text:
                result["fecha_actualizacion"] = text.split("actualizada al")[-1].strip()
            elif "Ley" in text:
                result["ley"] = text.strip()

        return result
