"""Servicio de alto nivel para consultas SUNAT."""

from typing import Optional

from .client import SunatHttpClient
from .constants import DEFAULT_TOKEN
from .parser import SunatParser
from .processors import default_processors
from .queries import PayloadBuilder, QueryType
from .searcher import DniSearchStrategy, NombreSearchStrategy, SearchEngine
from .sender import SunatEmailSender
from .validators import DniValidator, NombreValidator, NonEmptyValidator, RucValidator, ValidatorEngine


class SunatService:
    """Orquesta: arma payload, consulta SUNAT, parsea respuesta y ejecuta procesadores adicionales."""

    def __init__(
        self,
        client: Optional[SunatHttpClient] = None,
        parser: Optional[SunatParser] = None,
        token: str = DEFAULT_TOKEN,
        processors=None,
    ):
        self.client = client or SunatHttpClient()
        self.parser = parser or SunatParser()
        self.token = token
        self.processors = processors if processors is not None else default_processors()
        search_engine = SearchEngine(self.client)
        search_engine.register("nombre", NombreSearchStrategy())
        search_engine.register("dni", DniSearchStrategy())
        self.search_engine = search_engine
        self.email_sender = SunatEmailSender(self.client)
        validator_engine = ValidatorEngine()
        validator_engine.register("ruc", RucValidator())
        validator_engine.register("dni", DniValidator())
        validator_engine.register("nombre", NombreValidator())
        self.validators = validator_engine

    def consultar(self, query_type: QueryType, value: str) -> dict:
        self.client.init_session()
        payload = PayloadBuilder.build(query_type, value, self.token)
        html = self.client.post_query(payload)
        result = self.parser.parse(html)

        if result.get("success"):
            for processor in self.processors:
                try:
                    extra_payload = processor.build_payload(query_type, value, result)
                    if extra_payload:
                        extra_html = self.client.post_query(extra_payload)
                        extra_data = processor.parse(extra_html)
                        result[processor.name] = extra_data
                except Exception as exc:
                    result[processor.name] = None
                    if __debug__:
                        print(f"Error en procesador '{processor.name}': {exc}")

        return result

    def search_by_name(self, name: str):
        self.client.init_session()
        return self.search_engine.search("nombre", name)

    def search_by_dni(self, dni: str):
        self.client.init_session()
        return self.search_engine.search("dni", dni)

    def enviar_por_correo(self, ruc: str, email: str) -> str:
        self.client.init_session()
        result = self.consultar(QueryType.RUC, ruc)
        razon_social = result.get("razon_social", "")
        msg = self.email_sender.send(ruc, razon_social, email)
        return msg
