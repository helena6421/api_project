from django.db.models import Sum
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from lessons.models import Lesson, LessonViewStudent
from products.models import Product, ProductStudent

User = get_user_model()


class ProductGetSerializer(serializers.ModelSerializer):
    '''serializer для получения Продукта'''

    class Meta:
        model = Product
        fields = '__all__'


class LessonGetSerializer(serializers.ModelSerializer):
    '''serializer для получения Урока'''

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    '''serializer для создания/обновления Продукта'''

    class Meta:
        model = Product
        fields = ['owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        owner = self.context.get('request').user
        product = Product.objects.create(owner=owner,
                                         **validated_data)
        return product


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    '''serializer для создания/обновления Урока'''
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True)

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'url_video',
            'duration_video',
            'products'
        ]

    def create(self, validated_data):
        products = validated_data.pop('products')

        lesson = Lesson.objects.create(**validated_data)
        for product in products:
            lesson.products.add(product)
        return lesson


class SeenSerializer(serializers.ModelSerializer):
    '''serializer для создания записи просмотра видео урока'''

    class Meta:
        model = LessonViewStudent
        fields = [
            'student',
            'lesson',
            'viewing_in_seconds',
        ]

    def validate(self, attributes):
        lesson = attributes.get('lesson')
        viewing_in_seconds = attributes.get('viewing_in_seconds')
        if lesson.duration_video < viewing_in_seconds:
            raise ValidationError(
                {
                    'errors': 'duration cannot be less than video'
                }
            )
        return attributes

    def create(self, validated_data):
        lesson = validated_data.get('lesson')
        duration_video = lesson.duration_video
        viewing_in_seconds = validated_data.get('viewing_in_seconds')
        calculation = viewing_in_seconds / duration_video * 100
        status = False
        if calculation > 80:
            status = True
        lesson_view_student = LessonViewStudent.objects.create(
            status=status,
            **validated_data)
        return lesson_view_student

    def to_representation(self, instance):
        request = self.context.get('request')
        return LessonViewStudentGetSerializer(
            instance,
            context={
                'request': request}
        ).data


class LessonViewStudentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewStudent
        fields = [
            'id',
            'student',
            'lesson',
            'viewing_datetime',
            'status',

        ]


class AddStudentToProductSerializer(serializers.ModelSerializer):
    '''serializer для создания записи доступа студента к продукту'''

    class Meta:
        model = ProductStudent
        fields = [
            'product',
            'student',
        ]

    def validate(self, attributes):
        product = attributes.get('product')
        student = attributes.get('student')
        if ProductStudent.objects.filter(
                product=product,
                student=student
        ).exists():
            raise ValidationError(
                {'errors': 'A student can have only one product'})
        return attributes


class LessonViewStudentShortGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewStudent
        fields = [
            'id',
            'viewing_datetime',
            'status',
        ]


class LessonShortGetSerializer(serializers.ModelSerializer):
    '''serializer для получения Урока'''
    views = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'url_video',
            'duration_video',
            'views',
        ]

    def get_views(self, object):
        return LessonViewStudentShortGetSerializer(
            object.lessonviewstudent_set.all(), many=True
        ).data


class GetAllByProductsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'lessons',
        ]

    def get_lessons(self, object):
        return LessonShortGetSerializer(
            object.lesson_set.all(), many=True
        ).data


class LessonShortPlusGetSerializer(serializers.ModelSerializer):
    '''serializer для получения Урока'''
    views = serializers.SerializerMethodField()
    last_view = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'url_video',
            'duration_video',
            'last_view',
            'views',

        ]

    def get_views(self, object):
        return LessonViewStudentShortGetSerializer(
            object.lessonviewstudent_set.all(), many=True
        ).data

    def get_last_view(self, object):
        obj_new = object.lessonviewstudent_set.order_by(
            '-viewing_datetime').first()
        if not obj_new:
            return None
        return obj_new.viewing_datetime


class GetAllBySingleProductSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'lessons',
        ]

    def get_lessons(self, object):
        return LessonShortPlusGetSerializer(
            object.lesson_set.all(), many=True
        ).data


class GetStatisticProductsSerializer(serializers.ModelSerializer):
    viewed_lessons = serializers.SerializerMethodField()
    count_time_video = serializers.SerializerMethodField()
    count_students = serializers.SerializerMethodField()
    percent_get_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'viewed_lessons',
            'count_time_video',
            'count_students',
            'percent_get_product',

        ]

    def get_viewed_lessons(self, object):
        """Количество просмотренных уроков от всех учеников."""
        return LessonViewStudent.objects.filter(
            lesson__lessonproduct__product=object).values(
            'lesson').distinct().count()

    def get_count_time_video(self, object):
        """Сколько в сумме все ученики потратили времени на
        просмотр роликов."""
        return LessonViewStudent.objects.filter(
            lesson__lessonproduct__product=object).aggregate(
            total_time_views=Sum("viewing_in_seconds"))[
            "total_time_views"] or 0

    def get_count_students(self, object):
        """Количество учеников занимающихся на продукте."""
        return object.students.count()

    def get_percent_get_product(self, object):
        """Процент приобретения продукта
        (рассчитывается исходя из количества
       полученных доступов к продукту деленное
       на общее количество пользователей на платформе)."""
        users_total = User.objects.count()
        if not users_total:
            return 0
        return int(object.students.count() / users_total * 100)
