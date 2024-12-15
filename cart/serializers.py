from rest_framework import serializers
from .models import Cart, CartItem, Order,OrderItem
from inventory.models import Material
from django.contrib.auth import get_user_model

class MaterialForCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'price_per_unit']


class CartItemSerializer(serializers.ModelSerializer):
    material = MaterialForCartItemSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','material','quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['items','created_at','updated_at', 'total_price']


class MaterialForOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id','name']


class AddToCartSerializer(serializers.Serializer):
    material_id = serializers.PrimaryKeyRelatedField(required=True,queryset=Material.objects.all(), source='material', error_messages={'does_not_exist': 'Матеріалу не існує'})
    quantity = serializers.IntegerField(min_value=1, default=1)


class OrderItemSerializer(serializers.ModelSerializer):
    material = MaterialForOrderItemSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['material','quantity','price_per_unit','total_price']

class UserForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserForOrderSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items','total_price']

