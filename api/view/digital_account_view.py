from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.domain.digital_account_domain import DigitalAccountDomain
from api.domain.portador_domain import PortadorDomain
from api.serializer import (
    DigitalAccountSerializer, 
    DigitalAccountDeserializer, 
    DeactivateAccountSerializer, 
    BlockUnblockAccountSerializer
)


class DigitalAccountView(APIView):
    domain = DigitalAccountDomain()
    domain_portador = PortadorDomain()

    def get(self, request, cpf):
        result = self.domain.get(query_params={'portador_id':cpf}, select_related=['portador'])
        serializer = DigitalAccountDeserializer(instance=result['message'])

        return Response(data={'data': serializer.data}, status=result['status'])

    def post(self, request):
        serializer = DigitalAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result_portador = self.domain_portador.get(query_params={'cpf':serializer.data['portador']})
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
    domain = DigitalAccountDomain()

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
    domain = DigitalAccountDomain()

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