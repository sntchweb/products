from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


MIN_VIEW_MULT_LIMIT = 0.8
MIN_LESSON_DURATION = 1
MAX_LESSON_DURATION = 32767
MIN_LESSON_DURATION_MESSAGE = ('Длительность урока не может быть '
                               'меньше 1 секунды.')
MAX_LESSON_DURATION_MESSAGE = ('Длительность урока не может быть '
                               'больше 32767 секунд.')


class Product(models.Model):
    """Модель продукта."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название продукта',
    )
    owner = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Владелец продукта'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name


class Lesson(models.Model):
    """Модель урока."""

    product = models.ManyToManyField(
        Product,
        related_name='lessons',
        verbose_name='Продукты',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название урока',
    )
    video_link = models.URLField(
        unique=True,
        verbose_name='Ссылка на урок',
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Длительность урока (в секундах)',
        validators=(
            MinValueValidator(
                MIN_LESSON_DURATION,
                message=MIN_LESSON_DURATION_MESSAGE,
            ),
            MaxValueValidator(
                MAX_LESSON_DURATION,
                message=MAX_LESSON_DURATION_MESSAGE,
            )
        ),
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name


class ProductAccess(models.Model):
    """Связующая модель доступа пользователя к продукту."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_accesses',
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_accesses',
        verbose_name='Продукт',
    )

    class Meta:
        verbose_name = 'Доступ к продукту'
        verbose_name_plural = 'Доступ к продуктам'
        ordering = ('product__name', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_access',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} имеет доступ к "{self.product}".'


class LessonView(models.Model):
    """Связующая модель просмотра урока пользователем."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_views',
        verbose_name='Пользователь',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_views',
        verbose_name='Урок',
    )
    view_time = models.PositiveSmallIntegerField(
        verbose_name='Время просмотра',
    )
    last_watch = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего просмотра',
    )

    class Meta:
        verbose_name = 'Просмотр урока'
        verbose_name_plural = 'Просмотры уроков'
        ordering = ('lesson__name', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'lesson'),
                name='unique_lesson_view',
            ),
        )

    def __str__(self) -> str:
        return (
            f'{self.user} просмотрел {self.view_time} секунд урока '
            f'"{self.lesson}".'
        )

    @property
    def view_status(self) -> str:
        """Возвращает статус просмотра урока пользователем."""

        if self.view_time >= self.lesson.duration * MIN_VIEW_MULT_LIMIT:
            return 'Просмотрено'
        return 'Не просмотрено'
