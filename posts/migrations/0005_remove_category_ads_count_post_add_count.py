# Generated by Django 5.0 on 2024-01-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_sub_category_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='ads_count',
        ),
        migrations.AddField(
            model_name='post',
            name='add_count',
            field=models.IntegerField(default=0),
        ),
    ]
