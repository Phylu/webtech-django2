# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(to='scorecard.Lecturer', null=True),
            preserve_default=True,
        ),
    ]
