import logging


class DomainBase:
    def __init__(self, repository):
        self.repository = repository
    
    def create(self, data):
        try:
            ret = self.repository.create(data)
            self.repository.save(ret)
        except Exception as e:
            logging.error(e)
            return {"message": "Não foi possível adicionar o objeto a base de dados.", "status": 400}
        
        return {"message": ret.pk, "status": 201}
    
    def list(self):
        try:
            ret = self.repository.list()
        except Exception as e:
            logging.error(e)
            return {"message": "Objeto não encontrado", "status": 404}
        
        return {"message": ret, "status": 200}

    def filter_by(self, field_values):
        try:
            ret = self.repository.filter_by(field_values)
        except Exception as e:
            logging.error(e)
            return {"message": "Objeto não encontrado", "status": 404}
        
        return {"message": ret, "status": 200}
    
    def get(self, query_params={}, select_related=[]):
        try:
            ret = self.repository.get(query_params=query_params, select_related=select_related)
        except Exception as e:
            logging.error(e)
            return {"message": "Objeto não encontrado", "status": 404}
        
        return {"message": ret, "status": 200}

    def update(self, obj, changed_data={}):
        try:
            self.repository.update(obj, changed_data)
        except Exception as e:
            logging.error(e)
            return {"message": "Não foi possível adicionar o objeto a base de dados.", "status": 400}
        
        return {"message": obj.pk, "status": 201}

    def delete(self, data):
        try:
            self.repository.delete(data)
        except Exception as e:
            logging.error(e)
            return {"message": "A exclusão falhou", "status": 400}

        return {"message": "", "status": 204}