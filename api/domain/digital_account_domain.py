import logging
from api.domain.base import DomainBase
from api.data_access.digital_account_repository import DigitalAccountRepository


class DigitalAccountDomain(DomainBase):
    def __init__(self):
        super().__init__(DigitalAccountRepository())
    
    def create(self, data):
        filter = {
            'portador_id': data['portador'],
            'active': True
        }
        accounts = self.filter_by(filter)

        if accounts['message'].exists():
            return {"message": "Usuário possui conta ativa", "status": 400}
        
        try:
            ret = self.repository.create(data)
            self.repository.save(ret)
        except Exception as e:
            logging.error(e)
            return {"message": "Não foi possível adicionar o objeto a base de dados.", "status": 400}
        
        return {"message": ret.pk, "status": 201}