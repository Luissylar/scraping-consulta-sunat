from .base import BaseProcessor
from .historica import InformacionHistoricaProcessor
from .reactiva import ReactivaPeruProcessor
from .trabajadores import TrabajadoresProcessor

__all__ = ["BaseProcessor", "InformacionHistoricaProcessor", "ReactivaPeruProcessor", "TrabajadoresProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [InformacionHistoricaProcessor(), TrabajadoresProcessor(), ReactivaPeruProcessor()]
