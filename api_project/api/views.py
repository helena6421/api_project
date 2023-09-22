from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from lessons.models import Lesson
from .permissions import IsOwnerOrReadOnly
from .serializers import (ProductGetSerializer,
                          ProductCreateUpdateSerializer, LessonGetSerializer,
                          LessonCreateUpdateSerializer,
                          SeenSerializer, AddStudentToProductSerializer,
                          GetAllByProductsSerializer,
                          GetAllBySingleProductSerializer,
                          GetStatisticProductsSerializer)
from products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProductGetSerializer
        return ProductCreateUpdateSerializer

    @action(detail=False, methods=['GET'])
    def get_all_by_products(self, request):
        '''
        выведения списка всех уроков по всем продуктам
        к которым пользователь имеет доступ, с выведением
        информации о статусе и времени просмотра
        '''

        products_by_student = request.user.student_in_product.all()
        serializer = GetAllByProductsSerializer(products_by_student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_all_by_single_product(self, request, pk):
        '''выведением списка уроков по конкретному продукту
        к которому пользователь имеет доступ, с выведением
        информации о статусе и времени просмотра,
        а также датой последнего просмотра ролика.
        '''

        product_by_student = request.user.student_in_product.filter(id=pk)
        if not product_by_student.exists():
            return Response(
                {'errors': 'no product for student is available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GetAllBySingleProductSerializer(
            product_by_student.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_statistic_products(self, request):
        '''
        Список всех продуктов на платформе,c информацией:
          Количество просмотренных уроков от всех учеников.
          Сколько в сумме все ученики потратили времени на просмотр роликов.
          Количество учеников занимающихся на продукте.
          Процент приобретения продукта (рассчитывается исходя из количества
           полученных доступов к продукту деленное на общее количество
           пользователей на платформе).
        '''
        serializer = GetStatisticProductsSerializer(
            Product.objects.all(), many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def add_student_to_product(self, request, pk):
        serializer = AddStudentToProductSerializer(
            data={
                'product': pk,
                'student': request.data.get(
                    'student'
                )
            },
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return LessonGetSerializer
        return LessonCreateUpdateSerializer

    @action(detail=True, methods=['POST'])
    def seen(self, request, pk):
        serializer = SeenSerializer(
            data={
                'student': request.user.id,
                'lesson': pk,
                'viewing_in_seconds': request.data.get(
                    'viewing_in_seconds')
            },
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
