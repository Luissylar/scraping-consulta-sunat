"""Modelos de datos para resultados de busqueda."""

from dataclasses import dataclass


@dataclass
class SearchResult:
    ruc: str
    razon_social: str
    ubicacion: str
    estado: str
