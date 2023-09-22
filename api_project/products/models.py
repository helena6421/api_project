from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(User,
                                      related_name='student_in_product',
                                      through="ProductStudent")


class ProductStudent(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                name='ProductStudentUniqueConstraint',
                fields=[
                    'product',
                    'student',

                ]
            )
        ]