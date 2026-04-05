"""Parser HTML para extraer datos de SUNAT."""

from bs4 import BeautifulSoup


def standardize_key(key: str) -> str:
    key = key.lower()
    key = key.replace(" ", "_")
    key = key.replace(":", "")
    key = key.replace("(", "").replace(")", "")
    return key


def clear_text(text: str) -> str:
    if not text:
        return ""

    cleaned = " ".join(text.split())
    if " - " in cleaned:
        parts = [part.strip() for part in cleaned.split("-", 1)]
        return " - ".join(parts)

    return cleaned


class SunatParser:
    """Transforma la respuesta HTML de SUNAT en un diccionario."""

    def parse(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        data = {}

        try:
            h4_headers = soup.find_all("h4", class_="list-group-item-heading")
            container = soup.find("div", class_="container")
            if not h4_headers or not container:
                return {
                    "success": False,
                    "message": "No se encontraron resultados o sesion expirada",
                }

            data["success"] = True
            self._extract_header_ruc_and_name(h4_headers, soup, data)
        except Exception as exc:
            print(f"Error especifico en RUC/Razon Social: {exc}")
            data["ruc"] = None
            data["razon_social"] = None

        items = soup.find_all("div", class_="list-group-item")
        self._extract_key_value_items(items, data)
        self._extract_tables(items, data)

        return data

    def _extract_header_ruc_and_name(self, h4_headers, soup, data: dict) -> None:
        header_ruc = None
        for h4 in h4_headers:
            text = h4.get_text(strip=True)
            if "-" in text and ("RUC" in text or text.split(" - ")[0].isdigit()):
                header_ruc = h4
                break

        if header_ruc:
            text_ruc = header_ruc.get_text(strip=True).replace("RUC: ", "")
            parts = text_ruc.split(" - ", 1)
            if len(parts) == 2:
                data["ruc"] = parts[0].strip()
                data["razon_social"] = parts[1].strip()
            else:
                data["ruc"] = text_ruc
                data["razon_social"] = "No encontrada"
            return

        direct_h4 = soup.select_one("div.list-group-item h4.list-group-item-heading")
        if direct_h4:
            text_ruc = direct_h4.get_text(strip=True).replace("RUC: ", "")
            parts = text_ruc.split(" - ", 1)
            data["ruc"] = parts[0].strip() if len(parts) > 0 else None
            data["razon_social"] = parts[1].strip() if len(parts) > 1 else None

    def _extract_key_value_items(self, items, data: dict) -> None:
        for item in items:
            h4_elements = item.find_all("h4", class_="list-group-item-heading")
            p_elements = item.find_all("p", class_="list-group-item-text")
            if len(h4_elements) != len(p_elements):
                continue

            for h4, p in zip(h4_elements, p_elements):
                key = standardize_key(h4.get_text(strip=True).rstrip(":"))
                raw_value = p.get_text()
                value = clear_text(raw_value)
                data[key] = value

    def _extract_tables(self, items, data: dict) -> None:
        for item in items:
            h4_element = item.find("h4", class_="list-group-item-heading")
            table_element = item.find("table", class_="tblResultado")
            if not h4_element or not table_element:
                continue

            table_key = standardize_key(h4_element.get_text(strip=True))
            table_data = []
            rows = table_element.find_all("tr")

            for row in rows:
                cells = row.find_all("td")
                for cell in cells:
                    value = cell.get_text(strip=True)
                    if value:
                        table_data.append(value)

            data[table_key] = table_data
