from django.urls import path

from . import views

urlpatterns = [
    path("v1/init", views.InitUser.as_view(), name='init'),
    path("v1/wallet", views.ActiveWallet.as_view(), name="enale_wallet"),
    path("v1/wallet/deposits", views.CreateDeposit.as_view(), name="create_deposit"),
    path("v1/wallet/withdrawals", views.CreateWidthdrawn.as_view(), name="create_withdrawn")
]