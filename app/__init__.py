"""Paquete principal para consultas SUNAT."""

from .service import SunatService
from .queries import QueryType

__all__ = ["SunatService", "QueryType"]
