# Generated by Django 2.1.7 on 2019-03-25 11:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eesti_ldap', '0002_auto_20190325_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthdate',
            name='possible_national_ids',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
