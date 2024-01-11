from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(null=True, max_length=10, verbose_name='Пол')


class Cinema(models.Model):
    cinema_name = models.CharField(max_length= 70, verbose_name='Название')
    year = models.DateField(verbose_name='Год')
    cinema_producer = models.ForeignKey('Producer', on_delete=models.CASCADE, null = True, verbose_name='Режиссёр')
    limit = models.IntegerField(verbose_name='Ограничение')
    story = models.TextField(verbose_name='Сюжет', max_length=500)
    trailer = models.URLField(verbose_name='Трейлер')
    movie = models.URLField(verbose_name='Смотреть')
    cinema_genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null = True, verbose_name='Жанр')
    raiting = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return "%s" % (self.cinema_name)


class Genre(models.Model):
    genre = models.CharField(max_length=32, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    def __str__(self):
        return "%s" % (self.genre)


class Producer(models.Model):
    producer_surname = models.CharField(max_length=32, verbose_name='Фамилия')
    producer_name = models.CharField(max_length=32, verbose_name='Имя')

    class Meta:
        verbose_name = 'Режиссёра'
        verbose_name_plural = 'Режиссёры'
    def __str__(self):
        return "%s %s" % (self.producer_name, self.producer_surname)


class Actor(models.Model):
    actor_surname = models.CharField(max_length=32, verbose_name='Фамилия')
    actor_name = models.CharField(max_length=32, verbose_name='Имя')

    class Meta:
        verbose_name = 'Актёра'
        verbose_name_plural = 'Актёры'

    def __str__(self):
        return "%s %s" % ( self.actor_name, self.actor_surname)


class Cast(models.Model):
    cinema_cast = models.ForeignKey('Cinema', on_delete=models.CASCADE, null=True, verbose_name='Фильм')
    actor_cast = models.ForeignKey('Actor', on_delete=models.CASCADE, null=True, verbose_name='Актёр')

    class Meta:
        verbose_name = 'Актёра и Фильм'
        verbose_name_plural = 'Актёрский состав'
    def __str__(self):
        return "%s %s" % (self.cinema_cast, self.actor_cast)


class History(models.Model):
    date = models.DateTimeField(null=True, verbose_name='Дата')
    history_login_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    history_cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, null=True, verbose_name='Фильм')
    is_favorite = models.BooleanField(null=False, default=False, verbose_name='В избранном')
    raiting = models.IntegerField(null=False, default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Историю'
        verbose_name_plural = 'История'

    def __str__(self):
        return "%s %s " % (self.history_login_user, self.history_cinema)
