from django.db.models import F
from rest_framework import serializers

from lessons.models import (MIN_VIEW_MULT_LIMIT, LessonView, Product,
                            ProductAccess, User)

PERCENTAGE_MULT = 100


class LessonViewSerializer(serializers.ModelSerializer):
    """Сериализатор уроков."""

    lesson = serializers.CharField(source='lesson.name')

    class Meta:
        model = LessonView
        fields = ('lesson', 'view_time', 'last_watch', 'view_status')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов."""

    lessons = serializers.SerializerMethodField()
    product = serializers.CharField(source='product.name')

    class Meta:
        model = ProductAccess
        fields = ('product', 'lessons')

    def get_lessons(self, obj):
        lessons_obj = LessonView.objects.filter(
            lesson__product=obj.product,
            user=obj.user,
        ).select_related('user', 'lesson')
        return LessonViewSerializer(lessons_obj, many=True).data


class StatisticsSerializer(serializers.ModelSerializer):
    """Сериализатор вывода статистики."""

    product_buy_percentage = serializers.SerializerMethodField()
    lessons_view_count = serializers.SerializerMethodField()
    total_view_time = serializers.IntegerField(read_only=True)
    students_on_product = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'total_view_time',
            'students_on_product',
            'lessons_view_count',
            'product_buy_percentage',
        )

    def get_product_buy_percentage(self, obj):
        """Возвращает процент приобретения продукта."""

        return (obj.product_accesses.count() /
                User.objects.count()) * PERCENTAGE_MULT

    def get_lessons_view_count(self, obj):
        """Возвращает количество просмотров уроков."""

        return LessonView.objects.filter(
            lesson__product=obj,
            view_time__gte=F('lesson__duration') * MIN_VIEW_MULT_LIMIT
        ).count()
