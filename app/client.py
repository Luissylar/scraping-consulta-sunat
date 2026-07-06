"""Cliente HTTP para consultas SUNAT."""

import requests
from typing import Optional

from .constants import DEFAULT_HEADERS, SUNAT_SESSION_URL, SUNAT_URL


class SunatHttpClient:
    """Encapsula el envio de peticiones HTTP a SUNAT con sesion persistente."""

    def __init__(self, url: str = SUNAT_URL, session_url: str = SUNAT_SESSION_URL,
                 headers: Optional[dict] = None, timeout: int = 30):
        self.url = url
        self.session_url = session_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(headers or DEFAULT_HEADERS)
        self._session_initialized = False

    def init_session(self) -> None:
        session_headers = {
            "Host": "e-consultaruc.sunat.gob.pe",
            "User-Agent": self.session.headers.get("User-Agent", ""),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-Ch-Ua": self.session.headers.get("Sec-Ch-Ua", ""),
            "Sec-Ch-Ua-Mobile": self.session.headers.get("Sec-Ch-Ua-Mobile", "?0"),
            "Sec-Ch-Ua-Platform": self.session.headers.get("Sec-Ch-Ua-Platform", ""),
        }
        self.session.get(self.session_url, headers=session_headers, timeout=self.timeout)
        self._session_initialized = True

    def post_query(self, payload: dict) -> str:
        response = self.session.post(
            self.url,
            data=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text
