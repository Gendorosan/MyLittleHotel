from django.db import models


class Room(models.Model):
    room_id = models.AutoField("Id номера", primary_key=True)
    name = models.CharField("Название номера", max_length=255)
    cost = models.DecimalField("Стоимость номера", max_digits=10, decimal_places=2)
    seating_capacity = models.IntegerField("Количество спальных мест")

    def __str__(self):
        return f"{self.name}"

    def get_id(self):
        return f"{self.room_id}"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"


class Client(models.Model):
    client_id = models.AutoField("Id клиента", primary_key=True)
    login = models.CharField("Логин клиента", unique=True, max_length=255)
    password = models.CharField("Пароль клиента", max_length=255)
    name = models.CharField("Имя клиента", max_length=255)
    phone_number = models.CharField("Номер телефона клиента", max_length=255)
    email = models.CharField("Email клиента", max_length=255)

    def __str__(self):
        return f"{self.name}"

    def get_id(self):
        return self.client_id

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Reserved(models.Model):
    reserved_id = models.AutoField("Id записи", primary_key=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Комната")
    start_date = models.DateField("Начало брони")
    end_date = models.DateField("Окончание брони")

    def __str__(self):
        return f"{self.reserved_id}"

    def get_room_name(self):
        return f"{self.room_id}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Бронь"


class Jwt(models.Model):
    token = models.CharField("Токен доступа", unique=True, max_length=255)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.token}"

    def get_token(self):
        return self.token
