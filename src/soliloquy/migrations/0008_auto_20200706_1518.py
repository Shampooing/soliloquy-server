# Generated by Django 3.0.4 on 2020-07-06 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soliloquy', '0007_auto_20200706_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.RemoveField(
            model_name='note',
            name='parent_note',
        ),
        migrations.AddField(
            model_name='note',
            name='parent_notebook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='soliloquy.Notebook'),
        ),
    ]
