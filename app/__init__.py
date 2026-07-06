"""Paquete principal para consultas SUNAT."""

from .models import SearchResult
from .processors import ActasProbatoriasProcessor, BaseProcessor, DeudaCoactivaProcessor, EstablecimientosAnexosProcessor, GarantiasCovidProcessor, InformacionHistoricaProcessor, OmisionesTributariasProcessor, ReactivaPeruProcessor, RepresentantesLegalesProcessor, TrabajadoresProcessor
from .queries import QueryType
from .searcher import DniSearchStrategy, NombreSearchStrategy, SearchEngine, SearchResponse, SearchStrategy
from .sender import EmailSender, SunatEmailSender
from .service import SunatService
from .validators import DniValidator, NombreValidator, NonEmptyValidator, RucValidator, ValidationError, Validator, ValidatorEngine

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "DeudaCoactivaProcessor", "DniSearchStrategy", "DniValidator", "EmailSender", "EstablecimientosAnexosProcessor", "GarantiasCovidProcessor", "InformacionHistoricaProcessor", "NombreSearchStrategy", "NombreValidator", "NonEmptyValidator", "OmisionesTributariasProcessor", "QueryType", "ReactivaPeruProcessor", "RepresentantesLegalesProcessor", "RucValidator", "SearchEngine", "SearchResponse", "SearchResult", "SearchStrategy", "SunatEmailSender", "SunatService", "TrabajadoresProcessor", "ValidationError", "Validator", "ValidatorEngine"]
