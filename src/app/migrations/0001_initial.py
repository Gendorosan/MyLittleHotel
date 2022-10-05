# Generated by Django 4.0.4 on 2022-10-04 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id клиента')),
                ('login', models.CharField(max_length=255, verbose_name='Логин клиента')),
                ('password', models.CharField(max_length=255, verbose_name='Пароль клиента')),
                ('name', models.CharField(max_length=255, verbose_name='Имя клиента')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Номер телефона клиента')),
                ('email', models.CharField(max_length=255, verbose_name='Email клиента')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id номера')),
                ('name', models.CharField(max_length=255, verbose_name='Название номера')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость номера')),
                ('seating_capacity', models.IntegerField(verbose_name='Количество спальных мест')),
            ],
        ),
        migrations.CreateModel(
            name='Reserved',
            fields=[
                ('reserved_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id записи')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.room')),
            ],
        ),
    ]