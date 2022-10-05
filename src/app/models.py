# from app.internal.models.admin_user import AdminUser
from django.db import models

"""
class AdminUser(models.Model):
    admin_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
"""


class Room(models.Model):
    room_id = models.AutoField('Id номера', primary_key=True)
    name = models.CharField('Название номера', max_length=255)
    cost = models.DecimalField('Стоимость номера', max_digits=10, decimal_places=2)
    seating_capacity = models.IntegerField('Количество спальных мест')

    def __str__(self):
        return f'{self.name}'

    """
    def is_reserved(self):
        return self.reserved_set.all()
        # a.reserved_set.create()
        # a.reserved_set.count()
        # a.reserved_set.filter()
        # __startswith = ''
    """

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


class Client(models.Model):
    client_id = models.AutoField('Id клиента', primary_key=True)
    login = models.CharField('Логин клиента', max_length=255)
    password = models.CharField('Пароль клиента', max_length=255)
    name = models.CharField('Имя клиента', max_length=255)
    phone_number = models.CharField('Номер телефона клиента', max_length=255)
    email = models.CharField('Email клиента', max_length=255)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Reserved(models.Model):
    reserved_id = models.AutoField('Id записи', primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reserved_id}'

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронь'
