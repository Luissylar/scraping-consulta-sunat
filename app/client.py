"""Cliente HTTP para consultas SUNAT."""

import requests
from typing import Optional

from .constants import DEFAULT_HEADERS, SUNAT_URL


class SunatHttpClient:
    """Encapsula el envio de peticiones HTTP a SUNAT con sesion persistente."""

    def __init__(self, url: str = SUNAT_URL, headers: Optional[dict] = None, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(headers or DEFAULT_HEADERS)

    def post_query(self, payload: dict) -> str:
        response = self.session.post(
            self.url,
            data=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text
