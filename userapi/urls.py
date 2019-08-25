from rest_framework import routers
from userapi.views import UserViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    #other paths
    path(r'', include(router.urls)),
]