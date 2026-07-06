from .actas_probatorias import ActasProbatoriasProcessor
from .anexos import EstablecimientosAnexosProcessor
from .base import BaseProcessor
from .deuda_coactiva import DeudaCoactivaProcessor
from .historica import InformacionHistoricaProcessor
from .reactiva import ReactivaPeruProcessor
from .trabajadores import TrabajadoresProcessor

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "EstablecimientosAnexosProcessor", "DeudaCoactivaProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [EstablecimientosAnexosProcessor(), InformacionHistoricaProcessor(), TrabajadoresProcessor(), ReactivaPeruProcessor(), DeudaCoactivaProcessor(), ActasProbatoriasProcessor()]
