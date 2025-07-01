from api.domain.base import DomainBase
from api.data_access.transaction_repository import TransactionRepository


class TransactionDomain(DomainBase):
    def __init__(self):
        super().__init__(TransactionRepository())