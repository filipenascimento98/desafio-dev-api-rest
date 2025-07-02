from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from api.view.portador_view import PortadorView


class TestPortadorView(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.view.portador_view.PortadorDomain')
    @patch('api.view.portador_view.PortadorSerializer')
    def test_post_success(self, mock_serializer_cls, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_domain.create.return_value = {'message': 1, 'status': 201}

        mock_serializer = mock_serializer_cls.return_value
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {
            'full_name': 'Maria Oliveira',
            'cpf': '12345678901'
        }

        data = {
            'full_name': 'Maria Oliveira',
            'cpf': '12345678901'
        }

        url = reverse('create-portador')
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'data': 1})
        mock_domain.create.assert_called_once_with(data)
    
    @patch('api.view.portador_view.PortadorDomain')
    def test_delete_success(self, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_portador = MagicMock()
        mock_domain.get.return_value = {'message': mock_portador, 'status': 200}
        mock_domain.delete.return_value = {'message': '', 'status': 204}

        url = reverse('delete-portador', args=[12345678901])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {'data': ''})
        mock_domain.get.assert_called_once_with(query_params={'cpf': 12345678901})
        mock_domain.delete.assert_called_once_with(mock_portador)

    @patch('api.view.portador_view.PortadorDomain')
    def test_delete_not_found(self, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_domain.get.return_value = {'message': 'Portador não encontrado', 'status': 404}

        url = reverse('delete-portador', args=[12345678901])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Portador não encontrado')
        mock_domain.get.assert_called_once_with(query_params={'cpf': 12345678901})

    @patch('api.view.portador_view.PortadorDomain')
    def test_delete_failed_to_delete(self, mock_domain_cls):
        mock_domain = mock_domain_cls.return_value
        mock_portador = MagicMock()
        mock_domain.get.return_value = {'message': mock_portador, 'status': 200}
        mock_domain.delete.return_value = {'message': 'Erro ao deletar', 'status': 400}

        url = reverse('delete-portador', args=[12345678901])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'Erro ao deletar')
        mock_domain.get.assert_called_once_with(query_params={'cpf': 12345678901})
        mock_domain.delete.assert_called_once_with(mock_portador)