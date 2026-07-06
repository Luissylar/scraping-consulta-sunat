"""Paquete principal para consultas SUNAT."""

from .processors import ActasProbatoriasProcessor, BaseProcessor, DeudaCoactivaProcessor, EstablecimientosAnexosProcessor, GarantiasCovidProcessor, InformacionHistoricaProcessor, ReactivaPeruProcessor, TrabajadoresProcessor
from .service import SunatService
from .queries import QueryType

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "DeudaCoactivaProcessor", "EstablecimientosAnexosProcessor", "GarantiasCovidProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor", "SunatService", "QueryType"]
