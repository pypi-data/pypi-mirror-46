# Generated by Django 2.1.7 on 2019-04-09 02:09

import uuid

import django.db.models.deletion
from django.db import migrations, models

import katka.fields


class Migration(migrations.Migration):

    dependencies = [
        ('katka', '0011_auto_20190318_0806'),
    ]

    operations = [
        migrations.CreateModel(
            name='SCMRelease',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_username', katka.fields.AutoUsernameField(max_length=50)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('modified_username', katka.fields.AutoUsernameField(max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('public_identifier', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('released', models.DateTimeField(null=True)),
                ('from_hash', models.CharField(max_length=64)),
                ('to_hash', models.CharField(max_length=64)),
                ('scm_pipeline_run', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='katka.SCMPipelineRun')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
