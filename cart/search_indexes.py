from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import OrderItem, Order
from django.db.models import Sum

@registry.register_document
class OrderItemDocument(Document):
    order = fields.KeywordField(attr='order_id')
    material = fields.KeywordField(attr='material_id')
    quantity = fields.IntegerField(attr='quantity')
    price_per_unit = fields.FloatField(attr='price_per_unit')
    total_price = fields.FloatField(attr='total_price')

    class Index:
        name = 'order_items'  # Название индекса в Elasticsearch

    class Django:
        model = OrderItem

    def get_queryset(self):
        """
        Метод для выборки данных для индексации
        """
        return super().get_queryset().select_related('order', 'material')

    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

