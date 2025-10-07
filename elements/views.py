from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Factory, RetailNetwork, IndividualEntrepreneur
from .permissions import IsActiveUser
from .serializers import FactorySerializer, RetailNetworkSerializer, IndividualEntrepreneurSerializer


class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


class RetailNetworkViewSet(viewsets.ModelViewSet):
    queryset = RetailNetwork.objects.all()
    serializer_class = RetailNetworkSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


class IndividualEntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = IndividualEntrepreneur.objects.all()
    serializer_class = IndividualEntrepreneurSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]
