import unittest
from unittest.mock import MagicMock, patch
from api.domain.base import DomainBase 


class TestDomainBase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock()
        self.domain = DomainBase(self.mock_repository)
    
    def test_create_success(self):
        mock_obj = MagicMock(pk=1)
        self.mock_repository.create.return_value = mock_obj

        response = self.domain.create({'campo': 'valor'})

        self.mock_repository.create.assert_called_with({'campo': 'valor'})
        self.mock_repository.save.assert_called_with(mock_obj)
        self.assertEqual(response, {"message": 1, "status": 201})

    def test_create_exception(self):
        self.mock_repository.create.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.create({'campo': 'valor'})
            mock_log.error.assert_called_once()
        
        self.assertEqual(response, {"message": "Não foi possível adicionar o objeto a base de dados.", "status": 400})

    def test_list_success(self):
        self.mock_repository.list.return_value = ['obj1', 'obj2']
        response = self.domain.list()

        self.assertEqual(response, {"message": ['obj1', 'obj2'], "status": 200})

    def test_list_exception(self):
        self.mock_repository.list.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.list()
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Objeto não encontrado", "status": 404})

    def test_filter_by_success(self):
        self.mock_repository.filter_by.return_value = ['obj1']
        response = self.domain.filter_by({'campo': 'valor'})

        self.assertEqual(response, {"message": ['obj1'], "status": 200})

    def test_filter_by_exception(self):
        self.mock_repository.filter_by.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.filter_by({'campo': 'valor'})
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Objeto não encontrado", "status": 404})

    def test_get_success(self):
        self.mock_repository.get.return_value = 'obj'
        response = self.domain.get({'id': 1}, ['relacionamento'])

        self.assertEqual(response, {"message": 'obj', "status": 200})

    def test_get_exception(self):
        self.mock_repository.get.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.get({'id': 1}, [])
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Objeto não encontrado", "status": 404})

    def test_update_success(self):
        obj = MagicMock(pk=99)
        response = self.domain.update(obj, {'campo': 'valor'})

        self.mock_repository.update.assert_called_with(obj, {'campo': 'valor'})
        self.assertEqual(response, {"message": 99, "status": 201})

    def test_update_exception(self):
        obj = MagicMock()
        self.mock_repository.update.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.update(obj, {'campo': 'valor'})
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "Não foi possível adicionar o objeto a base de dados.", "status": 400})

    def test_delete_success(self):
        obj = MagicMock()
        response = self.domain.delete(obj)

        self.mock_repository.delete.assert_called_with(obj)
        self.assertEqual(response, {"message": "", "status": 204})

    def test_delete_exception(self):
        self.mock_repository.delete.side_effect = Exception("erro")

        with patch('api.domain.base.logging') as mock_log:
            response = self.domain.delete(MagicMock())
            mock_log.error.assert_called_once()

        self.assertEqual(response, {"message": "A exclusão falhou", "status": 400})