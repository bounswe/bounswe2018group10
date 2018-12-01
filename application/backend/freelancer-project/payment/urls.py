
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('wallet', views.WalletViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accept', views.payment),
]
