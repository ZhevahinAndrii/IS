from django.urls import path
from .views import AddToCartView, CartView, CategorySalesAnalyticsView, ClearCartView, CreateOrderView, OrderDetailView, OrderListView, DeleteFromCartView,MaterialSalesAnalyticsView, UserSalesAnalyticsView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('delete/', DeleteFromCartView.as_view(), name='delete-from-cart'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('analytics/materials/<int:material_id>/', MaterialSalesAnalyticsView.as_view(), name='sales-by-material'),
    path('analytics/categories/<int:category_id>', CategorySalesAnalyticsView.as_view(),name='sales-by-category'),
    path('analytics/users/<int:user_id>/',UserSalesAnalyticsView.as_view(),name='sales-by-user')
   
    
]
