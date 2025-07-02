from django.urls import path
from api.view.portador_view import PortadorView
from api.view.digital_account_view import DigitalAccountView, DeactivateAccountView, BlockUnblockAccountView
from api.view.transaction_view import TransactionView


urlpatterns = [
    path('extract/', TransactionView.as_view(), name='extract'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('digital-account/', DigitalAccountView.as_view(), name='create-digital-account'),
    path('digital-account/deactivate/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('digital-account/block/', BlockUnblockAccountView.as_view(), name='block-unblock-account'),
    path('digital-account/<int:cpf>/', DigitalAccountView.as_view(), name='get-account'),
    path('portador/', PortadorView.as_view(), name='create-portador'),
    path('portador/<int:cpf>/', PortadorView.as_view(), name='delete-portador'),  
]