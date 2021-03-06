# Generated by Django 4.0 on 2022-03-01 07:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news_model',
            name='date',
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 1, 7, 14, 27, 418483, tzinfo=utc), verbose_name='Дата создания комментария'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 1, 13, 14, 27), verbose_name='Дата получения заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 1, 13, 14, 27), verbose_name='Дата окончания скидки'),
        ),
    ]
