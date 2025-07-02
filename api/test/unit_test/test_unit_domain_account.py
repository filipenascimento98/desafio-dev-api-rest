import unittest
from unittest.mock import MagicMock, patch
from api.domain.account_domain import AccountDomain


class TestAccountDomain(unittest.TestCase):
    def setUp(self):
        self.domain = AccountDomain()
        self.domain.repository = MagicMock()
        self.domain.filter_by = MagicMock() 
    
    def test_create_success_when_no_active_account(self):
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        self.domain.filter_by.return_value = {"message": mock_queryset}

        mock_obj = MagicMock(pk=1)
        self.domain.repository.create.return_value = mock_obj

        response = self.domain.create({'portador': 123})

        self.domain.repository.create.assert_called_with({'portador': 123})
        self.domain.repository.save.assert_called_with(mock_obj)
        self.assertEqual(response, {"message": 1, "status": 201})

    def test_create_fail_when_account_exists(self):
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        self.domain.filter_by.return_value = {"message": mock_queryset}

        response = self.domain.create({'portador': 123})

        self.assertEqual(response, {"message": "Usuário possui conta ativa", "status": 400})
        self.domain.repository.create.assert_not_called()

    def test_create_exception(self):
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = False
        self.domain.filter_by.return_value = {"message": mock_queryset}
        self.domain.repository.create.side_effect = Exception("erro")

        with patch('api.domain.account_domain.logging') as mock_log:
            response = self.domain.create({'portador': 123})
            mock_log.error.assert_called_once()

        self.assertEqual(response, {
            "message": "Não foi possível adicionar o objeto a base de dados.",
            "status": 400
        })

    def test_deactivate_account_success(self):
        account = MagicMock(active=True)
        self.domain.repository.update.return_value = account

        response = self.domain.deactivate_account(account)

        self.assertFalse(account.active)
        self.domain.repository.update.assert_called_with(account, ['active'])
        self.assertEqual(response, {"message": '', "status": 201})

    def test_deactivate_inactive_account(self):
        account = MagicMock(active=False)

        response = self.domain.deactivate_account(account)

        self.assertEqual(response, {"message": "Conta desativada", "status": 400})
        self.domain.repository.update.assert_not_called()

    def test_deactivate_account_exception(self):
        account = MagicMock(active=True)
        self.domain.repository.update.side_effect = Exception("erro")

        with patch('api.domain.account_domain.logging') as mock_log:
            response = self.domain.deactivate_account(account)
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Não foi desativar a conta", "status": 400})

    def test_block_unblock_account_success(self):
        account = MagicMock()
        self.domain.repository.update.return_value = account

        response = self.domain.block_unblock_account(account, True)

        self.assertTrue(account.blocked)
        self.domain.repository.update.assert_called_with(account, ['blocked'])
        self.assertEqual(response, {"message": 'Conta bloqueada', "status": 201})

    def test_block_unblock_account_exception(self):
        account = MagicMock()
        self.domain.repository.update.side_effect = Exception("erro")

        with patch('api.domain.account_domain.logging') as mock_log:
            response = self.domain.block_unblock_account(account, True)
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Não foi bloquear/desbloquear a conta", "status": 400})