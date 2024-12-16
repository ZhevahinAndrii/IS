from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrManager
from .models import Material, MaterialCategory
from .serializers import MaterialCategorySerializer, MaterialCreateUpdateSerializer, MaterialDetailSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response

class MaterialCategoryViewSet(ModelViewSet):
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]
        return super().get_permissions()
    

class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all().select_related('category')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price_per_unit', 'name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MaterialCreateUpdateSerializer
        return MaterialDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]
        return super().get_permissions()


# class SalesAnalyticsView(APIView):
#     def get(self, request, category_id=None, material_id=None):
#         if category_id:
#             total_sales = get_sales_by_category(category_id)
#         elif material_id:
#             total_sales = get_sales_by_material(material_id)
#         else:
#             return Response({'error': 'Invalid parameters'}, status=400)

#         return Response({'total_sales': total_sales})