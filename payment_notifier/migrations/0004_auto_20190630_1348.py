# Generated by Django 2.1 on 2019-06-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_notifier', '0003_auto_20190630_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappmessagestosend',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]