# Generated by Django 3.2.15 on 2022-12-05 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20220928_1014'),
        ('account', '0002_alter_subscription_responses'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.property'),
        ),
    ]