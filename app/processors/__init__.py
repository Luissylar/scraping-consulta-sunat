from .actas_probatorias import ActasProbatoriasProcessor
from .anexos import EstablecimientosAnexosProcessor
from .base import BaseProcessor
from .deuda_coactiva import DeudaCoactivaProcessor
from .garantias_covid import GarantiasCovidProcessor
from .historica import InformacionHistoricaProcessor
from .omisiones_tributarias import OmisionesTributariasProcessor
from .reactiva import ReactivaPeruProcessor
from .representantes_legales import RepresentantesLegalesProcessor
from .trabajadores import TrabajadoresProcessor

__all__ = ["ActasProbatoriasProcessor", "BaseProcessor", "EstablecimientosAnexosProcessor", "DeudaCoactivaProcessor", "GarantiasCovidProcessor", "InformacionHistoricaProcessor", "OmisionesTributariasProcessor", "ReactivaPeruProcessor", "RepresentantesLegalesProcessor", "TrabajadoresProcessor"]


def default_processors() -> list[BaseProcessor]:
    return [EstablecimientosAnexosProcessor(), InformacionHistoricaProcessor(), TrabajadoresProcessor(), ReactivaPeruProcessor(), DeudaCoactivaProcessor(), ActasProbatoriasProcessor(), GarantiasCovidProcessor(), OmisionesTributariasProcessor(), RepresentantesLegalesProcessor()]
