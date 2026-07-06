"""Envio de informacion por correo electronico."""

from abc import ABC, abstractmethod
from typing import Optional

from bs4 import BeautifulSoup

from .client import SunatHttpClient


class EmailSender(ABC):
    @abstractmethod
    def send(self, ruc: str, razon_social: str, email: str) -> str:
        ...


class SunatEmailSender(EmailSender):
    def __init__(self, client: SunatHttpClient):
        self.client = client

    def send(self, ruc: str, razon_social: str, email: str) -> str:
        payload = {
            "nroRuc": ruc,
            "desRuc": razon_social,
            "accion": "enviar",
            "pagina": "datosRuc",
            "correo": "",
            "email": email,
        }
        html = self.client.post_query(payload)
        soup = BeautifulSoup(html, "html.parser")
        msg = soup.select_one("p.error")
        if msg:
            return msg.get_text(strip=True)
        return "No se pudo determinar el resultado del envio."
