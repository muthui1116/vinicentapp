# Generated by Django 4.1 on 2022-08-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/categories'),
        ),
    ]
