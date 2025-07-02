from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.domain.transacation_domain import TransactionDomain
from api.domain.account_domain import AccountDomain
from api.serializer import TransactionSerializer, AccountStatementSerializer, AccountStatementDeserializer


class TransactionView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = TransactionDomain()
        self.account_domain = AccountDomain()

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query_params = {
            'number':serializer.data['number_account'], 
            'agency':serializer.data['agency_account']
        }
        account = self.account_domain.get(query_params=query_params)
        if account['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data={'message': 'Conta não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        result = self.domain.execute_transaction(account['message'], serializer.data['value'], serializer.data['type'])

        return Response(data={'message': result['message']}, status=result['status'])

    def get(self, request):
        serializer = AccountStatementSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_params = {
            'number': serializer.data['number_account'], 
            'agency': serializer.data['agency_account']
        }
        account = self.account_domain.get(query_params=query_params)

        query_params = {
            'account_id': account['message'].id,
            'created_at__month': serializer.data['month'],
            'created_at__year': serializer.data['year'],
        }
        transactions = self.domain.filter_by(query_params)

        if transactions['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data={'message': 'Nenhum extrato encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        transactions = transactions['message']
        deserializer = AccountStatementDeserializer(instance=transactions, many=True)

        return Response(data={'message': deserializer.data}, status=status.HTTP_200_OK)
