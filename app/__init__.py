"""Paquete principal para consultas SUNAT."""

from .processors import BaseProcessor, EstablecimientosAnexosProcessor, InformacionHistoricaProcessor, ReactivaPeruProcessor, TrabajadoresProcessor
from .service import SunatService
from .queries import QueryType

__all__ = ["BaseProcessor", "EstablecimientosAnexosProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor", "SunatService", "QueryType"]
