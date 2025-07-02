import re
from datetime import datetime

class Validator:
    def validate_cpf(self, cpf):
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11:
            return False

        sum_result = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_result * 10 % 11) % 10

        sum_result = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_result * 10 % 11) % 10

        return cpf[-2:] == f"{first_digit}{second_digit}"
    
    def validate_account_active_and_unblocked(self, account):
        if account.active and not account.blocked:
            return True
        
        return False

    def check_enough_balance(self, account, value):
        if account.current_balance >= value:
            return True
        
        return False

    def check_withdraw_daily_limit(self, transactions, value):
        withdraw_amount = 0

        for transaction in transactions:
            withdraw_amount += transaction.value
        withdraw_amount += value

        if withdraw_amount > 2000:
            return False
        
        return True
    
    def validate_month(self, month):
        if month <= 0 or month >= 13:
            return False

        return True

    def validate_year(self, year):
        if year <= 0 or year > datetime.now().year:
            return False

        return True