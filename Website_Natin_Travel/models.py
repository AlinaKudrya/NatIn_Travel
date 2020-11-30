import uuid

from django.db import models


class Tours(models.Model):
    title = models.CharField('Название тура', max_length=150)
    image = models.ImageField('Изображение', upload_to='tours')
    country = models.CharField('Страна', max_length=50)
    short_description = models.TextField('Краткое описание', max_length=200)
    description = models.TextField('Описание тура', null=True)
    price = models.PositiveIntegerField('Цена', default=0)
    currency = models.CharField('Символ валюты', max_length=1)
    category = models.CharField('Категория', max_length=200)
    link = models.SlugField('Название ссылки', max_length=200, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class FeaturedTours(models.Model):
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE)
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранный тур'
        verbose_name_plural = 'Избранные туры'


class UserApplications(models.Model):
    date = models.DateField('Дата заявки', blank=True, null=True)
    tour_title = models.CharField('Название тура', max_length=150)
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class AnonimUserApplications(models.Model):
    date = models.DateField('Дата заявки', blank=True, null=True)
    tour_title = models.CharField('Название тура', max_length=150)
    name = models.CharField('ФИО', max_length=150, null=True)

    class Meta:
        verbose_name = 'Анонимная заявка'
        verbose_name_plural = 'Заявки'


class UserInformation(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE, unique=True)
    name = models.CharField('ФИО', max_length=200)
    email = models.CharField('E-mail', max_length=150)
    phone = models.CharField('Телефон', max_length=150)

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
