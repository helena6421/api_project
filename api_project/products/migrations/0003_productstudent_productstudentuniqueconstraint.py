# Generated by Django 4.2.5 on 2023-09-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productstudent_product_students'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productstudent',
            constraint=models.UniqueConstraint(fields=('product', 'student'), name='ProductStudentUniqueConstraint'),
        ),
    ]
