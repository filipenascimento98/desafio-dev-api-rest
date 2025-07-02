import unittest
from unittest.mock import MagicMock
from api.data_access.base import RepositoryBase


class TestRepositoryBase(unittest.TestCase):
    def setUp(self):
        self.instance_mock = MagicMock()
        self.mock_model = MagicMock(return_value=self.instance_mock)
        self.repo = RepositoryBase(self.mock_model)
    
    def test_create(self):
        data = {'campo': 'valor'}
        instance = self.repo.create(data)
        self.mock_model.assert_called_with(**data)
        self.assertEqual(instance, self.instance_mock)     

    def test_save(self):
        obj = MagicMock()
        self.repo.save(obj)
        obj.save.assert_called_once()  
    
    def test_get_with_select_related(self):
        mock_qs = self.mock_model.objects.select_related.return_value
        mock_qs.get.return_value = 'mock_obj'

        result = self.repo.get(query_params={'id': 1}, select_related=['relation'])

        self.mock_model.objects.select_related.assert_called_with('relation')
        mock_qs.get.assert_called_with(id=1)
        self.assertEqual(result, 'mock_obj')

    def test_list(self):
        self.mock_model.objects.all.return_value = ['obj1', 'obj2']
        result = self.repo.list()
        self.mock_model.objects.all.assert_called_once()
        self.assertEqual(result, ['obj1', 'obj2'])

    def test_update(self):
        obj = MagicMock()
        self.repo.update(obj, fields=['campo1', 'campo2'])
        obj.save.assert_called_with(update_fields=['campo1', 'campo2'])
    
    def test_filter_by(self):
        filtros = {'nome__icontains': 'filipe'}
        self.mock_model.objects.filter.return_value = ['obj1', 'obj2']

        result = self.repo.filter_by(filtros)
        self.mock_model.objects.filter.assert_called_with(**filtros)
        self.assertEqual(result, ['obj1', 'obj2'])

    def test_delete(self):
        obj = MagicMock()
        self.repo.delete(obj)
        obj.delete.assert_called_once()