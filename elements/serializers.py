from rest_framework import serializers

from .models import Factory, RetailNetwork, IndividualEntrepreneur


class FactorySerializer(serializers.ModelSerializer):
    debt_to_supplier = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Factory
        fields = "__all__"


class RetailNetworkSerializer(serializers.ModelSerializer):
    debt_to_supplier = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = RetailNetwork
        fields = "__all__"


class IndividualEntrepreneurSerializer(serializers.ModelSerializer):
    debt_to_supplier = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = IndividualEntrepreneur
        fields = "__all__"
