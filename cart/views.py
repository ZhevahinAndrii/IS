from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from cart.serializers import AddToCartSerializer, CartSerializer, OrderSerializer
from inventory.models import Material
from users.models import RoleChoices
from .models import Cart, CartItem, Order, OrderItem
from django.db import models

def save_cart_item(cart_item:CartItem):
    cart_item.save()
    if cart_item.quantity == 0:
        cart_item.delete()

def update_cart_item(cart: Cart, material: Material, quantity: int, action: str ='add'):
    if action == 'add' and quantity > material.quantity:
        raise serializers.ValidationError({"detail":"Бажана кількість перевищує доступну"})
    
    created = False
    
    try:
        cart_item = cart.items.get(material=material)
    except CartItem.DoesNotExist:
        if action == 'remove':
            raise serializers.ValidationError({"detail":"Цього матеріалу не існує в корзині користувача"})
        else:
            cart_item, created = cart.items.get_or_create(material=material)
    if action == 'remove':
        if quantity > cart_item.quantity:
            raise serializers.ValidationError({"detail":f"В корзині немає {quantity} {material.name}"})
        cart_item.quantity -= quantity

    elif action == 'add':
        if created:
            cart_item.quantity = quantity
        else:
            if cart_item.quantity + quantity > material.quantity:
                raise serializers.ValidationError({'detail': 'Бажана кількість перевищує доступну'})
            cart_item.quantity = models.F('quantity') + quantity
    save_cart_item(cart_item)
    
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        responses={ 200:'Матеріал додано в корзину', 400: 'Errors'}
    )
    def post(self, request, *args, **kwargs):

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material, quantity = serializer.validated_data.get('material'),serializer.validated_data.get('quantity')
        cart, _ = Cart.objects.get_or_create(user=request.user)
        update_cart_item(cart, material, quantity)
        return Response({"detail": f"{quantity} {material.name} додано в корзину."}, status=status.HTTP_200_OK)

class DeleteFromCartView(APIView):
    permission_classes = [IsAuthenticated] 
    @swagger_auto_schema(request_body=AddToCartSerializer, responses={200: 'n material_name прибрано з корзини', 400: 'Errors'})
    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material, quantity= serializer.validated_data.get('material'), serializer.validated_data.get('quantity')

        cart, _ = Cart.objects.get_or_create(user=request.user)
        update_cart_item(cart, material, quantity,'remove')

        return Response({"detail": f"{quantity} {material.name} прибрано з корзини."}, status=status.HTTP_200_OK)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=None, responses={204:'No content'})
    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.clear_cart()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=None,
        responses={200: CartSerializer()}
    )
    def get(self,request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        for item in cart.items.all():
            save_cart_item(item)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=None,
        responses={200:OrderSerializer(), 400: 'Errors'}
    )
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Корзина користувача ще не існує"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_items = list(cart.items.all().select_related('material')) 
        for item in cart_items:
            save_cart_item(item)
        if not any(item.pk is not None for item in cart_items):
            return Response({'detail':"Корзина користувача пуста"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        order_items = []
        for item in cart_items:
            order_items.append(OrderItem(
                order=order,
                material = item.material,
                quantity = item.quantity,
                price_per_unit = item.material.price_per_unit
            ))
            item.material.quantity -= item.quantity
            item.material.save()
        OrderItem.objects.bulk_create(order_items)

        cart.clear_cart()
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        if request.user.role == RoleChoices.ADMIN:
            orders = Order.objects.prefetch_related('items__material').all()
        else:
            orders = Order.objects.prefetch_related('items__material').filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: OrderSerializer(), 403: "Ви не маєте доступу до цього замовлення", 404: "Замовлення не знайдено"})
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.prefetch_related('items__material').get(id=order_id)
            if not request.user.role == RoleChoices.ADMIN and not request.user==order.user:
                return Response({'detail':"Ви не маєте доступу до цього замовлення."}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({"detail": "Замовлення не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

