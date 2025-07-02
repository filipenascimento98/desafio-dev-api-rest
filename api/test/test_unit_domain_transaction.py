import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date
from api.domain.transacation_domain import TransactionDomain

class TestTransactionDomain(unittest.TestCase):
    def setUp(self):
        self.domain = TransactionDomain()
        self.domain.repository = MagicMock()
        self.domain.validator = MagicMock()
        self.domain.create = MagicMock(return_value={"message": "transaction_ok", "status": 201})
        self.domain.update = MagicMock()

        self.account = MagicMock()
        self.account.current_balance = 1000
        self.account.id = 123
    
    def test_execute_transaction_inactive_account(self):
        self.domain.validator.validate_account_active_and_unblocked.return_value = False

        response = self.domain.execute_transaction(self.account, 100, 'deposit')

        self.assertEqual(response, {"message": "Conta inativa e/ou bloqueada", "status": 400})
        self.domain.create.assert_not_called()
    
    def test_execute_transaction_deposit_success(self):
        self.domain.validator.validate_account_active_and_unblocked.return_value = True

        response = self.domain.execute_transaction(self.account, 200, 'deposit')

        self.assertEqual(self.account.current_balance, 1200)
        self.domain.create.assert_called_once()
        self.domain.update.assert_called_once_with(self.account, ['current_balance'])
        self.assertEqual(response, {"message": "transaction_ok", "status": 201})


    def test_execute_transaction_withdraw_insufficient_balance(self):
        self.domain.validator.validate_account_active_and_unblocked.return_value = True
        self.domain.validator.check_enough_balance.return_value = False

        self.domain.filter_by = MagicMock(return_value={"message": [], "status": 200})

        response = self.domain.execute_transaction(self.account, 2000, 'withdraw')

        self.assertEqual(response, {"message": "Saldo insuficiente", "status": 400})
        self.domain.create.assert_not_called()

    def test_execute_transaction_withdraw_daily_limit_reached(self):
        self.domain.validator.validate_account_active_and_unblocked.return_value = True
        self.domain.validator.check_enough_balance.return_value = True
        self.domain.validator.check_withdraw_daily_limit.return_value = False

        self.domain.filter_by = MagicMock(return_value={"message": ["transaction1", "transaction2"], "status": 200})

        response = self.domain.execute_transaction(self.account, 100, 'withdraw')

        self.assertEqual(response, {"message": "Limite diário de saque alcançado", "status": 400})
        self.domain.create.assert_not_called()

    def test_execute_transaction_withdraw_success(self):
        self.domain.validator.validate_account_active_and_unblocked.return_value = True
        self.domain.validator.check_enough_balance.return_value = True
        self.domain.validator.check_withdraw_daily_limit.return_value = True

        self.domain.filter_by = MagicMock(return_value={"message": [], "status": 200})

        initial_balance = self.account.current_balance
        value = 200

        response = self.domain.execute_transaction(self.account, value, 'withdraw')

        self.assertEqual(self.account.current_balance, initial_balance - value)
        self.domain.create.assert_called_once()
        self.domain.update.assert_called_once_with(self.account, ['current_balance'])
        self.assertEqual(response, {"message": "transaction_ok", "status": 201})

    def test_register_transaction(self):
        response = self.domain.register_transaction(self.account, 150, 'deposit')

        self.domain.create.assert_called_with({
            'digital_account': self.account,
            'value': 150,
            'transaction_type': 'deposit'
        })
        self.domain.update.assert_called_with(self.account, ['current_balance'])
        self.assertEqual(response, {"message": "transaction_ok", "status": 201})