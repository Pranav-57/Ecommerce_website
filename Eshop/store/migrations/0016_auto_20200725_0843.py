# Generated by Django 3.0.7 on 2020-07-25 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20200723_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='battery',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
    ]
