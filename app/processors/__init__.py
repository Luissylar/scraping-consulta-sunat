from .base import BaseProcessor
from .historica import InformacionHistoricaProcessor
from .trabajadores import TrabajadoresProcessor

__all__ = ["BaseProcessor", "InformacionHistoricaProcessor", "TrabajadoresProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [InformacionHistoricaProcessor(), TrabajadoresProcessor()]
