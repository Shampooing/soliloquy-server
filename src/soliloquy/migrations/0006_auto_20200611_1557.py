# Generated by Django 3.0.4 on 2020-06-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soliloquy', '0005_auto_20200603_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='key',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(),
        ),
    ]
