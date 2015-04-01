# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0002_auto_20150329_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(to='scorecard.Lecturer'),
            preserve_default=True,
        ),
    ]
