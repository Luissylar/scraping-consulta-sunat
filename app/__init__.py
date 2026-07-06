"""Paquete principal para consultas SUNAT."""

from .models import SearchResult
from .processors import ActasProbatoriasProcessor, BaseProcessor, DeudaCoactivaProcessor, EstablecimientosAnexosProcessor, GarantiasCovidProcessor, InformacionHistoricaProcessor, OmisionesTributariasProcessor, ReactivaPeruProcessor, RepresentantesLegalesProcessor, TrabajadoresProcessor
from .queries import QueryType
from .searcher import DniSearchStrategy, NombreSearchStrategy, SearchEngine, SearchResponse, SearchStrategy
from .sender import EmailSender, SunatEmailSender
from .service import SunatService

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "DeudaCoactivaProcessor", "DniSearchStrategy", "EmailSender", "EstablecimientosAnexosProcessor", "GarantiasCovidProcessor", "InformacionHistoricaProcessor", "NombreSearchStrategy", "OmisionesTributariasProcessor", "QueryType", "ReactivaPeruProcessor", "RepresentantesLegalesProcessor", "SearchEngine", "SearchResponse", "SearchResult", "SearchStrategy", "SunatEmailSender", "SunatService", "TrabajadoresProcessor"]
