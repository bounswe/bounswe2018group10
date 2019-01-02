
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('dashboard', views.DashboardViewSet, base_name='recommend.dashboard')
router.register('project/(?P<project_id>\d+)', views.ProjectViewSet, base_name='recommend.project')

urlpatterns = [
    path('', include(router.urls)),
]
