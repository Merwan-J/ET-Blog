# Generated by Django 3.1.5 on 2021-01-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20210117_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='proflie_pic',
            field=models.ImageField(blank=True, default='user.png', upload_to=''),
        ),
    ]