# Generated by Django 4.0 on 2022-04-25 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category', to='store.category'),
        ),
    ]
