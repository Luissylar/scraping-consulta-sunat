from typing import Any, Optional

from bs4 import BeautifulSoup

from ..queries import QueryType
from .base import BaseProcessor, clear_text, normalize_key


class EstablecimientosAnexosProcessor(BaseProcessor):
    @property
    def name(self) -> str:
        return "establecimientos_anexos"

    def build_payload(self, query_type: QueryType, query_value: str, main_data: dict) -> Optional[dict]:
        if not main_data.get("success"):
            return None
        ruc = main_data.get("ruc")
        razon_social = main_data.get("razon_social")
        if not ruc:
            return None
        return {
            "accion": "getLocAnex",
            "contexto": "ti-it",
            "modo": "1",
            "nroRuc": ruc,
            "desRuc": razon_social or "",
        }

    def _find_table(self, soup: BeautifulSoup):
        print_div = soup.find(id="print")
        if print_div:
            table = print_div.find("table", class_="table")
            if table:
                return table
        table = soup.select_one(".list-group-item table.table")
        if table:
            return table
        table = soup.find("table", class_="table")
        if table and table.find("thead"):
            return table
        return None

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        table = self._find_table(soup)
        if not table:
            return result

        headers = []
        thead = table.find("thead")
        if thead:
            for th in thead.find_all("th"):
                header = normalize_key(th.get_text(strip=True))
                headers.append(header)

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

        result["locales"] = rows
        return result
