from django.urls import path
from api.view.portador_view import PortadorView
from api.view.account_view import AccountView, DeactivateAccountView, BlockUnblockAccountView
from api.view.transaction_view import TransactionView


urlpatterns = [
    path('extract/', TransactionView.as_view(), name='extract'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('account/deactivate/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('account/block/', BlockUnblockAccountView.as_view(), name='block-unblock-account'),
    path('account/<int:document>/', AccountView.as_view(), name='get-account'),
    path('account/', AccountView.as_view(), name='create-digital-account'),
    path('portador/', PortadorView.as_view(), name='create-portador'),
    path('portador/<int:document>/', PortadorView.as_view(), name='delete-portador'),  
]