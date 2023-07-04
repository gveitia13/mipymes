from rest_framework import generics, viewsets

from main.api.pagination import EnterprisePaginator
from main.api.serializers import EnterpriseSerializer
from main.models import Enterprise


class EnterpriseVS(viewsets.ModelViewSet):
    queryset = Enterprise.objects.filter(is_active=True)
    serializer_class = EnterpriseSerializer
    pagination_class = EnterprisePaginator
