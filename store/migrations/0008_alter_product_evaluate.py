# Generated by Django 4.0 on 2022-04-29 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_comment_product_detail_information_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='evaluate',
            field=models.TextField(default='100%'),
        ),
    ]
