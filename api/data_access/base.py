class RepositoryBase:
    def __init__(self, model):
        self.model = model
    
    def create(self, obj):
        '''
        Realiza a criação de um model
        Args:
        - obj: Dicionário com os campos do model
        Returns:
        - obj: Instância do objeto(model) criado
        '''
        return self.model(**obj)
        
    def save(self, obj):
        '''
        Realiza a inserção de um model na base de dados
        Args:
        - obj: Objeto(model) criado porém ainda não salvo
        '''
        obj.save()
    
    def get(self, query_params={}, select_related=[]):
        '''
        Retorna um único objeto com base nos parâmetros definidos:
        Args:
            - query_params: Dicionário com os valores referentes a filtragem
            da consulta no ORM.
            - select_related: Lista de strings com os campos a serem chamados
            no select related da consulta.
        Returns:
            - obj: Objeto.
        '''
        return self.model.objects.select_related(*select_related).get(**query_params)

    def list(self):
        '''
        Realiza a listagem de dados.
            Returns:
            - Lista de objetos.
        '''
        return self.model.objects.all()
    
    def update(self, obj, fields):
        """
        Realiza a alteração parcial dos campos de um objeto via ORM.
        Args:
        - obj: Objeto com as alterações.
        - changed_data: Dicionário com o campo update_fields e o seu 
        valor sendo uma lista indicando os campos alterados
        Returns:
        - obj: Objeto alterado.
        """
        changed_data={'update_fields': fields}
        return obj.save(**changed_data)
    
    def filter_by(self, field_values={}):
        '''
        Realiza a filtragem dos registros em banco com base no parâmetro passado
        Args:
        - field: Campo a ser usa na busca
        - value: Valor do campo a ser buscado
        Returns:
        - Todos os registros que tem o campo e valor especificado.
        '''
        return self.model.objects.filter(**field_values)

    def delete(self, obj):
        '''
        Realiza a exclusão de um objeto do banco de dados.
        Args:
        - obj: Instância do objeto a ser deletado.
        '''
        obj.delete()