from datetime import datetime
from api.domain.base import DomainBase
from api.data_access.transaction_repository import TransactionRepository
from api.data_access.digital_account_repository import DigitalAccountRepository
from api.validators import Validator


class TransactionDomain(DomainBase):
    def __init__(self):
        super().__init__(TransactionRepository())
        self.validator = Validator()
    
    def execute_transaction(self, account, value, type):
        if not self.validator.validate_account_active_and_unblocked(account):
            return {"message": "Conta inativa e/ou bloqueada", "status": 400}
        
        if type == 'deposit':
            account.current_balance += value
        elif type == 'withdraw':
            filter = {
                'created_at': datetime.now().date(),
                'transaction_type': 'withdraw',
                'digital_account_id': account.id
            }

            result = self.filter_by(filter)
            transactions = []
            if result['status'] == 200:
                transactions = result['message']

            if not self.validator.check_enough_balance(account, value):
                return {"message": "Saldo insuficiente", "status": 400}
            if not self.validator.check_withdraw_daily_limit(transactions, value):
                return {"message": "Limite diário de saque alcançado", "status": 400}
            
            account.current_balance -= value

        return self.register_transaction(account, value, type)

    def register_transaction(self, account, value, type):
        obj = {
            'digital_account': account,
            'value': value,
            'transaction_type': type
        }
        result = self.create(obj)
        self.update(account, ['current_balance'])

        return result