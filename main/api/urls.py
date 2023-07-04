from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main.api.views import EnterpriseVS

router = DefaultRouter()
router.register('empresa', EnterpriseVS, basename='empresa')

urlpatterns = [
    path('', include(router.urls)),
]
