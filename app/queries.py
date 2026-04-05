"""Tipos de consulta y armado de payload."""

from enum import Enum


class QueryType(str, Enum):
    RUC = "ruc"
    DNI = "dni"
    NOMBRE = "nombre"


class PayloadBuilder:
    """Crea payloads para cada tipo de consulta de SUNAT."""

    @staticmethod
    def build(query_type: QueryType, value: str, token: str) -> dict:
        base_payload = {
            "razSoc": "",
            "nroRuc": "",
            "nrodoc": "",
            "token": token,
            "contexto": "ti-it",
            "modo": "1",
            "rbtnTipo": "1",
            "search1": "",
            "tipdoc": "1",
            "search2": "",
            "search3": "",
            "codigo": "",
        }

        if query_type == QueryType.RUC:
            base_payload.update(
                {
                    "accion": "consPorRuc",
                    "nroRuc": value,
                    "search1": value,
                    "rbtnTipo": "1",
                }
            )
            return base_payload

        if query_type == QueryType.DNI:
            base_payload.update(
                {
                    "accion": "consPorTipdoc",
                    "nrodoc": value,
                    "tipdoc": "1",
                    "search2": value,
                    "rbtnTipo": "2",
                }
            )
            return base_payload

        if query_type == QueryType.NOMBRE:
            base_payload.update(
                {
                    "accion": "consPorNombre",
                    "razSoc": value,
                    "search3": value,
                    "rbtnTipo": "3",
                }
            )
            return base_payload

        raise ValueError(f"Tipo de consulta no soportado: {query_type}")
