# Generated by Django 2.2.2 on 2019-07-05 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0007_subject_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='status',
            field=models.CharField(choices=[('WAITING_FOR_CONFIRMATION', 'waiting_for_confirmation'), ('ACCEPTED', 'accepted')], default='WAITING_FOR_CONFIRMATION', max_length=50),
        ),
    ]