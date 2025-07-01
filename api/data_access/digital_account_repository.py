from api.data_access.base import RepositoryBase
from api.models import DigitalAccount


class DigitalAccountRepository(RepositoryBase):
    def __init__(self):
        super().__init__(DigitalAccount)