"""Paquete principal para consultas SUNAT."""

from .processors import ActasProbatoriasProcessor, BaseProcessor, DeudaCoactivaProcessor, EstablecimientosAnexosProcessor, InformacionHistoricaProcessor, ReactivaPeruProcessor, TrabajadoresProcessor
from .service import SunatService
from .queries import QueryType

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "DeudaCoactivaProcessor", "EstablecimientosAnexosProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor", "SunatService", "QueryType"]
