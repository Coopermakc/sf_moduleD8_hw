# Generated by Django 2.2.10 on 2020-10-29 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20201029_0606'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PriorityCounter',
        ),
        migrations.AddField(
            model_name='todoitem',
            name='high_priority_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='todoitem',
            name='low_priority_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='todoitem',
            name='medium_priority_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]