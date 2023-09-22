from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product

User = get_user_model()


class Lesson(models.Model):
    name = models.CharField(max_length=150)
    url_video = models.URLField(max_length=500)
    duration_video = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='video duration in seconds')
    students = models.ManyToManyField(User, through="LessonViewStudent")
    products = models.ManyToManyField(Product, through="LessonProduct")


class LessonProduct(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class LessonViewStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewing_datetime = models.DateTimeField(auto_now_add=True)
    viewing_in_seconds = models.IntegerField(
        validators=[MinValueValidator(1)])
    status = models.BooleanField(default=False)
