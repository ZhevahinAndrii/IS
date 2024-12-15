from django.db import models
from django.db.models import Prefetch


class MaterialCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва категорії", error_messages={'unique':'Категорія з такою назвою вже існує'})
    # parent = models.ForeignKey(to='self', on_delete=models.SET_NULL, related_name='children', related_query_name='child', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Опис категорії")
    created_at = models.DateTimeField(verbose_name='Дата створення',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата останньої зміни',auto_now=True)

    def __str__(self):
        return f'Категорія {self.name}'

    class Meta:
        verbose_name = 'Категорія матеріалу'
        verbose_name_plural = 'Категорії матеріалів'
        indexes = (
            models.Index(fields=('name',), name='material_category_name_index'),
        )

    # def get_descendants_tree(self):
    #     category = MaterialCategory.objects.prefetch_related(
    #             Prefetch('children', queryset=MaterialCategory.objects.all())
    #     ).get(id=self.id)

    #     def build_tree(category: MaterialCategory):
    #         return {
    #             "id": category.id,
    #             "name": category.name,
    #             "children": [build_tree(child) for child in category.children.all()]
    #         }
    #     return build_tree(category)
    
class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва матеріалу', unique=True)
    description = models.TextField(blank=True, verbose_name='Опис матеріалу')
    category = models.ForeignKey(to=MaterialCategory, db_constraint=True,on_delete=models.SET_NULL, null=True, blank=True, related_name='materials', related_query_name='material', verbose_name='Категорія матеріалу')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість на складі')
    price_per_unit = models.DecimalField(max_digits=10,decimal_places=2,blank=False, null=False, verbose_name='Ціна за одиницю')
    image = models.ImageField(verbose_name='Зображення матеріалу',upload_to='materials/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата створення",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата останньої зміни',auto_now=True)

    def __str__(self):
        return f'Матеріал {self.name}'

    class Meta:
        verbose_name = 'Матеріал'
        verbose_name_plural = 'Матеріали'
        constraints = (
            models.UniqueConstraint(fields=('name',), name='material_unique_name_constraint'),
        )

    
