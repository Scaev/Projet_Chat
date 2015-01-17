# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texte', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b"Date d'envoi")),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pseudo', models.CharField(max_length=20)),
                ('mot_de_passe', models.CharField(max_length=20)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
            ],
            options=None,
            bases=None,
        ),
        migrations.AddField(
            model_name='message',
            name='auteur',
            field=models.ForeignKey(related_name='messages', to='discussion.Utilisateur'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conversation',
            name='messages',
            field=models.ManyToManyField(to='discussion.Message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conversation',
            name='participants',
            field=models.ManyToManyField(related_name='conversations', to='discussion.Utilisateur'),
            preserve_default=True,
        ),
    ]
