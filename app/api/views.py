from django.db.models import Count, Sum
from rest_framework.generics import ListAPIView

from api.serializers import (LessonViewSerializer, ProductSerializer,
                             StatisticsSerializer)
from lessons.models import LessonView, Product, ProductAccess


class StatisticsView(ListAPIView):
    """Представление для получения статистики."""

    serializer_class = StatisticsSerializer
    queryset = Product.objects.all().prefetch_related(
        'lessons', 'product_accesses'
    ).annotate(
        students_on_product=Count('product_accesses', distinct=True),
        total_view_time=Sum('lessons__lesson_views__view_time', distinct=True),
    )


class ProductsLessonsView(ListAPIView):
    """Представление для получения продуктов и уроков."""

    serializer_class = ProductSerializer

    def get_queryset(self):
        return ProductAccess.objects.filter(
            user=self.request.user
        ).select_related('user', 'product')


class ProductsView(ListAPIView):
    """Представление для получения продуктов."""

    serializer_class = LessonViewSerializer

    def get_queryset(self):
        return LessonView.objects.filter(
            user=self.request.user,
            lesson__product__id=self.kwargs['product_id'],
        ).select_related('user', 'lesson')
