# Generated by Django 3.0.3 on 2020-03-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20200301_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmodel',
            name='status',
            field=models.CharField(choices=[('error', 'error'), ('processing', 'processing'), ('done', 'done')], default='processing', max_length=256),
        ),
    ]
