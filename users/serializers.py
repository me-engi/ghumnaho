from rest_framework import serializers

from .models import Customer, ShopOwner, Tourguide, UserPro


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPro
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a new UserPro instance
        user = UserPro.objects.create_user(**validated_data)
        return user


class CustomerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Customer
        fields = UserSerializer.Meta.fields
        # Include additional fields specific to Customer model if any


class DeliveryBoySerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Tourguide
        fields = UserSerializer.Meta.fields
        # Include additional fields specific to DeliveryBoy model if any


class ShopOwnerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = ShopOwner
        fields = UserSerializer.Meta.fields
        # Include additional fields specific to ShopOwner model if any