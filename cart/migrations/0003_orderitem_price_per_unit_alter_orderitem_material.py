# Generated by Django 5.1.4 on 2024-12-14 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0002_alter_cart_options_alter_cartitem_material_order_and_more"),
        ("inventory", "0003_remove_materialcategory_parent_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="price_per_unit",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Ціна за одиницю",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="material",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orderitems",
                related_query_name="orderitem",
                to="inventory.material",
                verbose_name="Матеріал",
            ),
        ),
    ]
