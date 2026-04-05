"""Cliente HTTP para consultas SUNAT."""

import requests
from typing import Optional

from .constants import DEFAULT_HEADERS, SUNAT_URL


class SunatHttpClient:
    """Encapsula el envio de peticiones HTTP a SUNAT."""

    def __init__(self, url: str = SUNAT_URL, headers: Optional[dict] = None, timeout: int = 30):
        self.url = url
        self.headers = headers or DEFAULT_HEADERS
        self.timeout = timeout

    def post_query(self, payload: dict) -> str:
        response = requests.post(
            self.url,
            headers=self.headers,
            data=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text
