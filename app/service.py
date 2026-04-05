"""Servicio de alto nivel para consultas SUNAT."""

from typing import Optional

from .client import SunatHttpClient
from .constants import DEFAULT_TOKEN
from .parser import SunatParser
from .queries import PayloadBuilder, QueryType


class SunatService:
    """Orquesta: arma payload, consulta SUNAT y parsea respuesta."""

    def __init__(
        self,
        client: Optional[SunatHttpClient] = None,
        parser: Optional[SunatParser] = None,
        token: str = DEFAULT_TOKEN,
    ):
        self.client = client or SunatHttpClient()
        self.parser = parser or SunatParser()
        self.token = token

    def consultar(self, query_type: QueryType, value: str) -> dict:
        payload = PayloadBuilder.build(query_type, value, self.token)
        html = self.client.post_query(payload)
        return self.parser.parse(html)
