"""Interfaz de linea de comandos para consultar SUNAT."""

import json

from .queries import QueryType
from .service import SunatService


def _read_query_type() -> QueryType:
    print("Seleccione tipo de consulta:")
    print("1) RUC")
    print("2) DNI")
    print("3) NOMBRE")

    option_map = {
        "1": QueryType.RUC,
        "2": QueryType.DNI,
        "3": QueryType.NOMBRE,
    }

    while True:
        option = input("Opcion: ").strip()
        if option in option_map:
            return option_map[option]
        print("Opcion invalida. Intente nuevamente.")


def _read_query_value(query_type: QueryType) -> str:
    labels = {
        QueryType.RUC: "Escriba el RUC: ",
        QueryType.DNI: "Escriba el DNI: ",
        QueryType.NOMBRE: "Escriba el nombre o razon social: ",
    }

    while True:
        value = input(labels[query_type]).strip()
        if value:
            return value
        print("El valor no puede ser vacio.")


def run_cli() -> None:
    service = SunatService()
    query_type = _read_query_type()
    query_value = _read_query_value(query_type)

    try:
        resultado = service.consultar(query_type, query_value)
        with open("consulta.json", "w", encoding="utf-8") as json_file:
            json.dump(resultado, json_file, ensure_ascii=False, indent=4)

        print("Consulta completada. Resultado guardado en consulta.json")
    except Exception as exc:
        print(f"Error durante la consulta: {exc}")
