"""Paquete principal para consultas SUNAT."""

from .models import SearchResult
from .processors import ActasProbatoriasProcessor, BaseProcessor, DeudaCoactivaProcessor, EstablecimientosAnexosProcessor, GarantiasCovidProcessor, InformacionHistoricaProcessor, OmisionesTributariasProcessor, ReactivaPeruProcessor, RepresentantesLegalesProcessor, TrabajadoresProcessor
from .queries import QueryType
from .searcher import NombreSearchStrategy, SearchEngine, SearchResponse, SearchStrategy
from .service import SunatService

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "DeudaCoactivaProcessor", "EstablecimientosAnexosProcessor", "GarantiasCovidProcessor", "InformacionHistoricaProcessor", "NombreSearchStrategy", "OmisionesTributariasProcessor", "QueryType", "ReactivaPeruProcessor", "RepresentantesLegalesProcessor", "SearchEngine", "SearchResponse", "SearchResult", "SearchStrategy", "SunatService", "TrabajadoresProcessor"]
