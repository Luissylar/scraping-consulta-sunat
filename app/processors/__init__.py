from .base import BaseProcessor
from .historica import InformacionHistoricaProcessor

__all__ = ["BaseProcessor", "InformacionHistoricaProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [InformacionHistoricaProcessor()]
