# Generated by Django 3.2.3 on 2021-05-21 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metahumans', '0002_auto_20210521_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metahumano',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='metahumans'),
        ),
    ]
