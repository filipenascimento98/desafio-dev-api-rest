from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.domain.portador_domain import PortadorDomain
from api.serializer import PortadorSerializer


class PortadorView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = PortadorDomain()

    @swagger_auto_schema(query_serializer=PortadorSerializer())
    def post(self, request):
        serializer = PortadorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.domain.create(serializer.data)

        return Response(data={'data': result['message']}, status=result['status'])

    path_param = openapi.Parameter(
        'document', openapi.IN_PATH,
        description="CPF do usuário",
        type=openapi.TYPE_STRING
    )
    @swagger_auto_schema(manual_parameters=[path_param])
    def delete(self, request, document):
        result_get = self.domain.get(query_params={'document':document})

        if result_get['status'] == 404:
            return Response(data=result_get['message'], status=result_get['status'])

        portador_obj = result_get['message']
        result = self.domain.delete(portador_obj)
        
        if result['status'] != 204:
            return Response(data=result['message'], status=result['status'])

        return Response(data={'data': result['message']}, status=result['status'])