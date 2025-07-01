from api.data_access.base import RepositoryBase
from api.models import Transaction


class TransactionRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Transaction)