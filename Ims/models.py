from django.db import models


class Course(models.Model):
    """
    Класс Курс.
    Поля класса: название, описание, превью (картинка).
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название курса',
        help_text='Введите название')
    description = models.TextField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Описание курса',
        help_text='Введите описание')
    png = models.ImageField(
        upload_to='Ims/png',
        blank=True,
        null=True,
        verbose_name='Превью курса',
        help_text='Добавьте превью')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name', 'description', 'png', ]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Класс Урок.
    Поля класса: название, описание, превью (картинка), ссылка на видео.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название урока',
        help_text='Введите название')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Курс',
        help_text='Прикрепите урок к курсу')
    description = models.TextField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Описание урока',
        help_text='Введите описание')
    png = models.ImageField(
        upload_to='Ims/png',
        blank=True,
        null=True,
        verbose_name='Превью урока',
        help_text='Добавьте картинку')
    link = models.TextField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Ссылка на видео',
        help_text='Введите ссылку')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name', 'course', 'description', 'png', 'link', ]

    def __str__(self):
        return self.name
