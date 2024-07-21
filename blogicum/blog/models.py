from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    """Базовая абстрактная модель."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите флажок, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    """Модель для категорий."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'Допускаются латинские символы, цифры, '
                   'дефисы и подчеркивания.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    """Модель для местоположений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название местоположения'
    )

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(BaseModel):
    """Модель для публикаций."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить будущую дату и время, '
                   'вы сможете сделать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        blank=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    def save(self, *args, **kwargs):
        self.future_post = self.pub_date > timezone.now()
        super().save(*args, **kwargs)

    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def comment_count(self):
        """Возвращает общее количество комментариев к этой публикации."""
        return self.comments.count()


class Comment(models.Model):
    """Модель для комментариев."""

    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return 'Комментарий'
