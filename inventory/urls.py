from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MaterialCategoryViewSet, MaterialViewSet

app_name = 'inventory'

router = DefaultRouter()
router.register('categories', MaterialCategoryViewSet, basename='categories')
router.register('materials', MaterialViewSet, basename='materials')

urlpatterns = [
    path('',include(router.urls))
]

