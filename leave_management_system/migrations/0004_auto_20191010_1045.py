# Generated by Django 2.2.4 on 2019-10-10 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management_system', '0003_auto_20191009_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_leave',
            name='l_days',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tbl_leave',
            name='l_status',
            field=models.CharField(max_length=10),
        ),
    ]
