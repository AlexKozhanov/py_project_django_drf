from django.contrib.auth.models import AbstractUser
from django.db import models

from Ims.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Укажите Email')
    phone_number = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Телефон',
        help_text='Укажите Телефон')
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Страна',
        help_text='Укажите Страну')
    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Добавьте Аватарку')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя')
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Оплаченный курс',
        help_text='Выберите оплаченный курс')
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Оплаченный урок',
        help_text='Выберите оплаченный урок')
    payment_amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Сумма оплаты',
        help_text='Укажите сумма оплаты')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name='Способ оплаты',
        help_text='Укажите способ оплаты')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.user_name
