from django.urls import path
from api.view.portador_view import PortadorView
from api.view.digital_account_view import DigitalAccountView


urlpatterns = [
    path('digital-account/', DigitalAccountView.as_view(), name='create-digital-account'),
    path('digital-account/<int:cpf>/', DigitalAccountView.as_view(), name='get-digital-account'),
    path('portador/', PortadorView.as_view(), name='create-portador'),
    path('portador/<int:cpf>/', PortadorView.as_view(), name='delete-portador'),  
]