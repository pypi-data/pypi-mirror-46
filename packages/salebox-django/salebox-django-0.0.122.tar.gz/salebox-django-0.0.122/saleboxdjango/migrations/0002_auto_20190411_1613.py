# Generated by Django 2.1.4 on 2019-04-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saleboxdjango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='active_flag',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='tax_id',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
