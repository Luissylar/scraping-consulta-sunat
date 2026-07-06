from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor, normalize_key


class TrabajadoresProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "trabajadores_prestadores_servicio"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getCantTrab",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        table = soup.select_one(".table-responsive table.table")
        if not table:
            return result

        headers = []
        thead = table.find("thead")
        if thead:
            headers = [
                normalize_key(th.get_text(strip=True))
                for th in thead.find_all("th")
            ]

        if not headers:
            return result

        rows = []
        tbody = table.find("tbody")
        if tbody:
            for tr in tbody.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                if len(cells) == len(headers) and cells[0]:
                    row = {}
                    for i, key in enumerate(headers):
                        row[key] = cells[i]
                    rows.append(row)

        result["periodos"] = rows
        return result
