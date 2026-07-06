"""Interfaz de linea de comandos para consultar SUNAT."""

import json

from .queries import QueryType
from .service import SunatService
from .validators import ValidationError


def _read_query_type() -> QueryType:
    print("Seleccione tipo de consulta:")
    print("1) RUC")
    print("2) DNI")
    print("3) NOMBRE (busqueda interactiva)")
    print("4) ENVIAR POR CORREO")

    option_map = {
        "1": QueryType.RUC,
        "2": QueryType.DNI,
        "3": QueryType.NOMBRE,
    }

    while True:
        option = input("Opcion: ").strip()
        if option in option_map:
            return option_map[option]
        if option == "4":
            return None
        print("Opcion invalida. Intente nuevamente.")


def _read_query_value(service: SunatService, query_type: QueryType) -> str:
    labels = {
        QueryType.RUC: "Escriba el RUC: ",
        QueryType.DNI: "Escriba el DNI: ",
        QueryType.NOMBRE: "Escriba el nombre o razon social: ",
    }
    validator_keys = {
        QueryType.RUC: "ruc",
        QueryType.DNI: "dni",
        QueryType.NOMBRE: "nombre",
    }

    while True:
        value = input(labels[query_type]).strip()
        try:
            return service.validators.validate(validator_keys[query_type], value)
        except ValidationError as e:
            print(f"  {e}")


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


def _run_email_flow(service: SunatService) -> None:
    ruc = input("Escriba el RUC: ").strip()
    try:
        ruc = service.validators.validate("ruc", ruc)
    except ValidationError as e:
        print(f"  {e}")
        return
    email = input("Escriba el correo electronico: ").strip()
    if not email or "@" not in email:
        print("Correo no valido.")
        return
    msg = service.enviar_por_correo(ruc, email)
    print(msg)


def run_cli() -> None:
    service = SunatService()
    query_type = _read_query_type()

    if query_type is None:
        _run_email_flow(service)
        return

    query_value = _read_query_value(service, query_type)

    try:
        if query_type == QueryType.NOMBRE:
            results = service.search_by_name(query_value)
        elif query_type == QueryType.DNI:
            results = service.search_by_dni(query_value)
        else:
            results = None

        if results is not None:
            if not results.results:
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
