from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor, normalize_key


class InformacionHistoricaProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "informacion_historica"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getinfHis",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        h4_date = soup.find("h4")
        if h4_date and "actualizada al" in h4_date.get_text():
            date_text = h4_date.get_text(strip=True)
            if "actualizada al" in date_text:
                result["fecha_actualizacion"] = date_text.split("actualizada al")[-1].strip()

        tables = soup.select(".table-responsive table.table")

        for table in tables:
            headers = []
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True).rstrip(":") for th in thead.find_all("th")]

            if not headers:
                continue

            rows = []
            tbody = table.find("tbody")
            if tbody:
                for tr in tbody.find_all("tr"):
                    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                    if cells and not all(c in ("-", "No hay Información", "") for c in cells):
                        row_dict = {}
                        for i, header in enumerate(headers):
                            key = normalize_key(header)
                            row_dict[key] = cells[i] if i < len(cells) else ""
                        rows.append(row_dict)

            if rows:
                key = normalize_key(headers[0])
                result[key] = rows

        return result
