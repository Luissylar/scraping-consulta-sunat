"""Paquete principal para consultas SUNAT."""

from .processors import BaseProcessor, InformacionHistoricaProcessor, TrabajadoresProcessor
from .service import SunatService
from .queries import QueryType

__all__ = ["BaseProcessor", "InformacionHistoricaProcessor", "TrabajadoresProcessor", "SunatService", "QueryType"]
