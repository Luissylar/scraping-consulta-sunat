"""Paquete principal para consultas SUNAT."""

from .processors import BaseProcessor, InformacionHistoricaProcessor, ReactivaPeruProcessor, TrabajadoresProcessor
from .service import SunatService
from .queries import QueryType

__all__ = ["BaseProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor", "SunatService", "QueryType"]
