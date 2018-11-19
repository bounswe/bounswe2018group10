
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router = DefaultRouter()

router.register('register', views.UserViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('profile', views.ProfileViewSet, base_name='profile')
router.register('freelancerprofile', views.FreelancerProfileViewSet)
router.register('clientprofile', views.ClientProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
