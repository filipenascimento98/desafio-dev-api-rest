from api.domain.base import DomainBase
from api.data_access.digital_account_repository import DigitalAccountRepository


class DigitalAccountDomain(DomainBase):
    def __init__(self):
        super().__init__(DigitalAccountRepository())