# Generated by Django 5.1.1 on 2024-09-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_event_category_event_tickets_sold_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='total_tickets',
            field=models.PositiveIntegerField(),
        ),
    ]
