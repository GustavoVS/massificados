from rest_framework import serializers
from .models import Buyer, BuyerAddress


class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = ('name', 'email', 'phone',)


class BuyerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyerAddress
        fields = ('street', 'district', 'complement', 'number', 'city', 'state', 'postal_code',)
