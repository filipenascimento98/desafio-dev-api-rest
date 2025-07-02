from api.data_access.base import RepositoryBase
from api.models import Account


class AccountRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Account)