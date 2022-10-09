## Api MyLittleHottel имеет следующие эндпоинты:

---
## *admin/* 
Вход в админку отеля

Для проверки решения используйте следующие данные:
```
Логин - gendor
Пароль - q1w2e3
```
Админ умеет добавлять/удалять/редактировать комнаты и
редактировать записи о бронях через админ панель Django
---
## *api/registration* 
Регистрация клиента

Это **POST** запрос, который принимает на вход следующие параметры:
```
{
    'login': login,
    'password': password,
    'name': 'Ivan',
    'phone_number': '88005553535',
    'email': 'email@mail.ru'
}
```

Если регистрация прошла успешно, то вернется jwt токен, который в дальнейшем будет передаваться в запросах,
исходящих от авторизованного а клиента
```
{
   "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6InF3ZXJ0eSJ9.Xvdu_WJtN7McLcwL0LkdQKQM1PWwUhEfQJPC5w-UgrM"
}
```
В случае, когда пользователь с таким логином уже существует, вернется код 400
```
{
    "code": 400,
    "message": "Such login already exists"
}
```
---
## *api/authentication* 
Аутентификация клиента

Это **POST** запрос, который принимает на вход следующие параметры:
```
{
    'login': login,
    'password': password,
}
```

Если аутентификация прошла успешно, то вернется jwt токен
```
{
   "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6InF3ZXJ0eSJ9.Xvdu_WJtN7McLcwL0LkdQKQM1PWwUhEfQJPC5w-UgrM"
}
```
---
## *api/all_rooms*
Список всех комнат отеля 

Это Get запрос, который возвращает ответ в следующем виде:
```
{
   "rooms":[
      {
         "name":"Люкс №1",
         "price":10000.0,
         "seating_capacity":2
      },
      {
         "name":"Люкс №2",
         "price":10000.0,
         "seating_capacity":3
      },
        ...
   ]
}
```
---
## *api/minimum_price*
Список комнат, отсортированный по возрастанию цены

Это Get запрос, который возвращает ответ в следующем виде:
```
{
   "rooms": [
      {
         "name": "Общага",
         "price": 2000,
         "seating_capacity": 10
      },
      {
         "name": "Стандарт №1",
         "price": 3000,
         "seating_capacity": 2
      },
      ...
   ]
}
```
---
## *api/maximum_price* 
Список комнат, отсортированный по убыванию цены

```
{
   "rooms": [
      {
         "name": "Люкс №1",
         "price": 10000,
         "seating_capacity": 2
      },
      {
         "name": "Люкс №2",
         "price": 10000,
         "seating_capacity": 3
      },
      {
         "name": "Стандарт №1",
         "price": 3000,
         "seating_capacity": 2
      },
      ...
      }
   ]
}
```
---
## *api/minimum_seating_capacity* 
Список комнат, отсортированный по возрастанию количества спальных мест

Это Get запрос, который возвращает ответ в следующем виде:
```
{
   "rooms": [
      {
         "name": "Люкс №1",
         "price": 10000,
         "seating_capacity": 2
      },
      {
         "name": "Стандарт №1",
         "price": 3000,
         "seating_capacity": 2
      },
      ...
   ]
}
```
---
## *api/maximum_seating_capacity* 
Список комнат, отсортированный по убыванию количества спальных мест

```
{
   "rooms": [
      {
         "name": "Общага",
         "price": 2000,
         "seating_capacity": 10
      },
      {
         "name": "Люкс №2",
         "price": 10000,
         "seating_capacity": 3
      },
      ...
   ]
}
```
---

## *api/get_free_rooms* 
Список всех свободных комнат в заданном промежутке

```
{
   "rooms": [
      {
         "name": "Люкс №2",
         "price": 10000,
         "seating_capacity": 3
      },
      {
         "name": "Стандарт №1",
         "price": 3000,
         "seating_capacity": 2
      },
       ....
   ]
}
```
---
## *api/get_reserved_rooms* 
Комнаты, зарезервированные клиентом

Это **POST** запрос, который принимает на вход следующие параметры:
```
{
    'login': login,
}
```
Для того чтобы данный запрос мог исходить только от авторизированного пользователя,
сервер ожидает увидеть в заголовке запроса jwt токен
```
"Authorization": jwt_token
```
Если его там не будет, то сервер вернет код 400
```
{
    "code": 400, 
    "message": "Validation Failed"
}
```
Если же токен в наличии, то:
1. Пришедший jwt сверится с jwt, находяшимся в бд
2. Пришедший jwt расшифруется и сверится с логином в бд
3. Логин в бд сверится с пришедшим логином

При совпадении этих 3 условий мы можем считать, что пользователь и вправду авторизован,
в противном случаее вернется код 400. Такая логика работает для всех запросов, которые требуют авторизации
```
{
   "rooms": [
      {
         "name": "Люкс №2",
         "price": 10000,
         "seating_capacity": 3,
         "start_date": "2022-10-05",
         "end_date": "2022-10-07"
      }
   ]
}
```
---
## *api/cancel_reservation* 
отмена брони комнаты

Это **POST** запрос, который принимает на вход следующие параметры:
```
{
    'login': login,
    'room_name': 'Люкс №2',
    'start_date': '2022-10-5',
    'end_date': '2022-10-7'
}
```
**Логика проверки авторизации как в api/get_reserved_rooms**

```
{
   "code": 200,
   "message": "Room reserved successfully"
}
```
---
## *api/create_reservation* 
создание брони комнаты

Это **POST** запрос, который принимает на вход следующие параметры:
```
{
    'login': login,
    'room_name': 'Люкс №2',
    'start_date': '2022-10-5',
    'end_date': '2022-10-7'
}
```
**Логика проверки авторизации как в api/get_reserved_rooms**


```
{
   "code": 200,
   "message": "Success"
}
```
---