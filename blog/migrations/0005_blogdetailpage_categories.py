# Generated by Django 3.0.9 on 2020-08-18 10:17

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
