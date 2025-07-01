from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.domain.transacation_domain import TransactionDomain
from api.domain.digital_account_domain import DigitalAccountDomain
from api.serializer import TransactionSerializer


class TransactionView(APIView):
    domain = TransactionDomain()
    digital_account_domain = DigitalAccountDomain()

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query_params = {
            'number':serializer.data['number_account'], 
            'agency':serializer.data['agency_account']
        }
        digital_account = self.digital_account_domain.get(query_params=query_params)
        if digital_account['status'] == status.HTTP_404_NOT_FOUND:
            return Response(data={'message': 'Conta não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        result = self.domain.execute_transaction(digital_account['message'], serializer.data['value'], serializer.data['type'])

        return Response(data={'message': result['message']}, status=result['status'])