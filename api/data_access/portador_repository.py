from api.data_access.base import RepositoryBase
from api.models import Portador


class PortadorRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Portador)