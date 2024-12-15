from typing import Union
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from inventory.models import Material

class Cart(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Володар корзини')
    created_at = models.DateTimeField(verbose_name="Дата створення",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата останньої зміни',auto_now=True)
    
    def clear_cart(self):
        self.items.all().delete()

    @property
    def total_price(self):
        return self.items.aggregate(total=Sum(models.F('quantity') * models.F('material__price_per_unit'))).get('total') or 0

    def __str__(self):
        return f'Корзина користувача {self.user.username}'    
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзини'
        ordering = ['-created_at']

    
class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, verbose_name="Корзина",on_delete=models.CASCADE, related_name='items', related_query_name='item')
    material = models.ForeignKey(to=Material, on_delete=models.CASCADE,related_name='cartitems', related_query_name='cartitem', verbose_name='Матеріал')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    def save(self, *args, **kwargs):
        self.quantity = self.material.quantity if self.quantity > self.material.quantity else self.quantity
        return super().save(*args,**kwargs)

    @property
    def total_price(self):
        return self.quantity * self.material.price_per_unit

    def __str__(self):
        return f'{self.quantity} {self.material.name if self.material else "товарів"} в корзині користувача {self.cart.user.username}'
    
    class Meta:
        verbose_name = 'Товар в корзині'
        verbose_name_plural = 'Товари в корзині'
        constraints = (
            models.UniqueConstraint(fields=('cart', 'material'), name='cart_item_unique_constraint'),
        )

        
class Order(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Автор замовлення')
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)

    @property
    def total_price(self):
        return self.items.aggregate(total=Sum(models.F('quantity') * models.F('price_per_unit'))).get('total') or 0

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.id} від {self.user.username}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items', related_query_name='item',verbose_name='Замовлення')
    material = models.ForeignKey(to=Material, on_delete=models.SET_NULL, related_name='orderitems', related_query_name='orderitem', verbose_name='Матеріал',null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна за одиницю', null=True, blank=True)
    
    def save(self,*args,**kwargs):
        if not self.price_per_unit and self.material:
            self.price_per_unit = self.material.price_per_unit
        return super().save(*args,**kwargs)

    @property
    def total_price(self):
        return self.price_per_unit * self.quantity

    def __str__(self):
        return f'{self.quantity} {self.material.name if self.material else "товарів"} в замовленні #{self.order.id} користувача {self.order.user.username}'

    class Meta:
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'

        constraints = (
            models.UniqueConstraint(fields=('order','material'), name='order_item_unique_constraint'),
            )
    
    

    
    