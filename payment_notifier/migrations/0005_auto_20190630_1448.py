# Generated by Django 2.1 on 2019-06-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_notifier', '0004_auto_20190630_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsapplogs',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
