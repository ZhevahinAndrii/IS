from rest_framework import serializers
from .models import Material, MaterialCategory


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CategoryForMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ['id','name']

class MaterialDetailSerializer(serializers.ModelSerializer):
    category = CategoryForMaterialSerializer(read_only=True)
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'category', 'quantity','price_per_unit', 'image', 'created_at','updated_at']

class MaterialCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=MaterialCategory.objects.all(),
                                                     source='category')
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Material
        fields = [
            'id', 'name', 'description', 'category_id',
            'quantity', 'price_per_unit', 'image', 'created_at','updated_at'
        ]
        read_only_fields = ['id','created_at','updated_at']