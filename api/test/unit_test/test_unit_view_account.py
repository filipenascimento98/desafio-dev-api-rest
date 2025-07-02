from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.domain.account_domain import AccountDomain


class TestAccountViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.view.account_view.AccountDomain')
    def test_get_success(self, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_account = MagicMock()
        mock_domain.get.return_value = {'message': mock_account, 'status': 200}

        with patch('api.view.account_view.AccountDeserializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.data = {'number': 1, 'agency': 123}

            url = reverse('get-account', args=[12345678900])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, {'data': {'number': 1, 'agency': 123}})

    @patch('api.view.account_view.AccountDomain')
    def test_get_account_not_found(self, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_account = MagicMock()
        mock_domain.get.return_value = {'message': 'Objeto não encontrado', 'status': 404}

        with patch('api.view.account_view.AccountDeserializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.data = {'number': 1, 'agency': 123}

            url = reverse('get-account', args=[12345678900])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, {'data': 'Objeto não encontrado'})

    @patch('api.view.account_view.PortadorDomain')
    @patch('api.view.account_view.AccountDomain')
    def test_post_success(self, mock_account_cls, mock_portador_cls):
        portador_domain = mock_portador_cls.return_value
        account_domain = mock_account_cls.return_value

        portador_domain.get.return_value = {'message': MagicMock(), 'status': 200}
        account_domain.create.return_value = {'message': 1, 'status': 201}

        data = {'number': 1, 'agency': 123, 'portador': '12345678900'}

        with patch('api.view.account_view.AccountSerializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.is_valid.return_value = True
            mock_serializer.data = data

            url = reverse('create-digital-account')
            response = self.client.post(url, data=data, format='json')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, {'data': 1})

    @patch('api.view.account_view.PortadorDomain')
    def test_post_portador_not_found(self, mock_portador_cls):
        portador_domain = mock_portador_cls.return_value
        portador_domain.get.return_value = {'message': 'Portador não encontrado', 'status': 404}

        data = {'number': 1, 'agency': 123, 'portador': 'cpf_invalido'}

        with patch('api.view.account_view.AccountSerializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.is_valid.return_value = True
            mock_serializer.data = data

            url = reverse('create-digital-account')
            response = self.client.post(url, data=data, format='json')

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, 'Portador não encontrado')


class TestDeactivateAccountView(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.view.account_view.AccountDomain')
    def test_deactivate_account_success(self, mock_domain_cls):
        domain = mock_domain_cls.return_value
        domain.get.return_value = {'message': MagicMock(), 'status': 200}
        domain.deactivate_account.return_value = {'message': '', 'status': 201}

        data = {'number': 1, 'agency': 123}

        with patch('api.view.account_view.DeactivateAccountSerializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.is_valid.return_value = True
            mock_serializer.data = data

            url = reverse('deactivate-account')
            response = self.client.post(url, data=data, format='json')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, {'data': ''})

    @patch('api.view.account_view.AccountDomain')
    def test_deactivate_account_not_found(self, mock_domain_cls):
        domain = mock_domain_cls.return_value
        domain.get.return_value = {'message': 'Conta não encontrada', 'status': 404}

        data = {'number': 1, 'agency': 123}

        with patch('api.view.account_view.DeactivateAccountSerializer') as mock_serializer_cls:
            mock_serializer = mock_serializer_cls.return_value
            mock_serializer.is_valid.return_value = True
            mock_serializer.data = data

            url = reverse('deactivate-account')
            response = self.client.post(url, data=data, format='json')

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, {'data': 'Conta não encontrada'})


class TestBlockUnblockAccountView(APITestCase):
    def setUp(self):
        self.domain = AccountDomain()
        self.domain.repository = MagicMock()

    def test_block_active_account(self):
        account = MagicMock(active=True, blocked=False)
        self.domain.repository.update.return_value = account

        result = self.domain.block_unblock_account(account, block=True)

        self.assertEqual(result['status'], 201)
        self.assertEqual(result['message'], 'Conta bloqueada')
        self.domain.repository.update.assert_called_once_with(account, ['blocked'])

    def test_unblock_active_account(self):
        account = MagicMock(active=True, blocked=True)
        self.domain.repository.update.return_value = account

        result = self.domain.block_unblock_account(account, block=False)

        self.assertEqual(result['status'], 201)
        self.assertEqual(result['message'], 'Conta desbloqueada')
        self.domain.repository.update.assert_called_once_with(account, ['blocked'])

    def test_block_inactive_account(self):
        account = MagicMock(active=False)

        result = self.domain.block_unblock_account(account, block=True)

        self.assertEqual(result['status'], 400)
        self.assertEqual(result['message'], 'Não é possível bloquear/desbloquear uma conta desativada')
        self.domain.repository.update.assert_not_called()