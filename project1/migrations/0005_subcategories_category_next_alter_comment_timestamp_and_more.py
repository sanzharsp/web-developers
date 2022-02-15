# Generated by Django 4.0 on 2022-02-13 06:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project1', '0004_remove_category_content_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategories',
            name='category_next',
            field=models.ManyToManyField(to='project1.Category'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 13, 6, 18, 41, 103969, tzinfo=utc), verbose_name='Дата создания комментария'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2022, 2, 13, 12, 18, 41), verbose_name='Дата получения заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 13, 12, 18, 41), verbose_name='Дата окончания скидки'),
        ),
    ]
