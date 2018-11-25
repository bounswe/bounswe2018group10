
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('freelancer', views.FreelancerCommentViewSet)
router.register('client', views.ClientCommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
