from django.contrib import admin

from .models import Lesson, LessonProduct, LessonViewStudent


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
@admin.register(LessonProduct)
class LessonProductAdmin(admin.ModelAdmin):
    pass
@admin.register(LessonViewStudent)
class LessonViewStudentAdmin(admin.ModelAdmin):
    pass
