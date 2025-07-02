import logging
from api.domain.base import DomainBase
from api.data_access.account_repository import AccountRepository


class AccountDomain(DomainBase):
    def __init__(self):
        super().__init__(AccountRepository())
    
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
    
    def deactivate_account(self, account):
        try:
            if not account.active:
                return {"message": "Conta desativada", "status": 400}
            account.active = False
            account = self.repository.update(account, ['active'])
        except Exception as e:
            logging.error(e)
            return {"message": "Não foi desativar a conta", "status": 400}

        return {"message": '', "status": 201}

    def block_unblock_account(self, account, block):
        try:
            account.blocked = block
            account = self.repository.update(account, ['blocked'])
        except Exception as e:
            logging.error(e)
            return {"message": "Não foi bloquear/desbloquear a conta", "status": 400}

        return {"message": '', "status": 201}