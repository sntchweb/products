from django.contrib import admin

from lessons.models import Lesson, LessonView, Product, ProductAccess


class ProductAccessInline(admin.TabularInline):
    model = ProductAccess
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'lessons_in_product')
    list_filter = ('name', 'owner')
    search_fields = ('name', 'owner')
    inlines = (ProductAccessInline, )

    def lessons_in_product(self, obj):
        return ', '.join([lesson.name for lesson in obj.lessons.all()])
    lessons_in_product.short_description = 'Уроки в продукте'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_link', 'duration')
    list_filter = ('name', 'product__name')
    search_fields = ('name', )
    filter_horizontal = ('product', )


@admin.register(LessonView)
class LessonViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'view_time', 'last_watch', 'view_status')
    list_filter = ('user', 'lesson')
    search_fields = ('user', 'lesson')
