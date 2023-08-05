from django.urls import path, include
from rest_framework import routers
from .viewsets import PollViewSet

router = routers.DefaultRouter()

router.register(r"polls", PollViewSet)

urlpatterns = [path("", include(router.urls))]
