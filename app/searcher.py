"""Estrategias de busqueda de contribuyentes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional

from bs4 import BeautifulSoup

from .client import SunatHttpClient
from .models import SearchResult


@dataclass
class SearchResponse:
    results: list[SearchResult]
    truncated: bool = False
    total_count: int = 0


class SearchStrategy(ABC):
    @abstractmethod
    def build_payload(self, value: str) -> dict:
        ...

    @abstractmethod
    def parse_response(self, html: str) -> SearchResponse:
        ...

    def execute(self, client: SunatHttpClient, value: str) -> SearchResponse:
        payload = self.build_payload(value)
        html = client.post_query(payload)
        return self.parse_response(html)


class _BaseRucListStrategy(SearchStrategy):
    def parse_response(self, html: str) -> SearchResponse:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("a.list-group-item.aRucs")
        results = []
        for item in items:
            ruc = item.get("data-ruc", "").strip()
            headings = item.find_all("h4", class_="list-group-item-heading")
            razon_social = ""
            for h4 in headings:
                text = h4.get_text(strip=True)
                if "RUC:" not in text:
                    razon_social = text
                    break
            p_texts = item.find_all("p", class_="list-group-item-text")
            ubicacion = ""
            estado = ""
            for p in p_texts:
                text = p.get_text(strip=True)
                if "Ubicaci" in text:
                    ubicacion = text.split(":")[-1].strip() if ":" in text else text
                elif "Estado" in text:
                    strong = p.find("strong")
                    if strong:
                        span = strong.find("span")
                        estado = span.get_text(strip=True) if span else strong.get_text(strip=True)
            if ruc:
                results.append(SearchResult(ruc=ruc, razon_social=razon_social, ubicacion=ubicacion, estado=estado))

        truncated = "Se encontraron m" in html
        return SearchResponse(results=results, truncated=truncated, total_count=len(results))


class NombreSearchStrategy(_BaseRucListStrategy):
    _action: ClassVar[str] = "consPorRazonSoc"

    def build_payload(self, value: str) -> dict:
        return {
            "accion": self._action,
            "razSoc": value,
            "nroRuc": "",
            "nrodoc": "",
            "token": "",
            "contexto": "ti-it",
            "modo": "1",
            "search1": "",
            "tipdoc": "1",
            "search2": "",
            "rbtnTipo": "3",
            "search3": value,
            "codigo": "",
        }


class DniSearchStrategy(_BaseRucListStrategy):
    _action: ClassVar[str] = "consPorTipdoc"

    def build_payload(self, value: str) -> dict:
        return {
            "accion": self._action,
            "razSoc": "",
            "nroRuc": "",
            "nrodoc": value,
            "token": "",
            "contexto": "ti-it",
            "modo": "1",
            "search1": "",
            "rbtnTipo": "2",
            "tipdoc": "1",
            "search2": value,
            "search3": "",
            "codigo": "",
        }


class SearchEngine:
    def __init__(self, client: SunatHttpClient):
        self.client = client
        self._strategies: dict[str, SearchStrategy] = {}

    def register(self, name: str, strategy: SearchStrategy):
        self._strategies[name] = strategy

    def search(self, name: str, value: str) -> Optional[SearchResponse]:
        strategy = self._strategies.get(name)
        if not strategy:
            return None
        return strategy.execute(self.client, value)
