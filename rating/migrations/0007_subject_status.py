# Generated by Django 2.2.2 on 2019-07-05 10:18

from django.db import migrations, models
import rating.models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0006_subject_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='status',
            field=models.CharField(choices=[(rating.models.Status('waiting_for_confirmation'), 'waiting_for_confirmation'), (rating.models.Status('accepted'), 'accepted')], default=rating.models.Status('waiting_for_confirmation'), max_length=50),
        ),
    ]
