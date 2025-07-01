from django.urls import path
from api.view.portador_view import PortadorView


urlpatterns = [
    path('portador/', PortadorView.as_view(), name='create-portador'),
    path('portador/<int:cpf>/', PortadorView.as_view(), name='create-portador')
]