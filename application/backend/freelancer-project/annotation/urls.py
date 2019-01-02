
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('textannotation', views.TextAnnotationViewSet)
router.register('imageannotation', views.ImageAnnotationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
