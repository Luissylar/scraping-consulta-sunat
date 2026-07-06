from .anexos import EstablecimientosAnexosProcessor
from .base import BaseProcessor
from .deuda_coactiva import DeudaCoactivaProcessor
from .historica import InformacionHistoricaProcessor
from .reactiva import ReactivaPeruProcessor
from .trabajadores import TrabajadoresProcessor

__all__ = ["BaseProcessor", "EstablecimientosAnexosProcessor", "DeudaCoactivaProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [EstablecimientosAnexosProcessor(), InformacionHistoricaProcessor(), TrabajadoresProcessor(), ReactivaPeruProcessor(), DeudaCoactivaProcessor()]
