from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor, clear_text, normalize_key


class DeudaCoactivaProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "deuda_coactiva"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getInfoDC",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def _find_table(self, soup: BeautifulSoup):
        table = soup.select_one(".panel-primary .table-responsive table.table")
        if table:
            return table
        table = soup.find("table", class_="table")
        if table and table.find("thead"):
            return table
        return None

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        h4 = soup.find("h4")
        if h4:
            text = h4.get_text(strip=True)
            if "actualizada al" in text:
                result["fecha_actualizacion"] = text.split("actualizada al")[-1].strip(" ;.")

        table = self._find_table(soup)
        if not table:
            return result

        headers = []
        thead = table.find("thead")
        if thead:
            for th in thead.find_all("th"):
                headers.append(normalize_key(th.get_text(strip=True)))

        if not headers:
            return result

        rows = []
        tbody = table.find("tbody")
        if tbody:
            for tr in tbody.find_all("tr"):
                cells = [clear_text(td.get_text()) for td in tr.find_all("td")]
                if len(cells) == len(headers) and cells[0]:
                    row = {}
                    for i, key in enumerate(headers):
                        row[key] = cells[i]
                    rows.append(row)

        result["historicos"] = rows
        return result
