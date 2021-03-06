# Generated by Django 3.0.4 on 2020-04-10 09:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('name', models.CharField(blank=True, max_length=120)),
                ('content', models.TextField(blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soliloquy.Client')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_soliloquy.entry_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
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
        migrations.CreateModel(
            name='Project',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('unit_of_work', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.CreateModel(
            name='Saga',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.IntegerField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references_as_source', to='soliloquy.Entry')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references_as_target', to='soliloquy.Entry')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='references',
            field=models.ManyToManyField(blank=True, related_name='referenced_by', through='soliloquy.Reference', to='soliloquy.Entry'),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='entries', to='soliloquy.Tag'),
        ),
        migrations.AddField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soliloquy.User'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('entry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='soliloquy.Entry')),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('effort_estimate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit_of_work', models.IntegerField(blank=True, null=True)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='soliloquy.User')),
                ('parent_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='soliloquy.Project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('soliloquy.entry',),
        ),
        migrations.AddConstraint(
            model_name='reference',
            constraint=models.UniqueConstraint(fields=('source', 'reference_id'), name='reference_composite_key_constraint'),
        ),
        migrations.AddField(
            model_name='note',
            name='parent_notebook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='soliloquy.Notebook'),
        ),
        migrations.AddField(
            model_name='event',
            name='parent_saga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='soliloquy.Saga'),
        ),
        migrations.AddConstraint(
            model_name='entry',
            constraint=models.UniqueConstraint(fields=('id', 'client'), name='entry_composite_key_constraint'),
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.UniqueConstraint(fields=('owner', 'name'), name='client_composite_key_constraint'),
        ),
    ]
