# Generated by Django 2.2.4 on 2019-10-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_profile',
            name='emp_phone',
            field=models.IntegerField(max_length=10, null=True),
        ),
    ]
