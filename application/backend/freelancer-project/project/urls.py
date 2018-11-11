
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('create', views.ProjectViewSet)
router.register('tag', views.TagViewSet)
router.register('category', views.CategoryViewSet)
router.register('bid', views.BidViewSet)
router.register('milestone', views.MilestoneViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
