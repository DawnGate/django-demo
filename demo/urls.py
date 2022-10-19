from django.urls import path

from . import views

urlpatterns = [
    path("v1/init", views.InitUser.as_view(), name='init')
]