"""Interfaz de linea de comandos para consultar SUNAT."""

import json

from .queries import QueryType
from .service import SunatService


def _read_query_type() -> QueryType:
    print("Seleccione tipo de consulta:")
    print("1) RUC")
    print("2) DNI")
    print("3) NOMBRE (busqueda interactiva)")

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


def _select_from_results(results) -> str:
    print()
    print(f"Se encontraron {results.total_count} resultado(s):")
    print()
    for i, r in enumerate(results.results, 1):
        print(f"  {i:>3}. RUC: {r.ruc}")
        print(f"       Razon Social: {r.razon_social}")
        print(f"       Ubicacion: {r.ubicacion}")
        print(f"       Estado: {r.estado}")
        print()

    if results.truncated:
        print("  (la busqueda fue truncada, refinar para mas resultados)")
        print()

    while True:
        try:
            sel = input("Seleccione un numero (0 para cancelar): ").strip()
            if sel == "0":
                return None
            idx = int(sel) - 1
            if 0 <= idx < len(results.results):
                return results.results[idx].ruc
            print("Numero invalido.")
        except ValueError:
            print("Ingrese un numero valido.")


def run_cli() -> None:
    service = SunatService()
    query_type = _read_query_type()
    query_value = _read_query_value(query_type)

    try:
        if query_type == QueryType.NOMBRE:
            results = service.search_by_name(query_value)
            if not results or not results.results:
                print("No se encontraron resultados.")
                return
            ruc = _select_from_results(results)
            if ruc is None:
                print("Busqueda cancelada.")
                return
            resultado = service.consultar(QueryType.RUC, ruc)
        else:
            resultado = service.consultar(query_type, query_value)

        with open("consulta.json", "w", encoding="utf-8") as json_file:
            json.dump(resultado, json_file, ensure_ascii=False, indent=4)

        print("Consulta completada. Resultado guardado en consulta.json")
    except Exception as exc:
        print(f"Error durante la consulta: {exc}")
