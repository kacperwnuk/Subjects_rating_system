# Generated by Django 2.2.2 on 2019-06-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0002_auto_20190630_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='rating',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
