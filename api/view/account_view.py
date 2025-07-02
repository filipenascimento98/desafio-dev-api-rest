from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.domain.account_domain import AccountDomain
from api.domain.portador_domain import PortadorDomain
from api.serializer import (
    AccountSerializer, 
    AccountDeserializer, 
    DeactivateAccountSerializer, 
    BlockUnblockAccountSerializer
)


class AccountView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = AccountDomain()
        self.domain_portador = PortadorDomain()

    def get(self, request, document):
        result = self.domain.get(query_params={'portador_id':document}, select_related=['portador'])
        serializer = AccountDeserializer(instance=result['message'])

        return Response(data={'data': serializer.data}, status=result['status'])

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result_portador = self.domain_portador.get(query_params={'document':serializer.data['portador']})
        if result_portador['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data=result_portador['message'], status=result_portador['status'])
        
        portador_obj = result_portador['message']
        digital_account_obj = {
            'number': serializer.data['number'],
            'agency': serializer.data['agency'],
            'portador': portador_obj
        }
        result = self.domain.create(digital_account_obj)
        
        return Response(data={'data': result['message']}, status=result['status'])


class DeactivateAccountView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = AccountDomain()

    def post(self, request):
        serializer = DeactivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query_params = {
            'number': serializer.data['number'],
            'agency': serializer.data['agency']
        }
        result = self.domain.get(query_params=query_params)

        if result['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data=result['message'], status=result['status'])
        
        account = result['message']
        result = self.domain.deactivate_account(account)

        return Response(data={'data': result['message']}, status=result['status'])
    

class BlockUnblockAccountView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = AccountDomain()

    def post(self, request):
        serializer = BlockUnblockAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query_params = {
            'number': serializer.data['number'],
            'agency': serializer.data['agency']
        }
        result = self.domain.get(query_params=query_params)

        if result['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data=result['message'], status=result['status'])

        account = result['message']
        result = self.domain.block_unblock_account(account, serializer.data['block'])

        return Response(data={'data': result['message']}, status=result['status'])