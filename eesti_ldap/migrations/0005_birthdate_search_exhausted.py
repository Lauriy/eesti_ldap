# Generated by Django 2.2.3 on 2019-08-09 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eesti_ldap', '0004_auto_20190619_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthdate',
            name='search_exhausted',
            field=models.BooleanField(default=False),
        ),
    ]
