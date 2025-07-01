from api.domain.base import DomainBase
from api.data_access.portador_repository import PortadorRepository


class PortadorDomain(DomainBase):
    def __init__(self):
        super().__init__(PortadorRepository())